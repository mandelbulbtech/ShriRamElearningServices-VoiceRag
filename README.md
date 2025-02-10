# ShriRamElearningServices-VoiceRag

# Setting Up a Python Virtual Environment and Configuring Environment Variables

## 1. Creating a Virtual Environment in Python
A virtual environment allows you to create an isolated Python environment for your projects. To create one, follow these steps:

### Windows
```sh
python -m venv venv
```
To activate the virtual environment:
```sh
venv\Scripts\activate
```

### macOS/Linux
```sh
python3 -m venv venv
```
To activate the virtual environment:
```sh
source venv/bin/activate
```

Once activated, the terminal will show the `(venv)` prefix.

## 2. Setting Up Environment Variables
You can store sensitive credentials like API keys in environment variables. Here is where you can set your environment variables:

### Example Environment Variables:
```sh
AZURE_OPENAI_API_KEY="your_api_key_here"
AZURE_OPENAI_ENDPOINT="https://your_endpoint_here.azure.com/"
AZURE_OPENAI_DEPLOYMENT_NAME="your_deployment_name_here"

AZURE_SPEECH_KEY="your_speech_key_here"
AZURE_SPEECH_REGION="your_speech_region_here"
```

You can set these in your local environment according to your operating system.

## 3. Installing Dependencies from `requirements.txt`
After activating the virtual environment, install required dependencies from `requirements.txt` using:
```sh
pip install -r requirements.txt
```
This will install all necessary Python packages listed in the file.

## 3. Run the Python Script
After installing using `requirements.txt` run your python script:
```sh
python .\continous_detection.py 
```
for continous detection of voice
```sh
python .\streaming_tts.py       
```
for streaming the tts (Text-to-speech) output



