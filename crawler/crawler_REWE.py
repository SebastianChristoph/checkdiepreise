import crawler_handler
import scraper.scraper_REWE as scraper_REWE

SHOW_PRINTS = False

Crawler_Handler = crawler_handler.CrawlerHandler("REWE", "rewe", with_id = True)

print("Start Scraping")
found_products = scraper_REWE.getting_articles_from_shop()
Crawler_Handler.handle_with_id(found_products, "API")

print("Done")

Crawler_Handler.clean_data()
Crawler_Handler.save_data()
Crawler_Handler.give_infos()