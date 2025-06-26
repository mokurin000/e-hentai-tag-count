import pickle

with open("smmap.pickle", "rb") as f:
    d: dict[str, str] = pickle.load(f)
    print(d.items())
