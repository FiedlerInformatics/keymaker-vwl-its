import tkinter as tk
from tkinter import filedialog

def open_file():
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    if file_path:  # if user selected a file
        print("User selected:", file_path)
        # React here: for example, read file, display content, etc.
        with open(file_path, 'r') as file:
            content = file.read()
            text_area.delete("1.0", tk.END)  # clear previous content
            text_area.insert(tk.END, content)
    else:
        print("No file selected.")

root = tk.Tk()
root.title("File Dialog Example")

open_button = tk.Button(root, text="Open File", command=open_file)
open_button.pack(pady=10)

text_area = tk.Text(root, wrap='word', width=50, height=15)
text_area.pack()

root.mainloop()
