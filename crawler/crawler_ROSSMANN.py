import crawler_handler
import scraper_ROSSMANN

Crawler_Handler = crawler_handler.CrawlerHandler("Rossmann", "drogerie")
SHOW_PRINTS = False

Crawler_Handler.print_message("Start Scraping")
for product_to_find in Crawler_Handler.PRODUCTS_TO_CHECK:
     if SHOW_PRINTS:
          print("Searching products for:", product_to_find, ", found: ", end = "")
     found_products = scraper_ROSSMANN.getting_articles_from_shop(product_to_find)
     Crawler_Handler.handle(found_products, product_to_find)
print("Done")

Crawler_Handler.clean_data()
Crawler_Handler.save_data()
Crawler_Handler.give_infos()