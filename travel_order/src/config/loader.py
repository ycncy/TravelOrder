import os
from typing import Tuple

import networkx as nx
import pandas as pd
import spacy

from src.config.logger import logger
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

spacy_model = spacy.load(os.path.join(os.path.dirname(__file__), '../../data/spacy/model-best'))

camembert_model_path = os.path.join(os.path.dirname(__file__), '../../data/camembert/trained_model')
tokenizer = AutoTokenizer.from_pretrained(camembert_model_path)
model = AutoModelForTokenClassification.from_pretrained(camembert_model_path)

camembert_ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")


def load_connections_data(data_path: str) -> Tuple[nx.DiGraph, pd.DataFrame]:
    connections = pd.read_csv(data_path)
    logger.info("Loaded SNCF connections")

    G = nx.DiGraph()
    for index, row in connections.iterrows():
        G.add_edge(row['stop_id_start'], row['stop_id_end'], weight=row['travel_time'])

    logger.info(f"Graph created with {len(G.edges)} edges")

    return G, connections


G, connections = load_connections_data(
    os.path.join(os.path.dirname(__file__), '../../data/output/sncf_connections.csv')
)
