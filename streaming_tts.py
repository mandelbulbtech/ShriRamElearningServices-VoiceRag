import os
import openai
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
 
# Load environment variables
load_dotenv()
 
# Azure OpenAI Configuration from environment variables
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')
 
# Azure Speech Configuration from environment variables
AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')
AZURE_SERVICE_REGION = os.getenv('AZURE_SERVICE_REGION')
 
# Set OpenAI API Configuration
openai.api_type = "azure"
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_version = "2024-02-01"
openai.api_key = AZURE_OPENAI_API_KEY
 
# Configure Speech Service
speech_config = speechsdk.SpeechConfig(
    endpoint=f"wss://{AZURE_SERVICE_REGION}.tts.speech.microsoft.com/cognitiveservices/websocket/v2",
    subscription=AZURE_SPEECH_KEY
)
 
# Speech Configuration
speech_config.speech_synthesis_voice_name = "en-US-BrianMultilingualNeural"
 
# Low Latency Settings
speech_config.set_property(
    speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, "100"
)
speech_config.set_property(
    speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "50"
)
 
# Audio Configuration
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
 
# Real-time Audio Streaming
speech_synthesizer.synthesizing.connect(lambda evt: print("[AUDIO]", end=""))
 
# Timeout Configuration
properties = {
    "SpeechSynthesis_FrameTimeoutInterval": "100000000",
    "SpeechSynthesis_RtfTimeoutThreshold": "10"
}
speech_config.set_properties_by_name(properties)
 
# Create Speech Request
tts_request = speechsdk.SpeechSynthesisRequest(
    input_type=speechsdk.SpeechSynthesisRequestInputType.TextStream
)
tts_task = speech_synthesizer.speak_async(tts_request)
 
# OpenAI API Call
completion = openai.ChatCompletion.create(
    deployment_id=AZURE_OPENAI_DEPLOYMENT_NAME,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me all about azure tools in 10000 words"}
    ],
    max_tokens=800,
    temperature=0,
    stream=True
)
 
# Process Stream
for chunk in completion:
    if "choices" in chunk and len(chunk["choices"]) > 0:
        delta = chunk["choices"][0].get("delta", {})
        chunk_text = delta.get("content", "")
       
        if chunk_text:
            print(chunk_text, end="")
            tts_request.input_stream.write(chunk_text)
 
# Cleanup
tts_request.input_stream.close()
result = tts_task.get()
print("[TTS END]", end="")
 