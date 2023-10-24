import crawler_handler
import scraper.scraper_KAUFLAND_API as scraper_KAUFLAND_API

SHOW_PRINTS = True
MAX_PAGE_ITERATIONS = 10
Crawler_Handler = crawler_handler.CrawlerHandler(store = "KAUFLAND", mapping_cat="kaufland_api", with_id = True)

current = 0

print("Start Scraping")

for product_to_find in Crawler_Handler.PRODUCTS_TO_CHECK:
    if SHOW_PRINTS:
        print("______________________________________________")
        print(current, "of", len(Crawler_Handler.mapping))
        print("Searching products for:", product_to_find, " >> Scrape", MAX_PAGE_ITERATIONS," pages per keyword")
    found_products = scraper_KAUFLAND_API.fetch(product_to_find, max_page_iteration = MAX_PAGE_ITERATIONS)
    Crawler_Handler.handle_with_id(found_products, product_to_find)
    current += 1

print("Done")

Crawler_Handler.clean_data()
Crawler_Handler.save_data()
Crawler_Handler.give_infos()