# -*- coding: utf-8 -*-
"""Genereert statische HTML uit voorraad.csv: voorraad.html, heftruck/<slug>.html en sitemap.xml.
Draait automatisch in de GitHub Action na elke sheet-sync. Doel: voorraad leesbaar voor zoek- en AI-crawlers."""
import csv, io, json, os, re, html, glob, datetime, unicodedata
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
BASE = 'https://b-spaansen.nl'
TODAY = datetime.date.today().isoformat()
e = html.escape
WA = 'https://wa.me/31629061612?text='

def num(v):
    d = re.sub(r'\D', '', str(v or '')); return int(d) if d else 0
def fmt(n): return f'{int(round(n)):,}'.replace(',', '.')
def slugify(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

fotomap = json.load(open(os.path.join(ROOT, 'fotos.json'), encoding='utf-8')) if os.path.exists(os.path.join(ROOT, 'fotos.json')) else {}
def photo(u):
    u = (u or '').strip()
    if not u: return ''
    if u in fotomap: return f'https://lh3.googleusercontent.com/d/{fotomap[u]}=w1200'
    m = re.search(r'drive\.google\.com/file/d/([\w-]+)', u) or re.search(r'drive\.google\.com/(?:open|uc|thumbnail)\?[^#]*id=([\w-]+)', u)
    if m: return f'https://lh3.googleusercontent.com/d/{m.group(1)}=w1200'
    return u if re.match(r'https?://', u) else ''

def load():
    text = open(os.path.join(ROOT, 'voorraad.csv'), encoding='utf-8').read()
    rows = [r for r in csv.reader(io.StringIO(text)) if any(c.strip() for c in r)]
    head = [h.strip().lower() for h in rows[0]]
    out, used = [], set()
    for r in rows[1:]:
        g = lambda n: (r[head.index(n)].strip() if n in head and head.index(n) < len(r) else '')
        merk, typ = g('merk'), g('type')
        if not merk or not typ or re.fullmatch(r'[-–—\s]*', merk) or re.fullmatch(r'[-–—\s]*', typ): continue
        status = g('status').lower()
        if status == 'verkocht': continue
        b = g('brandstof').lower()
        brand = 'Diesel' if 'diesel' in b else ('Gas (LPG)' if re.search(r'gas|lpg', b) else ('Elektrisch' if re.search(r'elek|electr|accu', b) else ''))
        hr = (g('hefvermogen (kg)') or g('hefvermogen')).lower()
        if 'ton' in hr:
            try: hef = round(float(re.sub(r'[^\d.]', '', hr.replace(',', '.'))) * 1000)
            except ValueError: hef = 0
        else: hef = num(hr)
        year = num(g('bouwjaar'))
        fotos_ = [p for p in (photo(g(f'foto {k}')) for k in range(1, 9)) if p]
        if not (fotos_ or num(g('prijs')) or hef): continue  # geen bruikbare gegevens: geen eigen pagina
        slug = slugify(f'{merk} {typ} {year or ""}')
        base, n = slug, 2
        while slug in used: slug = f'{base}-{n}'; n += 1
        used.add(slug)
        out.append(dict(slug=slug, merk=merk, type=typ, year=year, hef=hef, uren=num(g('draaiuren')), prijs=num(g('prijs')),
                        brand=brand, status='gereserveerd' if status == 'gereserveerd' else 'beschikbaar',
                        mast=g('mast'), conditie=g('conditie'), besch=g('beschrijving'),
                        fotos=[p for p in (photo(g(f'foto {k}')) for k in range(1, 9)) if p]))
    return out

CSS = """:root{--navy:#0a1628;--accent:#f59e0b;--gray:#f4f6f9;--mut:#475569}
*{margin:0;padding:0;box-sizing:border-box}html{scroll-padding-top:84px}
body{font-family:'Barlow',sans-serif;color:#0f172a;background:#fff;line-height:1.65}
header{position:sticky;top:0;z-index:20;background:#eef1f6;border-bottom:3px solid var(--accent)}
.bar{max-width:1100px;margin:auto;padding:8px 20px;display:flex;align-items:center;justify-content:space-between;gap:12px}
.bar img{height:44px;width:auto;display:block}
.bar nav{display:flex;gap:22px;align-items:center;font-family:'Barlow Condensed',sans-serif;font-weight:600;letter-spacing:.04em;text-transform:uppercase}
.bar nav a{color:var(--navy);text-decoration:none}.tel{background:var(--accent);padding:8px 14px;border-radius:6px}
.wrap{max-width:1100px;margin:auto;padding:0 20px}
.hero{background:var(--navy);color:#fff;padding:40px 0 34px}
.crumbs{font-size:14px;color:#94a3b8;margin-bottom:12px}.crumbs a{color:#94a3b8}
h1{font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:clamp(30px,5.5vw,48px);line-height:1.08}
h1 em{font-style:normal;color:var(--accent)}
.sub{color:#cbd5e1;margin-top:8px;font-size:17px}
main{padding:30px 0 60px}
.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px;margin-bottom:26px}
.gal img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:10px;background:#e2e8f0}
.gal img:first-child{grid-column:1/-1;aspect-ratio:16/10;max-height:560px}
.price{font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:40px;color:var(--accent);line-height:1}
.price small{display:block;font-family:'Barlow',sans-serif;font-weight:400;font-size:14px;color:var(--mut);margin-top:6px}
table{border-collapse:collapse;width:100%;max-width:560px;margin:20px 0}
td,th{text-align:left;padding:10px 12px;border-bottom:1px solid #e2e8f0}th{width:45%;color:var(--mut);font-weight:500}
.desc p{margin-bottom:12px;max-width:760px}
.btns{display:flex;gap:10px;flex-wrap:wrap;margin:22px 0}
.btn{display:inline-flex;align-items:center;justify-content:center;background:var(--accent);color:var(--navy);font-family:'Barlow Condensed',sans-serif;font-weight:700;letter-spacing:.04em;text-transform:uppercase;text-decoration:none;padding:12px 20px;border-radius:8px;font-size:16px}
.btn.wa{background:#25d366;color:#fff}
.badge{display:inline-block;background:var(--accent);color:var(--navy);font-weight:600;font-size:13px;letter-spacing:.06em;text-transform:uppercase;padding:4px 10px;border-radius:4px;margin-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px;margin-top:22px}
.card{display:block;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;text-decoration:none;color:inherit}
.card img{width:100%;aspect-ratio:16/10;object-fit:cover;background:#e2e8f0;display:block}
.card div{padding:14px 16px}.card h2{font-size:20px;color:var(--navy);margin-bottom:4px}.card p{color:var(--mut);font-size:15px}
.card .p{font-weight:700;color:var(--navy);margin-top:6px}
footer{background:var(--navy);color:#cbd5e1;padding:36px 0;font-size:15px}footer a{color:var(--accent);text-decoration:none}
@media(max-width:700px){.gal{grid-template-columns:1fr 1fr;gap:8px}.hero{padding:30px 0 26px}.bar nav a:not(.tel){display:none}.bar img{height:36px}.price{font-size:34px}.btn{flex:1}}"""

LANDING = ['gebruikte-heftruck-kopen', 'heftruck-verkopen-inruilen', 'heftruck-huren', 'heftruckdealer-noord-holland']

def shell(title, desc, canonical, ld, body, og_img=None, extra_css=''):
    return f'''<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0a1628">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="/logo.png">
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canonical}">
<meta property="og:locale" content="nl_NL"><meta property="og:site_name" content="B-Spaansen Heftrucks">
<meta property="og:image" content="{og_img or BASE + '/logo.png'}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;800&family=Barlow:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}{extra_css}</style>
</head>
<body>
<header><div class="bar"><a href="/"><img src="/logo.png" alt="B-Spaansen Heftrucks"></a>
<nav><a href="/voorraad.html">Voorraad</a><a href="/bezoek-onze-locatie.html">Showroom</a><a href="/faq.html">Kennisbank</a><a class="tel" href="tel:+31629061612">+31 6 29061612</a></nav></div></header>
{body}
<footer><div class="wrap"><strong style="color:#fff">B-Spaansen In- en Verkoop Heftrucks</strong><br>
Schelphorst 22, A1 · 1771 SL Wieringerwerf<br>
<a href="tel:+31629061612">+31 6 29061612</a> · <a href="mailto:Barryspaansen@gmail.com">Barryspaansen@gmail.com</a><br>
Open donderdag t/m zondag, 08:00 – 19:00<br><br>
<a href="/">Home</a> · <a href="/voorraad.html">Voorraad</a> · <a href="/faq.html">Kennisbank</a> · <a href="/bezoek-onze-locatie.html">Showroom</a><br><a href="/gebruikte-heftruck-kopen.html">Heftruck kopen</a> · <a href="/heftruck-verkopen-inruilen.html">Verkopen of inruilen</a> · <a href="/heftruck-huren.html">Heftruck huren</a> · <a href="/heftruckdealer-noord-holland.html">Dealer Noord-Holland</a></div></footer>
</body></html>'''

SELLER = {"@type": "AutoDealer", "name": "B-Spaansen In- en Verkoop Heftrucks", "url": BASE + "/", "telephone": "+31629061612",
          "address": {"@type": "PostalAddress", "streetAddress": "Schelphorst 22, A1", "postalCode": "1771 SL", "addressLocality": "Wieringerwerf", "addressCountry": "NL"}}

def kind(t): return 'heftruck' if t['hef'] else 'machine'
def title_of(t):
    return f"{t['merk']} {t['type']}" + (f" ({t['year']})" if t['year'] else '')

def truck_page(t):
    name = title_of(t)
    specs = [('Merk', t['merk']), ('Type', t['type'])]
    if t['year']: specs.append(('Bouwjaar', str(t['year'])))
    if t['uren']: specs.append(('Draaiuren', fmt(t['uren'])))
    if t['hef']: specs.append(('Hefvermogen', f"{fmt(t['hef'])} kg"))
    if t['brand']: specs.append(('Brandstof / aandrijving', t['brand']))
    if t['mast']: specs.append(('Mast', t['mast']))
    if t['conditie']: specs.append(('Conditie', t['conditie']))
    specs.append(('Status', 'Gereserveerd' if t['status'] == 'gereserveerd' else 'Beschikbaar'))
    desc = f"Gebruikte {name}" if t['hef'] else f"{name}"; desc = desc + (f", {fmt(t['hef'])} kg hefvermogen" if t['hef'] else '') + (f", {t['brand'].lower()}" if t['brand'] else '') + \
           (f", {fmt(t['uren'])} draaiuren" if t['uren'] else '') + (f", € {fmt(t['prijs'])} excl. btw" if t['prijs'] else '') + \
           ". Te koop bij B-Spaansen in Wieringerwerf, bezichtigen op afspraak."
    ld = {"@context": "https://schema.org", "@type": "Product", "name": (f"{name} heftruck" if t['hef'] else name), "description": desc,
          "brand": {"@type": "Brand", "name": t['merk']}, "model": t['type'], "category": "Heftruck" if t['hef'] else "Overig",
          "itemCondition": "https://schema.org/UsedCondition", "url": f"{BASE}/heftruck/{t['slug']}.html",
          "additionalProperty": [{"@type": "PropertyValue", "name": k, "value": v} for k, v in specs if k not in ('Merk', 'Type')]}
    if t['fotos']: ld["image"] = t['fotos']
    offer = {"@type": "Offer", "priceCurrency": "EUR", "seller": SELLER,
             "availability": "https://schema.org/LimitedAvailability" if t['status'] == 'gereserveerd' else "https://schema.org/InStock",
             "url": f"{BASE}/heftruck/{t['slug']}.html", "itemCondition": "https://schema.org/UsedCondition"}
    if t['prijs']:
        offer["price"] = str(t['prijs']); offer["valueAddedTaxIncluded"] = False
    ld["offers"] = offer
    if not t['prijs']:
        # Prijs op aanvraag: wel productgegevens, geen Offer (er is geen prijs om te noemen).
        ld.pop("offers", None)
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Voorraad", "item": BASE + "/voorraad.html"},
        {"@type": "ListItem", "position": 3, "name": name, "item": f"{BASE}/heftruck/{t['slug']}.html"}]}
    gal = ''.join(f'<img src="{e(p)}" alt="{e(name)}{' heftruck' if t['hef'] else ''}, foto {i}" loading="{"eager" if i == 1 else "lazy"}">' for i, p in enumerate(t['fotos'], 1))
    paras = ''.join(f'<p>{e(x.strip())}</p>' for x in re.split(r'\n\s*\n|\n', t['besch']) if x.strip())
    price = (f'<div class="price">€ {fmt(t["prijs"])}<small>Prijs excl. btw · vrijblijvend bezichtigen op afspraak</small></div>'
             if t['prijs'] else '<div class="price" style="font-size:28px">Prijs op aanvraag</div>')
    msg = f"Hallo, ik heb interesse in de {name} (zie b-spaansen.nl/heftruck/{t['slug']}.html)."
    from urllib.parse import quote
    body = f'''<section class="hero"><div class="wrap">
<div class="crumbs"><a href="/">Home</a> › <a href="/voorraad.html">Voorraad</a> › {e(name)}</div>
{'<span class="badge">Gereserveerd</span><br>' if t['status'] == 'gereserveerd' else ''}
<h1>{e(t['merk'])} <em>{e(t['type'])}</em>{' · ' + str(t['year']) if t['year'] else ''}</h1>
<p class="sub">{'Gebruikte heftruck' if t['hef'] else 'Te koop bij B-Spaansen'}{' · ' + e(t['brand']) if t['brand'] else ''}{' · ' + fmt(t['hef']) + ' kg' if t['hef'] else ''}</p></div></section>
<main><div class="wrap">
<div class="gal">{gal}</div>
{price}
<table>{''.join(f'<tr><th>{e(k)}</th><td>{e(v)}</td></tr>' for k, v in specs)}</table>
<div class="desc">{paras}</div>
<div class="btns"><a class="btn" href="/#contact">Vraag aan of plan bezichtiging</a>
<a class="btn wa" href="{WA}{quote(msg)}" target="_blank" rel="noopener">WhatsApp</a>
<a class="btn" style="background:#e2e8f0" href="tel:+31629061612">Bel +31 6 29061612</a></div>
<p style="color:var(--mut);font-size:15px">Zoek je iets anders? Bekijk de <a href="/voorraad.html">complete voorraad</a> of lees de <a href="/faq.html">kennisbank</a>. Transport door heel Nederland is bespreekbaar.</p>
</div></main>'''
    page = shell((f"{name} te koop – gebruikte heftruck | B-Spaansen" if t['hef'] else f"{name} te koop | B-Spaansen"), desc, f"{BASE}/heftruck/{t['slug']}.html", [ld, crumbs], body, t['fotos'][0] if t['fotos'] else None)
    return page

