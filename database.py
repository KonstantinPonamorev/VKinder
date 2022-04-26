from sqlalchemy import MetaData, Table, String, Integer, Column, ForeignKey, insert, select, delete
import sqlalchemy
from decouple import config



DBDIALECT = config('DBDIALECT', default='')
DBUSERBANE = config('DBUSERBANE', default='')
DBPASSWORD = config('DBPASSWORD', default='')
DBHOST = config('DBHOST', default='')
DBPORT = config('DBPORT', default='')
DBDB = config('DBDB', default='')

URL = f'{DBDIALECT}://{DBUSERBANE}:{DBPASSWORD}@{DBHOST}:{DBPORT}/{DBDB}'


class NewDataBase:
    '''Класс для создания новой БД'''

    def __init__(self, URL):
        '''Определение класса подключение к БД'''

        self.engine = sqlalchemy.create_engine(URL)
        self.connection = self.engine.connect()
        self.metadata = MetaData()
        self.metadata.drop_all(self.engine)

        user = Table('user', self.metadata,
                       Column('id', Integer(), primary_key=True),
                       Column('age', Integer(), nullable=False),
                       Column('sex', Integer, nullable=False),
                       Column('city_id', Integer(), nullable=False)
                        )

        match = Table('match', self.metadata,
                        Column('id', Integer(), primary_key=True),
                        Column('url', String(), nullable=False),
                        Column('photo1_url', String()),
                        Column('photo2_url', String()),
                        Column('photo3_url', String())
                        )

        user_match = Table('user_match', self.metadata,
                            Column('user_id', ForeignKey('user.id')),
                            Column('match_id', ForeignKey('match.id'))
                            )

        self.metadata.create_all(self.engine)



class DataBaseWork:
    '''Класс для работы с БД'''

    def __init__(self, URL):
        '''Определение класса, подключение к БД'''

        self.engine = sqlalchemy.create_engine(URL)
        self.connection = self.engine.connect()
        self.metadata = MetaData()
        self.metadata.drop_all(self.engine)

        self.user = Table('user', self.metadata,
                       Column('id', Integer(), primary_key=True),
                       Column('age', Integer(), nullable=False),
                       Column('sex', Integer, nullable=False),
                       Column('city_id', Integer(), nullable=False)
                       )

        self.match = Table('match', self.metadata,
                      Column('id', Integer(), primary_key=True),
                      Column('url', String(), nullable=False),
                      Column('photo1_url', String()),
                      Column('photo2_url', String()),
                      Column('photo3_url', String())
                      )

        self.user_match = Table('user_match', self.metadata,
                           Column('user_id', ForeignKey('user.id')),
                           Column('match_id', ForeignKey('match.id'))
                           )

    def check_user(self, user_id):
        '''Проверка есть ли пользователь в БД'''

        self.check = select([self.user]).where(self.user.c.id == user_id)
        exist = self.connection.execute(self.check)
        return exist

    def check_match(self, match_id):
        '''Проверка есть ли совпадение в БД'''

        self.check = select([self.match]).where(self.match.c.id == match_id)
        exist = self.connection.execute(self.check)

        return exist

    def insert_user(self, user_info):
        '''Добавление нового пользователя'''

        self.ins_user = insert(self.user)
        self.connection.execute(self.ins_user, user_info)

    def insert_match(self, match_info, user_id):
        '''Добавление пар для пользователя'''

        self.ins_match = insert(self.match)
        self.connection.execute(self.ins_match, match_info)
        self.ins_user_match = insert(self.user_match)
        self.connection.execute(self.ins_user_match,
                                {'user_id': user_id,
                                 'match_id': match_info['id']}
                                )

    def delete_user_match(self, user_id):
        '''Удалить отношения с парами для пользователя'''

        self.delete = delete(self.user_match).where(self.user_match.c.user_id == user_id)
        self.connection.execute(self.delete)

    def delete_match_user(self, match_id):
        '''Удалить отношения с парами для пары'''

        self.delete = delete(self.user_match).where(self.user_match.c.match_id == match_id)
        self.connection.execute(self.delete)

    def delete_user(self, user_id):
        '''Удалить пользователя'''

        self.delete = delete(self.user).where(self.user.c.id == user_id)
        self.connection.execute(self.delete)

    def delete_match(self, match_id):
        '''Удалить пары'''

        self.delete = delete(self.match).where(self.match.c.id == match_id)
        self.connection.execute(self.delete)


