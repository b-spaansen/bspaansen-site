# -*- coding: utf-8 -*-
"""Bouwt de vier commerciële landingspagina's. Draait na build_voorraad.py (zelfde workflow)."""
import os, sys, json, html
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_voorraad as bv
e = html.escape
BASE = bv.BASE
SUP = "https://www.supralift.com/nl/article/wat-kost-een-gebruikte-heftruck-151"
OND = "https://ondernemersplein.overheid.nl/wetten-en-regels/arbeidsmiddelen-keuren-en-machineveiligheid/"
STI = "https://stigas.nl/heftruckinstructie-het-nederlands"
WA = bv.WA
def wa(msg): return WA + quote(msg)

EXTRA = """.art{max-width:800px}.art h2{font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:28px;color:var(--navy);margin:34px 0 10px;border-left:5px solid var(--accent);padding-left:12px}
.art p,.art li{margin-bottom:10px}.art ul,.art ol{margin:0 0 14px 22px}.art a{color:#b45309}
.answer{background:#fff7e6;border-left:5px solid var(--accent);padding:16px 18px;border-radius:8px;font-size:18px;margin:6px 0 18px}
.faq h3{font-size:18px;color:var(--navy);margin:20px 0 6px}.srcs{font-size:14px;color:var(--mut);margin-top:30px}
@media(max-width:700px){.art h2{font-size:24px}}"""

def li(items): return '<ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'
def ol(items): return '<ol>' + ''.join(f'<li>{x}</li>' for x in items) + '</ol>'

def stock_cards(ts, n=6):
    out = ''
    for t in sorted(ts, key=lambda t: not t['hef'])[:n]:
        img = f'<img src="{e(t["fotos"][0])}" alt="{e(bv.title_of(t))}" loading="lazy">' if t['fotos'] else ''
        meta = ' · '.join(x for x in [t['brand'], f"{bv.fmt(t['hef'])} kg" if t['hef'] else '', f"{bv.fmt(t['uren'])} uur" if t['uren'] else ''] if x)
        pr = f"€ {bv.fmt(t['prijs'])} excl. btw" if t['prijs'] else 'Prijs op aanvraag'
        out += f'<a class="card" href="/heftruck/{t["slug"]}.html">{img}<div><h2>{e(bv.title_of(t))}</h2><p>{e(meta)}</p><p class="p">{pr}</p></div></a>'
    return f'<div class="grid">{out}</div>' if out else ''

def page(slug, title, desc, h1, h1em, sub, body, faq, sources, ts):
    ld = [{"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": f"{BASE}/{slug}.html", "description": desc,
           "dateModified": bv.TODAY, "inLanguage": "nl-NL", "publisher": bv.SELLER, "about": {"@type": "Thing", "name": "Gebruikte heftrucks"}},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
              {"@type": "ListItem", "position": 2, "name": h1 + ' ' + h1em, "item": f"{BASE}/{slug}.html"}]}]
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re_text(a) + f" Meer informatie: B-Spaansen Heftrucks, Wieringerwerf – {BASE}/{slug}.html"}} for q, a in faq]})
    faq_html = ''
    if faq:
        faq_html = '<h2>Veelgestelde vragen</h2><div class="faq">' + ''.join(f'<h3>{e(q)}</h3><p>{a}</p>' for q, a in faq) + '</div>'
    src_html = '<p class="srcs">Bronnen: ' + ' · '.join(f'<a href="{u}" target="_blank" rel="noopener">{e(t)}</a>' for t, u in sources) + '. Bedragen zijn indicaties uit de genoemde bron en kunnen per machine verschillen.</p>' if sources else ''
    cta = f'''<h2>Neem contact op met B-Spaansen</h2><p>B-Spaansen Heftrucks, Schelphorst 22 A1, 1771 SL Wieringerwerf. Open donderdag t/m zondag van 08:00 tot 19:00.</p>
<div class="btns"><a class="btn wa" href="{wa(f'Hallo, ik heb een vraag via b-spaansen.nl/{slug}.html')}" target="_blank" rel="noopener">WhatsApp</a>
<a class="btn" href="tel:+31629061612">Bel +31 6 29061612</a><a class="btn" style="background:#e2e8f0" href="/#contact">Contactformulier</a></div>'''
    html_body = f'''<section class="hero"><div class="wrap"><div class="crumbs"><a href="/">Home</a> › {e(h1)} {e(h1em)}</div>
<h1>{e(h1)} <em>{e(h1em)}</em></h1><p class="sub">{e(sub)}</p></div></section>
<main><div class="wrap art">{body}{faq_html}{cta}{src_html}</div></main>'''
    return bv.shell(title, desc, f"{BASE}/{slug}.html", ld, html_body, extra_css=EXTRA)

