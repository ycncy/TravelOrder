import pandas as pd
import re
import requests
import math
import csv
import sys

args = sys.argv
if (len(args) != 3):
  print("There needs to be two arguments, one for the template csv path, and one for the target path.")
  sys.exit()


def get_cities_set(cities_set, number_of_cities):
  cities = []
  if number_of_cities > len(cities_set):
    number_of_cities = len(cities_set)
  factor = math.ceil(len(cities_set) / number_of_cities)
  for i in range(number_of_cities):
    if i != 0:
       number = factor * i
    else:
       number = 0
    if number > len(cities_set):
       break
    cities.append(cities_set[number])
  return cities

def get_couples(cities):
  couple_ids = [(x, y) for x in range(len(cities)) for y in range(len(cities)) if x != y]
  cities_couples = []
  for couple in couple_ids:
    cities_couples.append((cities[couple[0]], cities[couple[1]]))
  return cities_couples

def get_cities_from_country(country):
  url = "https://countriesnow.space/api/v0.1/countries/cities"
  response = requests.request("POST", url, headers={}, data={ "country": country })
  JSONresponse = response.json()
  return JSONresponse["data"]

def fill_sentences(cities_couples, template_path):
  data = pd.read_csv(template_path, delimiter=",")
  sentences = []
  for index, row in data.iterrows():
    for couple in cities_couples:
      newSentence = row.SENTENCE.replace("X", couple[0])
      newSentence = newSentence.replace("Y", couple[1])
      sentences.append(newSentence)
  return sentences

def write_to_csv(sentences, path):
   with open(path, 'w', newline="") as file:
      writer = csv.writer(file)
      for sentence in sentences:
        writer.writerow([sentence])
         

all_cities = get_cities_from_country("france")
cities = get_cities_set(all_cities, 50)
cities_couples = get_couples(cities)
sentences = fill_sentences(cities_couples, args[1])
write_to_csv(sentences, args[2])
print("done")


# data = pd.read_csv("./dataset_template.csv", delimiter=",")


# AFTER
def extract_data(text):
    # Use regular expressions to find all occurrences of <ORIG> and <DEST> tags
    pattern = r"<(ORIG|DEST)>([^<]+)<\1/>"
    matches = list(re.finditer(pattern, text))

    # Create a modified version of the text with tags removed
    modified_text = re.sub(r"<(ORIG|DEST)>([^<]+)<\1/>", r"\2", text)

    # Calculate the new positions based on the modified text
    entities = []
    offset = 0
    for match in matches:
        tag, value = match.groups()
        start = match.start(2) - offset
        end = start + len(value)
        entities.append((start, end, tag))
        # Adjust offset by the length of removed tags
        offset += len(f"<{tag}>") + len(f"<{tag}/>")

    return (modified_text, entities)

# for index, row in data.iterrows():
#   print(row.SENTENCE)
#   data = extract_data(row.SENTENCE)
#   print(data)
  # Find <ORIG>
  # Remove, keep id
  # FIND <ORIG/>
  # Remove, keep id
  # Find <DEST>
  # Remove, keep id
