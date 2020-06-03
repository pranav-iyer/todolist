from datetime import datetime
import os

class Item():
    """Represents an item on the todo list, with text and a due date"""
    def __init__(self, item_id, text, duedate):
        self.text = text

        # parse date into datetime object
        self.duedate = datetime.strptime(duedate, "%Y-%m-%d %H:%M")
        self.is_complete = False

        self.id = item_id

    def complete(self):
        """Marks the task as complete"""
        self.is_complete = True

    def is_overdue(self):
        """Checks if the task is overdue. Once complete a task cannot be
        overdue."""
        if not self.is_complete:
            return ( self.duedate < datetime.now() )
        else:
            return False

    def to_tuple(self):
        """Returns the representation of the item as a tuple, for use in the
        GUI [see gui.py]"""

        complete = ""
        if self.is_complete:
            complete = "complete!"
        else:
            complete = "incomplete"
        return (str(self.id), self.text,
            datetime.strftime(self.duedate,"%Y-%m-%d %H:%M"), complete)

    def __str__(self):
        text_with_overdue = self.text
        if self.is_overdue():
            text_with_overdue = '***' + text_with_overdue
            text_with_overdue += "***"
        out = "{0:4}{1:65}{2:18}".format(str(self.id), text_with_overdue,
            self.duedate.strftime("%Y-%m-%d %H:%M"))
        if self.is_complete: out += 'complete!'
        return out




class ToDoList():
    """Represents a list of Items, that can be searched and modified."""
    def __init__(self):
        self.items = []

    """
    @classmethod
    def from_list(cls, list):
        "Creates a ToDoList object from a list of Items"
        tdl = cls()
        tdl.items = list
        return tdl
    """

    def _get_next_id(self):
        """Returns the id number that should be associated to the next added 
        task. Just gets the maximum id of any item in the list and adds 1"""
        if not self.items:
            return 1
        else:
            return max(self.items, key=lambda x: x.id).id + 1


    def add_item(self,text, duedate, new_id=None):
        """Adds a item into the Todo List, with text, and due date. If no id
        is provided, calculates the id using self._get_next_id(). Returns the
        newly added Item."""
        if not new_id:
            newly_added = Item(self._get_next_id(), text, duedate)
        else:
            newly_added = Item(new_id, text, duedate)
        self.items.append(newly_added)
        return newly_added

    def get_incomplete(self):
        """Returns a list of all of the items that are not yet complete,
        organized by their due date
        """
        incomplete = [i for i in self.items if not i.is_complete]
        incomplete.sort(key=lambda x: x.duedate)
        return incomplete

    def find(self, fil):
        """Searches the todo list for a task matching the filter string"""
        found = [i for i in self.items if fil in i.text]
        found.sort(key=lambda x: x.duedate)
        return found

    def _find_by_id(self, search_id):
        """Returns the ToDo Item which matches the given id"""
        for i in self.items:
            if i.id == search_id:
                return i
        return None

    def modify_item(self, search_id, new_text):
        """Modifies the item with the given id, and returns the changed item"""
        to_change = self._find_by_id(search_id)
        if to_change:
            to_change.text = new_text
            return to_change
        else:
            return None

    def remove_item(self, search_id):
        """Removes the item with the given id"""
        to_remove = self._find_by_id(search_id)
        if to_remove:
            self.items.remove(to_remove)
        else:
            return None

    def complete_item(self, search_id):
        """Marks the item with the given id as complete"""
        to_change = self._find_by_id(search_id)
        to_change.complete()

    def write_to_file(self, filename):
        """Writes the todo list data to the filename given, in a tab-separated
        values format."""
        old_cwd = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        data = [( '\t'.join(x.to_tuple()) + '\n' ) for x in self.items]
        with open(filename, 'w') as f:
            f.writelines(data)
        os.chdir(old_cwd)

    @classmethod
    def read_file(cls, filename):
        """Reads in todo list data from the filename given. Should be in the
        same format as created in ToDoList.write_to_file(self, filename)."""
        tdl = cls()
        with open(filename, 'r') as f:
            text_data = f.readlines()
        # convert text file into an array of tuples, one for each item
        # that has to be added
        data = [tuple(x.split('\t')) for x in text_data]

        for d in data:
            new_item = tdl.add_item(text=d[1], duedate=d[2], new_id=int(d[0]))
            if d[3] == "complete!\n": new_item.complete()

        return tdl


