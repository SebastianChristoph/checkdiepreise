
import time
t0 = time.time()
print("START EVERYTHING")

import crawler_HELLWEG, crawler_KAUFLAND, crawler_MUELLER, crawler_NETTO, crawler_ROSSMANN


import data_overview

import testing


t1 = time.time()

total_seconds = t1-t0
minutes = int(total_seconds // 60)
seconds = int(total_seconds % 60)
formatted_time = f"{minutes}min, {seconds}s"

print("*****************************************************")
print("MASTER DONE in", formatted_time)