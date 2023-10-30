import crawler_handler, os, sys


SHOW_PRINTS = False

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

import scraper.scraper_ALDI_SUED as scraper

Crawler_Handler = crawler_handler.CrawlerHandler("Aldi Süd", with_id = True)

print("Start Scraping")

found_products = scraper.get_products_from_shop()
Crawler_Handler.handle_with_id(found_products)

print("Done")

Crawler_Handler.clean_data()
Crawler_Handler.save_data()
Crawler_Handler.give_infos()