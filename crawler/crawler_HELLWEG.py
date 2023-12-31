import crawler_handler
import scraper.scraper_HELLWEG as scraper_HELLWEG

SHOW_PRINTS = False

Crawler_Handler = crawler_handler.CrawlerHandler("Hellweg", "baumarkt", with_id=True)

Crawler_Handler.print_message("Start Scraping")
for product_to_find in Crawler_Handler.PRODUCTS_TO_CHECK:
     if SHOW_PRINTS:
          print("Searching products for:", product_to_find, ", found: ", end = "")
     found_products = scraper_HELLWEG.getting_articles_from_shop(product_to_find)
     Crawler_Handler.handle_with_id(found_products, product_to_find)

print("Done")

Crawler_Handler.clean_data()
Crawler_Handler.save_data()
Crawler_Handler.give_infos()