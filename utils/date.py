from datetime import datetime

"""
获得当月的开始时间和结束时间
如：2023-03-01 ----》 2023-04-01
"""


def getDateRange() -> tuple[datetime, datetime]:
    # get the first day of the current month
    today = datetime.today()
    # today = datetime.date(2023,12,23)
    first_day_this_month = datetime(today.year, today.month, 1)

    # get the first day of the next month
    if today.month == 12:
        first_day_next_month = datetime(today.year + 1, 1, 1)
    else:
        first_day_next_month = datetime(today.year, today.month + 1, 1)
    print("First day of the month:", first_day_this_month.strftime("%Y%m%d"))
    print("Last day of the month:", first_day_next_month.strftime("%Y%m%d"))
    return (first_day_this_month.strftime("%Y%m%d"), first_day_next_month.strftime("%Y%m%d"))
# formatted_date = now.strftime("%Y-%m-%d")


if __name__ == "__main__":
    print(getDateRange())
