dates = {
    "08-10-2023": "13.90",
    "09-10-2023": "13.90",
    "10-10-2023": "13.90",
    "07-10-2023": "15.00"
}

sorted_dates = dict(sorted(dates.items(), key=lambda x: x[0]))

print(sorted_dates)