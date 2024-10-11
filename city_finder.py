import pandas as pd
import re

def find_city(sentence):
    dep_city = None
    dest_city = None

    pattern_departure = r'(de|depuis)\s([A-Z][\w\-\']+)'
    pattern_destination = r'(à|vers|jusqu\'à)\s([A-Z][\w\-\']+)'

    match_dep = re.search(pattern_departure, sentence)
    if match_dep:
        dep_city = match_dep.group(2)
    else:
        dep_city = "Inconnu"

    match_dest = re.search(pattern_destination, sentence)
    if match_dest:
        dest_city = match_dest.group(2)
    else:
        dest_city = "Inconnu"

    return dep_city, dest_city

df = pd.read_csv('sentences.csv', sep=';')

df['Ville de départ'], df['Ville d\'arrivée'] = zip(*df['sentences'].apply(find_city))

df.to_csv('results.csv', index=False)

print("Les villes de départ et d'arrivée ont été détectées et sauvegardées dans 'results.csv'.")
