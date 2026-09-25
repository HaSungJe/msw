"""Call the already-installed local Maker MCP over its documented stdio protocol."""
import json, subprocess, threading, queue, sys
sys.stdout.reconfigure(encoding='utf-8')
proc = subprocess.Popen([r'C:\Users\timec\AppData\Local\Nexon\MapleStory Worlds\MakerMCP\MakerMCP_run.exe'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)
responses = queue.Queue()
def read():
    for line in proc.stdout:
        responses.put(json.loads(line))
threading.Thread(target=read, daemon=True).start()
def request(payload):
    proc.stdin.write(json.dumps(payload)+'\n'); proc.stdin.flush()
    while True:
        response=responses.get(timeout=25)
        if response.get('id')==payload['id']: return response
try:
    request({'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'codex-motion-inspect','version':'1.0'}}})
    proc.stdin.write(json.dumps({'jsonrpc':'2.0','method':'notifications/initialized'})+'\n'); proc.stdin.flush()
    arguments={}
    if len(sys.argv)>2:
        raw=sys.argv[2]
        if raw.startswith('@'):
            with open(raw[1:],encoding='utf-8-sig') as source: raw=source.read()
        arguments=json.loads(raw)
    if len(sys.argv)>3:
        with open(sys.argv[3],encoding='utf-8') as source: arguments['script']=source.read()
    print(json.dumps(request({'jsonrpc':'2.0','id':2,'method':'tools/call','params':{'name':sys.argv[1],'arguments':arguments}}),ensure_ascii=False))
finally:
    proc.terminate()
