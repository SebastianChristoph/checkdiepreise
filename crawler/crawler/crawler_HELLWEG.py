import crawler_handler
import os, sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)
import scraper.scraper_HELLWEG as scraper


SHOW_PRINTS = True

Crawler_Handler = crawler_handler.CrawlerHandler("Hellweg", "baumarkt", with_id=True)

Crawler_Handler.print_message("Start Scraping")
for product_to_find in Crawler_Handler.PRODUCTS_TO_CHECK:
     if SHOW_PRINTS:
          print("Searching products for:", product_to_find, ", found: ", end = "")
     found_products = scraper.getting_articles_from_shop(product_to_find)
     Crawler_Handler.handle_with_id(found_products, product_to_find)

print("Done")

Crawler_Handler.clean_data()
Crawler_Handler.save_data()
Crawler_Handler.give_infos()