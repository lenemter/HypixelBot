from pprint import pprint

from database.__all_models import *
from database.db_session import create_session, global_init

global_init("database/database.db")
session = create_session()

user = User(id=-1)
session.add(user)
music = Music(user_id=user.id, title="Aria math")
session.add(music)
session.commit()


print(session.query(Music).first().user)
