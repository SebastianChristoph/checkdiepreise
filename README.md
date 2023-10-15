# Preischeck WebScraper

## WebScraping

Im Ordner **scraper** befinden sich alle bisherigen Scraper sowie der `crawler_handler` und der `mapper.py`
Die jeweiligen scraper-scripts werden täglich am morgen auf einem Server ausgeführt, auf dem auch Flask gehostet wird.
Wenn du ein scraper-script ausführen willst, benötigst du eine JSON im gleichen Verzeichnis mit folgender Struktur:

```
{ "store": "STORENAME", "products": [] }
```

Ein Produkt in dieser products-Liste ist wie folgt beschrieben:

```
{ "name": "Store-Name", "category": "kategorie", "found_by_keyword" : "keyword", "original_link" : "shoplink", "dates" : { "01-01-2023" : "0.59", "02-01-2023" : 0.58" } }
```

### Beispiel

- hab eine KAUFLAND.json mit dem Inhalt `{ "store": "Kaufland", "products": [] }` im gleichen Verzweichnis wie der Crawler
- starte den Crawler `crawler_kaufland.py`

## Crawler_Handler

Der Crawler_Handler nimmt eine Liste mit Dictionaries mit folgendem Muster entgegen, iteriert darüber und updated/added das Produkt der store-Json (z.B. KAUFLAND.json):

```
product_dict = {"imageURL" : imageURL, "name" : title, "price" : price, "original_link" : original_link}
```

## Mapper

In der `mapper.py` liegt ein Dictionary mit den derzeitigen Mappings bzw Suchbegriffen für die Online-Shops.
**Stell gern einen PullRequest, um dieses Mapping zu erweitern**

## Flask

Zur Visualisierung der Daten wird **Chart.js** und im backend **Flask** genutzt. Alle nötigen routings passieren in der `app.py`

## benötigte Module

Im Projekt werden neben Python-buildin-libs folgende externe imports benötigt:

- BeautifulSoup
- requests
- flask
