
import crawler_handler

SHOW_PRINTS = False

Crawler_Handler = crawler_handler.CrawlerHandler("Testing")

found_products = [
                    {    "imageURL" : "http...", 
                         "name" : "Tintmann",
                         "price" : "2,99€ pro kg",
                         "original_link" : "www.."},

                         {"imageURL" : "http...", 
                         "name" : "Saftmeister",
                         "price" : "2,87m²",
                         "original_link" : "www.."},

                           {"imageURL" : "http...", 
                         "name" : "Neuberger",
                         "price" : "3.999€",
                         "original_link" : "www.."},

                           {"imageURL" : "http...", 
                         "name" : "Apfelbert",
                         "price" : "18.90€",
                         "original_link" : "www.."}
               ]

Crawler_Handler.print_message("Start Scraping")
Crawler_Handler.handle(found_products, "apfel")
print("Done")

Crawler_Handler.clean_data()
Crawler_Handler.save_data()
Crawler_Handler.give_infos()

