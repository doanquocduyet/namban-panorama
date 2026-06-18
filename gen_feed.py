#!/usr/bin/env python3
# Sinh feed.xml (RSS 2.0) cho Namban Panorama tu cac file HTML o thu muc goc repo.
import glob, re, html, subprocess
from email.utils import format_datetime
from datetime import datetime, timezone

SITE  = "https://nambanpanorama.com"
TITLE = "Namban Panorama"
DESC  = "Phan tich doc lap ve bat dong san va doi song vung Nam Ban, Lam Ha, Lam Dong. Doc rui ro, khong ban giac mo."
EXCLUDE = {
    "index.html","index-good.html","namban-panorama-v2.html",
    "namban-intelligence-homepage.html","namban-intelligence-homepage-v2.html",
    "doc-nhanh.html","trao-doi.html","nguoi-nam-ban-01.html",
}

def og(s, prop):
    m = re.search(r'<meta[^>]+property=["\']'+re.escape(prop)+r'["\'][^>]*content=["\']([^"\']*)', s, re.I)
    if not m:
        m = re.search(r'<meta[^>]+content=["\']([^"\']*)["\'][^>]*property=["\']'+re.escape(prop)+r'["\']', s, re.I)
    return m.group(1).strip() if m else None

def meta_name(s, name):
    m = re.search(r'<meta[^>]+name=["\']'+re.escape(name)+r'["\'][^>]*content=["\']([^"\']*)', s, re.I)
    return m.group(1).strip() if m else None

def git_date(path):
    try:
        out = subprocess.check_output(["git","log","-1","--format=%cI","--",path], stderr=subprocess.DEVNULL).decode().strip()
        if out:
            return datetime.fromisoformat(out)
    except Exception:
        pass
    return datetime.now(timezone.utc)

items=[]
for f in sorted(glob.glob("*.html")):
    if f in EXCLUDE: continue
    s=open(f,encoding="utf-8",errors="replace").read()
    title=og(s,"og:title")
    if not title:
        m=re.search(r"<title>(.*?)</title>",s,re.S); title=m.group(1).strip() if m else f
    desc=og(s,"og:description") or meta_name(s,"description") or ""
    url=og(s,"og:url") or (SITE+"/"+f[:-5])
    items.append((git_date(f),title,desc,url))
items.sort(key=lambda x:x[0],reverse=True)

def esc(t): return html.escape(t or "", quote=False)
now=format_datetime(datetime.now(timezone.utc))
p=['<?xml version="1.0" encoding="UTF-8"?>',
   '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">','<channel>',
   f'<title>{esc(TITLE)}</title>',f'<link>{SITE}</link>',
   f'<description>{esc(DESC)}</description>','<language>vi</language>',
   f'<lastBuildDate>{now}</lastBuildDate>',
   f'<atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>']
for dt,title,desc,url in items:
    p+=['<item>',f'<title>{esc(title)}</title>',f'<link>{esc(url)}</link>',
        f'<guid isPermaLink="true">{esc(url)}</guid>',
        f'<pubDate>{format_datetime(dt)}</pubDate>']
    if desc: p.append(f'<description>{esc(desc)}</description>')
    p.append('</item>')
p+=['</channel>','</rss>']
open("feed.xml","w",encoding="utf-8").write("\n".join(p)+"\n")
print(f"feed.xml: {len(items)} items")
