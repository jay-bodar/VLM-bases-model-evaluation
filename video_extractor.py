import os
import zipfile
from datasets import load_dataset


# Configs
ZIP_PATH = r""      # Path to your zip file
NUM_VIDEOS = 100


OUTPUT_DIR = r"aip-sdk\MSRVTT_Test_100"    # Target extraction folder
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get the first 100 test video IDs from Hugging Face

print("Loading MSR-VTT test dataset metadata...")
hf_dataset = load_dataset("friedrichor/MSR-VTT", "test_1k", split="test")

target_video_ids = set()
for index, entry in enumerate(hf_dataset):
    if index >= NUM_VIDEOS:
        break
    video_id = str(entry.get("video_id", f"video{index}"))
    target_video_ids.add(video_id)

print(f"Targeting {len(target_video_ids)} test video IDs (e.g., {list(target_video_ids)[:3]})...\n")






# Extract matching video files from zip

extracted_count = 0

with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
    zip_members = zf.namelist()
    
    for member in zip_members:
        # Skip directory entries
        if member.endswith('/'):
            continue
            
        filename = os.path.basename(member)           
        file_stem, _ = os.path.splitext(filename)      
        
        # Check if this zip entry matches one of our target video IDs
        if file_stem in target_video_ids:
            target_path = os.path.join(OUTPUT_DIR, filename)
            
            # Stream extract directly to output folder
            with zf.open(member) as source, open(target_path, "wb") as target_file:
                target_file.write(source.read())
                
            extracted_count += 1
            print(f"[{extracted_count}/{NUM_VIDEOS}] Extracted: {filename}")
            
            target_video_ids.remove(file_stem)
            
            if not target_video_ids:
                break

print(f"\nSuccessfully extracted {extracted_count} videos to:\n{OUTPUT_DIR}")