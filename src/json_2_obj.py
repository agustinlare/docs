import json
from types import SimpleNamespace

def create_obj(file):
  f = open(file)
  data = json.load(f)
  f.close()

  return json.loads(json.dumps(data), object_hook=lambda d: SimpleNamespace(**d))

new_obj = create_obj("./config.json")