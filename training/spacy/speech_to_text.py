import speech_recognition as sr
import spacy

nlp = spacy.load("./output/model-best")

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak something in French:")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio, language='fr-FR')
    print(f"Transcription: {text}")
    doc = nlp(text)
    for ent in doc.ents:
        print(f"{ent.text} - {ent.label_}")
except sr.UnknownValueError:
    print("Sorry, I could not understand the audio.")
except sr.RequestError:
    print("Could not request results; check your network connection.")