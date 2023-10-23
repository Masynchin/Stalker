from db import Database
from gui import GUI
from synth import insert


with Database.initialize(":memory:") as db:
    insert(db, 20, 500, 2000, 10000)
    GUI(db).run()
