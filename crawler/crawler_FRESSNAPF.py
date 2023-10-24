import crawler_handler
import scraper.scraper_FRESSNAPF as scraper_FRESSNAPF

SHOW_PRINTS = True


Crawler_Handler = crawler_handler.CrawlerHandler(store = "Fressnapf", mapping_cat="fressnapf_api", with_id = True)

print("Start Scraping")
found_products = scraper_FRESSNAPF.get_products_from_shop()

if found_products != None:
    Crawler_Handler.handle_with_id(found_products, "API")
    print("Done")
    Crawler_Handler.clean_data()
    Crawler_Handler.save_data()
    Crawler_Handler.give_infos()
else:
    print("Aborted")
    Crawler_Handler.save_error_log()