import re
def re_text(a): return re.sub(r'<[^>]+>', '', a)

def build():
    ts = bv.load()
    out = {}
    # 1. KOPEN
    out['gebruikte-heftruck-kopen'] = page('gebruikte-heftruck-kopen',
        'Gebruikte heftruck kopen in Noord-Holland | B-Spaansen Wieringerwerf',
        'Gebruikte heftruck kopen? B-Spaansen in Wieringerwerf verkoopt tweedehands heftrucks met foto, prijs en specificaties. Bezichtigen op afspraak, transport bespreekbaar.',
        'Gebruikte heftruck kopen', 'bij B-Spaansen', 'Tweedehands heftrucks uit voorraad · Wieringerwerf, Noord-Holland · bezichtigen op afspraak',
        f'''<div class="answer"><strong>Waar kan ik een gebruikte heftruck kopen?</strong> Bij B-Spaansen Heftrucks in Wieringerwerf (Noord-Holland). Je ziet de actuele voorraad met foto&#39;s en prijs op <a href="/voorraad.html">b-spaansen.nl/voorraad.html</a>, bezichtigen kan op afspraak en transport door heel Nederland is bespreekbaar.</div>
<h2>Actuele voorraad</h2><p>Dit zijn machines die nu bij ons staan. Prijzen zijn exclusief btw. <a href="/voorraad.html">Bekijk alle heftrucks</a>.</p>{stock_cards(ts)}
<h2>Waar let je op bij een gebruikte heftruck?</h2>
{li(['<strong>Draaiuren in verhouding tot staat:</strong> onder ongeveer 5.000 uur geldt als weinig slijtage, boven 10.000 uur is een grondige inspectie verstandig.',
     '<strong>Onderhoudshistorie en keuring:</strong> vraag naar het onderhoudsboek en een recente keuring.',
     '<strong>Lekkages en slijtage:</strong> kijk naar olie en hydrauliek, mast, kettingen, vorken, banden, remmen en stuurwerk.',
     '<strong>Aandrijving en accu:</strong> bij elektrisch is de accu een van de grootste kostenposten. Laat hem testen.',
     '<strong>Hefvermogen en hefhoogte:</strong> kies met een veiligheidsmarge en let op het lastzwaartepunt en eventuele attachments.',
     '<strong>Zelf zien en proberen:</strong> bekijk de machine en vraag of je hem kunt zien werken.'])}
<h2>Wat kost een tweedehands heftruck?</h2>
<p>De prijs hangt af van merk, bouwjaar, draaiuren, hefvermogen, hefhoogte, aandrijving en onderhoudsstaat. Volgens <a href="{SUP}" target="_blank" rel="noopener">Supralift (2025)</a> liggen gebruikte elektrische heftrucks grofweg tussen € 5.000 en € 20.000, diesel tussen € 6.000 en € 25.000 en LPG tussen € 4.500 en € 18.000. Reken ook op kosten naast de aanschaf, zoals transport, keuring en onderhoud. De prijs van elke machine van B-Spaansen staat bij de machine zelf.</p>
<h2>Elektrisch, diesel of LPG?</h2>
<p>Elektrisch is meestal de keuze voor binnen: schoon, stil en weinig onderhoud. Diesel past bij zwaar werk buiten. LPG zit daartussenin en is inzetbaar binnen en buiten. Twijfel je? Beschrijf je situatie via <a href="{wa('Hallo, ik zoek een heftruck. Mijn situatie: ')}" target="_blank" rel="noopener">WhatsApp</a>, dan denken we mee.</p>
<h2>Heftruck inruilen bij aankoop</h2><p>Je kunt je huidige heftruck laten meenemen. Lees <a href="/heftruck-verkopen-inruilen.html">hoe verkopen en inruilen werkt</a>.</p>''',
        [('Kan ik een gebruikte heftruck eerst bekijken?', 'Ja. Bij B-Spaansen kan dat op afspraak in Wieringerwerf, open donderdag t/m zondag van 08:00 tot 19:00.'),
         ('Kan een gebruikte heftruck bezorgd worden?', f'Transport door heel Nederland is bij B-Spaansen bespreekbaar. Volgens <a href="{SUP}" target="_blank" rel="noopener">Supralift</a> kost transport grofweg € 200 tot € 600, afhankelijk van afstand en machine.'),
         ('Zijn de prijzen inclusief of exclusief btw?', 'De prijzen op de website van B-Spaansen zijn exclusief btw.'),
         ('Kan ik een specifiek merk of type aanvragen?', 'Ja. Geef je wens door via WhatsApp of het contactformulier, dan kijken we wat er beschikbaar is of komt.')],
        [('Supralift: wat kost een tweedehands vorkheftruck', SUP)], ts)
    # 2. VERKOPEN / INRUILEN
    out['heftruck-verkopen-inruilen'] = page('heftruck-verkopen-inruilen',
        'Heftruck verkopen of inruilen | B-Spaansen koopt gebruikte heftrucks in',
        'Je gebruikte heftruck verkopen of inruilen? B-Spaansen in Wieringerwerf koopt heftrucks in. Stuur merk, type, bouwjaar, uren en foto\'s en ontvang een eerlijk bod.',
        'Heftruck verkopen', 'of inruilen', 'B-Spaansen koopt gebruikte heftrucks in en neemt machines in ruil',
        f'''<div class="answer"><strong>Waar kan ik mijn gebruikte heftruck verkopen?</strong> Bij B-Spaansen Heftrucks in Wieringerwerf. Wij kopen gebruikte heftrucks in en nemen ze ook in ruil. Stuur merk, type, bouwjaar, draaiuren en foto&#39;s via <a href="{wa('Hallo, ik wil mijn heftruck verkopen of inruilen. Merk/type/bouwjaar/uren: ')}" target="_blank" rel="noopener">WhatsApp</a> of het <a href="/#contact">contactformulier</a>, dan nemen we contact op voor een eerlijk bod.</div>
<h2>Zo werkt het</h2>
{ol(['<strong>Stuur de gegevens:</strong> merk, type, bouwjaar, draaiuren, hefvermogen en aandrijving, plus foto&#39;s van de machine (voor, zij, mast, cabine, typeplaatje en eventuele gebreken).',
     '<strong>Wij beoordelen en doen een bod:</strong> we nemen contact met je op. Bij twijfel kijken we de machine ter plaatse of in Wieringerwerf na.',
     '<strong>Afspraak en overdracht:</strong> we spreken af wanneer en hoe de machine wordt overgedragen. Ophalen of bezorgen bespreken we samen.'])}
<h2>Wat bepaalt de waarde van je heftruck?</h2>
{li(['Merk, type en bouwjaar', 'Draaiuren en algemene staat', 'Onderhoudshistorie en keuringsrapport', 'Hefvermogen, hefhoogte, mast en attachments', 'Bij elektrisch: de staat van de accu', 'Vraag en aanbod voor dat type op dat moment'])}
<h2>Inruilen voor een andere heftruck</h2><p>Zoek je een andere machine? Dan kun je je huidige heftruck bij de aankoop laten meenemen. Bekijk eerst de <a href="/voorraad.html">actuele voorraad</a> of lees <a href="/gebruikte-heftruck-kopen.html">waar je op let bij het kopen</a>.</p>''',
        [('Welk bedrijf koopt oude heftrucks in?', 'B-Spaansen Heftrucks in Wieringerwerf koopt gebruikte heftrucks in. Stuur de gegevens en foto&#39;s via WhatsApp of het contactformulier.'),
         ('Kan ik een defecte heftruck verkopen?', 'Meld de gebreken en stuur foto&#39;s. B-Spaansen beoordeelt of inkoop mogelijk is.'),
         ('Kan ik mijn heftruck direct verkopen?', 'Stuur de gegevens, dan nemen we zo snel mogelijk contact op. Of en wanneer we kunnen kopen hangt af van de machine.'),
         ('Kan mijn heftruck bij mij worden opgehaald?', 'Dat bespreken we samen. Vraag naar de mogelijkheden voor jouw locatie.')],
        [], ts)
    # 3. HUREN
    out['heftruck-huren'] = page('heftruck-huren',
        'Heftruck huren | B-Spaansen Wieringerwerf',
        'Heftruck huren? Bij B-Spaansen in Wieringerwerf is verhuur mogelijk in overleg, van een korte periode tot langer. Vraag beschikbaarheid en voorwaarden aan.',
        'Heftruck huren', 'in overleg', 'Verhuur voor korte of langere periode · beschikbaarheid en voorwaarden in overleg',
        f'''<div class="answer"><strong>Waar kan ik een heftruck huren?</strong> Bij B-Spaansen Heftrucks in Wieringerwerf is een heftruck huren mogelijk in overleg, voor een korte of langere periode. Vraag via <a href="{wa('Hallo, ik wil een heftruck huren. Periode en type: ')}" target="_blank" rel="noopener">WhatsApp</a> of het <a href="/#contact">contactformulier</a> naar actuele beschikbaarheid en voorwaarden.</div>
<h2>Wat geef je door bij een huuraanvraag?</h2>
{li(['Gewenst type (elektrisch, diesel of LPG) en hefvermogen', 'Benodigde hefhoogte en of de machine binnen of buiten werkt', 'Huurperiode', 'Locatie voor levering of ophalen', 'Wie de machine bedient'])}
<h2>Wat heb je nodig om te mogen werken met een gehuurde heftruck?</h2>
<p>Alleen geïnstrueerde bestuurders mogen een heftruck bedienen; de instructie wordt vastgelegd. Voor rijden op de openbare weg is een T-rijbewijs nodig bij heftrucks breder dan 130 cm. Zie ook <a href="{STI}" target="_blank" rel="noopener">Stigas: heftruckinstructie</a>. Controleer ook vooraf de voorwaarden voor verzekering en schade.</p>
<h2>Huren of kopen?</h2><p>Huren past bij een tijdelijke piek of een kortlopend project. Wordt de heftruck langdurig dagelijks ingezet, dan is kopen vaak voordeliger. Bekijk de <a href="/voorraad.html">gebruikte heftrucks uit voorraad</a>.</p>''',
        [('Wat kost het huren van een heftruck?', 'De huurprijs hangt af van type, hefvermogen en huurperiode. Voor een prijs van B-Spaansen: vraag een offerte aan via WhatsApp of het contactformulier.'),
         ('Kan ik een heftruck voor langere tijd huren?', 'Dat kan in overleg. Geef je gewenste periode door, dan bespreken we de mogelijkheden.'),
         ('Kan een gehuurde heftruck worden bezorgd?', 'Transport is bespreekbaar. Vraag naar de mogelijkheden voor jouw locatie.')],
        [('Stigas: heftruckinstructie', STI)], ts)
    # 4. LOKAAL
    out['heftruckdealer-noord-holland'] = page('heftruckdealer-noord-holland',
        'Heftruckdealer Noord-Holland: B-Spaansen in Wieringerwerf',
        'Heftruckdealer in Noord-Holland? B-Spaansen Heftrucks in Wieringerwerf (Wieringermeer): gebruikte heftrucks kopen, verkopen, inruilen en huren in overleg. Bezichtigen op afspraak.',
        'Heftruckdealer', 'Noord-Holland', 'B-Spaansen Heftrucks · Schelphorst 22 A1 · Wieringerwerf',
        f'''<div class="answer"><strong>Waar kan ik een gebruikte heftruck kopen in Noord-Holland?</strong> B-Spaansen Heftrucks zit in Wieringerwerf, in de Wieringermeer in het noorden van Noord-Holland. Je kunt er gebruikte heftrucks kopen, verkopen en inruilen, en huren in overleg. Bezichtigen kan op afspraak.</div>
<h2>Adres en openingstijden</h2>
<p><strong>B-Spaansen In- en Verkoop Heftrucks</strong><br>Schelphorst 22, A1<br>1771 SL Wieringerwerf<br>Telefoon: <a href="tel:+31629061612">+31 6 29061612</a><br>Open: donderdag t/m zondag, 08:00 tot 19:00</p>
<div class="btns"><a class="btn" href="https://www.google.com/maps/dir/?api=1&destination=Schelphorst+22+A1%2C+1771+SL+Wieringerwerf" target="_blank" rel="noopener">Route plannen</a><a class="btn" style="background:#e2e8f0" href="/bezoek-onze-locatie.html">Bekijk de showroom</a></div>
<h2>Wat kun je bij ons doen?</h2>
{li(['<a href="/gebruikte-heftruck-kopen.html">Gebruikte heftruck kopen</a> uit de actuele voorraad','<a href="/heftruck-verkopen-inruilen.html">Heftruck verkopen of inruilen</a>','<a href="/heftruck-huren.html">Heftruck huren</a> in overleg','Een heftruck laten keuren: neem contact op voor de mogelijkheden','Transport door heel Nederland is bespreekbaar'])}
<h2>Actuele voorraad</h2>{stock_cards(ts, 3)}<p><a href="/voorraad.html">Bekijk alle heftrucks in voorraad</a></p>''',
        [('Waar zit B-Spaansen?', 'In Wieringerwerf (Schelphorst 22 A1, 1771 SL), in de Wieringermeer in Noord-Holland.'),
         ('Wanneer kan ik langskomen?', 'Op afspraak, donderdag t/m zondag van 08:00 tot 19:00. Bel of app even vooraf.'),
         ('Leveren jullie ook buiten Noord-Holland?', 'Transport door heel Nederland is bespreekbaar.')],
        [], ts)
    return out

if __name__ == '__main__':
    for slug, h in build().items():
        open(os.path.join(bv.ROOT, slug + '.html'), 'w', encoding='utf-8').write(h)
    print('landing ok')
