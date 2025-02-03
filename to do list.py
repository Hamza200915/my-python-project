import sqlite3
import tkinter as tk
from tkinter import messagebox

class Todolistapp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("400x400")
        self.title('To do list')

        self.create_widgets()
        self.load_tasks()

    def create_widgets(self):
        self.task_input = tk.Entry(self, width=30)
        self.task_input.pack(pady=10)

        self.add_task_button = tk.Button(self, text="Add task", command=self.add_task)
        self.add_task_button.pack(pady=5)

        self.task_listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.task_listbox.pack(pady=5)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=5)

        self.delete_task_button = tk.Button(self.button_frame, text="Delete Task", command=self.delete_task)
        self.delete_task_button.grid(row=0, column=0, padx=5)

        self.mark_done_button = tk.Button(self.button_frame, text="Mark as Done", command=self.mark_done)
        self.mark_done_button.grid(row=0, column=1, padx=5)

        self.save_button = tk.Button(self, text="Save", command=self.save_task)
        self.save_button.pack(pady=5)

    def add_task(self):
        task = self.task_input.get()
        if task:
            self.task_listbox.insert(tk.END, task)
            self.task_input.delete(0, tk.END)

    def delete_task(self):
        task_index = self.task_listbox.curselection()
        if task_index:
            self.task_listbox.delete(task_index)

    def save_task(self):
        conn = sqlite3.connect('todo_list.db')
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(tasks)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'completed' not in columns:
            cursor.execute("ALTER TABLE tasks ADD COLUMN completed INTEGER NOT NULL DEFAULT 0")
            conn.commit()

        tasks = self.task_listbox.get(0, tk.END)
        cursor.execute("DELETE FROM tasks")
        conn.commit()

        for task in tasks:
            completed = 1 if task.startswith("✓") else 0
            task_text = task.lstrip("✓ ")
            cursor.execute("INSERT INTO tasks (task, completed) VALUES (?, ?)", (task_text, completed))

        conn.commit()
        conn.close()
        messagebox.showinfo("Saved", "Tasks saved successfully!")

    def load_tasks(self):
        conn = sqlite3.connect('todo_list.db')
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT NOT NULL, completed INTEGER NOT NULL DEFAULT 0)")
        conn.commit()

        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()

        for task in tasks:
            task_text, completed = task[1], task[2]
            task_display = "✓ " + task_text if completed else task_text
            self.task_listbox.insert(tk.END, task_display)

        conn.close()

    def mark_done(self):
        task_index = self.task_listbox.curselection()
        if task_index:
            task = self.task_listbox.get(task_index)
            if task.startswith("✓"):
                new_task = task[2:]
            else:
                new_task = "✓ " + task
            self.task_listbox.delete(task_index)
            self.task_listbox.insert(task_index, new_task)

if __name__ == "__main__":
    app = Todolistapp()
    app.mainloop()
