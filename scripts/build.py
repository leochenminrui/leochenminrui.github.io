#!/usr/bin/env python3
"""Build Minrui Chen's Japanese / English academic homepage using Python 3."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
ORIGIN = "https://leochenminrui.github.io"
GITHUB = "https://github.com/leochenminrui"
SCHOLAR = "https://scholar.google.com/citations?user=_2mpWrUAAAAJ"
ORCID = "https://orcid.org/0000-0002-5845-3200"
LAB = "https://www.isee.kyushu-u.ac.jp/laboratory_ist.html#saigo"
SUPERVISOR = "https://hyoka.ofc.kyushu-u.ac.jp/html/100021288_ja.html"
EMAIL = "minrui.chen@kyudai.jp"
SELF_NAMES = {"Minrui Chen", "Min-Rui Chen", "Chen Minrui"}
PAPERS = json.loads((ROOT / "data/publications.json").read_text())
TALKS = json.loads((ROOT / "data/presentations.json").read_text())
INVITED_TALKS = json.loads((ROOT / "data/talks.json").read_text())
RESEARCH = json.loads((ROOT / "data/research.json").read_text())
BIOGRAPHY = json.loads((ROOT / "data/biography.json").read_text())

def esc(value):
    return html.escape(str(value), quote=True)

def icon(name):
    paths = {
        "moon": '<path d="M20.9 13A9 9 0 0 1 11 3.1 9 9 0 1 0 20.9 13Z"/>',
        "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.4 1.4m11.2 11.2L19 19M5 19l1.4-1.4M17.6 6.4 19 5"/>',
        "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
        "arrow": '<path d="M5 12h14m-5-5 5 5-5 5"/>',
    }
    return f'<svg class="icon icon-{name}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'

def author_list(authors):
    return ", ".join(f'<strong class="self-author">{esc(a)}</strong>' if a in SELF_NAMES else esc(a) for a in authors)

def paper_markup(paper, lang):
    ja = lang == "ja"
    status = paper['status']
    labels = {"published": "学術誌論文" if ja else "Journal article", "accepted": "受理済み" if ja else "Accepted", "preprint": "プレプリント" if ja else "Preprint"}
    label = "国際会議論文" if ja else "Conference paper" if paper['type'] == "conference paper" else ""
    if paper['type'] != "conference paper":
        label = labels[status]
    venue = esc(paper.get('acceptedVenue') or paper['venue'])
    details = ""
    if status == "published":
        if paper.get('volume'):
            details = ", " + ("LNCS " if paper.get('series') else "") + esc(paper['volume'])
            if paper.get('issue'):
                details += f'({esc(paper["issue"])})'
        if paper.get('pages') or paper.get('articleNumber'):
            details += ": " + esc(paper.get('pages') or paper.get('articleNumber'))
    elif status == "accepted":
        details = " · 受理済み（公開プレプリント：Research Square）" if ja else " · Accepted; public preprint on Research Square"
    primary_label = ("プレプリント" if ja else "Preprint") if status != "published" else "DOI"
    links = f'<a class="paper-link" href="{esc(paper["url"])}">{primary_label} ↗</a>'
    if paper.get('codeUrl'):
        links += f'<a class="paper-link" href="{esc(paper["codeUrl"])}">{"コード" if ja else "Code"} ↗</a>'
    if paper.get('correctionUrl'):
        links += f'<a class="paper-link" href="{esc(paper["correctionUrl"])}">{"訂正記事" if ja else "Correction"} ↗</a>'
    return f'''<li class="publication" id="{esc(paper['id'])}" data-status="{status}"><div class="pub-heading"><span class="pub-kind">{label}</span></div>
    <h3><a href="{esc(paper['url'])}">{esc(paper['title'])}</a></h3><p class="authors">{author_list(paper['authors'])}.</p>
    <p class="venue"><em>{venue}</em>{details}, {paper['year']}.</p><div class="paper-links">{links}</div></li>'''

def biography(lang):
    ja = lang == 'ja'
    rows = []
    for item in BIOGRAPHY:
        if ja:
            rows.append(f'<tr><th scope="row">{esc(item["era"])}</th><td class="western-year">{esc(item["yearJa"])}</td><td>{item["eventJa"]}</td></tr>')
        else:
            rows.append(f'<tr><th scope="row">{esc(item["dateEn"])}</th><td>{item["eventEn"]}</td></tr>')
    return f'<table class="biography-table {"era-table" if ja else "english-table"}"><caption class="visually-hidden">{"学歴・略歴" if ja else "Education and biography"}</caption><tbody>{"".join(rows)}</tbody></table>'

def invited_talks(lang):
    ja = lang == 'ja'
    items=[]
    for talk in INVITED_TALKS:
        date = talk['dateJa' if ja else 'dateEn']
        kind = talk['typeJa' if ja else 'typeEn']
        venue = talk['venueJa' if ja else 'venueEn']
        url = talk['urlJa' if ja else 'url']
        items.append(f'<li class="presentation"><p class="presentation-year">{esc(date)} <span>{esc(kind)}</span></p><h3><a href="{esc(url)}">{esc(talk["title"])}</a></h3><p class="venue">{esc(venue)}</p></li>')
    return ''.join(items)

def home(lang):
    ja = lang == 'ja'
    name, other = ('陳 民瑞','Minrui Chen') if ja else ('Minrui Chen','陳 民瑞')
    if ja:
        affiliation = '九州大学大学院システム情報科学府<br>情報理工学専攻 博士後期課程'
        role = '機械学習・計算生物学・形式手法'
        lab_text = '統計的学習研究室（西郷研究室）'
        award = '<strong>2019–2023</strong><span>マカオ科学技術大学 Excellent Scholarship</span>'
        intro = f'指導教員：<a href="{SUPERVISOR}">西郷 浩人 准教授</a>'
    else:
        affiliation = 'Department of Information Science and Technology<br>Graduate School of Information Science and Electrical Engineering<br>Kyushu University'
        role = 'PhD student'
        lab_text = 'Statistical Learning Laboratory (Saigo Lab)'
        award = '<strong>2019–2023</strong><span>Excellent Scholarship, Macau University of Science and Technology</span>'
        intro = f'Advisor: <a href="{SUPERVISOR}">Hiroto Saigo</a>'
    research = ''.join(f'<div class="research-theme"><h3>{esc(item["titleJa" if ja else "titleEn"])}</h3><p>{esc(item["textJa" if ja else "textEn"])}</p></div>' for item in RESEARCH)
    selected_ids = ('glycoaudit', 'sapse', 'bat')
    selected = [next(p for p in PAPERS if p['id']==pid) for pid in selected_ids]
    return f'''<section class="profile" aria-labelledby="profile-name"><img class="portrait" src="../assets/avatar.png" width="240" height="240" alt="{'陳民瑞のピクセルアート・アバター' if ja else 'Pixel-art portrait of Minrui Chen'}" fetchpriority="high"><div class="profile-text"><h1 id="profile-name">{name}<span class="other-name" lang="{'en' if ja else 'ja'}">{other}</span></h1><p class="role">{role}</p><p class="affiliation">{affiliation}</p><p class="lab"><a href="{LAB}">{lab_text}</a></p><p class="advisor">{intro}</p></div></section>
    <section class="section research-copy"><h2>{'研究について' if ja else 'Research Interests'}</h2>{research}</section>
    <section class="section links-section"><h2>{'リンク・連絡先' if ja else 'Links & Contact'}</h2><div class="link-list"><a href="{SCHOLAR}">Google Scholar</a><span aria-hidden="true">/</span><a href="{ORCID}">ORCID</a><span aria-hidden="true">/</span><a href="{GITHUB}">GitHub</a><span aria-hidden="true">/</span><a href="https://x.com/leo_minrui_chen">X</a><span aria-hidden="true">/</span><a href="https://www.linkedin.com/in/min-rui-chen-271707227/">LinkedIn</a></div><p class="email">Email: <a href="mailto:{EMAIL}">{EMAIL}</a></p></section>
    <section class="section biography"><h2>{'略歴' if ja else 'Biography'}</h2>{biography(lang)}</section>
    <section class="section awards"><h2>{'奨学金' if ja else 'Scholarship'}</h2><p class="award-entry">{award}</p></section>
    <section class="section talks-home"><h2>{'講演' if ja else 'Invited Talks & Seminars'}</h2><ol class="presentation-list">{invited_talks(lang)}</ol></section>
    <section class="section recent"><div class="section-heading"><h2>{'主要論文' if ja else 'Selected Publications'}</h2><a class="text-link" href="publications/">{'すべての業績' if ja else 'All publications'} {icon('arrow')}</a></div><ol class="publication-list">{''.join(paper_markup(p,lang) for p in selected)}</ol></section>'''

def publications(lang):
    ja = lang == 'ja'
    labels = {'all':'すべて' if ja else 'All', 'published':'査読論文' if ja else 'Peer-reviewed', 'accepted':'受理済み' if ja else 'Accepted', 'preprint':'プレプリント' if ja else 'Preprints'}
    filters = ''.join(f'<button type="button" data-filter="{k}" aria-pressed="{"true" if k=="all" else "false"}">{v}<span>{len(PAPERS) if k=="all" else sum(p["status"]==k for p in PAPERS)}</span></button>' for k,v in labels.items())
    years=[]
    for year in sorted({p['year'] for p in PAPERS},reverse=True):
        years.append(f'<section class="pub-year" aria-labelledby="year-{year}"><h2 id="year-{year}">{year}</h2><ol class="publication-list">{"".join(paper_markup(p,lang) for p in PAPERS if p["year"]==year)}</ol></section>')
    talks=[]
    for talk in TALKS:
        title = talk.get('titleJa',talk['title']) if ja else talk['title']
        venue = talk.get('venueJa',talk['venue']) if ja else talk['venue']
        extra = ' · ' + talk['presentationId'] if talk.get('presentationId') else ''
        talks.append(f'<li class="presentation"><p class="presentation-year">{talk["year"]} <span>{"ポスター発表" if ja else "Poster presentation"}{extra}</span></p><h3><a href="{esc(talk["url"])}">{esc(title)}</a></h3><p class="authors">{author_list(talk["authors"])}.</p><p class="venue"><em>{esc(venue)}</em>.</p></li>')
    return f'''<header class="page-intro"><p class="eyebrow">RESEARCH</p><h1>{'研究業績' if ja else 'Publications'}</h1><p>{'査読付き論文、受理済み論文、プレプリント。' if ja else 'Peer-reviewed papers, accepted manuscripts, and preprints.'} <a href="{SCHOLAR}">Google Scholar ↗</a></p></header><div class="filters" role="group" aria-label="{'論文の状態で絞り込む' if ja else 'Filter papers by publication status'}" hidden>{filters}</div><p class="visually-hidden" id="filter-status" role="status" aria-live="polite"></p><div class="all-publications">{''.join(years)}</div><p class="publication-note">{'受理済み論文は、学術誌版が公開されるまでプレプリントにリンクしています。' if ja else 'Accepted work links to the public preprint until a journal version is available.'}</p><section class="section presentations"><h2>{'講演・学会発表' if ja else 'Talks & Presentations'}</h2><ol class="presentation-list">{invited_talks(lang)}{''.join(talks)}</ol></section>'''

def document(lang,page):
    ja = lang=='ja'
    home_page = page=='home'
    prefix = '../' if home_page else '../../'
    home_link = './' if home_page else '../'
    other = 'en' if ja else 'ja'
    suffix = '' if home_page else page+'/'
    path = f'/{lang}/{suffix}'
    titles = {'home':'ホーム' if ja else 'Home','publications':'研究業績' if ja else 'Publications'}
    name = '陳 民瑞' if ja else 'Minrui Chen'
    description = '陳民瑞。九州大学大学院システム情報科学府・博士後期課程。機械学習、計算生物学、形式手法を研究しています。' if ja else 'Minrui Chen, PhD student at Kyushu University. Research in machine learning, computational biology, optimization, and formal methods.'
    nav = ''.join(f'<a href="{home_link if key=="home" else ("./" if key==page else home_link+key+"/")}" {"aria-current="+chr(34)+"page"+chr(34) if key==page else ""}>{value}</a>' for key,value in titles.items())
    schema={'@context':'https://schema.org','@type':'Person','name':'Minrui Chen','alternateName':'陳 民瑞','url':ORIGIN,'image':ORIGIN+'/assets/avatar.png','affiliation':{'@type':'Organization','name':'Kyushu University'},'sameAs':[SCHOLAR,GITHUB,ORCID]}
    content={'home':home,'publications':publications}[page](lang)
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light dark"><title>{titles[page]} | {name}</title><meta name="description" content="{esc(description)}"><link rel="canonical" href="{ORIGIN}{path}"><link rel="alternate" hreflang="ja" href="{ORIGIN}/ja/{suffix}"><link rel="alternate" hreflang="en" href="{ORIGIN}/en/{suffix}"><link rel="alternate" hreflang="x-default" href="{ORIGIN}/ja/{suffix}"><meta property="og:type" content="website"><meta property="og:title" content="{titles[page]} | {name}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{ORIGIN}{path}"><meta property="og:image" content="{ORIGIN}/assets/avatar.png"><meta name="twitter:card" content="summary"><link rel="icon" href="{prefix}assets/avatar.png" type="image/png"><script src="{prefix}assets/theme.js"></script><link rel="stylesheet" href="{prefix}assets/style.css"><script defer src="{prefix}assets/main.js"></script><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head>
<body><a class="skip-link" href="#main">{'本文へ移動' if ja else 'Skip to content'}</a><header class="site-header"><nav class="nav-shell" aria-label="{'メインナビゲーション' if ja else 'Main navigation'}"><a class="brand" href="{home_link}"><img src="{prefix}assets/avatar.png" alt="" width="30" height="30"><span>@leochenminrui</span></a><div class="nav-links" id="navigation">{nav}</div><div class="nav-actions"><button class="theme-toggle icon-button" type="button" aria-label="{'ダークモードに切り替え' if ja else 'Switch to dark mode'}" aria-pressed="false" hidden>{icon('moon')}{icon('sun')}</button><a class="language-toggle" href="{prefix}{other}/{suffix}" lang="{other}" hreflang="{other}" aria-label="{'Switch to English' if ja else '日本語に切り替え'}">{'EN' if ja else '日本語'}</a><button class="menu-toggle icon-button" type="button" aria-controls="navigation" aria-expanded="false" aria-label="{'メニューを開く' if ja else 'Open navigation menu'}" hidden>{icon('menu')}</button></div></nav></header>
<main id="main" class="content {page}-page">{content}</main><footer class="site-footer"><div><span>© 2026 {name}</span><span class="footer-note">{'2026年11月更新' if ja else 'Updated November 2026'}</span><a href="{GITHUB}">GitHub {icon('arrow')}</a></div></footer></body></html>'''

for lang in ('ja','en'):
    for page in ('home','publications'):
        target=SITE/lang/('' if page=='home' else page)/'index.html'
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(document(lang,page))
(SITE/'index.html').write_text('''<!doctype html><html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>陳 民瑞 | Minrui Chen</title><meta http-equiv="refresh" content="0; url=ja/"><link rel="canonical" href="https://leochenminrui.github.io/ja/"></head><body><p><a href="ja/">陳 民瑞 — 日本語</a> · <a href="en/">Minrui Chen — English</a></p></body></html>''')
(SITE/'404.html').write_text('''<!doctype html><html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>ページが見つかりません | Minrui Chen</title><link rel="stylesheet" href="/assets/style.css"></head><body><main class="content"><p class="eyebrow">404</p><h1>ページが見つかりません</h1><p lang="en">This page could not be found.</p><p><a href="/ja/">ホームへ →</a> · <a href="/en/">Home →</a></p></main></body></html>''')
(SITE/'.nojekyll').touch()
(SITE/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n')
urls=[f'{ORIGIN}/{lang}/{suffix}' for lang in ('ja','en') for suffix in ('','publications/')]
(SITE/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{u}</loc></url>' for u in urls)+'</urlset>\n')
print('Built Japanese / English homepage, research records, and site metadata.')
