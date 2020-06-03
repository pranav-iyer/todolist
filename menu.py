from .item import Item, ToDoList
import sys, os

class Menu():
    "Class for handling the menu display and interface with command line"
    def __init__(self):

        #—————————————————————load in saved todolist————————————————————————————
        # change directories to where this script is located, then change back
        old_cwd = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        if os.path.exists("TDL_data.txt"):
            print("Reading in existing todolist data from TDL_data.txt")
            self.todolist = ToDoList.read_file("TDL_data.txt")
        else:
            self.todolist = ToDoList()
        os.chdir(old_cwd)
        #——————————————————————done loading—————————————————————————————————————


        self.choices = {
            'i': self.show_incomplete,
            'a': self.show_all,
            'n': self.add_task,
            'f': self.find_task,
            'c': self.complete_task,
            'd': self.delete_task,
            'q': self.quit
        }

    def display_menu(self):
        "Prints the list of options to the command line"
        print("""\033[1mTo Do List Options:\033[0m
    i: show incomplete tasks
    a: show all tasks (even completed ones)
    n: add task
    f: find task
    c: mark task as complete
    d: delete task
    q: quit
            """)

    def run(self):
        "Main loop in which the menu runs"
        while True:
            self.display_menu()
            choice = input("Enter option you would like: ")
            if choice not in self.choices.keys():
                print("Invalid Option.")
                continue
            else:
                self.choices[choice]()

    def show_incomplete(self):
        """Displays all of the incomplete tasks in the todo list, sorted by
        their due date"""

        # get terminal length for proper formatting
        terminal_length = os.get_terminal_size()[0]

        # prints a horizontal line
        print('—'*terminal_length)
        print("{0:4}{1:65}{2:18}{3:11}".format("ID", "Item [*** if overdue]", "Due Date", "Complete?"))
        print('-'*terminal_length)

        inc = self.todolist.get_incomplete()
        for i in inc:
            print(i)

        print('—'*terminal_length)

    def show_all(self):
        """Displays all of the tasks, both complete and incomplete, sorted by
        their id"""

        # get terminal length for proper formatting
        terminal_length = os.get_terminal_size()[0]

        # prints a horizontal line
        print('—'*terminal_length)
        print("{0:4}{1:65}{2:18}{3:11}".format("ID", "Item [*** if overdue]", "Due Date", "Complete?"))
        print('-'*terminal_length)

        items = self.todolist.items
        for i in items:
            print(i)

        print('—'*terminal_length)


    def add_task(self):
        """Runs interface to add a new task to the list, prompts the user for 
        the text and due date of item"""

        memo = input("Item text: ")
        duedate = input("Due date [format: yyyy-mm-dd HH:MM]: ")
        self.todolist.add_item(memo, duedate)

    def find_task(self):
        """Prompts user to enter a filter string, and returns all of the tasks,
        complete or not, that match the filter."""

        fil = input("Enter string to search for: ")
        matches = self.todolist.find(fil)

        # get terminal length for proper formatting
        terminal_length = os.get_terminal_size()[0]

        # prints a horizontal line
        print('—'*terminal_length)
        print("{0:4}{1:65}{2:18}{3:11}".format("ID", "Item [*** if overdue]", "Due Date", "Complete?"))
        print('-'*terminal_length)

        for i in matches:
            print(i)

        print('—'*terminal_length)

    def complete_task(self):
        """Prompts user for a task id, and marks the corresponding task as
        complete."""

        id_compl = int(input("Enter id of task to mark as complete: "))
        self.todolist.complete_item(id_compl)

    def delete_task(self):
        """Propts user for a task id, and then permanently deleters the task
        with the given id."""

        id_rem = int(input("Enter id of task to remove: "))
        self.todolist.remove_item(id_rem)


    def quit(self):
        "Saves the task list and quits the program successfully."
        print('saving task list data in TDL_data.txt')
        self.todolist.write_to_file("TDL_data.txt")

        print('quitting....')
        sys.exit(0)
