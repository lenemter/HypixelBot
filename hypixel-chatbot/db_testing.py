from database.db_session import global_init, create_session
from database.models import *

global_init("database/database.db")
session = create_session()

user = User()
session.add(user)
music = Music(user)
session.add(music)
