import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sql

def add_task():
    task_string = task_text.get("1.0", "end-1c") 
    if len(task_string) == 0:
        messagebox.showinfo('Error', 'Field is Empty.')
    else:
        tasks.append(task_string)
        the_cursor.execute('insert into tasks values (?)', (task_string,))
        list_update()
        task_text.delete("1.0", "end")  

def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert('end', task)

def delete_task():
    try:
        the_value = task_listbox.get(task_listbox.curselection())
        if the_value in tasks:
            tasks.remove(the_value)
            list_update()
            the_cursor.execute('delete from tasks where title = ?', (the_value,))
    except:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')

def delete_all_tasks():
    message_box = messagebox.askyesno('Delete All', 'Are you sure?')
    if message_box == True:
        while(len(tasks) != 0):
            tasks.pop()
        the_cursor.execute('delete from tasks')
        list_update()

def clear_list():
    task_listbox.delete(0, 'end')

def close():
    print(tasks)
    guiWindow.destroy()

def retrieve_database():
    while(len(tasks) != 0):
        tasks.pop()
    for row in the_cursor.execute('select title from tasks'):
        tasks.append(row[0])

if __name__ == "__main__":
    guiWindow = tk.Tk()
    guiWindow.title("top toDO lista nadrealista")
    guiWindow.geometry("700x450+750+250")  
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#3498db")  

    the_connection = sql.connect('listOfTasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('create table (title text)')

    tasks = []

    header_frame = tk.Frame(guiWindow, bg="#3498db")  
    functions_frame = tk.Frame(guiWindow, bg="#3498db")  
    listbox_frame = tk.Frame(guiWindow, bg="#3498db")  

    header_frame.pack(fill="both")
    functions_frame.pack(side="left", expand=True, fill="both")
    listbox_frame.pack(side="right", expand=True, fill="both")

    header_label = ttk.Label(
        header_frame,
        text="toDO lista",
        font=("Consolas", "30"),
        background="#3498db",  
        foreground="#ffffff"  
    )

    header_label.pack(padx=20, pady=20)

    task_label = ttk.Label(
        functions_frame,
        text="Enter the Task:",
        font=("Consolas", "11", "bold"),
        background="#3498db",  
        foreground="#ffffff"  
    )

    task_label.place(x=30, y=40)

    task_text = tk.Text(
        functions_frame,
        font=("Consolas", "10"),  
        width=40,  
        height=5,  
        background="#ffffff",  
        foreground="#000000"  
    )

    task_text.place(x=30, y=80)  

    add_button = ttk.Button(
        functions_frame,
        text="Add Task",
        width=30,  
        command=add_task,
        style="TButton"  
    )
    del_button = ttk.Button(
        functions_frame,
        text="Delete Task",
        width=30,  
        command=delete_task,
        style="TButton"  
    )
    del_all_button = ttk.Button(
        functions_frame,
        text="Delete All Tasks",
        width=30,  
        command=delete_all_tasks,
        style="TButton"  
    )
    exit_button = ttk.Button(
        functions_frame,
        text="Exit",
        width=30,  
        command=close,
        style="TButton"  
    )

    add_button.place(x=30, y=210)  
    del_button.place(x=30, y=250)
    del_all_button.place(x=30, y=290)
    exit_button.place(x=30, y=330)  

    task_listbox = tk.Listbox(
        listbox_frame,
        width=40,  
        height=13,
        selectmode='SINGLE',
        background="#ffffff",  
        foreground="#000000",  
        selectbackground="#3498db",  
        selectforeground="#ffffff"  
    )

    task_listbox.place(x=10, y=20)

    retrieve_database()
    list_update()

    guiWindow.mainloop()

    the_connection.commit()
    the_cursor.close()
