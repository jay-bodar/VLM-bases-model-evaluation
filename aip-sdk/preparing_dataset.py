import os
import cv2
import base64
import requests
import pandas as pd
from datasets import load_dataset
from dotenv import load_dotenv

load_dotenv()

VIDEO_DIR = r"C:\Users\JAY\OneDrive\Desktop\Resaro\evaluation pipeline\aip-sdk\MSRVTT_Test_100"
OUTPUT_CSV = "dataset.csv"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")



def extract_base64_frames(video_path, num_frames=3):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return []

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames <= 0:
        cap.release()
        return []

    step = max(total_frames // num_frames, 1)
    base64_frames = []

    for i in range(num_frames):
        frame_idx = i * step
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        success, frame = cap.read()
        if success:
            _, buffer = cv2.imencode(".jpg", frame)
            b64_str = base64.b64encode(buffer).decode("utf-8")
            base64_frames.append(b64_str)

    cap.release()
    return base64_frames






hf_dataset = load_dataset("friedrichor/MSR-VTT", "test_1k", split="test")
rows = []
for index, entry in enumerate(hf_dataset):
    if index >= 100:
        break

    video_id = str(entry["video_id"])
    video_path = os.path.join(VIDEO_DIR, f"{video_id}.mp4")

   
    frames = extract_base64_frames(video_path, num_frames=3)
   
    prompt_text = (
        "Describe what happens in these sequential video frames in a single concise "
        "sentence of roughly 10 to 12 words."
    )

    content_payload = [{"type": "text", "text": prompt_text}]
    for b64 in frames:
        content_payload.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
        })





    print(f"[{index+1}/{100}] Generating caption for {video_id}...")   
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": [{"role": "user", "content": content_payload}],
            "max_tokens": 30,  
        },
    )




    if response.status_code == 200:
        sut_summary = response.json()["choices"][0]["message"]["content"].strip()
    else:
        print(f"API Error ({response.status_code}): {response.text}")
        sut_summary = ""

    rows.append({
        "input_id": str(video_id),
        "task_type": "single_turn_llm",
        "prompt": prompt_text,
        "expected_output": entry["caption"],
        "sut_response": sut_summary,
        "category": str(entry["category"]),
        "start_time": float(entry["start time"]),
        "end_time": float(entry["end time"]),
    })




df = pd.DataFrame(rows)
df.to_csv(OUTPUT_CSV, index=False)

print(f"\nSuccessfully generated 100 rows and saved to '{OUTPUT_CSV}'.")