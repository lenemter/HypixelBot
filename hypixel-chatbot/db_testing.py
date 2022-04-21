from database.db_session import global_init, create_session
from database.__all_models import *

global_init("database/database.db")
session = create_session()

# user = User()
# session.add(user)
music = Music(user_id=1)
session.add(music)
session.commit()

print([music.user_id for music in session.query(Music).all()])
