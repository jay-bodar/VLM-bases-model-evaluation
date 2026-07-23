# VLM-bases-model-evaluation
Using AIP platform and it's APIs to evaluate VLM(Visual Language Models) based models for short video summarization. 


## I am using [MST-VTT dataset](https://huggingface.co/datasets/friedrichor/MSR-VTT) to evaluate model(OpenRouter)'s performance: Here are the steps to run the end to end evaluation.

### Step 1: Download the provided aip-sdk-0.1.3.zip


### Step 2: Extract it inside your project folder
It will create \aip-sdk folder in which all the setup files ".whl" will be given.

### Step 3: Creating a virtual enviromnent
Create environment and then activate it. 


### Step 4: Install all the dependencies

Install below given libraries along with AIP-SDK
- pandas
- requests
- datasets
- opencv-python
- python-dotenv


### Step 5: Now set the environment variables in a ".env" file
Copy this variables in your .env file and set your model's API key here.
```
# ── AIP connection (Step 0.1) ─────────────────────────────
AIP_BASE_URL = "https://api.trials.aip-v2.resarodev.ai"   # remote trial host
AIP_WEB_UI = "https://trials.aip-v2.resarodev.ai"       # optional (auto-derived if omitted)

# Auth — use the AIP username/password from the credentials email
AIP_USERNAME = "<AIP-USERNAME>"                            # required (unless using AIP_TOKEN)
AIP_PASSWORD = "<AIP-PASSWORD>"                            # required (unless using AIP_TOKEN)
# os.environ["AIP_TOKEN"]  = "<AIP-TOKEN>"              # alternative to username/password

# ── OpenAI SUT (Step 0.2 / 1e) — REQUIRED ──────────────────
OPENROUTER_API_KEY = "<YOUR-API-KEY>"        
 
```             

### Step 6: Then download the MSR-VTT dataset from HuggingFace
You can get the zip file of the dataset by clonning this huggingface repository
Run this code in command prompt at a location where you want to clone.
```
git clone https://huggingface.co/datasets/friedrichor/MSR-VTT
```
After running it you will find MSRVTT_Videos.zip folder inside MSR-VTT repo folder.


### Step 7: Extract only test set videos
As this MSRVTT_Videos.zip folder contain all the training and testing video clips
run video_extractor.py file to extract only test set's selected files from zip folder

You can select as many rows of test set as you want. I have selected 100 rows for testing purpose by setting a variable "NUM_VIDEOS = 100" inside video_extractor.py file. 

### Step 7: Prepare final dataset
Once you extract all the videos, you can generate final dataset by running preparing_dataset.py inside aip-sdk folder.
In final dataset, we are setting all the necessary columns(contains sample summary of video and more) of our test dataset along with one extra column of our model's output that we want to evaluate.

### Step 8: Evaluate the model
Now we are pushing our model's response appended dataset onto the AIP platform through it's API for evaluation on different banchmark matrices.
This can be done by running evaluation.py file in aip-sdk folder.
The results will be available in terminal as well as web UI of AIP under "Projects/GPT video summarization eval/Runs" section.

