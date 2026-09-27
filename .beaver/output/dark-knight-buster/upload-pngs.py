import json,pathlib,urllib.request,concurrent.futures
root=pathlib.Path(__file__).parent
rows=json.loads((root/'upload-requests.private.json').read_text())
def upload(row):
    payload=pathlib.Path(row['file']).read_bytes()
    request=urllib.request.Request(row['url'],data=payload,method='PUT',headers={'Content-Length':str(len(payload))})
    try:
        with urllib.request.urlopen(request,timeout=45) as response:return {'key':row['key'],'status':response.status}
    except Exception as exc:return {'key':row['key'],'error':type(exc).__name__}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: results=list(pool.map(upload,rows))
(root/'upload-put-results.json').write_text(json.dumps(results,indent=2))
print(json.dumps({'success':sum(r.get('status')==200 for r in results),'failures':[r for r in results if r.get('status')!=200]}))
