import json

with open("db.text.json", encoding="utf-8") as f:
    tagdb = json.load(f)['data']

tagdb = { item['namespace']: item['data'] for item in tagdb if not item['namespace'] in ['rows', 'reclass']}

for namespace, tags in tagdb.items():
    for tag, info in tags.items():
        full_tag = f"{namespace}:{tag}"
        print(full_tag, info['name'], info['intro'], sep=',')
