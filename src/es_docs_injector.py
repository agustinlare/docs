# I created this script because I was having a problem with log overflow but could not find
# which application was. So I took 10000 documents and scrape them here.
import json
from collections import defaultdict

with open('documents.json') as f:
    data = json.load(f)

final_count = defaultdict(int)

for i in data["hits"]["hits"]:
    app = i["_source"]["kubernetes"]["container"]["name"]
    final_count[app] += 1

print(final_count)