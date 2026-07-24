#!/usr/bin/env python3
"""
Tạo audio tiếng Việt MIỄN PHÍ bằng edge-tts (giọng Neural của Microsoft).
Không cần API key, không GPU. Chạy trên GitHub Actions.

Biến môi trường (tùy chọn):
  VOICE   giọng đọc (mặc định vi-VN-NamMinhNeural = nam; vi-VN-HoaiMyNeural = nữ)
  RATE    tốc độ (mặc định -4% cho êm)
  SCOPE   all | <slug> | nhiều slug cách nhau dấu phẩy  (mặc định 1 bài mẫu)
  OVERWRITE  1 = tạo lại kể cả đã có
"""
import os, re, glob, sys, html, asyncio
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(ROOT, "audio")
VOICE = os.environ.get("VOICE", "vi-VN-NamMinhNeural").strip()
RATE = os.environ.get("RATE", "-4%").strip()
SCOPE = os.environ.get("SCOPE", "dat-nam-ban-trong-cay-gi").strip()
OVERWRITE = os.environ.get("OVERWRITE", "0").strip() == "1"
MAX_CHARS = 4000

class Grab(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_body=False; self.depth=0; self.container=None
        self.cap=None; self.buf=[]; self.parts=[]; self.skip=0; self.cur_li=False; self.li_a=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs); cls=a.get('class','')
        if not self.in_body:
            if (tag=='div' and 'art-body' in cls) or tag=='article':
                self.in_body=True; self.container=tag; self.depth=1
            return
        if tag==self.container: self.depth+=1
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
            self.depth-=1
            if self.depth<=0: self.in_body=False
    def handle_data(self,d):
        if self.in_body and self.cap and not self.skip: self.buf.append(d)

def narration(fp):
    h=open(fp,encoding='utf-8').read()
    g=Grab(); g.feed(h); parts=g.parts
    m=re.search(r'<div class="art-header">.*?<h1>(.*?)</h1>', h, re.S) or re.search(r'<h1>(.*?)</h1>', h, re.S)
    h1=re.sub(r'<[^>]+>','',html.unescape(m.group(1))).strip() if m else ''
    if h1 and (not parts or parts[0]!=h1): parts=[h1]+[p for p in parts if p!=h1]
    return "\n".join(parts)

def chunk(text, limit):
    out=[]; cur=""
    for para in text.split("\n"):
        para=para.strip()
        if not para: continue
        if len(para)>limit:
            for s in re.findall(r'[^.!?…]+[.!?…]*\s*', para) or [para]:
                if len(cur)+len(s)>limit and cur: out.append(cur.strip()); cur=""
                cur+=s
        else:
            if len(cur)+len(para)+1>limit and cur: out.append(cur.strip()); cur=""
            cur+=("\n"+para if cur else para)
    if cur.strip(): out.append(cur.strip())
    return out

def add_meta(fp, slug):
    h=open(fp,encoding='utf-8').read()
    if 'name="pm-audio"' in h: return
    tag='<meta name="pm-audio" content="/audio/'+slug+'.mp3">\n'
    m=re.search(r'(<link rel="canonical"[^>]*>\n)', h)
    h=h[:m.end()]+tag+h[m.end():] if m else re.sub(r'(</head>)', tag+r'\1', h, count=1)
    open(fp,'w',encoding='utf-8').write(h)

def article_files():
    fs=[f for f in glob.glob(os.path.join(ROOT,"*.html")) if not os.path.basename(f).startswith("_")]
    for sub in ("fr","zh","ko","ja"): fs+=glob.glob(os.path.join(ROOT,sub,"*.html"))
    out=[]
    for f in fs:
        h=open(f,encoding='utf-8').read()
        if 'class="art-body"' in h or '<article' in h: out.append(f)
    return sorted(out)

async def synth_to(text, path):
    import edge_tts
    data=b""
    for c in chunk(text, MAX_CHARS):
        com=edge_tts.Communicate(c, VOICE, rate=RATE)
        async for ch in com.stream():
            if ch["type"]=="audio": data+=ch["data"]
    open(path,"wb").write(data)
    return len(data)

def main():
    os.makedirs(AUDIO_DIR, exist_ok=True)
    byslug={os.path.splitext(os.path.basename(f))[0]:f for f in article_files()}
    targets=list(byslug) if SCOPE=="all" else [s.strip() for s in SCOPE.split(",") if s.strip()]
    print("Giọng:",VOICE,"| tốc độ:",RATE,"|",len(targets),"bài")
    done=0
    for slug in targets:
        fp=byslug.get(slug)
        if not fp: print("  bỏ (không thấy):",slug); continue
        mp3=os.path.join(AUDIO_DIR, slug+".mp3")
        if os.path.exists(mp3) and not OVERWRITE:
            add_meta(fp,slug); print("  đã có, gắn meta:",slug); continue
        text=narration(fp)
        if len(text)<80: print("  bỏ (ít nội dung):",slug); continue
        try:
            n=asyncio.run(synth_to(text, mp3))
        except Exception as e:
            print("  LỖI:",slug,e); continue
        add_meta(fp,slug); done+=1
        print(f"  ✓ {slug}.mp3 ({n//1024} KB)")
    print(f"\nXong: {done} bài.")

if __name__=="__main__":
    main()
