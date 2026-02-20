#!/usr/bin/env python3
import os, json, ssl, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Reads vapi_last6h_report.json and sends a compact HTML email.

def load_dotenv(path='.env'):
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k,v=line.split('=',1)
            if k not in os.environ:
                os.environ[k]=v.strip().strip('"').strip("'")

load_dotenv()

SMTP_HOST=os.environ.get('GMAIL_SMTP_HOST','smtp.gmail.com')
SMTP_PORT=int(os.environ.get('GMAIL_SMTP_PORT','587'))
USER=os.environ.get('GMAIL_USER')
APP_PW=os.environ.get('GMAIL_APP_PASSWORD')

TO=os.environ.get('REPORT_TO','taruner420@gmail.com')
SUBJECT=os.environ.get('REPORT_SUBJECT','Ellavox Hackathon — Manager Agent 6h Call Review')

if not USER or not APP_PW:
    raise SystemExit('Missing GMAIL_USER or GMAIL_APP_PASSWORD in env')

with open('vapi_last6h_report.json','r',encoding='utf-8') as f:
    rep=json.load(f)

rows=rep.get('rows',[])

# compact table (top 30)
def esc(s):
    return (s or '').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

trs=[]
for r in rows[:30]:
    trs.append(f"""
    <tr>
      <td style='padding:6px;border-bottom:1px solid #eee;'>{esc(r.get('endedAt',''))}</td>
      <td style='padding:6px;border-bottom:1px solid #eee;'>{esc(r.get('agentName',''))}</td>
      <td style='padding:6px;border-bottom:1px solid #eee;'>{esc(r.get('caller',''))}</td>
      <td style='padding:6px;border-bottom:1px solid #eee;'>{esc(r.get('emoji',''))} {esc(r.get('verdict',''))}</td>
      <td style='padding:6px;border-bottom:1px solid #eee;'>{esc(str(r.get('score','')))}</td>
      <td style='padding:6px;border-bottom:1px solid #eee;'>{esc(r.get('priority',''))}</td>
      <td style='padding:6px;border-bottom:1px solid #eee;'>{esc(r.get('sentiment',''))}</td>
      <td style='padding:6px;border-bottom:1px solid #eee;'>{esc(r.get('summary',''))}</td>
      <td style='padding:6px;border-bottom:1px solid #eee;'><a href='{esc(r.get('recordingUrl',''))}'>recording</a></td>
    </tr>
    """)

html=f"""
<!doctype html>
<html><body style='font-family:Arial,sans-serif;'>
<h2>Manager Agent — Last {rep.get('windowHours')}h Call Review</h2>
<p><b>Window start:</b> {esc(rep.get('since'))}<br/>
<b>Total calls:</b> {rep.get('totalCalls')} • ✅ Pass: {rep.get('pass')} • ⚠️ Follow-up: {rep.get('followUp')} • 🚨 Escalate: {rep.get('escalate')}</p>

<p style='color:#555'>Note: This is a hackathon POC. For this run, scoring uses a safe heuristic + metadata. Next iteration will score strictly against each agent's prompt (blueprint → scorer) once we wire prompt extraction reliably per assistant.</p>

<table cellpadding='0' cellspacing='0' style='border-collapse:collapse;width:100%;font-size:12px;'>
<thead>
<tr style='background:#f6f6f6'>
  <th style='text-align:left;padding:6px;border-bottom:1px solid #ddd;'>EndedAt (UTC)</th>
  <th style='text-align:left;padding:6px;border-bottom:1px solid #ddd;'>Agent</th>
  <th style='text-align:left;padding:6px;border-bottom:1px solid #ddd;'>Caller</th>
  <th style='text-align:left;padding:6px;border-bottom:1px solid #ddd;'>Verdict</th>
  <th style='text-align:left;padding:6px;border-bottom:1px solid #ddd;'>Score</th>
  <th style='text-align:left;padding:6px;border-bottom:1px solid #ddd;'>Priority</th>
  <th style='text-align:left;padding:6px;border-bottom:1px solid #ddd;'>Sentiment</th>
  <th style='text-align:left;padding:6px;border-bottom:1px solid #ddd;'>Summary</th>
  <th style='text-align:left;padding:6px;border-bottom:1px solid #ddd;'>Recording</th>
</tr>
</thead>
<tbody>
{''.join(trs) if trs else '<tr><td colspan="9" style="padding:8px;">No calls in this window.</td></tr>'}
</tbody>
</table>
</body></html>
"""

msg=MIMEMultipart('alternative')
msg['From']=USER
msg['To']=TO
msg['Subject']=SUBJECT
msg.attach(MIMEText(html,'html','utf-8'))

ctx=ssl.create_default_context()
with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
    s.ehlo()
    s.starttls(context=ctx)
    s.login(USER, APP_PW)
    s.sendmail(USER, [TO], msg.as_string())

print('sent')
