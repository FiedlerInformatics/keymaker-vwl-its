import tkinter as tk

def link_geklickt(event):
    print("Klickbarer Text wurde geklickt!")

root = tk.Tk()
root.title("Klickbarer Text")
root.geometry("300x200")

# Label als klickbarer Text
link_label = tk.Label(root,
                      text="Klick mich!",
                      fg="blue",
                      cursor="hand2",
                      font=("Helvetica", 10, "underline"),
                      bg="white")  # ggf. Hintergrund anpassen

link_label.pack(pady=50)

# Klick-Ereignis binden
link_label.bind("<Button-1>", link_geklickt)

root.mainloop()
