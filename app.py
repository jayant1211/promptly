from customtkinter import *
import pandas as pd
import csv
import os
from datetime import datetime
import sys

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(application_path, "alarms.csv")

class App(CTk):
    def __init__(self, fg_color = "black"):
        super().__init__(fg_color)

        self.title("Promptly")
        
        #geometry
        self.geometry("800x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=5)

        #labels
        CTkLabel(self,text="Time",text_color="white",font=("Segoe UI",20)).grid(row=0,column=0,padx=20,pady=20,sticky="w")
        CTkLabel(self,text="Message",text_color="white",font=("Segoe UI",20)).grid(row=0,column=1,padx=20,pady=20,sticky="w")

        #entries
        self.time_entry = CTkEntry(self,placeholder_text="enter time HH:MM",corner_radius=0,font=("Segoe UI",16))
        self.time_entry.grid(row=1,column=0,padx=20,sticky="ew")
        self.message_entry = CTkEntry(self,placeholder_text="enter message",corner_radius=0,font=("Segoe UI",16))
        self.message_entry.grid(row=1,column=1,padx=20,sticky="ew")

        #button
        CTkButton(self,text="Add Reminder",command=self.addReminder,corner_radius=0,fg_color="black",border_color="#FFFFFF",border_width=2,font=("Segoe UI", 16)).grid(row=1,column=2)

        #frame to display current list
        CTkLabel(self,text="Reminders List",font=("Segoe UI", 24)).grid(row=2,column=0,padx=20,pady=(50,0),sticky="w")
        self.list_frame = CTkScrollableFrame(self,height=600, corner_radius=0,fg_color="black")
        self.list_frame.grid(row=3, columnspan=2, padx=20, pady=20, sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=2)
        self.list_frame.grid_columnconfigure(1, weight=5)
        self.list_frame.grid_columnconfigure(2, weight=1)
       

        #load reminders
        if(not os.path.exists(csv_path)):
            header = ['time','message']
            with open(csv_path,'w',newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)

        self.df = pd.read_csv(csv_path)
        self.triggered = set()
        self.last = ""
        self.load_reminders() #first instance for loading reminders
        self.check_alarms() #start this, is periodic; every sec
    
    def addReminder(self):
        #TODO:validate time and message(null)
        t = self.time_entry.get()
        m = self.message_entry.get()
        with open(csv_path,'a',newline='\n') as file:
            writer = csv.writer(file)
            writer.writerow([t,m])
        
        self.df = pd.read_csv(csv_path)
        self.time_entry.delete(0, END)
        self.message_entry.delete(0, END)
        self.load_reminders() #refresh reminders
    
    def delete_reminder(self,idx):
        self.df = self.df.drop(idx)
        self.df.to_csv(csv_path,index=False)
        self.load_reminders()

    def load_reminders(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        for idx, row in self.df.iterrows():
            CTkLabel(self.list_frame, text=row['time'], fg_color="black", font=("Segoe UI",12),text_color="white").grid(row=idx, column=0, sticky="w")
            CTkLabel(self.list_frame, text=row['message'], fg_color="black", font=("Segoe UI",12),text_color="white").grid(row=idx, column=1, sticky="w")
            CTkButton(self.list_frame, text="Delete", command=lambda i=idx: self.delete_reminder(i),font=("Segoe UI",12),corner_radius=0, border_color="white",border_width=1,fg_color="black", hover_color="#941E1E", text_color="white").grid(row=idx, column=2,sticky="e")

    def check_alarms(self):
        self.df = pd.read_csv(csv_path)
        now = datetime.now().strftime("%H:%M")
        
        if(self.last!=now):
            self.triggered.clear()
            self.last=now
        
        for i, row in self.df.iterrows():
            key = (row['time'], row['message'])
            if now == row['time'] and key not in self.triggered:
                self.triggered.add(key)
                self.flash_screen(row['message'])
        self.after(1000, self.check_alarms)  # run every second

    def flash_screen(self, msg):
        if hasattr(self, "_overlay") and self._overlay.winfo_exists():
            return  #already displayed
        
        #black overlay
        overlay = CTkToplevel(self)
        self._overlay = overlay
        overlay.attributes("-fullscreen", True)
        overlay.configure(fg_color="black")
        overlay.lift()
        overlay.attributes("-topmost",True)
        #centered message
        label = CTkLabel(overlay, text=msg, font=("Segoe UI", 52), text_color="white", fg_color="black")
        label.pack(expand=True)

        overlay.bind("<Button-1>", lambda e: overlay.destroy())  #any mouse click
        overlay.bind("<Motion>", lambda e: overlay.destroy())    #mouse move/hover
        overlay.bind("<Key>", lambda e: overlay.destroy())       #any key press
        overlay.after(10000, overlay.destroy)

        overlay.focus_set()

app = App()
app.mainloop()