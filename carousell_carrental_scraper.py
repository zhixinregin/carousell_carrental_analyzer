from bs4 import BeautifulSoup as bs
import requests
import csv
from csv import writer
from datetime import datetime, timedelta
import schedule
import time

def time_finder():
    global d #let the "d" be used throughtout
    d = datetime.now()
    return(d) #ensure the "d" to be used again in "data_scraper(item)"

#create the excel file
filename = "carouselldata2" + ".csv" #name the excel file
csv_file = open(filename,'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Date(Collected)', 'Time(Collected)', 'Name', 'Car','Price','Likes', 'Bump','Time Posted']) #headers for excel

csv_file.close()

def data_finder(): #"function" to find the data from the website
    global items
    url = "https://www.carousell.sg/categories/cars-32/car-rental-singapore-1181/?sc=1202081422120a0c74696d655f63726561746564120208002a150a0b636f6c6c656374696f6e7322060a04313138313a0408bbe17242037765624a02656e&sort_by=time_created%2Cdescending"
    source = requests.get(url).text #where to get the source from
    soup = bs(source,features="html.parser")
    main = soup.find('main').div.div.div #finding from the 
    items = main.findChildren('div',recursive=False)
    return(items) #to use the "items" again 


def data_scraper(item): #define the "function" of the "data scraper"
        global item_list
        
        likes = item.findChildren('div', recursive=False)[1].button.span.text

        item = item.find_all('div')[0]

        car = item.find_all('a')[1].p.text
        
        name = item.a.find_all('div')[1].p.text

        price = item.find_all('a')[1].find_all('p')[1].text

        bumped = item.a.find_all('div')[1].div.svg

        time = item.a.find_all('div')[1].div.p.text

        numeric_filter = filter(str.isdigit,time) #filtering out the numbers only (step1)

        newtime = int("".join(numeric_filter)) #extract the numbers only (step2)

        datetime_new = d - timedelta(minutes = newtime)

        time_new = datetime_new.strftime('%H:%M')

        date_collect = d.strftime('%d %b %Y')

        time_collect = d.strftime('%H:%M')


        if bumped:
            bump = "yes"
        else:
            bump = "no"

        print(date_collect)
        print(time_collect)
        print(name)
        print(car)
        print(price)
        print(likes)
        print(bump)
        print(time_new)
            
        item_list = [date_collect,time_collect,name,car,price,likes,bump,time_new] #create the "item list" of what it consisits of so the attributes can be used altogether
        
        return(item_list) #to use 

def data_loop():
    for item in items:
        try:
            data_scraper(item) #carry out the feature function of "data_scraper()"
            with open(filename, 'a+', newline='') as write_obj:
                # Create a writer object from csv module
                csv_writer = writer(write_obj)
                # Add contents of list as last row in the csv file
                csv_writer.writerow(item_list)
        except:
            continue
        
def update_function(): #define the function to carry out the function of the "data_finder()", "time_find()" & "data_loop()"
    time_finder()
    data_finder()
    data_loop()


update_function() #apply the function
#schedule.every(10).seconds.do(update_function) #update every x seconds
#schedule.every().minutes.do(update_function) #update every x minutes
#schedule.every().hour.do(update_function) #update every hour
schedule.every().day.at("08:00").do(update_function)
schedule.every().day.at("09:00").do(update_function)
schedule.every().day.at("10:00").do(update_function)
schedule.every().day.at("11:00").do(update_function)
schedule.every().day.at("12:00").do(update_function)
schedule.every().day.at("13:00").do(update_function)
schedule.every().day.at("14:00").do(update_function)
schedule.every().day.at("15:00").do(update_function)
schedule.every().day.at("16:00").do(update_function)
schedule.every().day.at("17:00").do(update_function)
schedule.every().day.at("18:00").do(update_function)
schedule.every().day.at("19:00").do(update_function)
schedule.every().day.at("20:00").do(update_function)
schedule.every().day.at("21:00").do(update_function)

while True:
    schedule.run_pending()
    time.sleep(1)