def index_page(ts):
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Actuele voorraad gebruikte heftrucks",
          "itemListElement": [{"@type": "ListItem", "position": i, "url": f"{BASE}/heftruck/{t['slug']}.html", "name": title_of(t)} for i, t in enumerate(ts, 1)]}
    cards = ''
    for t in ts:
        img = f'<img src="{e(t["fotos"][0])}" alt="{e(title_of(t))}" loading="lazy">' if t['fotos'] else ''
        meta = ' · '.join(x for x in [t['brand'], f"{fmt(t['hef'])} kg" if t['hef'] else '', f"{fmt(t['uren'])} uur" if t['uren'] else ''] if x)
        cards += f'<a class="card" href="/heftruck/{t["slug"]}.html">{img}<div><h2>{e(title_of(t))}</h2><p>{e(meta)}</p><p class="p">{"€ " + fmt(t["prijs"]) + " excl. btw" if t["prijs"] else "Prijs op aanvraag"}{" · Gereserveerd" if t["status"] == "gereserveerd" else ""}</p></div></a>'
    body = f'''<section class="hero"><div class="wrap"><div class="crumbs"><a href="/">Home</a> › Voorraad</div>
<h1>Gebruikte heftrucks <em>uit voorraad</em></h1>
<p class="sub">{len(ts)} machine{'s' if len(ts) != 1 else ''} beschikbaar · bijgewerkt {datetime.date.today().strftime('%d-%m-%Y')} · bezichtigen op afspraak in Wieringerwerf</p></div></section>
<main><div class="wrap"><div class="grid">{cards}</div>
<p style="margin-top:28px;color:var(--mut)">Niet gevonden wat je zoekt? <a href="/#contact">Vraag het ons</a> of app via <a href="{WA}Hallo%2C%20ik%20zoek%20een%20heftruck.">WhatsApp</a>. Meer weten over kopen, huren of inruilen? Lees de <a href="/faq.html">kennisbank</a>.</p></div></main>'''
    return shell(f"Voorraad gebruikte heftrucks ({len(ts)}) | B-Spaansen Wieringerwerf", "Actuele voorraad gebruikte heftrucks van B-Spaansen in Wieringerwerf: Toyota, Doosan en meer. Met foto's, prijs en specificaties.", BASE + "/voorraad.html", ld, body)

def sitemap(ts):
    urls = [('/', '1.0'), ('/voorraad.html', '0.9'), ('/faq.html', '0.8'), ('/bezoek-onze-locatie.html', '0.7')] + [(f'/{n}.html', '0.9') for n in LANDING] + [(f"/heftruck/{t['slug']}.html", '0.8') for t in ts]
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    x += ''.join(f'  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>\n' for u, p in urls)
    return x + '</urlset>\n'

if __name__ == '__main__':
    ts = load()
    d = os.path.join(ROOT, 'heftruck'); os.makedirs(d, exist_ok=True)
    for f in glob.glob(os.path.join(d, '*.html')): os.remove(f)
    for t in ts: open(os.path.join(d, t['slug'] + '.html'), 'w', encoding='utf-8').write(truck_page(t))
    open(os.path.join(ROOT, 'voorraad.html'), 'w', encoding='utf-8').write(index_page(ts))
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(sitemap(ts))
    print('trucks:', [t['slug'] for t in ts])
