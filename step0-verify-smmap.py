import pickle

with open("slave-master-map.pickle", "rb") as f:
    d: dict[str, str] = pickle.load(f)
    print(d.items())
