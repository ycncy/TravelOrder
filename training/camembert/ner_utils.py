import re

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