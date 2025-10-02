from datetime import datetime
import pandas as pd
import csv
import time

df = pd.read_csv('alarms.csv')
time_arr = df["time"].to_list()
message = df["message"].to_list()
triggered = set()

def add_reminder():
    t = input("Enter time HH:MM format")
    m = input("Enter message")

    with open('alarms.csv','a',newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow([t,m])
    
    #since changed
    df = pd.read_csv('alarms.csv')
    global time_arr,message
    time_arr = df["time"].to_list()
    message = df["message"].to_list()
    

def startApp():
    global triggered
    last_min=""
    while True:
        #get time_arr
        now = datetime.now().strftime("%H:%M")
        
        #clear trigger alarms
        if now != last_min:
            triggered.clear()
            last_min = now

        #get arrays from csv
        for i in range(0,len(time_arr)):
            key = (time_arr[i],message[i])
            if(now==time_arr[i]) and key not in triggered:
                print(message[i])
                triggered.add(key)

        time.sleep(1)
        
#add_reminder()
startApp()