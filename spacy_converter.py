import re
import pandas as pd
import spacy
from spacy.tokens import DocBin
import sys

args = sys.argv
if (len(args) < 2):
   print("You need to provide the name of the dataset csv file as an argument")
   sys.exit()

# AFTER
def extract_data(text):
    # Use regular expressions to find all occurrences of <ORIG> and <DEST> tags
    pattern = r"<(ORIG|DEST)>([^<]+)<\1/>"
    matches = list(re.finditer(pattern, text))

    # Create a modified version of the text with tags removed
    modified_text = re.sub(r"<(ORIG|DEST)>([^<]+)<\1/>", r"\2", text)

    # Calculate the new positions based on the modified text
    entities = []
    offset = 6
    for match in matches:
        tag, value = match.groups()
        start = match.start(2) - offset
        end = start + len(value)
        entities.append((start, end, tag))
        # Adjust offset by the length of removed tags
        offset += len(f"<{tag}>") + len(f"<{tag}/>")
    return (modified_text, entities)

def get_formatted_array(path):
  cols = ["SENTENCE"]
  formatted_array = []
  data = pd.read_csv(path, delimiter=",", header=None, names=cols)
  for index, row in data.iterrows():
    if (row.SENTENCE == None or row.SENTENCE == ""):
       break
    data = extract_data(row.SENTENCE)
    formatted_array.append(data)
  return formatted_array

def write_db_to_disk(data):
  db = DocBin()
  nlp = spacy.blank("fr")
  for text, annotations in data:
      doc = nlp(text)
      ents = []
      for start, end, label in annotations:
          span = doc.char_span(start, end, label=label)
          ents.append(span)
      doc.ents = ents
      db.add(doc)
  db.to_disk("./train.spacy")

path = args[1]
print("Getting formatted array...")
data = get_formatted_array(path)
print("Writing DocBin to disk...")
write_db_to_disk(data)
print("Done.")