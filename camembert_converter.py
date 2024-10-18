from transformers import AutoTokenizer, AutoModelForTokenClassification, Trainer, TrainingArguments, pipeline
import re

# Load pre-trained tokenizer and model
model_name = "Jean-Baptiste/camembert-ner"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
model = AutoModelForTokenClassification.from_pretrained(model_name)

nlp = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

sentence = "Je veux aller de <ORIG>Aast<ORIG/> à <DEST>La Grigonnais<DEST/>"
sentence2 = "Je veux aller de <ORIG>Aast<ORIG/> à <DEST>Saint-Tropez<DEST/>"

# Extract <ORIG> and <DEST> tags
def extract_data(text):
    # Use regular expressions to find all occurrences of <ORIG> and <DEST> tags
    pattern = r"<(ORIG|DEST)>([^<]+)<\1/>"
    matches = list(re.finditer(pattern, text))

    # Create a modified version of the text with tags removed
    modified_text = re.sub(r"<(ORIG|DEST)>([^<]+)<\1/>", r"\2", text)
    
    # Perform NER on modified text
    result = nlp(modified_text)

    # NER result from Camembert
    print("NER from Camembert:")
    for entity in result:
        print(f"Entity: {entity['word']}, Label: {entity['entity_group']}, Score: {entity['score']}")

    # Calculate the new positions based on the modified text
    entities = []
    offset = 6
    for match in matches:
        tag, value = match.groups()
        start = match.start(2) - offset
        end = start + len(value)
        entities.append({'entity_group': tag, 'word': value, 'start': start, 'end': end})
        # Adjust offset by the length of removed tags
        offset += len(f"<{tag}>") + len(f"<{tag}/>")

    # Combine NER results and custom tag extraction
    print("=================================================")
    print("Combined Results (CamemBERT NER + Custom Tags):")
    combined_results = result + entities
    for entity in combined_results:
        print(f"Entity: {entity['word']}, Label: {entity['entity_group']}")

    return combined_results


def merge_subwords(tokens):
    merged_tokens = []
    current_word = ""
    for token in tokens:
        if token.startswith("▁"):  # New word starts
            if current_word:
                merged_tokens.append(current_word)
            current_word = token[1:]  # Remove the leading '▁'
        else:
            current_word += token  # Continue subword
    if current_word:
        merged_tokens.append(current_word)  # Append last word
    return merged_tokens


# Extract data
single_sentence_result = extract_data(sentence)

# Tokenization
cleaned_sentence = re.sub(r"<(ORIG|DEST)>([^<]+)<\1/>", r"\2", sentence)
tokens = tokenizer.tokenize(cleaned_sentence)
print("=================================================")
print("Tokens:", tokens)

# Join, merge tokens
merged_tokens = merge_subwords(tokens)
print("=================================================")
print("Merged Tokens:", merged_tokens)

# Encode the tokens
#inputs = tokenizer.encode_plus(merged_tokens, return_tensors="pt", is_split_into_words=True)
#print("Encoded Input IDs:", inputs['input_ids'])