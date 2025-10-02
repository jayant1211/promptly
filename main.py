from customtkinter import *

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
        CTkLabel(self,text="Time",text_color="white").grid(row=0,column=0,padx=20,pady=20,sticky="w")
        CTkLabel(self,text="Message",text_color="white").grid(row=0,column=1,padx=20,pady=20,sticky="w")

        #entries
        CTkEntry(self,placeholder_text="enter time HH:MM",corner_radius=0).grid(row=1,column=0,padx=20,sticky="ew")
        #TODO:variable for time
        CTkEntry(self,placeholder_text="enter message",corner_radius=0).grid(row=1,column=1,padx=20,sticky="ew")
        #TODO:variable for message

        #button
        CTkButton(self,text="Add Reminder",corner_radius=0,fg_color="black",border_color="#FFFFFF",border_width=2).grid(row=1,column=2)

app = App()
app.mainloop()