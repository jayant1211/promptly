from customtkinter import *
import pandas as pd
import csv

class App(CTk):
    def __init__(self, fg_color = "black"):
        super().__init__(fg_color)

        self.title("Promptly")
        
        #geometry
        self.geometry("800x600")
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=2)
        self.grid_columnconfigure(2,weight=1)

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
        CTkLabel(self,text="Reminders List",font=("Segoe UI", 24)).grid(row=2,column=0,padx=20,pady=(20,0),sticky="w")
        self.list_frame = CTkScrollableFrame(self,height=600, corner_radius=0,fg_color="black")
        self.list_frame.grid(row=3, columnspan=3, padx=20, pady=20, sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(1, weight=2)
        self.list_frame.grid_columnconfigure(2, weight=1)

        #load reminders
        self.df = pd.read_csv('alarms.csv') #TODO:create if does not exist
        self.triggered = set()
        self.load_reminders() #first instance for loading reminders
    
    def addReminder(self):
        #TODO:validate time and message(null)
        t = self.time_entry.get()
        m = self.message_entry.get()
        with open('alarms.csv','a',newline='\n') as file:
            writer = csv.writer(file)
            writer.writerow([t,m])
        
        self.time_entry.delete(0, END)
        self.message_entry.delete(0, END)
        self.load_reminders() #refresh reminders
        
    def load_reminders(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        for idx, row in self.df.iterrows():
            CTkLabel(self.list_frame, text=row['time'], fg_color="black", text_color="white").grid(row=idx, column=0, sticky="w")
            CTkLabel(self.list_frame, text=row['message'], fg_color="black", text_color="white").grid(row=idx, column=1, sticky="w")
            CTkButton(self.list_frame, text="Delete", command=lambda i=idx: self.delete_reminder(i),corner_radius=0, border_color="white",border_width=1,fg_color="black", hover_color="red", text_color="white").grid(row=idx, column=2,sticky="e")

app = App()
app.mainloop()