#!/usr/bin/env python3
"""
Send briefing.md as a Gmail draft via the session's MCP endpoint.
Reads the live MCP config from /tmp so it works for any session.
Run via: python3 send_draft.py [briefing.md path]
"""

import json, os, sys, re, glob, urllib.request, urllib.error, time
from pathlib import Path
from datetime import date

# ── 1. Find the current session's MCP config ───────────────────────────────
configs = glob.glob('/tmp/mcp-config-*.json')
if not configs:
    sys.exit("ERROR: No MCP config found in /tmp. Is this running inside a Claude Code session?")

with open(configs[0]) as f:
    config = json.load(f)

gmail = config['mcpServers']['Gmail']
endpoint = gmail['url']

SESSION_TOKEN_FILE = '/home/claude/.claude/remote/.session_ingress_token'

base_headers = dict(gmail['headers'])
base_headers['Content-Type'] = 'application/json'
base_headers['Accept'] = 'application/json, text/event-stream'

token = Path(SESSION_TOKEN_FILE).read_text().strip() if Path(SESSION_TOKEN_FILE).exists() else ''
if token:
    base_headers['Authorization'] = f'Bearer {token}'
else:
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if api_key:
        base_headers['x-api-key'] = api_key

# ── 2. Read briefing ────────────────────────────────────────────────────────
briefing_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/home/user/morning-briefing/briefing.md')
if not briefing_path.exists():
    sys.exit(f"ERROR: {briefing_path} not found")

md = briefing_path.read_text()

# ── 3. Markdown → HTML (stdlib only) ───────────────────────────────────────
def md_to_html(md: str) -> str:
    lines = md.split('\n')
    out = []
    in_table = False
    table_header_done = False

    def inline(s):
        s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
        s = re.sub(r'\*(.+?)\*', r'<em>\1</em>', s)
        s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
        s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
        return s

    for line in lines:
        if line.startswith('|'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if all(re.match(r'^[-: ]+$', c) for c in cells if c):
                if not in_table:
                    in_table = True
                    out.append('<table border="1" cellpadding="4" cellspacing="0" style="border-collapse:collapse;font-size:13px">')
                table_header_done = True
                continue
            if not in_table:
                in_table = True
                out.append('<table border="1" cellpadding="4" cellspacing="0" style="border-collapse:collapse;font-size:13px">')
            tag = 'th' if not table_header_done else 'td'
            row = ''.join(f'<{tag}>{inline(c)}</{tag}>' for c in cells if c != '')
            out.append(f'<tr>{row}</tr>')
            continue
        else:
            if in_table:
                out.append('</table>')
                in_table = False
                table_header_done = False

        m = re.match(r'^(#{1,4})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            text = inline(m.group(2))
            sizes = {1: '22px', 2: '18px', 3: '15px', 4: '13px'}
            mt = {1: '24px', 2: '20px', 3: '16px', 4: '12px'}
            out.append(f'<h{level} style="font-size:{sizes[level]};margin-top:{mt[level]};margin-bottom:4px">{text}</h{level}>')
            continue

        if re.match(r'^---+$', line.strip()):
            out.append('<hr style="border:none;border-top:1px solid #ccc;margin:16px 0">')
            continue

        m = re.match(r'^(\s*)[-*]\s+(.*)', line)
        if m:
            indent = len(m.group(1))
            content = inline(m.group(2))
            margin = 8 + indent * 12
            out.append(f'<div style="margin-left:{margin}px;margin-bottom:4px">• {content}</div>')
            continue

        m = re.match(r'^(\d+)\.\s+(.*)', line)
        if m:
            content = inline(m.group(2))
            out.append(f'<div style="margin-bottom:6px"><strong>{m.group(1)}.</strong> {content}</div>')
            continue

        if not line.strip():
            out.append('<br>')
            continue

        out.append(f'<p style="margin:4px 0">{inline(line)}</p>')

    if in_table:
        out.append('</table>')

    body = '\n'.join(out)
    return f'''<html><body style="font-family:Georgia,serif;font-size:14px;line-height:1.6;max-width:800px;margin:0 auto;padding:20px;color:#1a1a1a">
{body}
</body></html>'''

html_body = md_to_html(md)

# ── 4. MCP protocol helpers ─────────────────────────────────────────────────
_msg_id = [0]

def mcp_post(method: str, params: dict, expect_response: bool = True):
    _msg_id[0] += 1
    body = {"jsonrpc": "2.0", "method": method, "params": params}
    if expect_response:
        body["id"] = _msg_id[0]

    data = json.dumps(body).encode()
    req = urllib.request.Request(endpoint, data=data, headers=base_headers, method='POST')

    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                raw = resp.read().decode()
                if 'data:' in raw:
                    lines = [l for l in raw.splitlines() if l.startswith('data:')]
                    if lines:
                        raw = lines[-1][5:].strip()
                if not raw or not expect_response:
                    return {}
                return json.loads(raw)
        except urllib.error.HTTPError as e:
            print(f"HTTP {e.code} on attempt {attempt+1}: {e.read().decode()[:200]}", file=sys.stderr)
            if attempt < 3:
                time.sleep(2 ** attempt)
        except Exception as e:
            print(f"Error on attempt {attempt+1}: {e}", file=sys.stderr)
            if attempt < 3:
                time.sleep(2 ** attempt)
    sys.exit("ERROR: All retry attempts failed")

# ── 5. MCP handshake ────────────────────────────────────────────────────────
print("Initialising MCP session...", flush=True)
mcp_post("initialize", {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "morning-briefing", "version": "1.0"}
}, expect_response=True)

mcp_post("notifications/initialized", {}, expect_response=False)

# ── 6. Create draft ─────────────────────────────────────────────────────────
first_line = md.splitlines()[0] if md else ''
m = re.match(r'^#\s+(Morning Briefing\s+[—–-].+)', first_line)
subject = m.group(1).strip() if m else f"Morning Briefing — {date.today().strftime('%-d %B %Y')}"

print(f"Creating draft: {subject}", flush=True)
result = mcp_post("tools/call", {
    "name": "create_draft",
    "arguments": {
        "to": ["dylanjrogers0@gmail.com"],
        "subject": subject,
        "htmlBody": html_body
    }
})

print("Result:", json.dumps(result, indent=2)[:500], flush=True)
