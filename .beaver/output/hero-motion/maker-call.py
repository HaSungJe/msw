"""Local installed Maker MCP stdio client; responses remain in this workspace."""
import json, subprocess, threading, queue, sys, pathlib, base64
sys.stdout.reconfigure(encoding='utf-8')
proc=subprocess.Popen([r'C:\Users\timec\AppData\Local\Nexon\MapleStory Worlds\MakerMCP\MakerMCP_run.exe'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)
responses=queue.Queue()
def read():
    for line in proc.stdout:
        try: responses.put(json.loads(line))
        except ValueError: pass
threading.Thread(target=read,daemon=True).start()
def request(p):
    proc.stdin.write(json.dumps(p)+'\n');proc.stdin.flush()
    while True:
        r=responses.get(timeout=40)
        if r.get('id')==p['id']:return r
try:
    request({'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'codex-hero-motion','version':'1.0'}}})
    proc.stdin.write(json.dumps({'jsonrpc':'2.0','method':'notifications/initialized'})+'\n');proc.stdin.flush()
    if sys.argv[1]=='list':p={'jsonrpc':'2.0','id':2,'method':'tools/list'}
    else:
        args=json.loads(pathlib.Path(sys.argv[2]).read_text(encoding='utf-8-sig')) if len(sys.argv)>2 else {}
        p={'jsonrpc':'2.0','id':2,'method':'tools/call','params':{'name':sys.argv[1],'arguments':args}}
    r=request(p)
    folder=pathlib.Path(__file__).parent
    (folder/'maker-response.json').write_text(json.dumps(r,ensure_ascii=False),encoding='utf-8')
    if sys.argv[1]=='list':
        (folder/'maker-schemas.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps(r,ensure_ascii=False))
    else:
        for i,c in enumerate(r.get('result',{}).get('content',[])):
            if c.get('type')=='image':
                dest=folder/f'maker-capture-{i}.png';dest.write_bytes(base64.b64decode(c.pop('data')));c['savedPath']=str(dest)
        print(json.dumps(r,ensure_ascii=False))
finally:proc.terminate()
