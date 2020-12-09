class ToDoList:

    def __init__(self, tasks=None):
        if tasks is None:
            tasks = list()
        self.tasks: list = tasks

    def show_tasks(self):
        print("Today:")
        for index, task in enumerate(self.tasks):
            print(f"{index+1}) {task}")


all_tasks = [
    "Do yoga",
    "Make breakfast",
    "Learn basics of SQL",
    "Learn what is ORM"
]
todolist = ToDoList(all_tasks)
todolist.show_tasks()
