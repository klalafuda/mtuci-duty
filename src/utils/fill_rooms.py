from sqlmodel import Session, select
from src.database.database import engine
from src.database.models import Room

floors = {2: range(13, 51), 3: range(51, 89), 4: range(89, 127), 5: range(127, 165)}


def fill_rooms():
    with Session(engine) as session:
        count = len(session.exec(select(Room)).fetchall())
        if count > 0:
            print("Таблица Room уже заполнена.")
            return

        for floor, room_range in floors.items():
            for room_number in room_range:
                room = Room(number=room_number, floor=floor)
                session.add(room)

        session.commit()
        print("Таблица Room успешно заполнена!")


if __name__ == "__main__":
    fill_rooms()
