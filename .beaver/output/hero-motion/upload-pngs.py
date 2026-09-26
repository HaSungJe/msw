import json,pathlib,urllib.request
root=pathlib.Path(__file__).parent
for row in json.loads((root/'upload-requests.private.json').read_text()):
    payload=pathlib.Path(row['file']).read_bytes()
    req=urllib.request.Request(row['url'],data=payload,method='PUT',headers={'Content-Length':str(len(payload))})
    with urllib.request.urlopen(req,timeout=40) as response: print(row['name'],response.status)
