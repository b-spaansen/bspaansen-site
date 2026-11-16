# Hoe het werkt
Google Sheet (jullie bewerken) → elke 10 min haalt GitHub de lijst op → `voorraad.csv` in de repository wordt bijgewerkt → Cloudflare publiceert automatisch opnieuw.

## Eenmalig
1. Google Sheet: Bestand → Delen → Publiceren op internet → tabblad "Voorraad" → CSV → Publiceren. Kopieer de link.
2. GitHub-repo → Settings → Secrets and variables → Actions → tabblad Variables → New repository variable: naam `SHEET_CSV_URL`, waarde = de link.
3. Cloudflare → Pages → Connect to Git → deze repo (build command leeg, output directory `/`).
4. Actions-tab → "Voorraad synchroniseren" → Run workflow om meteen te testen.

## Dagelijks
Alleen de Google Sheet aanpassen. Foto's: in een Google Drive-map, delen met "Iedereen met de link", link in Foto 1, Foto 2, ...
