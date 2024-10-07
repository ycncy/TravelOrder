import pandas as pd
import re
import requests
import math

def get_cities(number_of_cities):
  cities = []
  number_of_cities = 100
  if number_of_cities > len(response_cities):
    number_of_cities = len(response_cities)
  factor = math.ceil(len(response_cities) / number_of_cities)
  for i in range(number_of_cities):
    if i != 0:
       number = factor * i
    else:
       number = 0
    if number > len(response_cities):
       break
    cities.append(response_cities[number])
  return cities

def get_couples(cities):
  couple_ids = [(x, y) for x in range(len(cities)) for y in range(len(cities)) if x != y]
  cities_couples = []
  for couple in couple_ids:
    cities_couples.append((cities[couple[0]], cities[couple[1]]))
    # print(cities[couple[0]], "," , cities[couple[1]])
  return cities_couples

url = "https://countriesnow.space/api/v0.1/countries/cities"

headers = {}

response = requests.request("POST", url, headers=headers, data={ "country": "france"})
JSONresponse = response.json()
response_cities = JSONresponse["data"]
cities = get_cities(100)
cities_couples = get_couples(cities)
print(cities_couples)


data = pd.read_csv("./dataset_template.csv", delimiter=",")


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
