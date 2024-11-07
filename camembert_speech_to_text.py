import speech_recognition as sr
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

model_path = './trained_model'
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForTokenClassification.from_pretrained(model_path)

ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak something in French:")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

try:
    # Transcribe audio to text
    text = recognizer.recognize_google(audio, language='fr-FR')
    print(f"Transcription: {text}")
    
    # Use the Camembert NER model on the transcribed text
    ner_results = ner_pipeline(text)
    for entity in ner_results:
        print(f"{entity['word']} - {entity['entity_group']} - {entity['score']:.2f}")
        
except sr.UnknownValueError:
    print("Sorry, I could not understand the audio.")
except sr.RequestError:
    print("Could not request results; check your network connection.")