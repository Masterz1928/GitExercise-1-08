import tkinter as tk
from tkinter import StringVar, messagebox, ttk
import time
from datetime import datetime
#git add .
#git commit -m "name"
#git push

root = tk.Tk()
root.title("Todolist")
root.geometry("800x800")

input_frame = tk.Frame(root)
input_frame.pack(pady=10, fill="x") 

#task entry
task_label = tk.Label(input_frame, text="Task")
task_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

task_entry = tk.Entry(input_frame, width=40)
task_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")  

#priority
priority_label = tk.Label(input_frame, text="Priority")
priority_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

priority_frame = tk.Frame(input_frame)
priority_frame.grid(row=0, column=3, padx=5, pady=5, sticky="w")

priority_var = StringVar()
priority_var.set("Medium")

tk.Radiobutton(priority_frame, text="High", variable=priority_var, value="High").pack(side="left")
tk.Radiobutton(priority_frame, text="Medium", variable=priority_var, value="Medium").pack(side="left")
tk.Radiobutton(priority_frame, text="Low", variable=priority_var, value="Low").pack(side="left")

#add task function
def addtask(event = None):
        date = time.strftime("%Y-%m-%d")                                                        #get date
        task = task_entry.get()                                                                 #get task
        priority = priority_var.get()                                                           #get priority
        if task == "" :                                                                         #show no task or not
            messagebox.showerror("task","no task")                                              
        else:                                                                                   
            task_tree.insert("", "end", values=("☐", date, task, priority), tags=(priority))   #add task to list 
            task_entry.delete(0, tk.END)                                                       #delete entry after task added  
        tdl_task()                                                                             #save to txt file
        temp_message("Task marked as completed!")

#delete task function
def deletetask():
        whichtask = task_tree.selection()                                                       #see which task selecred
        if whichtask:                           
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected task?"):
                task_tree.delete(whichtask)
                tdl_task()
                
        else:
             messagebox.showerror("Error","No task selected")                                   #if didnt select task

        tdl_task()                                                                              #update the txt file
        temp_message("Task deleted!", color="red")

completed_task = []                                                                             #list to hold completed tasks

#toggle function
def togglecheckbox(event):
    selected = task_tree.selection()                                                            #get task              
    if selected:
        for task in selected:
            status = list(task_tree.item(task, "values"))                                       #get task data in list 
            if status[0] == "☐":
                status[0] = "☑"
                completed_task.append(status)                                                   #add to completed list
                task_tree.delete(task)                                                          #delete from the task tree list
    
    tdl_task()
    tracker_task()
    temp_message("Task marked as completed!")

completed_tasktree = None                                                                       #global the treeview

#untoggle function
def undo_completedtask(event):
    selected = completed_tasktree.selection()
    if selected:
        for task in selected:
            status = list(completed_tasktree.item(task, "values"))
            if status[0] == "☑":
                status[0] = "☐"
                task_tree.insert("", "end", values=status, tags=status[3])                      #reinsert the task to list with correct values
                completed_tasktree.delete(task)                                                 #delete the task from tracker

                for task in completed_task:
                    if task[1:] == status[1:]:                                                  #compare the task values
                        completed_task.remove(task)                                             #if match then remove it
                        break   
    
    tdl_task()
    tracker_task()
    temp_message("Task restored!", color="red")

button_frame = tk.Frame(root)
button_frame.pack(pady=10, fill="x")

message_label = tk.Label(root, text="", fg="green", font=("Arial", 10))
message_label.pack(pady=(0, 5))

addtask_btn = tk.Button(button_frame, text="Add Task", command=addtask)
addtask_btn.pack(side="left", padx=10, pady=5) 

deltask_btn = tk.Button(button_frame, text="Delete Task", command=deletetask)
deltask_btn.pack(side="left", padx=10, pady=5)

listbox_frame = tk.Frame(root)
listbox_frame.pack(fill="both", expand=True, padx=10, pady=10)
listbox_frame.grid_rowconfigure(0, weight=1)
listbox_frame.grid_columnconfigure(0, weight=1)

section = ("status", "Date", "Task", "Priority")
task_tree = ttk.Treeview(listbox_frame, columns=section, show="headings")

scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=task_tree.yview)
task_tree.configure(yscrollcommand=scrollbar.set)
task_tree.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

