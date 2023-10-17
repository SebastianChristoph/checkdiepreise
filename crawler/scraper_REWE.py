import subprocess
import json

items = []  # Eine leere Liste, um die Produkte zu sammeln
totalPages = 10  # Ersetzen Sie 10 durch die gewünschte Anzahl der Seiten

pageId = 1  # Startseitennummer

for i in range(2, totalPages + 1):
    # Das cURL-Kommando für die API-Anfrage
    curl_command = (
        f'curl -s "https://mobile-api.rewe.de/api/v3/product-search?searchTerm=*&page={pageId}&sorting=RELEVANCE_DESC&objectsPerPage=250&marketCode=440405&serviceTypes=PICKUP" '
        '-H "Rd-Service-Types: PICKUP" -H "Rd-Market-Id: 440405" -H "User-Agent: curl/7.84.0"'
    )

    # Das cURL-Kommando ausführen und die Ausgabe abrufen
    response = subprocess.run(curl_command, shell=True, capture_output=True, text=True)

    # Den Inhalt der Antwort ausgeben
    print("Response for page", pageId)
    print(response.stdout)

    if response.returncode == 0:
        try:
            # Die Antwort in JSON parsen und die Produkte zur Liste hinzufügen
            products = json.loads(response.stdout)['products']
            items.extend(products)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print(f"Fehler bei der Anfrage. Returncode: {response.returncode}")

    # Inkrementiere die Seitennummer für die nächste Anfrage
    pageId += 1

# Die Liste der Produkte "items" enthält jetzt alle Produkte von den verschiedenen Seiten
