import crawler_handler
import scraper_BIOCOMPANY

Crawler_Handler = crawler_handler.CrawlerHandler("Biocompany", "biocompany")
SHOW_PRINTS = False

Crawler_Handler.print_message("Start Scraping")
found_products = scraper_BIOCOMPANY.getting_articles_from_shop()
Crawler_Handler.handle(found_products, "Angebot")
print("Done")

Crawler_Handler.clean_data()
Crawler_Handler.save_data()
Crawler_Handler.give_infos()