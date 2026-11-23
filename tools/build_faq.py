# -*- coding: utf-8 -*-
import sys, json, html, os
sys.path.insert(0, os.path.dirname(__file__))
from faq_data import CATS, SOURCES
BASE = "https://b-spaansen.nl"
DATE = "2026-11-23"
WA = "https://wa.me/31629061612?text=Hallo%2C%20ik%20heb%20een%20vraag%20over%20heftrucks."
CTA = {
 "koop": ("Bekijk de actuele voorraad", "index.html#voorraad"),
 "huur": ("Vraag een huurofferte aan", "index.html#contact"),
 "inruil": ("Vraag een vrijblijvend bod aan", "index.html#contact"),
 "keur": ("Vraag een keuring aan", "index.html#contact"),
 "loc": ("Plan een bezichtiging", "bezoek-onze-locatie.html"),
}
e = html.escape
def slug(i, cat): return f"{cat}-{i}"

total = sum(len(c[3]) for c in CATS)
ld_items = []
for cs, ct, _, items in CATS:
    for i, (q, gen, spec, cta) in enumerate(items, 1):
        txt = gen + (" " + spec if spec else "") + f" Meer informatie: B-Spaansen Heftrucks, Wieringerwerf – {BASE}/faq.html#{slug(i,cs)}"
        ld_items.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": txt}})
ld = [
 {"@context": "https://schema.org", "@type": "FAQPage", "@id": BASE + "/faq.html#faq", "url": BASE + "/faq.html",
  "inLanguage": "nl-NL", "dateModified": DATE, "mainEntity": ld_items,
  "publisher": {"@type": "AutoDealer", "name": "B-Spaansen In- en Verkoop Heftrucks", "url": BASE + "/"}},
 {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
  {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
  {"@type": "ListItem", "position": 2, "name": "Kennisbank heftrucks", "item": BASE + "/faq.html"}]},
]

nav_chips = "".join(f'<a href="#{cs}">{e(ct)}</a>' for cs, ct, _, _ in CATS)
body = []
for cs, ct, defcta, items in CATS:
    body.append(f'<section class="cat" id="{cs}"><h2>{e(ct)}</h2>')
    for i, (q, gen, spec, cta) in enumerate(items, 1):
        qid = slug(i, cs)
        body.append(f'<article class="qa" id="{qid}"><h3>{e(q)}</h3><p>{e(gen)}</p>')
        if spec:
            body.append(f'<div class="bs"><strong>Bij B-Spaansen:</strong> {e(spec)}</div>')
        cta = cta or defcta
        body.append(f'<p class="src-line">Antwoord van <a href="index.html">B-Spaansen Heftrucks</a>, Wieringerwerf · <a href="#{qid}">link naar deze vraag</a></p>')
        if cta in CTA:
            lbl, href = CTA[cta]
            body.append(f'<p class="cta"><a class="btn" href="{href}">{e(lbl)}</a> <a class="btn wa" href="{WA}" target="_blank" rel="noopener">WhatsApp</a></p>')
        body.append('</article>')
    body.append('</section>')
src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in SOURCES)

