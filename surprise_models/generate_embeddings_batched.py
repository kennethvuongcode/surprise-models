import os
from pathlib import Path
from safetensors.torch import safe_open, save_file
from transformers import LlavaProcessor, LlavaForConditionalGeneration
from PIL import Image
import torch
import traceback
from tqdm import tqdm

# Setup
BASE_DIR = Path("/deepfreeze/share_read_only/surprise_driving/comma2k19/chunks_processed_backup") #update with path
OUTPUT_DIR = Path("/deepfreeze/user_shares/kennethvuong/surprise_driving/comma2k19/chunks_embedded_backup") #update with new directory
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_FILES = None  # set to int for debug

# Load LLaVa model
print("Loading LLaVa model...")
model_path = "/deepfreeze/share_read_only/llava-v1.6-mistral-7b-hf"
processor = LlavaProcessor.from_pretrained(model_path, use_fast=True)
GPU_ID = 1

model = LlavaForConditionalGeneration.from_pretrained(
    model_path,
    torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
    device_map={"": GPU_ID}
)
model.eval()

# Get safetensor chunks
chunk_paths = list(Path(BASE_DIR).rglob("*.safetensors"))
os.makedirs(OUTPUT_DIR, exist_ok=True)
if MAX_FILES:
    chunk_paths = chunk_paths[:MAX_FILES]

print(f"Found {len(chunk_paths)} chunks.")

for chunk_path in tqdm(chunk_paths, desc="Processing chunks"):
    try:
        rel_path = chunk_path.relative_to(BASE_DIR)
        safe_rel_path = Path(str(rel_path).replace("|", "_"))
        chunk_name = chunk_path.stem.replace("|", "_")

        output_dir = Path(OUTPUT_DIR) / safe_rel_path.parent
        output_path = output_dir / f"{chunk_name}_embedded.safetensors"
        if output_path.exists():
            tqdm.write(f"Skipping {chunk_name} - already processed")
            continue

        with safe_open(chunk_path, framework="pt", device="cpu") as f:
            keys = list(f.keys())
            frame_key = next(k for k in keys if "frame" in k.lower())
            frame_data = f.get_tensor(frame_key)

        valid_images = []
        valid_indices = []

        for i in range(frame_data.shape[0]):
            frame = frame_data[i].numpy().astype("uint8")

            if frame.ndim == 2:
                tqdm.write(f"{chunk_name}: Grayscale frame at index {i}, skipping...")
                continue
            elif frame.shape[-1] == 4:
                tqdm.write(f"{chunk_name}: RGBA frame at index {i}, dropping alpha")
                frame = frame[..., :3]
            elif frame.shape[-1] != 3:
                tqdm.write(f"{chunk_name}: Unexpected channel count at index {i}: {frame.shape}")
                continue

            valid_images.append(Image.fromarray(frame))
            valid_indices.append(i)

        if not valid_images:
            tqdm.write(f"{chunk_name}: No valid frames, skipping chunk.")
            continue

        # Batch process
        inputs = processor(images=valid_images, text=["Describe the driving scene."] * len(valid_images), return_tensors="pt")
        inputs = {k: v.to(f"cuda:{GPU_ID}") for k, v in inputs.items()}

        pixel_values = inputs["pixel_values"]
        if pixel_values.ndim == 5:
            pixel_values = pixel_values.view(-1, *pixel_values.shape[-3:])  # flatten [B, N, 3, H, W] → [B*N, 3, H, W]

        with torch.no_grad():
            vision_features = model.vision_tower(pixel_values)[0]  # [B, seq_len, dim]
            pooled = vision_features.mean(dim=1).cpu()  # [B, dim]

        # Insert embeddings in original order
        embeddings = [None] * frame_data.shape[0]
        for idx, emb in zip(valid_indices, pooled):
            embeddings[idx] = emb

        # Fill skipped frames with zeros
        embedding_data = torch.stack([
            emb if emb is not None else torch.zeros_like(pooled[0])
            for emb in embeddings
        ])

        output_dir.mkdir(parents=True, exist_ok=True)
        save_file({"frame_data": frame_data, "embedding_data": embedding_data}, str(output_path))
        tqdm.write(f"Processed: {rel_path} to {output_path}")

    except Exception as e:
        tqdm.write(f"Failed on {chunk_path}: {e}")
        traceback.print_exc()
