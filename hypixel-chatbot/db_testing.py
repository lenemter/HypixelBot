from database.db_session import global_init, create_session
from database.__all_models import *

from pprint import pprint

global_init("database/database.db")
session = create_session()

user = User(id=-1)
session.add(user)
music = Music(user_id=user.id, title="Aria math")
session.add(music)
session.commit()


print(session.query(Music).first().user)
