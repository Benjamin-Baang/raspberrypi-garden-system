from __future__ import annotations
from abc import ABC, abstractmethod
#import sqlite3 as sql
import psycopg2, psycopg2.extras
from config_db import config

class Context:

    _state = None 

    def __init__(self, state: State) -> None:
        self._state = state

    def set_state(self, state: State):

        print(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def request(self):
        return self._state.handle()


class State(ABC):

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def handle(self) -> None:
        pass


class Automated(State):
    def handle(self) -> None:
        # Get user preferences here
#        print("Automated handles request.")
#        print("Automated changes state to Manual.")
#        self.context.set_state(Manual())
        with sql.connect(f'sensors.db') as db:
            db.row_factory = sql.Row
            cursor = db.cursor()
            cursor.execute("select * from user where id=?", (0,))
            default = cursor.fetchone()    
            print(f"Soil: {default['soil']}\n"
                f"Temperature: {default['temperature']}\n"
                f"Humidity: {default['humidity']}\n"
                f"Camera: {default['camera']}\n")
            if values['soil'] < default['soil'] and default['camera'] < user['camera']:
                return True
            elif values['temperature'] < default['temperature'] and values['humidity'] < default['humidity']:
                return True
            else:
                return False
           

        print(f"Soil: {values['soil']}\n"
            f"Temperature: {values['temperature']}\n"
            f"Humidity: {values['humidity']}\n"
            f"Camera: {values['camera']}\n")


class Manual(State):
    def handle(self) -> None:
        with sql.connect(f'sensors.db') as db:
            db.row_factory = sql.Row
            cursor = db.cursor()
            cursor.execute("select * from manual where id=?", (1,))
            user = cursor.fetchone()
            cursor.execute("select * from sensors order by DateTaken desc limit 1")
            values = cursor.fetchone()
            print("User inputs...")
            print(f"Soil: {user['soil']}\n"
                f"Temperature: {user['temperature']}\n"
                f"Humidity: {user['humidity']}\n"
                f"Camera: {user['camera']}\n")
            print("Sensor inputs...")
            print(f"Soil: {values['soil']}\n"
                f"Temperature: {values['temperature']}\n"
                f"Humidity: {values['humidity']}\n"
                f"Camera: {values['camera']}\n")
            if values['soil'] < user['soil'] - 1.5 and values['camera'] < user['camera']:
                return True
            elif values['temperature'] > user['temperature'] + 5 and values['humidity'] < user['humidity'] - 5:
                return True
            else:
                return False


class Scheduler(State):
    def handle(self) -> None:
        print("Scheduler handles request.")
        print("Scheduler changes state to Automated.")
        self.context.set_state(Automated())


if __name__ == "__main__":
    # The client code.

    context = Context(Automated()) 

    with sql.connect(r'sensors.db') as db:
        db.row_factory = sql.Row
        cursor = db.cursor()
        cursor.execute("select * from user where id=?", (1,))
        user = cursor.fetchone()
        if user['State'] == 'automated':
            context.set_state(Automated())
        elif user['State'] == 'manual':
            context.set_state(Manual())
        elif user['State'] == 'scheduler':
            context.set_state(Scheduler())

    print(context.request())
