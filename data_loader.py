import pandas as pd
import numpy as np


def load_items():

    items = pd.read_csv("data/items.csv")
    tags = pd.read_csv("data/itemtags.csv")

    return items, tags


def load_celebrities():

    celebs = pd.read_csv("data/celebrities.csv")

    return celebs


def load_embeddings():

    embeddings = np.load("embeddings/clothing_embeddings.npy")

    return embeddings
