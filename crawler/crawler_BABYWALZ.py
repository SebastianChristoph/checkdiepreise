import crawler_handler
import scraper.scraper_BABYWALZ as scraper_BABYWALZ

SHOW_PRINTS = True


Crawler_Handler = crawler_handler.CrawlerHandler(store = "BabyWalz", mapping_cat="babywalz_api", with_id = True)

print("Start Scraping")
found_products = scraper_BABYWALZ.get_products_from_shop()

if found_products != None:
    Crawler_Handler.handle_with_id(found_products, "API")
    print("Done")
    Crawler_Handler.clean_data()
    Crawler_Handler.save_data()
    Crawler_Handler.give_infos()
else:
    print("Aborted")
    Crawler_Handler.save_error_log()