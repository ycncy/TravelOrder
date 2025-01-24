import re
import pandas as pd
import torch
from transformers import pipeline
from sklearn.metrics import precision_recall_fscore_support, classification_report

def preprocess_sentences(sentences):
    """
    Preprocessing pipeline:
    1. Extract tagged entities from text
    2. Create character-level BIO labels
    3. Maintains entity offsets for proper alignment
    """
    tag_pattern = r"<(ORIG|DEST)>([^<]+)<\1/>"
    clean_sentences = []
    entities = []

    for sentence in sentences:
        if not isinstance(sentence, str) or not sentence.strip():
            continue

        matches = list(re.finditer(tag_pattern, sentence))
        clean_text = re.sub(tag_pattern, r"\2", sentence)
        char_labels = ['O'] * len(clean_text)
        sentence_entities = []
        offset = 0

        for match in matches:
            tag, value = match.groups()
            start = clean_text.find(value, offset)
            end = start + len(value)

            label_prefix = "B-" + tag if tag == "ORIG" else "B-DEST"
            inside_label = "I-" + tag if tag == "ORIG" else "I-DEST"

            for i in range(start, end):
                char_labels[i] = label_prefix if i == start else inside_label

            sentence_entities.append({
                'text': value.strip(),
                'start': start,
                'end': end,
                'type': tag
            })

            offset = end

        clean_sentences.append(clean_text)
        entities.append({
            'entities': sentence_entities,
            'char_labels': char_labels
        })

    return clean_sentences, entities

def load_evaluation_dataset(file_path):
    """
    Load and preprocess evaluation dataset
    """
    data = pd.read_csv(file_path, names=["sentence"])
    sentences = data["sentence"].tolist()
    return preprocess_sentences(sentences)

def match_entities(true_entities, predictions):
    """
    Enhanced entity matching with more flexible criteria
    """
    matched_types = []
    unmatched_true_entities = true_entities.copy()

    for pred in predictions:
        best_match = None
        best_score = 0

        for i, true_entity in enumerate(unmatched_true_entities):
            # Compute matching score
            text_overlap = len(set(pred['word'].lower()) & set(true_entity['text'].lower()))
            type_match = pred['entity_group'] == true_entity['type']
            
            # Combined score with type matching
            score = text_overlap if type_match else (text_overlap / 2)

            if score > best_score:
                best_score = score
                best_match = (i, true_entity['type'])

        # If a good match is found
        if best_match and best_score > 0:
            matched_types.append(best_match[1])
            unmatched_true_entities.pop(best_match[0])

    # Ensure we capture all true types
    return matched_types, [entity['type'] for entity in true_entities]

def evaluate_model(nlp, sentences, entities, output_file="evaluation_results.txt"):
    """
    Comprehensive model evaluation with enhanced matching
    """
    all_true_types = []
    all_pred_types = []

    for sentence, sentence_entities in zip(sentences, entities):
        predictions = nlp(sentence)
        
        # Convert predictions to character positions
        for pred in predictions:
            pred['start'] = sentence.find(pred['word'])
            pred['end'] = pred['start'] + len(pred['word'])

        # Match entities
        matched_pred_types, true_types = match_entities(
            sentence_entities['entities'], 
            predictions
        )

        all_true_types.extend(true_types)
        all_pred_types.extend(matched_pred_types)

    # Print debugging information
    print(f"Number of True Labels: {len(all_true_types)}")
    print(f"Number of Predicted Labels: {len(all_pred_types)}")

    # Ensure labels are unique before computing metrics
    unique_true_types = list(dict.fromkeys(all_true_types))
    unique_pred_types = list(dict.fromkeys(all_pred_types))

    # Compute metrics
    precision, recall, f1, _ = precision_recall_fscore_support(
        all_true_types, all_pred_types, average='weighted'
    )
    report = classification_report(all_true_types, all_pred_types)

    # Write results to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Evaluation Metrics:\n")
        f.write(report)
        f.write(f"\nPrecision: {precision:.4f}\n")
        f.write(f"Recall: {recall:.4f}\n")
        f.write(f"F1-Score: {f1:.4f}\n")

    return precision, recall, f1

def main():
    # Load model
    model_path = "../../../models/camembert/trained_model"
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    
    nlp = pipeline(
        "ner", 
        model=model_path, 
        tokenizer=model_path, 
        aggregation_strategy="simple", 
        device=device
    )

    # Load and preprocess dataset
    file_path = "../../evaluation_data.csv"
    sentences, entities = load_evaluation_dataset(file_path)

    # Evaluate model
    precision, recall, f1 = evaluate_model(
        nlp, 
        sentences, 
        entities, 
        output_file="evaluation_results.txt"
    )

if __name__ == "__main__":
    main()