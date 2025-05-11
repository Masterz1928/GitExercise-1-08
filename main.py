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

task_label = tk.Label(input_frame, text="Task")
task_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

task_entry = tk.Entry(input_frame, width=40)
task_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")  

priority_label = tk.Label(input_frame, text="Priority")
priority_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

priority_frame = tk.Frame(input_frame)
priority_frame.grid(row=0, column=3, padx=5, pady=5, sticky="w")

priority_var = StringVar()
priority_var.set("Medium")

tk.Radiobutton(priority_frame, text="High", variable=priority_var, value="High").pack(side="left")
tk.Radiobutton(priority_frame, text="Medium", variable=priority_var, value="Medium").pack(side="left")
tk.Radiobutton(priority_frame, text="Low", variable=priority_var, value="Low").pack(side="left")

def addtask(event = None):
        date = time.strftime("%Y-%m-%d")
        task = task_entry.get()
        priority = priority_var.get()
        if task == "" : 
            messagebox.showerror("task","no task")
        else:     
            task_tree.insert("", "end", values=("☐", date, task, priority), tags=(priority))
            task_entry.delete(0, tk.END)

def deletetask():
        whichtask = task_tree.selection()
        if whichtask:
            task_tree.delete(whichtask)
        else:
             messagebox.showerror("error","no task selected")

completed_task = []

def togglecheckbox(event):
    selected = task_tree.selection()
    if selected:
        for task in selected:
            status = list(task_tree.item(task, "values"))
            if status[0] == "☐":
                status[0] = "☑"
                completed_task.append(status)
                task_tree.delete(task)

completed_tasktree = None

def undo_completedtask(event):
    selected = completed_tasktree.selection()
    if selected:
        for task in selected:
            status = list(completed_tasktree.item(task, "values"))
            if status[0] == "☑":
                status[0] = "☐"
                task_tree.insert("", "end", values=status, tags=status[3])
                completed_tasktree.delete(task)

                for task in completed_task:
                    if task[1:] == status[1:]:  
                        completed_task.remove(task)
                        break

button_frame = tk.Frame(root)
button_frame.pack(pady=10, fill="x")

addtask_btn = tk.Button(button_frame, text="Add Task", command=addtask)
addtask_btn.pack(side="left", padx=10, pady=5) 

deltask_btn = tk.Button(button_frame, text="Delete Task", command=deletetask)
deltask_btn.pack(side="left", padx=10, pady=5)

listbox_frame = tk.Frame(root)
listbox_frame.pack(fill="both", expand=True, padx=10, pady=10)

section = ("status", "Date", "Task", "Priority")
task_tree = ttk.Treeview(listbox_frame, columns=section, show="headings")

task_tree.heading("status", text="Status")
task_tree.column("status", width=50, stretch=tk.NO) 
task_tree.heading("Date", text="Date")
task_tree.column("Date", width=100, stretch=tk.NO)  
task_tree.heading("Task", text="Task")
task_tree.column("Task", width=300, stretch=tk.YES)  
task_tree.heading("Priority", text="Priority")
task_tree.column("Priority", width=100, stretch=tk.NO)

task_tree.pack(fill="both", expand=True)
task_tree.bind("<Double-1>", togglecheckbox)

task_tree.tag_configure("High", background="#ff9999")   
task_tree.tag_configure("Medium", background="#ffff99")  
task_tree.tag_configure("Low", background="#ccffcc")     

task_entry.bind("<Return>", addtask)

def completion_tracker():
    global completed_tasktree
    completiontracker = tk.Toplevel(root)  
    completiontracker.title("Completion Tracker")
    completiontracker.geometry("500x500")
    
    if not completed_task:
        label = tk.Label(completiontracker, text="No completed tasks yet.")
        label.pack(pady=20)
        return
    
    else:
        completed_tasktree = ttk.Treeview(completiontracker, columns=section, show="headings")
        completed_tasktree.heading("status", text="Status")
        completed_tasktree.column("status", width=50, stretch=tk.NO) 
        completed_tasktree.heading("Date", text="Date")
        completed_tasktree.column("Date", width=70, stretch=tk.NO)  
        completed_tasktree.heading("Task", text="Task")
        completed_tasktree.column("Task", width=100, stretch=tk.YES)  
        completed_tasktree.heading("Priority", text="Priority")
        completed_tasktree.column("Priority", width=80, stretch=tk.NO)

        for task in completed_task:
            completed_tasktree.insert("", "end", values=task)

        completed_tasktree.pack(fill="both", expand=True, padx=10, pady=10)
        completed_tasktree.bind("<Double-1>", undo_completedtask)

completion_tracker_btn = tk.Button(button_frame, text="Completion Tracker", command=completion_tracker)
completion_tracker_btn.pack(side="right", padx=10, pady=5)

root.mainloop()