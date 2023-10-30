import crawler_handler
import os, sys

SHOW_PRINTS = True
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

import scraper.scraper_BABYWALZ as scraper


Crawler_Handler = crawler_handler.CrawlerHandler(store = "Baby Walz", mapping_cat="babywalz_api", with_id = True)

print("Start Scraping")
found_products = scraper.get_products_from_shop()

if found_products != None:
    Crawler_Handler.handle_with_id(found_products, "API")
    print("Done")
    Crawler_Handler.clean_data()
    Crawler_Handler.save_data()
    Crawler_Handler.give_infos()
else:
    print("Aborted")
    Crawler_Handler.save_error_log()