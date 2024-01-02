import json

with open("db.text.json", encoding="utf-8") as f:
    tagdb = json.load(f)["data"]

tagdb = {
    item["namespace"]: item["data"]
    for item in tagdb
    if not item["namespace"] in ["rows", "reclass"]
}

with open("tag_name_intro.csv", encoding="utf-8", mode="w+") as o:
    for namespace, tags in tagdb.items():
        for tag, info in tags.items():
            full_tag = f"{namespace}:{tag}"
            print(
                f"'{full_tag}'",
                f"'{info['name']}'",
                f"'{info['intro'].replace('\n', '\\n')}'",
                sep=",",
                file=o,
            )
