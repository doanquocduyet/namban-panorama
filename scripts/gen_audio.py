#!/usr/bin/env python3
"""
Tự tạo audio giọng thật cho các bài viết Namban Panorama bằng ElevenLabs.
Chạy trên GitHub Actions (hoặc máy có internet). KHÔNG cần đọc/copy-paste tay.

Cần biến môi trường:
  ELEVENLABS_API_KEY  (bí mật)
  ELEVENLABS_VOICE_ID (giọng của Chú)
Tùy chọn:
  MODEL_ID   (mặc định eleven_multilingual_v2 — đọc tiếng Việt tự nhiên)
  SCOPE      (all | <slug> | danh sách slug cách nhau bởi dấu phẩy)  mặc định: một bài mẫu
  OVERWRITE  (1 = tạo lại kể cả đã có mp3)  mặc định: 0 (bỏ qua bài đã có)
"""
import os, re, glob, sys, json, html, time, urllib.request
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(ROOT, "audio")
API_KEY = os.environ.get("ELEVENLABS_API_KEY", "").strip()
VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "").strip()
MODEL_ID = os.environ.get("MODEL_ID", "eleven_multilingual_v2").strip()
SCOPE = os.environ.get("SCOPE", "dat-nam-ban-trong-cay-gi").strip()
OVERWRITE = os.environ.get("OVERWRITE", "0").strip() == "1"
MAX_CHARS = 2400          # cắt khúc an toàn dưới giới hạn/lần gọi
API = "https://api.elevenlabs.io/v1/text-to-speech/"

class Grab(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_body=False; self.body_depth=0; self.container=None
        self.cap=None; self.buf=[]; self.parts=[]
        self.skip=0; self.cur_li=False; self.li_a=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs); cls=a.get('class','')
        if not self.in_body:
            if (tag=='div' and 'art-body' in cls) or tag=='article':
                self.in_body=True; self.container=tag; self.body_depth=1
            return
        if tag==self.container: self.body_depth+=1
        if tag in ('script','style','figure') or 'source-box' in cls or 'pm-endcontact' in cls or 'pm-audio' in cls:
            self.skip+=1; return
        if self.skip: return
        if tag in ('h1','h2','h3','p','li','blockquote'):
            self.cap=tag; self.buf=[]; self.cur_li=(tag=='li'); self.li_a=False
        if tag=='a' and self.cur_li: self.li_a=True
    def handle_endtag(self,tag):
        if not self.in_body: return
        if self.skip and tag in ('script','style','figure'): self.skip-=1; return
        if self.skip:
            if tag=='div': self.skip-=1
            return
        if self.cap and tag==self.cap:
            t=re.sub(r'\s+',' ',html.unescape(''.join(self.buf))).strip()
            if t and not (self.cur_li and self.li_a) and not re.match(r'^Đọc gì tiếp',t):
                self.parts.append(t)
            self.cap=None; self.buf=[]; self.cur_li=False
        if tag==self.container:
            self.body_depth-=1
            if self.body_depth<=0: self.in_body=False
    def handle_data(self,d):
        if self.in_body and self.cap and not self.skip: self.buf.append(d)

def narration(fp):
    h=open(fp,encoding='utf-8').read()
    g=Grab(); g.feed(h); parts=g.parts
    m=re.search(r'<div class="art-header">.*?<h1>(.*?)</h1>', h, re.S) or re.search(r'<h1>(.*?)</h1>', h, re.S)
    h1=re.sub(r'<[^>]+>','',html.unescape(m.group(1))).strip() if m else ''
    if h1 and (not parts or parts[0]!=h1): parts=[h1]+[p for p in parts if p!=h1]
    return parts

def chunk(parts, limit):
    out=[]; cur=""
    for p in parts:
        if len(p)>limit:
            for s in re.findall(r'[^.!?…]+[.!?…]*\s*', p) or [p]:
                if len(cur)+len(s)>limit and cur: out.append(cur.strip()); cur=""
                cur+=s
        else:
            if len(cur)+len(p)+1>limit and cur: out.append(cur.strip()); cur=""
            cur+=("\n"+p if cur else p)
    if cur.strip(): out.append(cur.strip())
    return out

def tts(text):
    body=json.dumps({"text":text,"model_id":MODEL_ID,
        "voice_settings":{"stability":0.5,"similarity_boost":0.8,"style":0.0,"use_speaker_boost":True}}).encode()
    req=urllib.request.Request(API+VOICE_ID+"?output_format=mp3_44100_128", data=body,
        headers={"xi-api-key":API_KEY,"Content-Type":"application/json","Accept":"audio/mpeg"}, method="POST")
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()

def add_meta(fp, slug):
    h=open(fp,encoding='utf-8').read()
    if 'name="pm-audio"' in h: return False
    tag='<meta name="pm-audio" content="/audio/'+slug+'.mp3">\n'
    m=re.search(r'(<link rel="canonical"[^>]*>\n)', h)
    if m: h=h[:m.end()]+tag+h[m.end():]
    else: h=re.sub(r'(</head>)', tag+r'\1', h, count=1)
    open(fp,'w',encoding='utf-8').write(h); return True

def article_files():
    fs=[f for f in glob.glob(os.path.join(ROOT,"*.html")) if not os.path.basename(f).startswith("_")]
    for sub in ("fr","zh","ko","ja"): fs+=glob.glob(os.path.join(ROOT,sub,"*.html"))
    out=[]
    for f in fs:
        h=open(f,encoding='utf-8').read()
        if 'class="art-body"' in h or '<article' in h: out.append(f)
    return sorted(out)

def main():
    if not API_KEY or not VOICE_ID:
        print("!! Thiếu ELEVENLABS_API_KEY hoặc ELEVENLABS_VOICE_ID"); sys.exit(1)
    os.makedirs(AUDIO_DIR, exist_ok=True)
    files=article_files()
    byslug={os.path.splitext(os.path.basename(f))[0]:f for f in files}
    if SCOPE=="all": targets=list(byslug.keys())
    else: targets=[s.strip() for s in SCOPE.split(",") if s.strip()]
    done=0
    for slug in targets:
        fp=byslug.get(slug)
        if not fp: print("  bỏ (không thấy bài):",slug); continue
        mp3=os.path.join(AUDIO_DIR, slug+".mp3")
        if os.path.exists(mp3) and not OVERWRITE:
            add_meta(fp, slug); print("  đã có mp3, gắn meta:",slug); continue
        parts=narration(fp)
        if len(parts)<2: print("  bỏ (ít nội dung):",slug); continue
        chunks=chunk(parts, MAX_CHARS)
        total=sum(len(c) for c in chunks)
        print(f"  {slug}: {len(chunks)} khúc, {total} ký tự …")
        audio=b""
        for i,c in enumerate(chunks):
            for attempt in range(3):
                try: audio+=tts(c); break
                except Exception as e:
                    print(f"    khúc {i+1} lỗi ({e}), thử lại…"); time.sleep(3)
            else:
                print("    !! bỏ bài do lỗi lặp:",slug); audio=b""; break
        if not audio: continue
        open(mp3,"wb").write(audio)
        add_meta(fp, slug)
        print(f"    ✓ {slug}.mp3 ({len(audio)//1024} KB)")
        done+=1
    print(f"\nXong: {done} bài có audio mới.")

if __name__=="__main__":
    main()
