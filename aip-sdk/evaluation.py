import os
import pandas as pd
import aip_sdk as aip
from datasets import load_dataset


from dotenv import load_dotenv
load_dotenv()

INPUT_CSV = "dataset.csv"

BASE_URL = os.environ.get("AIP_BASE_URL", "http://localhost:8010")
WEB_UI = "http://localhost:3010"
CLIENT = aip.init(
    BASE_URL, 
    username=os.environ.get("AIP_USERNAME"), 
    password=os.environ.get("AIP_PASSWORD")
)

try:
    ws = aip.Workspace.get_by_name(os.environ.get("AIP_WORKSPACE_NAME", "Default"))
except Exception:
    existing = aip.Workspace.list()
    ws = existing[0] if existing else aip.Workspace.create(name="My Workspace")





project, _ = aip.Project.get_or_create(
    name="GPT video summarization eval",
    schema="gdi_text_v1",
    task_type="single_turn_llm",
    dimensions=[aip.Dimension(name="video_category", column="category",
                              values=[str(i) for i in range(20)])],
    workspace_id=ws.id,
)




df = pd.read_csv(INPUT_CSV)

df["input_id"] = df["input_id"].astype(str)
df["category"] = df["category"].astype(str)


dataset = project.upload_dataset(df.head(25),name="MSR-VTT Test Set")

version = dataset.latest_version()



report = dataset.run_checks(version.id, label="pre-promote")
if report.status == "PASS":
    version = dataset.promote(version.id)
else:
    version = dataset.promote(version.id, force=True, reason="demo dataset")



metrics = ["llm.rouge", "llm.correctness", "llm.conciseness", "llm.answer_relevance"]
# metrics = ["llm.rouge"] 



with aip.run(
    project=project.id,
    dataset=f"{dataset.id}@v{version.version}",
    metrics=metrics,
) as run:
    run.poll_status(interval=5, timeout=3600)
    page = run.results(page=1, page_size=100)
    run_id = run.id



for m in page.metrics:
    print(f"{m.scorer}: mean={m.mean:.3f} pass_rate={m.pass_rate:.0%} (n={m.count})")
