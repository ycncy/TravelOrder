from transformers import AutoTokenizer, AutoModelForTokenClassification, Trainer, TrainingArguments, pipeline
import re


model_name = "Jean-Baptiste/camembert-ner"

def prepare_tokenizer():
    # load pre-trained tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

    special_tokens = {
        "additional_special_tokens": [
            "<ORIG>", "</ORIG>",
            "<DEST>", "</DEST>"
        ]
    }

    tokenizer.add_special_tokens(special_tokens)

    return tokenizer


def extract_and_process_entities(text, tokenizer, nlp):
    # regex to find all occurrences of <ORIG> and <DEST> tags
    tag_pattern = r"<(ORIG|DEST)>([^<]+)<\1/>"
    matches = list(re.finditer(tag_pattern, text))

    # store original tagged entities
    tagged_entities = []
    for match in matches: 
        tag, value = match.groups()
        tagged_entities.append({
            'tag': tag,
            'value': value,
            'original_text': match.group(0)
        })

    # remove tag for ner processing
    clean_text = re.sub(tag_pattern, r"\2", text)

    ner_results = nlp(clean_text)

    print("=================================================")
    print("Tokenization analysis:")

    for entity in tagged_entities:
        tokens = tokenizer.tokenize(entity["value"])
        print("=================================================")
        print(f"{entity['tag']}: {entity['value']} -> {tokens}")

        # if city name being split, add as special token
        if len(tokens) > 1:
            print("=================================================")
            print(f"Adding {entity['value']} as special token")
            tokenizer.add_special_tokens({
                "additional_special_tokens": [entity['value']]
            })
            # Verify the new tokenization
            new_tokens = tokenizer.tokenize(entity['value'])
            print("=================================================")
            print(f"New tokenization: {entity['value']} -> {new_tokens}")

    print("=================================================")
    print("\nTokenization of text without tags:")
    tokens = tokenizer.tokenize(clean_text)
    print(tokens)

    return tagged_entities, ner_results


# init nlp
tokenizer = prepare_tokenizer()
model = AutoModelForTokenClassification.from_pretrained(model_name)
nlp = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

test_sentences = [
    "Je veux aller de <ORIG>Aast<ORIG/> à <DEST>Saint-Tropez<DEST/>"
]

for sentence in test_sentences:
    print(f"\nProcessing: {sentence}")
    tagged_entities, ner_results = extract_and_process_entities(sentence, tokenizer, nlp)
    
    print("\nNER Results:")
    for entity in ner_results:
        print(f"Entity: {entity['word']}, Label: {entity['entity_group']}, Score: {entity['score']:.4f}")
    
    print("\nTagged Entities:")
    for entity in tagged_entities:
        print(f"Tag: {entity['tag']}, Value: {entity['value']}")