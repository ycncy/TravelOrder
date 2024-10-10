import speech_recognition as sr

recognizer = sr.Recognizer()

# Use the microphone as the source
with sr.Microphone() as source:
    print("Speak something in French:")
    recognizer.adjust_for_ambient_noise(source)  # Adjust to ambient noise
    audio = recognizer.listen(source)  # Capture the audio

# Recognize the speech using Google Web Speech API
try:
    # Specify the language parameter for French ('fr-FR')
    text = recognizer.recognize_google(audio, language='fr-FR')
    print(f"Transcription: {text}")
except sr.UnknownValueError:
    print("Sorry, I could not understand the audio.")
except sr.RequestError:
    print("Could not request results; check your network connection.")