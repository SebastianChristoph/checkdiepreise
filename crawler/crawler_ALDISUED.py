import crawler_handler
import scraper.scraper_ALDI_SUED as scraper_ALDI_SUED

SHOW_PRINTS = False

Crawler_Handler = crawler_handler.CrawlerHandler("ALDISUED", "aldisued", with_id = True)

print("Start Scraping")

found_products = scraper_ALDI_SUED.get_products_from_shop()
Crawler_Handler.handle_with_id(found_products, "API")

print("Done")

Crawler_Handler.clean_data()
Crawler_Handler.save_data()
Crawler_Handler.give_infos()