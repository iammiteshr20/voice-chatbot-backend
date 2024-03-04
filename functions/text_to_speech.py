import os
import requests
import uuid
from settings import settings


# Generate a random UUID
output_random_filename = str(uuid.uuid4()) + ".wav"


# Eleven Labs convert text to speech
def convert_text_to_speech(message):
    body = {
        "text": message,
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0
        }
    }

    voice_shaun = "mTSvIrm2hmcnOvb21nW2"
    voice_rachel = "21m00Tcm4TlvDq8ikWAM"
    voice_antoni = "ErXwobaYiN019PkySvjV"

    # Construct request headers and url
    headers = { "xi-api-key": settings.eleven_labs_api_key, "Content-Type": "application/json", "accept": "audio/mpeg" }
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"

    try:
        response = requests.post(endpoint, json=body, headers=headers)
    except Exception as e:
        return

    if response.status_code == 200:
        # Write the audio file to the specified folder
        output_folder = 'audios/output/'
        output_path = os.path.join(output_folder, f"{output_random_filename}")
        with open(output_path, "wb") as f:
            f.write(response.content)

        return output_path
    else:
        return
