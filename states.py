from __future__ import annotations
from abc import ABC, abstractmethod
import psycopg2, psycopg2.extras
from config_db import config
from datetime import datetime

class Context:

    _state = None 

    def __init__(self, state: State) -> None:
        self._state = state

    def set_state(self, state: State):
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
        print("Automated...\n")
        with psycopg2.connect(**config()) as db: 
            # db.row_factory = sql.Row
            cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
#            cursor.execute("select * from user where id=?", (0,))
            cursor.execute("select * from sensors order by DateTaken desc limit 1")
            values = cursor.fetchone()
            print(f'Soil: {values[0]}\n'
                  f'Temperature: {values[1]}\n'
                  f'Humidity: {values[2]}\n'
                  f'Camera: {values[3]}\n')
            if values[0] < 4 and values[1] > 85 and values[2] < 30 and values[3] > 0.3:
                return True
            else:
                return False


class Manual(State):
    def handle(self) -> None:
        print("Manual...\n")
#        with sql.connect(f'sensors.db') as db:
        with psycopg2.connect(**config()) as db:
#            db.row_factory = sql.Row
            cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
            # cursor.execute("select * from manual where id=?", (1,))
            cursor.execute('select * from manual where id=%s', (1,))
            user = cursor.fetchone()
            cursor.execute("select * from sensors order by DateTaken desc limit 1")
            values = cursor.fetchone()
            print("User inputs...")
            print(f"Soil: {user[1]}\n"
                f"Temperature: {user[2]}\n"
                f"Humidity: {user[3]}\n"
                f"Camera: {user[4]}\n")
            print("Sensor inputs...")
            print(f"Soil: {values[0]}\n"
                f"Temperature: {values[1]}\n"
                f"Humidity: {values[2]}\n"
                f"Camera: {values[3]}\n")
            if values[0] < user[1] - 1.5 and values[3] < user[4]:
                return True
            elif values[1] > user[2] + 5 and values[2] < user[3] - 5:
                return True
            else:
                return False


class Scheduler(State):
    def handle(self) -> None:
        print("Timer...")
        today = datetime.now().strftime('%A')
        c_time = datetime.now().strftime('%H:%M')
        print(f"Today is {today} {c_time}.")
        with psycopg2.connect(**config()) as db:
#            db.row_factory = sql.Row
            cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
            # cursor.execute("select * from manual where id=?", (1,))
            cursor.execute('select * from timer where day=%s', (today,))
            user = cursor.fetchone()
            if user is not None:
                usr_hr_strt, usr_min_strt = [int(n) for n in user[1].split(':')]
                usr_hr_fin, usr_min_fin = [int(n) for n in user[2].split(':')]
                print("User inputs...")
                print(f"Day: {user[0]}\n"
                    f"Start time: {usr_hr_strt}:{usr_min_strt} {user[3]}\n"
                    f"End time: {usr_hr_fin}:{usr_min_fin} {user[4]}\n")
                cur_time = datetime.now().strftime('%H:%M')
                cur_hour, cur_min = [int(n) for n in cur_time.split(':')]
                # cur_ampm = datetime.now().strftime('%p')
                if user[3] in "AMam":
                    if usr_hr_strt == 12:
                        usr_hr_strt -= 12
                else:
                    if usr_hr_strt != 12:
                        usr_hr_strt += 12
                if user[4] in "AMam":
                    if usr_hr_fin == 12:
                        usr_hr_fin -= 12
                else:
                    if usr_hr_fin != 12:
                        usr_hr_fin += 12
                if cur_hour >= usr_hr_strt and cur_hour <= usr_hr_fin:
                    if cur_min >= usr_min_strt:
                        if cur_min < usr_min_fin or usr_min_fin == 0:
                            return True
            return False


class Admin(State):
    def handle(self) -> None:
        print("Admin...")
        with psycopg2.connect(**config()) as db:
            cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('select * from admin_user')
            user = cursor.fetchone()
            if user is not None:
                if user[0]:
                    print("ON\n")
                    return True
                print("OFF\n")
                return False


if __name__ == "__main__":
    # The client code.

    context = Context(Manual()) 

#    with sql.connect(r'sensors.db') as db:
    with psycopg2.connect(**config()) as db:
#        db.row_factory = sql.Row
        cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select * from app_user where id=%s", (1,))
        user = cursor.fetchone()
        print(user)
        if user[1] == 'automated':
            context.set_state(Automated())
        elif user[1] == 'manual':
            context.set_state(Manual())
        elif user[1] == 'timer':
            context.set_state(Scheduler())

    print(context.request())
