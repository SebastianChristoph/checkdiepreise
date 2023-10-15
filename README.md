# Preischeck WebScraper

## WebScraping

Im Ordner **scraper** befinden sich alle bisherigen Scraper sowie der `crawler_handler` und der `mapper.py`
Die jeweiligen scraper-scripts werden täglich am morgen auf einem Server ausgeführt, auf dem auch Flask gehostet wird.

Die JSON jedes Stores sieht wie folgt aus:

```
{ "store": "STORENAME", "store_units" : "pro Stk.", "products": [], "historical_labels" : ["01-01-2021", "02-01-2021"] }
```

Ein Produkt in dieser *products*-Liste ist wie folgt beschrieben:

```
{ "name": "Store-Name", "category": "kategorie", "found_by_keyword" : "keyword", "original_link" : "shoplink", "dates" : { "01-01-2023" : "0.59", "02-01-2023" : 0.58" } }
```

## Start Scraper

- starte die crawler_STORENAME.py
- das Ergebnis wird in die STORENAME.json geschrieben

## Crawler_Handler

Der Crawler_Handler nimmt eine Liste mit Dictionaries mit folgendem Muster entgegen, iteriert darüber, bereinigt es und updated/added das Produkt der store-Json (z.B. KAUFLAND.json):

```
product_dict = {"imageURL" : imageURL, "name" : title, "price" : price, "original_link" : original_link}
```

## Mapper

In der `mapper.py` liegt ein Dictionary mit den derzeitigen Mappings bzw Suchbegriffen für die Online-Shops.
**Stell gern einen PullRequest, um dieses Mapping zu erweitern**

## Flask

Zur Visualisierung der Daten wird **Chart.js** und im backend **Flask** genutzt. Der Code ist *nicht* teil dieser Repo.

## benötigte Module

Im Projekt werden neben Python-buildin-libs folgende externe imports benötigt:

- BeautifulSoup
- requests
