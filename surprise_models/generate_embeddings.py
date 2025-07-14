import os
from pathlib import Path
from safetensors.torch import safe_open, save_file
from transformers import LlavaProcessor, LlavaForConditionalGeneration
from PIL import Image
import torch
import traceback
from tqdm import tqdm

#Setup
BASE_DIR = Path("/deepfreeze/share_read_only/surprise_driving/comma2k19/chunks_processed")
OUTPUT_DIR = Path("/deepfreeze/user_shares/kennethvuong/surprise_driving/comma2k19/chunks_embedded")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_FILES = None #set to int for debug

#Loading LLaVa model
print("Loading LLaVa model...")
model_path = "/deepfreeze/share_read_only/llava-v1.6-mistral-7b-hf"
processor = LlavaProcessor.from_pretrained(model_path,use_fast=True) #define processor from pretrained LLaVa model

GPU_ID = 5

model = LlavaForConditionalGeneration.from_pretrained(
    model_path,
    torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
    device_map={"": GPU_ID}
)

model.eval() #put model in inference mode

#Process Safetensors
chunk_paths = list(Path(BASE_DIR).rglob("*.safetensors")) #finds all safetensor files
os.makedirs(OUTPUT_DIR,exist_ok=True)

if MAX_FILES:
    chunk_paths = chunk_paths[:MAX_FILES]
    
print(f"Found {len(chunk_paths)} chunks.")

for chunk_path in tqdm(chunk_paths, desc="Processing chunks"):
    try:
        rel_path = chunk_path.relative_to(BASE_DIR)
        safe_rel_path = Path(str(rel_path).replace("|", "_"))
        chunk_name = chunk_path.stem.replace("|", "_")

        output_dir = Path(OUTPUT_DIR) / safe_rel_path.parent #this is using the path library
        output_path = output_dir / f"{chunk_name}_embedded.safetensors" #constructing file specific path
        if output_path.exists():
            tqdm.write(f"Skipping {chunk_name} - already processed")
            continue
        
        #loading frame data
        with safe_open(chunk_path,framework="pt", device = "cpu") as f: #with ensures the file is properly closed afterwards
            keys = list(f.keys())
            frame_key = next(k for k in keys  if "frame" in k.lower()) #retrieves first key in list that has frame_data
            frame_data = f.get_tensor(frame_key) #retrieves tensor, [f,H,W,3]
            # tqdm.write(f"{chunk_name} frame_data shape: {frame_data.shape}")  

            
        embeddings = []
        
                
        for i in range(frame_data.shape[0]):
            frame = frame_data[i].numpy().astype("uint8")

            # Sanity check: ensure shape is (H, W, 3)
            if frame.ndim == 2:
                tqdm.write(f"Grayscale frame at index {i}, skipping...")
                continue
            elif frame.shape[-1] == 4:
                tqdm.write(f"RGBA frame at index {i}, dropping alpha")
                frame = frame[..., :3]
            elif frame.shape[-1] != 3:
                tqdm.write(f"Unexpected channel count at index {i}: {frame.shape}")
                continue

            img = Image.fromarray(frame)

            inputs = processor(images=[img], text="Describe the driving scene.", return_tensors="pt")
            inputs = {k: v.to(f"cuda:{GPU_ID}") for k, v in inputs.items()}
            
            pixel_values = inputs["pixel_values"]  # shape: [1, N, 3, 336, 336]
            if pixel_values.ndim == 5:
                # Flatten patches: [1, N, 3, H, W] -> [N, 3, H, W]
                pixel_values = pixel_values.squeeze(0)

            pixel_values = pixel_values.to(f"cuda:{GPU_ID}")

            with torch.no_grad():
                vision_features = model.vision_tower(pixel_values)[0]  # [1, seq_len, dim]
                pooled = vision_features.mean(dim=1).squeeze(0).cpu()
                embeddings.append(pooled)
    
        embedding_data = torch.stack(embeddings)
             
        #save embeddings     
        
        output_dir.mkdir(parents=True, exist_ok=True)

        save_file({
            "frame_data": frame_data,
            "embedding_data": embedding_data
        }, str(output_path))

        tqdm.write(f"Processed: {rel_path} to {output_path}")
        
    except Exception as e:
        tqdm.write(f"Failed on {chunk_path}: {e}") 
        traceback.print_exc()       
        