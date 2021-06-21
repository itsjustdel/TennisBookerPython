import tkinter as tk
from tkinter import Menu, ttk
from threading import Thread
from typing import Text
import imageLabel
import booker
import os
# this script builds the gui for the whole app

class AsyncBook(Thread):
    def __init__(self, dlbutton):
        super().__init__()
        self.book_button = dlbutton

    def run(self):    
        print (shutdownValue.get())
        booker.start_webdriver(self,usernameBox.get(), passwordBox.get(), shutdownValue.get())

    def setText(self,text):
        self.book_button['text'] =  str(text)

class App(tk.Tk):

    def __init__(self):        
        super().__init__()
        global usernameBox, passwordBox, shutdownValue

        xSize = 356
        ySize = 50 + 256 + 75+ 24 + 24 + 24 + 48 + 48 +48 +48+48

        self.title('Tennis Booker')        
        self.minsize(width=xSize, height=ySize)
        self.resizable(0, 0)
        
        self.create_gif()
        usernameBox = self.create_username_entrybox()        
        passwordBox = self.create_password_entrybox()
        self.create_shutdown_checkbox()
        self.create_location_dropdown()
        self.create_start_time_dropdown()
        self.create_end_time_dropdown()
        self.create_book_button(ySize)
        

    def create_shutdown_checkbox(self):
        global shutdownValue
        shutdownValue = tk.IntVar()
        c = tk.Checkbutton(self, text = "Shutdown after booking",variable= shutdownValue)
        c.place(relx=.5, y=256 + 75+ 24 + 24 + 24 + 48 + 48 +48 +48,width = 256, anchor = 'center')        

    def create_location_dropdown(self):
                
        OPTIONS = [
        "Kelvingove",
        "Knightswood",
        "Queen's Park"
        ] #

        optVariable = tk.StringVar(self)
        optVariable.set("Location") # default value        
        dropDown = tk.OptionMenu(self, optVariable, *OPTIONS)
        dropDown.place(relx=.5, y=256 + 75+ 24 + 24 + 24 + 48,width = 256, anchor = 'center')

    def create_start_time_dropdown(self):
        
        OPTIONS = [
        "09:00","10:00","11:00",
        "12:00","13:00","14:00",
        "15:00","16:00","17:00",
        "18:00","19:00","20:00",
        "21:00","22:00"
        ] #

        optVariable = tk.StringVar(self)
        optVariable.set("Attempt From") # default value        
        dropDown = tk.OptionMenu(self, optVariable, *OPTIONS)
        dropDown.place(relx=.5, y=256 + 75+ 24 + 24 + 24 + 48 + 48,width = 256, anchor = 'center')

    def create_end_time_dropdown(self):
        
        OPTIONS = [
        "09:00","10:00","11:00",
        "12:00","13:00","14:00",
        "15:00","16:00","17:00",
        "18:00","19:00","20:00",
        "21:00","22:00"
        ] #

        optVariable = tk.StringVar(self)
        optVariable.set("Attempt To") # default value        
        dropDown = tk.OptionMenu(self, optVariable, *OPTIONS)
        dropDown.place(relx=.5, y=256 + 75+ 24 + 24 + 24 + 48 + 48 + 48,width = 256, anchor = 'center')
        

    def create_username_entrybox(self):     
        
        # label
        tk.Label(self, text = "Glasgow Live Username",justify='center').place(relx = 0.5, y = 256 + 75,anchor = 'center')
        
        # entry box
        entrybox = tk.Entry(self,justify='center')
        entrybox.place(relx=.5, y= 256 + 75 + 24  ,width = 256, height = 24, anchor = 'center')        
        
        return entrybox

    def create_password_entrybox(self):

        # label/title
        tk.Label(self, text = "Password",justify='center').place(relx = 0.5, y =256 + 75 + 24 + 24,anchor = 'center')       

        #hide characters with bullet point ascii code
        bullet = "\u2022"
        entrybox = tk.Entry(self,justify='center',show=bullet)        
        
        entrybox.place(relx=.5, y=256 + 75+ 24 + 24 + 24,width = 256, height = 24, anchor = 'center')

        return entrybox


    def create_gif(self):
        lbl = imageLabel.ImageLabel(self)
        lbl.pack()
        lbl.load('tennis.gif')

    def create_book_button(self,ySize):
        # download button
        self.book_button = ttk.Button(text='Book')
        self.book_button['command'] = self.handle_book
        self.book_button.place(relx=.5, y=ySize -48, anchor = 'center',height = 48, width = 128)
        

    def handle_book(self):
        
        #grey out if clicked
        self.book_button['state'] = tk.DISABLED
        #change text
        self.book_button['text'] = "Waiting"

        #start process in other thread
        book_thread = AsyncBook(self.book_button )
        book_thread.start()

        #recurring method to check on progress of book method
        self.monitor(book_thread)        

    def monitor(self, thread):
        if thread.is_alive():
            # check the thread every 100ms
            self.after(100, lambda: self.monitor(thread))
        else:
            #self.html.insert(1.0, thread.html)
            self.book_button['state'] = tk.NORMAL

if __name__ == "__main__":
    app = App()
    app.mainloop()