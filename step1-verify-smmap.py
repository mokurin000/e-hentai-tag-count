import pickle

with open("smmap_get/smmap.pickle", "rb") as f:
    d: dict[str, str] = pickle.load(f)
    print(d.items())
