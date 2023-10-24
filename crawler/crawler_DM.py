import crawler_handler
import scraper.scraper_DM as scraper_DM
import time

SHOW_PRINTS = True
MAX_PAGE_ITERATIONS = 10
Crawler_Handler = crawler_handler.CrawlerHandler("DM", "dm", with_id = True)

amount_keys = 0
for key in Crawler_Handler.mapping:
    amount_keys += 1

current = 1

print("Start Scraping")

break_seconds = 45
number_of_requests = 3
break_counter = 0
iterations_of_pages = 5

for iteration in range(1, iterations_of_pages):

    for product_to_find in Crawler_Handler.PRODUCTS_TO_CHECK:
        if SHOW_PRINTS:
            print("______________________________________________")
            print(current, "of", amount_keys, "[ Iteration", iteration,"/", iterations_of_pages, "]")
            print("Searching products for:", product_to_find)
        found_products = scraper_DM.getting_articles_from_shop(product_to_find, iteration)
        Crawler_Handler.handle_with_id(found_products, product_to_find)
        print("...wait 12s")
        time.sleep(12)
        break_counter += 1

        if break_counter == number_of_requests:
            print("\n******************** Cool down for", break_seconds, "seconds\n")
            time.sleep(break_seconds)
            break_counter = 0

        current += 1
    print("DONE ITERATION", iteration)
    current = 1
    print("\n\nWait", break_seconds, "seconds...\n")

print("Done")

Crawler_Handler.clean_data()
Crawler_Handler.save_data()
Crawler_Handler.give_infos()