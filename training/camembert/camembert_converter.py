from transformers import AutoTokenizer, AutoModelForTokenClassification, Trainer, TrainingArguments, pipeline
from datasets import Dataset
import torch
import re


def prepare_tokenizer(model_name, sentences):
    """
    Prepares the tokenizer for NER
    1. Loads Camembert (pre-trained model)
    2. Extract all cities from the sentences
    3. Add special tokens and add cities as tokens
    """

    # Load Camembert tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

    # Regex to match <ORIG> <DEST> tags and extract city names
    tag_pattern = r"<(ORIG|DEST)>([^<]+)<\1/>"
    cities = set()

    # Loop through each sentence & find city names within <ORIG> <DEST>
    for sentence in sentences:
        if isinstance(sentence, str):
            matches = re.finditer(tag_pattern, sentence)
            for match in matches:
                cities.add(match.group(2).strip())

    special_tokens = {
        "additional_special_tokens": [
            "<ORIG>", "<ORIG/>",
            "<DEST>", "<DEST/>"
        ]
    }

    # Add special tokens to the tokenizer
    tokenizer.add_special_tokens(special_tokens)

    # Add cities as tokens to the tokenizer's vocabulary
    tokenizer.add_tokens(list(cities))

    return tokenizer


def load_sentences_from_csv(csv_path):
    # Read CSV dataset, stripping any extra whitespace
    with open(csv_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]


def preprocess_sentences(sentences):
    """
    Preprocessing pipeline:
    1. Extract tagged entities from text
    2. Create character-level BIO (Beginning, Inside, Outside) labels
    3. Maintains entity offsets for proper alignment
    """

    # Regex to match <ORIG> <DEST> tags and extract city names
    tag_pattern = r"<(ORIG|DEST)>([^<]+)<\1/>"
    clean_sentences = []
    entities = []  # Hold entities & labels for each sentence

    # Loop through each sentence, skip any that are not strings or are empty
    for sentence in sentences:
        if not isinstance(sentence, str) or not sentence.strip():
            continue

        # Extract entities and create clean text by removing tags
        matches = list(re.finditer(tag_pattern, sentence))
        clean_text = re.sub(tag_pattern, r"\2", sentence)

        # Initialize character-level BIO labels (O = outside entity, B/I = beginning/inside entity)
        char_labels = ['O'] * len(clean_text)
        sentence_entities = []
        offset = 0  # Track position to avoid overlapping matches

        for match in matches:
            # tag holds the entity type (ORIG or DEST)
            # value holds the city name
            # start and end calculate the character positions of the entity within clean_text
            # offset ensures that if an entity appears multiple times, the next search starts after the previous match
            tag, value = match.groups()
            start = clean_text.find(value, offset)
            end = start + len(value)

            label_prefix = "B-" + tag if tag == "ORIG" else "B-DEST"
            inside_label = "I-" + tag if tag == "ORIG" else "I-DEST"

            for i in range(start, end):
                char_labels[i] = label_prefix if i == start else inside_label

            # Append entity info to sentence_entities
            # Each entity is stored with its text, start and end positions, and type (either ORIG or DEST)
            sentence_entities.append({
                'text': value.strip(),
                'start': start,
                'end': end,
                'type': tag
            })
            # offset is updated to end to avoid overlapping matches
            offset = end

        # Append cleaned sentence and entity info
        clean_sentences.append(clean_text)
        entities.append({
            'entities': sentence_entities,
            'char_labels': char_labels
        })

    return clean_sentences, entities


def debug_tokenization(tokenizer, text, entities):
    """
    Helper function to debug tokenization, printing tokenization info
    and entity alignment with token offsets.
    """

    print("\nDebug Tokenization:")
    print(f"Text: {text}")

    # Get tokenization details
    tokens = tokenizer.tokenize(text)
    encoding = tokenizer(text, return_offsets_mapping=True)
    offsets = encoding.offset_mapping

    print("\nTokenization result:")
    for token, (start, end) in zip(tokens, offsets):
        print(f"Token: {token:15} Offset: ({start:3}, {end:3})")

    print("\nEntities:")
    for entity in entities['entities']:
        print(f"Entity: {entity['text']:15} Span: ({entity['start']:3}, {entity['end']:3})")


