import tkinter as tk
from tkinter import StringVar, messagebox
#git add .
#git commit -m "name"
#git push

root = tk.Tk()
root.title("Todolist")
root.geometry("800x800")

task_label = tk.Label(root, text="task")
task_label.pack()
task_entry = tk.Entry(root, width=100)
task_entry.pack()

def addtask():
        task = task_entry.get()
        if task == "" : 
            messagebox.showerror("task","no task")
        else:
            task_listbox.insert(tk.END, task)
            task_entry.delete(0, tk.END)
def deletetask():
        whichtask = task_listbox.curselection()
        if whichtask:
            task_listbox.delete(whichtask)
        else:
             messagebox.showerror("error","no task selected")

addtask_btn = tk.Button(root, text="Add Task", command=addtask)
addtask_btn.pack()
deltask_btn = tk.Button(root, text="Delete Task", command=deletetask)
deltask_btn.pack()
task_listbox = tk.Listbox(root, width=50, height=20)
task_listbox.pack()


root.mainloop()