from tkinter import *
import tkinter as tk
from PIL import  ImageTk

class GUI:
    def __init__(self, root):
        background_color = "#1E1E1E"
        text_color = "#AAAAAA"
        run_button_color = "#40B85A"
        alert_text_color = "#C24A4A"

        self.root = root
        self.root.geometry("600x350")
        self.root.config(bg=background_color)

        self.document_icon = ImageTk.PhotoImage(file = "./utils/icons/document_icon.png")
        self.document_button = tk.Button(self.root, image = self.document_icon, bg=background_color, border=0, 
                                        borderwidth=0, highlightthickness=0, activeforeground=background_color,
                                        activebackground=background_color)
        self.document_button.pack()
        self.document_button.place(x=25, y=26, anchor=CENTER)

        self.upload_icon = ImageTk.PhotoImage(file = "./utils/icons/upload_icon.png") 
        self.upload_button = tk.Button(self.root, image = self.upload_icon, bg=background_color, border=0, 
                                        borderwidth=0, highlightthickness=0, activeforeground=background_color,
                                        activebackground=background_color)
        self.upload_button.pack()
        self.upload_button.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.alert_label = tk.Label(text="Was not able to upload the file", fg=alert_text_color)
        self.alert_label.configure(bg=background_color)
        self.alert_label.pack()
        self.alert_label.place(in_=self.upload_button, y=-30, x=-47)

        self.upload_label = tk.Label(text="Upload excel file...", fg=text_color)
        self.upload_label.configure(bg=background_color)
        self.upload_label.pack()
        self.upload_label.place(in_=self.upload_button, y=100, x=-15)

        self.run_button = tk.Button(text="Run", bg=run_button_color, border=0, borderwidth=0, highlightthickness=0,
                                    width=8)
        self.run_button.pack()
        self.run_button.place(relx=0.5, rely=0.85, anchor=CENTER)    

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()