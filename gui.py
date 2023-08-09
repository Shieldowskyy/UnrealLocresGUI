import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import json

class UnrealLocresGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UnrealLocres GUI")

        self.locres_file_path = tk.StringVar()
        self.translation_file_path = tk.StringVar()
        self.output_filename = tk.StringVar(value="output")
        self.format_choice = tk.StringVar(value="csv")
        self.hide_console = tk.BooleanVar(value=False)

        self.load_settings()  # Load settings from config file
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="UnrealLocres GUI", font=("Helvetica", 16)).pack(pady=10)

        tk.Label(self.root, text="Locres File Path:").pack()
        tk.Entry(self.root, textvariable=self.locres_file_path).pack(fill=tk.X)
        tk.Button(self.root, text="Browse", command=self.browse_locres_file).pack()

        tk.Label(self.root, text="Translation File Path:").pack()
        tk.Entry(self.root, textvariable=self.translation_file_path).pack(fill=tk.X)
        tk.Button(self.root, text="Browse", command=self.browse_translation_file).pack()

        tk.Label(self.root, text="Output File Name:").pack()
        tk.Entry(self.root, textvariable=self.output_filename).pack(fill=tk.X)

        tk.Label(self.root, text="Output Format:").pack()
        tk.Radiobutton(self.root, text="CSV", variable=self.format_choice, value="csv").pack(anchor=tk.W)
        tk.Radiobutton(self.root, text="POT", variable=self.format_choice, value="pot").pack(anchor=tk.W)

        tk.Checkbutton(self.root, text="Hide Console", variable=self.hide_console).pack(anchor=tk.W)

        tk.Button(self.root, text="Export", command=self.export).pack(pady=10)
        tk.Button(self.root, text="Import", command=self.import_translation).pack()
        tk.Button(self.root, text="Merge", command=self.merge).pack()

        tk.Label(self.root, text="Export: Export strings from Locres to a translation file.").pack(anchor=tk.W)
        tk.Label(self.root, text="Import: Import translations into the original Locres file.").pack(anchor=tk.W)
        tk.Label(self.root, text="Merge: Merge two Locres files to add additional strings.").pack(anchor=tk.W)

        self.root.geometry("500x600")  # Set initial window size
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Save settings on window close

    def save_settings(self):
        settings = {
            "hide_console": self.hide_console.get()
        }
        with open("settings.json", "w") as file:
            json.dump(settings, file)

    def load_settings(self):
        try:
            with open("settings.json", "r") as file:
                settings = json.load(file)
                self.hide_console.set(settings.get("hide_console", False))
        except FileNotFoundError:
            pass

    def execute_command(self, command):
        if self.hide_console.get():
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        else:
            startupinfo = None

        try:
            subprocess.run(command, shell=True, check=True, startupinfo=startupinfo)
            messagebox.showinfo("Success", "Operation completed successfully.")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "An error occurred while executing the command.")

    def browse_locres_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Locres files", "*.locres")])
        self.locres_file_path.set(file_path)

    def browse_translation_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Translation files", "*.csv *.pot")])
        self.translation_file_path.set(file_path)

    def export(self):
        output_file = os.path.join(os.path.dirname(self.locres_file_path.get()), f"{self.output_filename.get()}.{self.format_choice.get()}")
        command = f'UnrealLocres.exe export "{self.locres_file_path.get()}" -f {self.format_choice.get()} -o "{output_file}"'
        self.execute_command(command)

    def import_translation(self):
        output_file = os.path.join(os.path.dirname(self.locres_file_path.get()), f"{self.output_filename.get()}.{self.format_choice.get()}")
        command = f'UnrealLocres.exe import "{self.locres_file_path.get()}" "{self.translation_file_path.get()}" -f {self.format_choice.get()} -o "{output_file}"'
        self.execute_command(command)

    def merge(self):
        output_file = os.path.join(os.path.dirname(self.locres_file_path.get()), f"{self.output_filename.get()}.{self.format_choice.get()}")
        command = f'UnrealLocres.exe merge "{self.locres_file_path.get()}" "{self.translation_file_path.get()}" -o "{output_file}"'
        self.execute_command(command)

    def on_closing(self):
        self.save_settings()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UnrealLocresGUI(root)
    root.mainloop()
