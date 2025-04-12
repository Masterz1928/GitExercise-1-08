import tkinter as tk # Getting tkinter into the program


root = tk.Tk()
root.title("Note Editor")
#root.state("zoomed") *Not sure to make it zoomed or not yet, but writing it here for referance*

# Create main frame
# (Putting the Text typing area and the scroll bar in the same area)
MainFrame = tk.Frame(root)
MainFrame.pack(pady=5, padx=5)

#Creating scrollbar
text_scroll =tk.Scrollbar(MainFrame)
text_scroll.pack(side="right", fill="y")

#Creating The Text Area to type
Text_Box = tk.Text(MainFrame, width=90, height=25, font=("Helvetica", 16), selectbackground="blue", selectforeground="black", undo=True, yscrollcommand=text_scroll.set, wrap="word")
Text_Box.pack(pady=20, padx=20, ipady=150, ipadx=300)
text_scroll.config(command=Text_Box.yview())


#Creating Menu Bar
TopMenuBar = tk.Menu(root)

root.mainloop()
