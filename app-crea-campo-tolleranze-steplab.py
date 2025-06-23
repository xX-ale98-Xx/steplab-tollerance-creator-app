import tkinter as tk
from tkinter import ttk
from tkintertable import TableCanvas, TableModel
import tkinter.messagebox as mb
from tksheet import Sheet
from PIL import Image, ImageTk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from myStyle import myStyles
import tkinter.filedialog as fd
import os
import sys
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class App:
 
    def __init__(self, root):

        myStyles()

        self.root = root   
        self.serial_obj = None
        self.stop = True
        self.enter = True
        self.zerospringpos = 0
        self.zeropos = 0
        self.arraypos = []
        self.arrayforce = []

        # Create the style object
        self.style = ttk.Style()  

        # Get the screen dimensions for adaptive sizing
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        window_width = int(self.screen_width * 0.8)
        window_height = int(self.screen_height * 0.8)

        # GUI setup with adaptive size
        root.title("Crea Tolleranze")
        root.geometry(f"{window_width}x{window_height}")

        # Configuring columns and rows to expand dynamically
        columnsNum = 6
        rowNum = 7

        for i in range(columnsNum):
            root.grid_columnconfigure(i, weight=1)

        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)
        for i in range(2, rowNum):
            root.grid_rowconfigure(i, weight=2)
        

        """HEADER SECTION"""
        self.headerFrame = ttk.Frame(root, padding=20, style='headerFrame.TFrame', )
        self.headerFrame.grid(row=0, column=0, columnspan=columnsNum, sticky="nsew")

        # Make the header frame expand vertically and horizontally
        self.headerFrame.grid_rowconfigure(0, weight=1)
        self.headerFrame.grid_columnconfigure(0, weight=1)
        self.headerFrame.grid_columnconfigure(1, weight=4)
        self.headerFrame.grid_columnconfigure(2, weight=1)


        # Load the original image
        self.original_image = Image.open(self.resource_path("img/logo_waya-removebg.png"))


        # Get the original dimensions of the image
        original_width, original_height = self.original_image.size

        # Define the new width or height (adjust this as needed)
        self.new_height = int(self.screen_height / 20) # should be adaptive to the screen height this way
        self.aspect_ratio = original_height / original_width

        # Calculate the new height while maintaining the aspect ratio
        self.new_width = int(self.new_height / self.aspect_ratio)

        # Resize the image
        image_resized = self.original_image.resize((self.new_width, self.new_height))

        # Convert the image to a Tkinter-compatible format
        self.logo = ImageTk.PhotoImage(image_resized)

        self.logo_label = ttk.Label(self.headerFrame, image=self.logo, anchor="center", style="headerLabel.TLabel")
        self.logo_label.grid(column=0, row=0, sticky="nswe", padx=5, pady=5)

        # Bind window resize event
        self.root.bind("<Configure>", self.resize_logo)
     
        # ttk.Label(self.headerFrame, image=self.logo, anchor="center", style="headerLabel.TLabel").grid(column=0, row=0, sticky="nswe", padx=5, pady=5)
        ttk.Label(self.headerFrame, text="App Crea Tolleranze", anchor="center", font=("Arial", 16, "bold"), style="headerLabel.TLabel").grid(column=1, row=0, sticky="nswe", padx=5, pady=5)

        root.grid_rowconfigure(1, minsize=2, weight=0)
        
        # Create an orange bottom border
        self.headerBorder = ttk.Frame(root, style="headerBorder.TFrame")
        self.headerBorder.grid(column=0, row=1, columnspan=columnsNum, sticky="nsew")

        """PANED WINDOW FOR THE LOWER SECTION"""
        self.pw = ttk.PanedWindow(root, orient ='horizontal', style="custom.TPanedwindow")
        self.pw.grid(row=2, column=0, rowspan=rowNum-2, columnspan=columnsNum, sticky="nsew")

        """BUTTONS & LABELS SECTION"""
        self.buttonsFrame = ttk.Frame(self.pw, padding=20)
        self.pw.add(self.buttonsFrame, weight=2)

        # Make the buttons frame expand vertically and horizontally
        self.buttonsFrame.grid_rowconfigure(0, weight=1)
        self.buttonsFrame.grid_columnconfigure(0, weight=1)

        self.zerosFrame = ttk.Frame(self.buttonsFrame, style="MyCustomFrame.TFrame")
        self.zerosFrame.grid(row=0, column=0, sticky="nsew")

        # Adjust row weights for better layout
        self.zerosFrame.grid_rowconfigure(0, weight=1)  # Title row
        self.zerosFrame.grid_rowconfigure(1, weight=1)  # Labelframe row
        self.zerosFrame.grid_rowconfigure(2, weight=8, minsize=300)  # Table row
        self.zerosFrame.grid_rowconfigure(3, weight=2)  # Buttons row

        self.zerosFrame.grid_columnconfigure(0, weight=3)
        self.zerosFrame.grid_columnconfigure(1, weight=2)


        self.importLabel = ttk.Label(self.zerosFrame, text="Selezionare file excel da cui importare i dati:", font=("Arial", 14), anchor='w', style="bodyLabel.TLabel")
        self.importLabel.grid(row=0, column=0, sticky="w")
        self.importData = ttk.Button(self.zerosFrame, text='Importa', style="posBtn.TButton", command=self.import_excel_data)
        self.importData.grid(row=0, column=1, sticky="w")

        self.labelImportData = ttk.Labelframe(self.zerosFrame, text='File selezionato:', style="customLabelframe.TLabelframe")
        self.labelImportData.grid(row=1, column=0, columnspan=2, sticky='nsew')

        # Configure the grid in Labelframe to expand
        self.labelImportData.grid_columnconfigure(0, weight=1)  # Allow the Entry to expand
        
        self.importFileName = tk.StringVar()
        self.vel = tk.StringVar()
        self.reb = tk.StringVar()
        self.comp = tk.StringVar()
        self.importFileEntry = ttk.Entry(self.labelImportData, textvariable=self.importFileName, background='lightblue', justify = CENTER, font=("Arial", 14), state='readonly')
        self.importFileEntry.grid(row=0, column=0, padx=(0,0), sticky='nsew')   

        
        self.tframe = ttk.Frame(self.zerosFrame)
        self.tframe.grid(row=2, column=0, columnspan=2, sticky='NSEW')
        self.tframe.grid_rowconfigure(0, weight=1)  # La riga 0 del frame si espande
        self.tframe.grid_columnconfigure(0, weight=1)  # La colonna 0 del frame si espande
        self.sheet = Sheet(
            self.tframe,
            data=[[f"0" for c in range(3)] for r in range(10)],
        )
        self.sheet.enable_bindings()
        self.sheet.headers(["Velocità [mm/s]", "Rimbalzo [N]", "Compressione[N]"])  # Imposta gli headers della tabella

        # Configura le opzioni per adattare larghezza colonne e altezza righe
        self.sheet.set_options(
            expand_sheet_if_paste_too_big=True,  # Espandi se i dati incollati sono grandi
            stretch_columns="all",  # Adatta larghezza colonne
            stretch_rows="all"  # Adatta altezza righe
        )

        self.sheet.grid(row=0, column=0, sticky="nsew")
        self.enable_excel_modified_feedback()

        self.okBtn = ttk.Button(self.zerosFrame, text='Aggiorna', style="startBtn.TButton", command=self.ok_button_action)
        self.okBtn.grid(row=3, column=0)

        self.resetBtn = ttk.Button(self.zerosFrame, text='Reset', style="stopBtn.TButton", command=self.reset_button_action)
        self.resetBtn.grid(row=3, column=1)


        """GRAPH SECTION"""
        self.graphFrame = ttk.Frame(self.pw, style="MyCustomFrame.TFrame", padding=20)
        self.pw.add(self.graphFrame, weight=4)

        # Make the buttons frame expand vertically and horizontally
        self.graphFrame.grid_columnconfigure(0, weight=1)
        self.graphFrame.grid_rowconfigure(0, weight=1)

        # Add buttons
        self.buttonSaveFrame = ttk.Frame(self.graphFrame, style="MyCustomFrame.TFrame")
        self.buttonSaveFrame.grid(row=0, column=0, sticky='NSEW')
        self.buttonSaveFrame.grid_columnconfigure(0, weight=1)
        self.buttonSaveFrame.grid_columnconfigure(1, weight=5)
        self.buttonSaveFrame.grid_rowconfigure(0, weight=1)
        self.buttonSaveFrame.grid_rowconfigure(1, weight=1)  # Labelframe row
        self.buttonSaveFrame.grid_rowconfigure(2, weight=8, minsize=300)  # Table row
        self.buttonSaveFrame.grid_rowconfigure(3, weight=2)


        self.helpLabel = ttk.Label(self.buttonSaveFrame, text='Verificare dati inseriti, poi cliccare su "Crea File .csv"', font=("Arial", 14), anchor='w', style="bodyLabel.TLabel")
        self.helpLabel.grid(row=0, column=0, sticky="w")
        self.saveRepBtn = ttk.Button(self.buttonSaveFrame, text='Crea File .csv', style="reportBtn.TButton", command=self.create_csv_file)
        self.saveRepBtn.grid(row=0, column=1, sticky='')

        self.labelReportNameEntry = ttk.Labelframe(self.buttonSaveFrame, text='Inserire nome file:', style="customLabelframe.TLabelframe")
        self.labelReportNameEntry.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=(15, 0))


        # Configure the grid in Labelframe to expand
        self.labelReportNameEntry.grid_columnconfigure(0, weight=1)  # Allow the Entry to expand
        
        self.reportName = tk.StringVar()
        self.reportNameEntry = ttk.Entry(self.labelReportNameEntry, textvariable=self.reportName, background='lightblue', justify = CENTER, font=("Arial", 14))
        self.reportNameEntry.grid(row=0, column=0, padx=(0,0), sticky='nsew') 


        # Ottieni il colore di sfondo dallo stile personalizzato
        bg_color = self.style.lookup("MyCustomFrame.TFrame", "background")     

        # Add graph
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel("Velocità [mm/s]")
        self.ax.set_ylabel("Forza [N]")
        # Creazione del canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.buttonSaveFrame)
        canvas_widget = self.canvas.get_tk_widget()
        # Imposta il colore di sfondo
        self.fig.patch.set_facecolor(bg_color)
        # Posiziona il grafico
        canvas_widget.grid(row=2, column=0, columnspan=2, sticky='NSEW')


        # Frame vuoto per mantenere corretto layout
        self.voidLbl = ttk.Label(self.buttonSaveFrame, text='', font=("Arial", 16), padding=(30,20), background=bg_color)
        self.voidLbl.grid(row=3, column=0)

        


    def resize_logo(self, event):
        """Dynamically resizes the logo based on window width"""
        self.new_height = max(1, int(root.winfo_height() / 20))  # Adaptive width
        self.new_width = max(1, int(self.new_height / self.aspect_ratio))

        resized_image = self.original_image.resize((self.new_width, self.new_height), Image.LANCZOS)
        self.logo_tk = ImageTk.PhotoImage(resized_image)

        self.logo_label.config(image=self.logo_tk)
        self.logo_label.image = self.logo_tk  # Keep reference
    
    def import_excel_data(self):
        """Handles the 'Importa' button click to import data from an Excel file."""
        # Open a file dialog to select an Excel file
        file_path = fd.askopenfilename(
            title="Seleziona un file Excel",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )

        if not file_path:
            return  # If no file is selected, exit the function

        # Update the importFileName variable with the selected file name
        self.importFileName.set(file_path.split("/")[-1])  # Display only the file name

        try:
            # Read the Excel file using pandas
            df = pd.read_excel(file_path)

            # Extract column headers and data
            data = df.values.tolist()  # Convert DataFrame to a list of lists

            # Update the table with the imported data
            
            self.sheet.set_sheet_data(data)  # Set table data

            # Optionally, store the data for further use
            self.vel = df.iloc[:, 0].tolist()  # First column (velocity)
            self.reb = df.iloc[:, 1].tolist()  # Second column (reb)
            self.comp = df.iloc[:, 2].tolist()  # Third column (comp)

            # Plot the data on the graph
            self.plot_data()

        except Exception as e:
            print(f"Errore durante l'importazione del file: {e}")
    
    def plot_data(self):
        """Plots the imported data on the graph."""
        # Clear the previous plot
        self.ax.clear()

        # Set labels
        self.ax.set_xlabel("Velocità [mm/s]")
        self.ax.set_ylabel("Forza [N]")

        # Plot reb and comp against vel
        self.ax.plot(self.vel, self.reb, label="Reb", marker="o")
        self.ax.plot(self.vel, self.comp, label="Comp", marker="x")

        # Add legend
        self.ax.legend()
        # Refresh the canvas
        self.canvas.draw()

    def create_csv_file(self):
        """Handles the 'Crea File .csv' button click to generate and save a CSV file."""
        # Check if the user has entered a file name
        file_name = self.reportName.get().strip()
        if not file_name:
            mb.showerror("Errore", "Inserire un nome per il file prima di procedere.")
            return

        # Open a file dialog to choose where to save the file
        file_path = fd.asksaveasfilename(
            title="Salva il file CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=file_name
        )

        if not file_path:
            return  # If the user cancels the dialog, exit the function

        try:
            # Get the data from the table
            table_data = self.sheet.get_sheet_data()  # Get a copy of the table data

            # Save the data to a CSV file
            with open(file_path, "w", encoding="utf-8") as file:
                # Write headers
                # headers = self.sheet.headers()
                # file.write("\t".join(headers) + "\n")  # Join headers with tab separator

                # Write table rows
                for row in table_data:
                    file.write("\t".join(map(str, row)) + "\n")  # Join row data with tab separator

            # Show a success message
            mb.showinfo("Successo", f"File salvato correttamente in:\n{file_path}")
        except Exception as e:
            mb.showerror("Errore", f"Si è verificato un errore durante il salvataggio del file:\n{e}")

    def ok_button_action(self):
        """Handles the 'Ok' button click to update the graph with table data."""
        try:
            # Get the data from the table
            table_data = self.sheet.get_sheet_data()

            # Extract columns for the graph
            self.vel = [float(row[0]) for row in table_data if row[0]]  # First column (Velocità)
            self.reb = [float(row[1]) for row in table_data if row[1]]  # Second column (Rimbalzo)
            self.comp = [float(row[2]) for row in table_data if row[2]]  # Third column (Compressione)

            # Plot the data on the graph
            self.plot_data()
        except Exception as e:
            mb.showerror("Errore", f"Si è verificato un errore durante l'aggiornamento del grafico:\n{e}")
        
    def reset_button_action(self):
        """Handles the 'Reset' button click to clear the table, graph, and file name."""
        try:
            # Reset the table with zeros
            self.sheet.set_sheet_data([[0, 0, 0] for _ in range(10)])  # Reset table to zeros

            # Clear the file name
            self.importFileName.set("")  # Clear the file name variable

            # Clear the CSV name input
            self.reportName.set("")  # Clear the CSV name input field

            # Clear the graph
            self.ax.clear()
            self.ax.set_xlabel("Velocità [mm/s]")
            self.ax.set_ylabel("Forza [N]")
            self.canvas.draw()

            # Show a success message
            mb.showinfo("Reset", "La tabella, il grafico e i nomi dei file sono stati resettati.")
        except Exception as e:
            mb.showerror("Errore", f"Si è verificato un errore durante il reset:\n{e}")

    def enable_excel_modified_feedback(self):
        """Enable feedback when the table data is modified."""
        self.sheet.bind("<<SheetCellEdited>>", self.mark_excel_as_modified)

    def mark_excel_as_modified(self, event):
        """Change the label color to red when the table data is modified."""
        try:
            # Create a custom style for the modified entry
            self.style.configure("Modified.TEntry", foreground="red")

            # Apply the custom style to the importFileEntry
            self.importFileEntry.configure(style="Modified.TEntry")
        except Exception as e:
            print(f"Errore durante il cambio colore del label: {e}")

    def resource_path(self, relative_path):
        """ Restituisce il path assoluto al file, funziona anche con PyInstaller """
        try:
            base_path = sys._MEIPASS  # Quando eseguito da exe PyInstaller
        except AttributeError:
            base_path = os.path.abspath(".")  # Durante lo sviluppo

        return os.path.join(base_path, relative_path)
    


if __name__ == "__main__":
    root = ttkb.Window(themename="simplex")
    app = App(root)
    root.mainloop()