task_tree.heading("status", text="Status")
task_tree.column("status", width=50, stretch=tk.NO) 
task_tree.heading("Date", text="Date", command=lambda: sorting(task_tree, "Date", sort_states.get("Date", False)))
task_tree.column("Date", width=100, stretch=tk.NO)  
task_tree.heading("Task", text="Task", command=lambda: sorting(task_tree, "Task", sort_states.get("Task", False)))
task_tree.column("Task", width=300, stretch=tk.YES)  
task_tree.heading("Priority", text="Priority", command=lambda: sorting(task_tree, "Priority", sort_states.get("Priority", False)))
task_tree.column("Priority", width=150, stretch=tk.NO)  

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
    frame = tk.Frame(completiontracker)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    
    if not completed_task:
        label = tk.Label(completiontracker, text="No completed tasks yet.")
        label.pack(pady=20)
        return
    
    else:
        completed_tasktree = ttk.Treeview(frame, columns=section, show="headings")
        completed_tasktree.heading("status", text="Status")
        completed_tasktree.column("status", width=50, stretch=tk.NO) 
        completed_tasktree.heading("Date", text="Date")
        completed_tasktree.column("Date", width=70, stretch=tk.NO)  
        completed_tasktree.heading("Task", text="Task")
        completed_tasktree.column("Task", width=100, stretch=tk.YES)  
        completed_tasktree.heading("Priority", text="Priority")
        completed_tasktree.column("Priority", width=80, stretch=tk.NO)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=completed_tasktree.yview)
        completed_tasktree.configure(yscrollcommand=scrollbar.set)
        completed_tasktree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        for task in completed_task:
            completed_tasktree.insert("", "end", values=task)

        completed_tasktree.bind("<Double-1>", undo_completedtask)

completion_tracker_btn = tk.Button(button_frame, text="Completion Tracker", command=completion_tracker)
completion_tracker_btn.pack(side="right", padx=10, pady=5)


def tdl_task():
    with open ("tdltask.txt", "w", encoding="utf-8") as file:                               
        for task in task_tree.get_children():
            values = task_tree.item(task)["values"]                                                 #get task values
            content = f"{values[0]} | {values[1]} | {values[2]} | {values[3]}\n"                    #split em in |
            file.write(content)

def tracker_task():
    with open ("trackertask.txt", "w", encoding="utf-8") as file:
        for task in completed_task:
            content = f"{task[0]} | {task[1]} | {task[2]} | {task[3]}\n"
            file.write(content)


def load_txt():
    try:
        with open ("tdltask.txt", "r", encoding="utf-8") as file:
            for content in file:
                parts = content.strip().split(" | ")                                                #split content into parts
                if len(parts) == 4:                                                                 #check wheter have 4 parts
                    task_tree.insert("", "end", values=parts, tags=(parts[3]))                      #true then insert all of the values
    except FileNotFoundError:
        pass

    try:
        with open("trackertask.txt", "r", encoding="utf-8") as file:
            for content in file:
                parts = content.strip().split(" | ")
                if len(parts) == 4:
                    completed_task.append(parts)
    except FileNotFoundError:
        pass

sort_states = {}                                                                                    #dict to store sort state

def sorting(tree, col, descending):
    global sort_states
    data = [(tree.set(item, col), item) for item in tree.get_children()]                            #get value and item id list

    if col == "Date":
        data.sort(key=lambda t: datetime.strptime(t[0], "%Y-%m-%d"), reverse=descending)            #convert date string and see wheter ascending or descending

    elif col == "Priority":
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        data.sort(key=lambda t: priority_order.get(t[0].capitalize(), 99), reverse=descending)      #get priority and make sure everything in correct form

    else:
        data.sort(key=lambda t: t[0].lower(), reverse=descending)

    for index, (val, item) in enumerate(data):                                                      #check all index and give all data a index
        tree.move(item, '', index)                                                                  #move it

    for colname in tree["columns"]:
        arrow = ""
        if colname == col:
            arrow = " ↓" if descending else " ↑"
        sort_states[col] = not descending                                              
        tree.heading(colname, text=colname + arrow, command=lambda c=colname: sorting(tree, c, sort_states.get(c, False))) #update the heading

def temp_message(message, color="green"):
    message_label.config(text=message, fg=color)
    root.after(1500, lambda: message_label.config(text=""))

load_txt()
root.mainloop()