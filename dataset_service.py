import pandas as pd
import requests
import math
import csv
import sys

args = sys.argv
if (len(args) != 4):
  print("There needs to be three arguments, one for the template csv path, one for the target path and one for the number of cities")
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
cities = get_cities_set(all_cities, int(args[3]))
cities_couples = get_couples(cities)
sentences = fill_sentences(cities_couples, args[1])
write_to_csv(sentences, args[2])
print("done")