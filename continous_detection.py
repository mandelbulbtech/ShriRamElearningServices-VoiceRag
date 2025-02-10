import azure.cognitiveservices.speech as speechsdk
import os
import time
from dotenv import load_dotenv


# Load the .env file to get the values
load_dotenv()

# Load API key and region securely (use environment variables)
speech_key = os.getenv('AZURE_SPEECH_KEY')  # Replace with actual API key if needed
service_region = os.getenv("AZURE_SERVICE_REGION")  # Change to your Azure region

# Check if API key is set
if not speech_key:
    raise ValueError("Azure Speech Key not set. Use environment variables.")

# Configure speech recognition settings
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.speech_recognition_language = "en-US"

# Create the recognizer
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

# Global variable to control listening state
is_listening = True

def stop_cb(evt):
    """Callback function to stop recognition"""
    print(f"CLOSING on event: {evt}")
    global is_listening
    is_listening = False
    speech_recognizer.stop_continuous_recognition()

def recognizing_callback(evt):
    """Callback when speech is detected but not yet finalized"""
    print(f"RECOGNIZING: {evt.result.text}")

def recognized_callback(evt):
    """Callback when speech is successfully recognized"""
    print(f"RECOGNIZED: {evt.result.text}")
    
    # Stop listening if the user says "stop listening"
    if evt.result.text.lower() == "stop listening":
        print("Voice command received: Stopping recognition...")
        stop_cb(evt)

def canceled_callback(evt):
    """Callback when an error occurs"""
    print(f"CANCELED: Reason = {evt.reason}")
    if evt.reason == speechsdk.CancellationReason.Error:
        print(f"Error Details: {evt.error_details}")
    stop_cb(evt)

# Attach event handlers
speech_recognizer.recognizing.connect(recognizing_callback)
speech_recognizer.recognized.connect(recognized_callback)
speech_recognizer.session_started.connect(lambda evt: print("SESSION STARTED"))
speech_recognizer.session_stopped.connect(lambda evt: print("SESSION STOPPED"))
speech_recognizer.canceled.connect(canceled_callback)

# Start continuous recognition
print("Listening... Say 'stop listening' to exit.")
speech_recognizer.start_continuous_recognition()

# Keep the script running while listening
while is_listening:
    time.sleep(0.5)

print("Recognition stopped. Exiting program.")
