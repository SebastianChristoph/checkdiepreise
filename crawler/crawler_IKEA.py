import crawler_handler
import scraper_IKEA

SHOW_PRINTS = False

Crawler_Handler = crawler_handler.CrawlerHandler("IKEA", "ikea", with_id = True)

print("Start Scraping")

found_products = scraper_IKEA.get_products_from_shop()
Crawler_Handler.handle_with_id(found_products, "API")

print("Done")

Crawler_Handler.clean_data()
Crawler_Handler.save_data()
Crawler_Handler.give_infos()