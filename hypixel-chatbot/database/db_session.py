import logging
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative


Base = sqlalchemy.ext.declarative.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        logging.error("Необходимо указать файл базы данных.")
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f"sqlite:///{db_file.strip()}?check_same_thread=False"
    logging.debug(f"Подключение к базе данных по адресу {conn_str}")

    engine = sqlalchemy.create_engine(conn_str, echo=False)
    __factory = sqlalchemy.orm.sessionmaker(bind=engine)

    from . import __all_models

    Base.metadata.create_all(engine)


def create_session() -> sqlalchemy.orm.Session:
    global __factory
    return __factory()
