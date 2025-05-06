import tkinter as tk
from tkinter import StringVar, messagebox, ttk
import time
##from datetime import datetime
#git add .
#git commit -m "name"
#git push

root = tk.Tk()
root.title("Todolist")
root.geometry("800x800")

input_frame = tk.Frame(root)
input_frame.pack(pady=10, fill="x") 

# Task 
task_label = tk.Label(input_frame, text="Task")
task_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

task_entry = tk.Entry(input_frame, width=40)
task_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")  

# Priority 
priority_label = tk.Label(input_frame, text="Priority")
priority_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

priority_var = StringVar()
priority_var.set("Medium")
priority_menu = tk.OptionMenu(input_frame, priority_var, "High", "Medium", "Low")
priority_menu.grid(row=0, column=3, padx=5, pady=5, sticky="w")

def addtask():
        date = time.strftime("%Y-%m-%d")
        task = task_entry.get()
        priority = priority_var.get()
        if task == "" : 
            messagebox.showerror("task","no task")
        else:
            taskWdateNpriority = f"[{priority}] {task} ({date})"       
            task_tree.insert("", "end", values=(date, task, priority))
            task_entry.delete(0, tk.END)
def deletetask():
        whichtask = task_tree.selection()
        if whichtask:
            task_tree.delete(whichtask)
        else:
             messagebox.showerror("error","no task selected")

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

addtask_btn = tk.Button(button_frame, text="Add Task", command=addtask)
addtask_btn.pack(side="left", padx=5)

deltask_btn = tk.Button(button_frame, text="Delete Task", command=deletetask)
deltask_btn.pack(side="left", padx=5)

listbox_frame = tk.Frame(root)
listbox_frame.pack(fill="both", expand=True, padx=10, pady=10)

section = ("Date", "Task", "Priority")
task_tree = ttk.Treeview(listbox_frame, columns=section, show="headings")
for col in section:
    task_tree.heading(col, text=col)
    task_tree.column(col, width=200)

task_tree.pack(fill="both", expand=True)
# Task Listbox
#listbox_frame = tk.Frame(root)
#listbox_frame.pack(fill="both", expand=True, padx=10, pady=10)
#task_listbox = tk.Listbox(listbox_frame)
#task_listbox.pack(fill="both", expand=True)

root.mainloop()