from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import  ImageTk
from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill, Font, Alignment

class GUI:
    def __init__(self, root):
        background_color = "#1E1E1E"
        text_color = "#AAAAAA"
        run_button_color = "#40B85A"
        alert_text_color = "#C24A4A"
        excel_cells_color = "3268A8"
        excel_headers = [
            ("A", "RIF"),
            ("B", "CÉDULA O PASAPORTE"),
            ("C", "NOMBRE"),
            ("D", "DETALLES"),
            ("E", "% RETENCIÓN"),
            ("F", "MENSAJE"),
            ("G", "INTENTOS")
        ]

        self.xlsx_file = ""

        def create_xlsx_file(folder_path):
            wb = Workbook()
            ws = wb.active

            fill = PatternFill(start_color=excel_cells_color, end_color=excel_cells_color, fill_type="solid")
            font = Font(name="Arial", bold=True, color="FFFFFF")
            alignment = Alignment(horizontal="center", vertical="center")

            for col, text in excel_headers:
                cell = ws[f"{col}1"]
                cell.value = text
                cell.fill = fill
                cell.font = font
                cell.alignment = alignment
                ws.column_dimensions[col].width = len(text) + 5

            file_path = folder_path + "/" + "get_rif.xlsx"
            wb.save(file_path)
        
        def check_headers_file(file_path):
            result = True
            wb = load_workbook(file_path)
            ws = wb.active

            for col, text in excel_headers:
                cell = ws[f"{col}1"]
                if cell.value != text:
                    result = False
                    break
            
            wb.close()
            return result

        def file_not_empty(file_path):
            wb = load_workbook(file_path)
            ws = wb.active
            
            rif_cell = ws["A2"]
            cedula_cell = ws["B2"]

            wb.close()
            
            return rif_cell.value != None or cedula_cell.value != None

        def upload_files():
            try:
                file_path = filedialog.askopenfilename(initialdir = "./",
                                                    title = "Select a File",
                                                    filetypes = (("xlsx files",
                                                                    "*.xlsx*"),
                                                                ("xlsx files",
                                                                    "*.xlsx*")))
                if file_path:
                    file_type = file_path.split(".")[-1]
                    if file_type == "xlsx":
                        if file_not_empty(file_path) and check_headers_file(file_path):
                            self.upload_label.config(text="xlsx file selected", fg=text_color)
                            self.xlsx_file = file_path
                        else:
                            self.upload_label.config(text="Headers not there or file empty", fg=alert_text_color)
                    else:
                        self.upload_label.config(text="Not a xlsx file", fg=alert_text_color)
                else:
                    self.upload_label.config(text="Error selecting the xlsx file", fg=alert_text_color)
            except Exception as e:
                print(e)
                self.upload_label.config(text="Error selecting the xlsx file", fg=alert_text_color)

        def select_folder():
            try:
                file_path = filedialog.askdirectory(initialdir = "./")
                create_xlsx_file(file_path)
                self.upload_label.config(text="xlsx file created", fg=text_color)
            except Exception as e:
                print(e)
                self.upload_label.config(text="Error creating xlsx file", fg=alert_text_color)

        def run():
            try:
                if self.xlsx_file != "":
                    self.upload_label.config(text=f"Running function on {self.xlsx_file}", fg=text_color)
                    print(self.xlsx_file)
                else:
                    self.upload_label.config(text="Error running the function", fg=alert_text_color)       
            except:
                self.upload_label.config(text="Error running the function", fg=alert_text_color)

        self.root = root
        self.root.geometry("600x350")
        self.root.config(bg=background_color)

        self.document_icon = ImageTk.PhotoImage(file = "./utils/icons/document_icon.png")
        self.document_button = tk.Button(self.root, image = self.document_icon, bg=background_color, border=0, 
                                        borderwidth=0, highlightthickness=0, activeforeground=background_color,
                                        activebackground=background_color, command=select_folder)
        self.document_button.pack()
        self.document_button.place(x=25, y=26, anchor=CENTER)

        self.upload_icon = ImageTk.PhotoImage(file = "./utils/icons/upload_icon.png") 
        self.upload_button = tk.Button(self.root, image = self.upload_icon, bg=background_color, border=0, 
                                        borderwidth=0, highlightthickness=0, activeforeground=background_color,
                                        activebackground=background_color, command=upload_files)
        self.upload_button.pack()
        self.upload_button.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.upload_label = tk.Label(text="Upload xlsx file...", fg=text_color)
        self.upload_label.configure(bg=background_color)
        self.upload_label.pack()
        self.upload_label.place(in_=self.upload_button, y=100, x=-15)

        self.run_button = tk.Button(text="Run", bg=run_button_color, border=0, borderwidth=0, highlightthickness=0,
                                    width=8, command=run)
        self.run_button.pack()
        self.run_button.place(relx=0.5, rely=0.85, anchor=CENTER)    

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()