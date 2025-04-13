import tkinter as tk # Getting tkinter into the program

root = tk.Tk()
root.title("Note Editor")
root.geometry("1200x600")
#root.state("zoomed") *Not sure to make it zoomed or not yet, but writing it here for referance*

# Create main frame
# (Putting the Text typing area and the scroll bar in the same area)
MainFrame = tk.Frame(root)
MainFrame.pack(pady=5, padx=5, fill="both", expand=True)

#Creating scrollbar
text_scroll =tk.Scrollbar(MainFrame)
text_scroll.pack(side="right", fill="y")

#Creating The Text Area to type
Text_Box = tk.Text(MainFrame, width=90, height=25, font=("Helvetica", 16), selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=text_scroll.set, wrap="word")
Text_Box.pack(pady=20, padx=20, fill="both", expand=True)
text_scroll.config(command=Text_Box.yview)

#Creating Menu Top menu bar
TopMenuBar = tk.Menu(root)
root.config(menu=TopMenuBar)

#Adding in File Menu into the Menu Bar
file_menu = tk.Menu(TopMenuBar, tearoff=False)
TopMenuBar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open")
file_menu.add_command(label="Save")

#Adding editing menu 
edit_menu = tk.Menu(TopMenuBar, tearoff=False)
TopMenuBar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Copy")
edit_menu.add_command(label="Paste")
edit_menu.add_command(label="Undo")
edit_menu.add_command(label="Redo")

#Adding a status bar (For referance)
#Status_bar = tk.Label(root, text="Ready    ", anchor="e")
#Status_bar.pack(fill="x", side="bottom", ipady=5)


root.mainloop()
