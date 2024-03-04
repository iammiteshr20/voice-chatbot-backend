# VOICE-CHATBOT-BACKEND

## Description
A doctor’s office is overloaded with patients calling in to schedule appointments.
They have tasked you with building a voice bot for the doctor's office that is capable
of engaging in conversation and responding to patient questions about scheduling
an appointment with a doctor.. The doctor will provide available time slots for
appointments. The patient will call the voice bot to schedule an appointment with
the doctor.

## Installation
1. Clone the repository

2. Setup virtual environment
   python3.11 -m venv venv

3. Activate venv
   source venv/bin/activate

4. pip install -r requirements.txt

## Voice Recognition
This project uses AssemblyAI for voice recognition. You will need to sign up for an account and obtain an API key. Once you have the API key, add it to the configuration file or set it as an environment variable.

## Text to Speech
Text-to-speech functionality is provided by Eleven Labs. Similar to voice recognition, you'll need to obtain an API key and add it to the configuration file or set it as an environment variable.

## Usage
Explain how to use your project. Include any important details about setting up/configuring the project or running it.

Running the Server
To run the FastAPI server, execute the following command:

uvicorn main:app --reload

Replace main with the name of your main Python file and app with the name of your FastAPI instance if necessary.

The --reload flag enables auto-reloading, which means the server will restart automatically whenever you make changes to your code during development.

## API Documentation
Once the server is running, you can access the API documentation by navigating to http://127.0.0.1:8000/docs in your web browser. This interactive documentation provides details about all the available endpoints, request parameters, and response formats.

