from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from collections import OrderedDict
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


class ToDoList:

    def __init__(self, session):
        self.session = session
        self.tasks = session.query(Table).all()
        self.show_menu: bool = True
        self.menu_options: OrderedDict = OrderedDict({
            "Today's tasks": "show_tasks",
            "Add task": "add_task",
        })

    def show_tasks(self):
        print("\nToday:")
        if self.tasks:
            for task in self.tasks:
                print(f"{task.id}. {task}")
            print()
        else:
            print("Nothing to do!\n")

    def add_task(self):
        description = input("\nEnter task\n")
        new_row = Table(
            task=description,
            deadline=datetime.today()
        )
        self.session.add(new_row)
        self.session.commit()
        self.tasks = self.session.query(Table).all()
        print("The task has been added!\n")

    def menu(self):
        for index, option in enumerate(self.menu_options):
            print(f"{index+1}) {option}")
        print("0) Exit")
        try:
            choice = int(input())
            if choice == 0:
                print("\nBye!")
                self.show_menu = False
            elif 0 < choice <= len(self.menu_options):
                operation = list(self.menu_options.values())[choice-1]
                getattr(self, operation)()
            else:
                print('Invalid Choice!')
        except:
            print('Invalid Choice!')


# Create Database
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
# Create Tables
Base.metadata.create_all(engine)
# Create Session (connection to Database)
Session = sessionmaker(bind=engine)
# Create todolist and start the menu
todolist = ToDoList(Session())
while todolist.show_menu:
    todolist.menu()