page = f'''<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kennisbank heftrucks: {total} veelgestelde vragen en antwoorden | B-Spaansen</title>
<meta name="description" content="Antwoorden op {total} vragen over heftrucks kopen, tweedehands heftrucks, huren, verkopen, inruilen, accu's, keuringen en onderhoud. Van B-Spaansen Heftrucks in Wieringerwerf.">
<meta name="robots" content="index, follow, max-snippet:-1">
<meta name="theme-color" content="#0a1628">
<link rel="canonical" href="{BASE}/faq.html">
<link rel="icon" href="logo.png">
<meta property="og:type" content="website">
<meta property="og:title" content="Kennisbank heftrucks: veelgestelde vragen | B-Spaansen">
<meta property="og:description" content="Duidelijke antwoorden over heftrucks kopen, huren, verkopen en inruilen.">
<meta property="og:url" content="{BASE}/faq.html">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="B-Spaansen Heftrucks">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;800&family=Barlow:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--navy:#0a1628;--accent:#f59e0b;--gray:#f4f6f9;--text:#0f172a;--mut:#475569}}
*{{margin:0;padding:0;box-sizing:border-box}}html{{scroll-behavior:smooth;scroll-padding-top:84px}}
body{{font-family:'Barlow',sans-serif;color:var(--text);background:#fff;line-height:1.65}}
header{{position:sticky;top:0;z-index:20;background:#eef1f6;border-bottom:3px solid var(--accent)}}
.bar{{max-width:1100px;margin:auto;padding:8px 20px;display:flex;align-items:center;justify-content:space-between;gap:12px}}
.bar img{{height:44px;width:auto;display:block}}
.bar nav{{display:flex;gap:22px;align-items:center;font-family:'Barlow Condensed',sans-serif;font-weight:600;letter-spacing:.04em;text-transform:uppercase}}
.bar nav a{{color:var(--navy);text-decoration:none}}.bar nav a:hover{{color:var(--accent)}}
.tel{{background:var(--accent);padding:8px 14px;border-radius:6px}}
.hero{{background:var(--navy);color:#fff;padding:56px 20px 44px}}
.wrap{{max-width:1100px;margin:auto}}
.hero h1{{font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:clamp(32px,6vw,54px);line-height:1.05;margin-bottom:14px}}
.hero h1 em{{font-style:normal;color:var(--accent)}}
.hero p{{max-width:720px;color:#cbd5e1;font-size:17px}}
.crumbs{{font-size:14px;color:#94a3b8;margin-bottom:16px}}.crumbs a{{color:#94a3b8}}
.chips{{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0 0}}
@media(max-width:700px){{.chips{{flex-wrap:nowrap;overflow-x:auto;margin-right:-20px;padding-right:20px;-webkit-overflow-scrolling:touch;scrollbar-width:none}}.chips a{{white-space:nowrap;flex:none}}.hero p{{font-size:16px}}}}
.chips a{{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);color:#fff;text-decoration:none;font-size:14px;padding:7px 12px;border-radius:99px}}
.chips a:hover{{background:var(--accent);color:var(--navy)}}
main{{max-width:1100px;margin:auto;padding:30px 20px 60px}}
.search{{width:100%;padding:14px 16px;font-size:16px;border:2px solid #cbd5e1;border-radius:10px;margin-bottom:10px;font-family:inherit}}
.search:focus{{outline:none;border-color:var(--accent)}}
#nores{{display:none;color:var(--mut);padding:10px 0}}
.cat{{margin-top:38px}}
.cat h2{{font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:30px;color:var(--navy);border-left:5px solid var(--accent);padding-left:12px;margin-bottom:6px}}
.qa{{padding:20px 0;border-bottom:1px solid #e2e8f0}}
.qa h3{{font-size:19px;font-weight:600;color:var(--navy);margin-bottom:8px;line-height:1.35}}
.qa p{{color:#1e293b}}
.bs{{margin-top:12px;background:#fff7e6;border-left:4px solid var(--accent);padding:12px 14px;border-radius:6px;font-size:15.5px}}
.src-line{{font-size:14px;color:var(--mut);margin-top:10px}}.src-line a{{color:var(--navy)}}
.cta{{margin-top:14px;display:flex;gap:10px;flex-wrap:wrap;align-items:stretch}}
.btn{{display:inline-block;background:var(--accent);color:var(--navy);font-family:'Barlow Condensed',sans-serif;font-weight:700;letter-spacing:.04em;text-transform:uppercase;text-decoration:none;padding:10px 18px;border-radius:8px;font-size:15px}}
.btn.wa{{background:#25d366;color:#fff}}
.src{{margin-top:48px;background:var(--gray);padding:20px 22px;border-radius:10px;font-size:15px;color:var(--mut)}}
.src h2{{font-size:20px;color:var(--navy);margin-bottom:8px}}.src li{{margin-left:20px;margin-bottom:4px}}
.note{{font-size:14px;color:var(--mut);margin-top:10px}}
footer{{background:var(--navy);color:#cbd5e1;padding:36px 20px;font-size:15px}}
footer a{{color:var(--accent);text-decoration:none}}
@media(max-width:700px){{.bar nav a:not(.tel){{display:none}}.bar img{{height:36px}}.hero{{padding:36px 20px 30px}}.cat h2{{font-size:25px}}.qa h3{{font-size:18px}}.btn{{flex:1;text-align:center;display:flex;align-items:center;justify-content:center}}}}
</style>
</head>
<body>
<header><div class="bar"><a href="index.html"><img src="logo.png" alt="B-Spaansen Heftrucks"></a>
<nav><a href="index.html#voorraad">Voorraad</a><a href="bezoek-onze-locatie.html">Showroom</a><a href="faq.html">Kennisbank</a><a class="tel" href="tel:+31629061612">+31 6 29061612</a></nav></div></header>
<section class="hero"><div class="wrap">
<div class="crumbs"><a href="index.html">Home</a> › Kennisbank</div>
<h1>Alles over heftrucks: <em>{total} vragen, duidelijk beantwoord</em></h1>
<p>Heftruck kopen, huren, verkopen of inruilen? Hier vind je praktische antwoorden van B-Spaansen Heftrucks in Wieringerwerf. Algemene vakkennis en informatie over ons bedrijf zijn duidelijk gescheiden.</p>
<div class="chips">{nav_chips}</div></div></section>
<main>
<input class="search" id="q" type="search" placeholder="Zoek in alle vragen, bijvoorbeeld: accu, keuring, huren…" aria-label="Zoek in de kennisbank">
<p id="nores">Geen vragen gevonden. Stel je vraag gerust via <a href="{WA}">WhatsApp</a>.</p>
{"".join(body)}
<div class="src"><h2>Bronnen</h2><ul>{src}</ul>
<p class="note">Prijzen en aantallen uit bronnen zijn indicaties en kunnen per machine en markt verschillen. Laatst bijgewerkt: 23 november 2026.</p></div>
</main>
<footer><div class="wrap"><strong style="color:#fff">B-Spaansen In- en Verkoop Heftrucks</strong><br>
Schelphorst 22, A1 · 1771 SL Wieringerwerf<br>
<a href="tel:+31629061612">+31 6 29061612</a> · <a href="mailto:Barryspaansen@gmail.com">Barryspaansen@gmail.com</a><br>
Open donderdag t/m zondag, 08:00 – 19:00<br><br>
<a href="index.html">Home</a> · <a href="index.html#voorraad">Voorraad</a> · <a href="bezoek-onze-locatie.html">Showroom</a></div></footer>
<script>
(function(){{var i=document.getElementById('q'),a=[].slice.call(document.querySelectorAll('.qa')),c=[].slice.call(document.querySelectorAll('.cat')),n=document.getElementById('nores');
i.addEventListener('input',function(){{var v=i.value.trim().toLowerCase(),s=0;a.forEach(function(x){{var m=!v||x.textContent.toLowerCase().indexOf(v)>-1;x.style.display=m?'':'none';if(m)s++}});
c.forEach(function(x){{x.style.display=x.querySelector('.qa:not([style*="none"])')?'':'none'}});n.style.display=s?'none':'block'}});}})();
</script>
</body></html>'''
open(os.path.join(os.path.dirname(__file__), '..', 'faq.html'), 'w', encoding='utf-8').write(page)
print('ok', total, len(page))
