import schedule

def foo():
    print("Fooing around")

schedule.every().day.at("00:00").do(foo)