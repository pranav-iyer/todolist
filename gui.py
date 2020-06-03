from .item import Item, ToDoList
import os
import tkinter as tk
from tkinter import ttk


class GUI():
    "Class for using tkinter to display the GUI version of the app"
    def __init__(self):
        
        #—————————————————————load in saved todolist————————————————————————————
        # change directories to where this script is located, then change back
        old_cwd = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        if os.path.exists("TDL_data.txt"):
            self.todolist = ToDoList.read_file("TDL_data.txt")
        else:
            self.todolist = ToDoList()
        os.chdir(old_cwd)
        #——————————————————————done loading—————————————————————————————————————

        self.main_window = None
        self.tasks = None

        # this controls whether to disply all tasks, or just the incomplete ones
        # shows incomplete tasks by default
        self.view_mode = "incomplete"

        
    def run(self):
        """Main function which sets up the window for the main view of the todo
        list. Can show either all tasks with the view parameter set to "all", or
        by default shows only the incomplete tasks (view="incomplete")
        """
        #————————————————————setup window frame—————————————————————————————————
        self.main_window = tk.Tk()
        self.main_window.title("ToDoList")
        self.main_window.protocol("WM_DELETE_WINDOW", self._save_and_close)
        self.main_window.rowconfigure(0, minsize=20)
        self.main_window.rowconfigure(1, weight=1, minsize=200)
        self.main_window.columnconfigure(0, weight=1, minsize=450)

        # top_options frame will contain all of the action buttons that make
        # up the top row
        top_options = tk.Frame(master=self.main_window)
        top_options.grid(row=0, column=0, sticky='ew')

        # make button for adding a new todo item
        new_button = tk.Button(master=top_options, text="Add a New Item",
            height=1, width=15, command=self.add_new_task_window)
        new_button.pack(side=tk.LEFT, fill=tk.BOTH, padx=0, pady=0)

        #-------------------------view switch button----------------------------
        view_switch_button = tk.Button(master=top_options,
            text="Show All Tasks")
        def view_switch():
            if self.view_mode == 'all':
                self.view_mode = 'incomplete'
                view_switch_button['text'] = 'Show All Tasks'
                self._reload_tasks()

            else:
                self.view_mode = 'all'
                view_switch_button['text'] = 'Show Incomplete Tasks'
                self._reload_tasks()

        view_switch_button.configure(command=view_switch)
        view_switch_button.pack(side=tk.LEFT, fill=tk.BOTH)
        #-----------------------------end view swtich button--------------------
        

        #----------------------------task list----------------------------------

        task_list = tk.Frame(master=self.main_window)
        task_list.grid(row=1, column=0, sticky='nsew')
        task_list.rowconfigure(0, weight=1)
        task_list.columnconfigure(0, weight=1)
        task_list.columnconfigure(1)

        scrollbar = tk.Scrollbar(master=task_list)

        self.tasks = ttk.Treeview(master=task_list, yscrollcommand=scrollbar.set)

        # bind double clicking on a task in the Treeview to mark it as complete
        
        self.tasks.bind('<Double-Button-1>', self._complete_on_double_click)

        scrollbar.configure(command = self.tasks.yview)

        self.tasks['columns'] = ("Task", "Due Date", "Complete?")

        # make all of the columns (four)
        self.tasks.column("#0", width=50, minwidth=50, stretch=tk.NO)
        self.tasks.column("Task", width=350, minwidth=350)
        self.tasks.column("Due Date", width=175, minwidth=175, stretch=tk.NO)
        self.tasks.column("Complete?", width=125, minwidth=125, stretch=tk.NO)

        # configures headings to show at the top of the Treeview
        self.tasks.heading("#0", text="ID", anchor="w")
        self.tasks.heading("Task", text="Task", anchor="w")
        self.tasks.heading("Due Date", text="Due Date", anchor="w")
        self.tasks.heading("Complete?", text="Complete?", anchor="w")

        self._reload_tasks()
        
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tasks.grid(row=0, column=0, sticky='nsew')

        #----------------------------end task list------------------------------


        #———————————————————————end window frame————————————————————————————————
        self.main_window.mainloop()

    def _reload_tasks(self):
        self.tasks.delete(*self.tasks.get_children())
        # add the tasks to the Treeview (either all tasks or only incomplete
        # tasks, depending on the view argument)
        if self.view_mode == "all":
            self.add_all()
        elif self.view_mode == "incomplete":
            self.add_incomplete()
        else:
            raise RuntimeError("view_mode has been set to something other \
than \'incomplete\' or \'all\'")

    def add_incomplete(self):
        """fills self.tasks with only the incomplete tasks in the todolist.
        Most recently due comes up at the top. Overdue items backgrounded in
        red."""
        to_show = self.todolist.get_incomplete()
        for item in to_show:
            vals = item.to_tuple()

            overdue_tag = ""
            if item.is_overdue(): overdue_tag = "overdue"
            self.tasks.insert("", tk.END, text=vals[0], values=vals[1:],
                tags=(overdue_tag, ))
        self.tasks.tag_configure("overdue", background="#f78f86")


    def add_all(self):
        """fills self.tasks with all tasks, complete and incomplete, in the 
        todolist, in order of ID."""
        to_show = self.todolist.items
        to_show.sort(key=lambda x: int(x.id))
        for item in to_show:
            vals = item.to_tuple()
            self.tasks.insert("", tk.END, text=vals[0], values=vals[1:])

    def add_new_task_window(self):
        """Function which displays the pop-up window dialog to add a new task
        to the todo list. Triggered when the button labeled 'Add a New Item' is
        pressed."""
        ntw = tk.Tk()
        ntw.title("Add a New Task")
        ntw.resizable(False, False)
        ntw.columnconfigure(1, minsize=300, weight=1)
        # ntw.grab_set()


        #-----------------------Text and Duedate boxes--------------------------

        text_label = tk.Label(master=ntw, text="Text:")
        text_entry = tk.Entry(master=ntw)

        text_label.grid(row=0, column=0)
        text_entry.grid(row=0, column=1, sticky='ew')

        text_entry.focus_set()


        date_label = tk.Label(master=ntw, text="Due Date:")
        date_entry = tk.Entry(master=ntw)

        date_label.grid(row=1, column=0)
        date_entry.grid(row=1, column=1, sticky='ew')

        # function which, when you press enter in the first box, moves you to
        # the date box
        def done_with_text_entry(_):
            date_entry.focus_set()

        text_entry.bind('<Return>', done_with_text_entry)
        #-----------------------------------------------------------------------

        #--------------------------Add Button-----------------------------------
        def add_to_list(event=None):
            # add a new task to the list with the entered information
            self.todolist.add_item(text_entry.get(), date_entry.get())

            # destroy the pop-up window
            ntw.destroy()

            # redraw the list in the main window
            self._reload_tasks()

        add_button = tk.Button(master=ntw, text="Add Task", command=add_to_list)
        add_button.grid(row=2, column=0, columnspan=2)

        # set so that when you press enter in the date_entry field,
        # it adds the task
        date_entry.bind('<Return>', add_to_list)

        ntw.mainloop()

    def _save_and_close(self):
        """Helper method that is called when the window is closed. Writes the
        current todolist data to a text file called TDL_data.txt"""
        self.todolist.write_to_file("TDL_data.txt")

        self.main_window.destroy()

    def _complete_on_double_click(self, event):
        """Helper method that handles what happens when the user double clicks
        an item. Opens up a new window that confirms whether or not to mark the
        selected item as complete"""
        clicked_item_number = self.tasks.identify('item', event.x, event.y)
        id_to_complete = int(self.tasks.item(clicked_item_number)['text'])
        
        ctw = tk.Tk()
        ctw.title("Complete Task?")
        ctw.resizable(False, False)
        ctw.grab_set()

        are_you_sure = tk.Label(master=ctw, text="Complete Task?")
        are_you_sure.pack(side=tk.TOP)

        def yes_action():
            self.todolist.complete_item(id_to_complete)
            ctw.destroy()
            self._reload_tasks()

        def no_action():
            ctw.destroy()
            self._reload_tasks()


        yes_button = tk.Button(master=ctw, text="Yes", command=yes_action)
        no_button = tk.Button(master=ctw, text="No", command=no_action)
        yes_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        no_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        yes_button.focus_set()

        ctw.mainloop()
