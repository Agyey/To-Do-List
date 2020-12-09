from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
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
        self.show_menu: bool = True
        self.today = datetime.today()
        self.menu_options: OrderedDict = OrderedDict({
            "Today's tasks": "today_tasks",
            "Week's tasks": "week_tasks",
            "All tasks": "show_tasks",
            "Add task": "add_task",
        })

    def today_tasks(self):
        print(f"\nToday {self.today.strftime('%d %b')}:")
        tasks = self.session.query(Table).filter(Table.deadline == self.today.date()).all()
        if tasks:
            for index, task in enumerate(tasks):
                print(f"{index + 1}. {task}. {task.deadline}")
            print()
        else:
            print("Nothing to do!\n")

    def week_tasks(self):
        for i in range(7):
            week_day = (self.today + timedelta(days=i))
            tasks = self.session.query(Table).filter(Table.deadline == week_day.date()).all()
            print(f"\n{week_day.strftime('%A %d %b')}:")
            if tasks:
                for index, task in enumerate(tasks):
                    print(f"{index + 1}. {task}. {task.deadline}")
                print()
            else:
                print("Nothing to do!\n")

    def show_tasks(self):
        print("\nAll tasks:")
        tasks = self.session.query(Table).order_by(Table.deadline).all()
        if tasks:
            for index, task in enumerate(tasks):
                print(f"{index+1}. {task}. {task.deadline.strftime('%d %b')}")
            print()
        else:
            print("Nothing to do!\n")

    def add_task(self):
        description = input("\nEnter task\n")
        deadline = datetime.strptime(input("Enter deadline\n"), "%Y-%m-%d")
        new_row = Table(
            task=description,
            deadline=deadline
        )
        self.session.add(new_row)
        self.session.commit()
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
                print('\nInvalid Choice!\n')
        except ValueError:
            print('\nInvalid Choice!\n')


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