def tokenize_and_align_labels(sentences, entities, tokenizer):
    """
    Takes preprocessed sentences and aligns their character-level BIO labels to token-level labels
    Needed for NER
    """

    # Tokenize sentences with truncation and padding; obtain token offsets
    tokenized_inputs = tokenizer(
        sentences,
        truncation=True,  # Ensures that long input sequences do not exceed the model’s maximum input length
        padding=True,
        # Ensures that all sentences in a batch have the same length, which is necessary for efficient processing in the model
        return_offsets_mapping=True
        # Returns the character start and end offsets of each token in offset_mapping, for aligning character-level labels to tokens.
    )

    labels = []  # Store label IDs aligned to tokens

    # Loops through each sentence and its corresponding entity information
    for i, (sentence, entity_info) in enumerate(zip(sentences, entities)):
        # Debug first few examples
        if i < 2:
            debug_tokenization(tokenizer, sentence, entity_info)

        label_ids = []

        # start and end positions of each token in the original sentence text, which is used to match tokens with character-level labels
        offset_mapping = tokenized_inputs['offset_mapping'][i]

        # Convert character-level labels to token-level labels
        for token_start, token_end in offset_mapping:

            # If token_start == token_end, it’s a special token and that should be ignored by the model during training, hence labeled as -100
            # -100 tells the model to ignore this token during loss computation
            if token_start == token_end:
                label_ids.append(-100)
                continue

            # Extracts the list of character-level labels for the current token span. 
            # These labels provide information about whether the token contains part of a location entity
            token_chars = entity_info['char_labels'][token_start:token_end]

            # Determine token label based on character labels
            if "B-ORIG" in token_chars:
                label_ids.append(1)
            elif 'I-ORIG' in token_chars:
                label_ids.append(2)
            elif 'B-DEST' in token_chars:
                label_ids.append(3)
            elif 'I-DEST' in token_chars:
                label_ids.append(4)
            else:
                label_ids.append(0)

        labels.append(label_ids)

    # Add labels to the tokenized input, remove offset mappings since no longer needed
    tokenized_inputs["labels"] = labels
    del tokenized_inputs['offset_mapping']

    return tokenized_inputs


def main():
    """
    NER fine-tuning pipeline:
    1. Data preparation & tokenization
    2. Model initialization with label scheme preservation
    3. Training configuration
    4. Model training & evaluation
    """

    # Configuration
    model_name = "Jean-Baptiste/camembert-ner"
    train_dataset_path = "../../data/dataset_output.csv"
    model_save_path = "../../travel_order/data/camembert/trained_model"

    # Load & prepare data
    train_sentences = load_sentences_from_csv(train_dataset_path)
    tokenizer = prepare_tokenizer(model_name, train_sentences)
    clean_sentences, entities = preprocess_sentences(train_sentences)

    # Get the original model's label structure
    original_model = AutoModelForTokenClassification.from_pretrained(model_name)
    num_labels = 5  # Adjusted for "O", "B-ORIG", "I-ORIG", "B-DEST", "I-DEST"
    id2label = {0: "O", 1: "B-ORIG", 2: "I-ORIG", 3: "B-DEST", 4: "I-DEST"}
    label2id = {v: k for k, v in id2label.items()}

    # Initialize model with the original label structure
    model = AutoModelForTokenClassification.from_pretrained(
        model_name,
        num_labels=num_labels,
        id2label=id2label,
        label2id=label2id
    )

    # Update the model's token embeddings for new vocabulary
    # This command resizes the token embeddings of the model to match the size of the vocabulary in the tokenizer
    # It is essential when you have added new tokens (such as custom tags like <ORIG> and <DEST>) to the tokenizer’s vocabulary
    # Without resizing, the model’s original embedding layer would not have entries for these new tokens, which could lead to issues during training or inference
    model.resize_token_embeddings(len(tokenizer))

    # Tokenize and align labels
    tokenized_data = tokenize_and_align_labels(clean_sentences, entities, tokenizer)

    # Convert to Hugging Face Dataset
    dataset = Dataset.from_dict({
        "input_ids": tokenized_data["input_ids"],
        "attention_mask": tokenized_data["attention_mask"],
        "labels": tokenized_data["labels"]
    })

    # Set up training arguments
    training_args = TrainingArguments(
        output_dir='./results',
        eval_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01,
        save_steps=1000,
        save_total_limit=2,
    )

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        eval_dataset=dataset,
        tokenizer=tokenizer
    )

    # Train the model
    print("\nStarting training...")
    trainer.train()

    # Save the model
    print(f"\nSaving model to {model_save_path}")
    model.save_pretrained(model_save_path)
    tokenizer.save_pretrained(model_save_path)

    # Test predictions
    print("\nTesting model with sample predictions:")
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    nlp = pipeline(
        "ner",
        model=model,
        tokenizer=tokenizer,
        aggregation_strategy="simple",
        device=device
    )

    # Test on a few samples
    test_samples = clean_sentences[:5]
    for sentence in test_samples:
        print(f"\nOriginal sentence: {sentence}")
        ner_results = nlp(sentence)
        for entity in ner_results:
            print(f"Entity: {entity['word']}, Label: {entity['entity_group']}, Score: {entity['score']:.4f}")


if __name__ == "__main__":
    main()
