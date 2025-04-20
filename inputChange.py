import tkinter as tk

def check_for_changes():
    current = entry.get()
    if current != check_for_changes.last_value:
        print("Eingabe verändert:", current)
        check_for_changes.last_value = current
    root.after(100, check_for_changes)

root = tk.Tk()
entry = tk.Entry(root)
entry.pack()

check_for_changes.last_value = ""
check_for_changes()  # Start der Überwachung

root.mainloop()
