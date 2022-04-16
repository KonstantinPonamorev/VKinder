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

    def insert_user(self, user_info):
        '''Добавление нового пользователя'''

        self.ins_user = insert(user)
        self.connection.execute(self.ins_user, user_info)

    def insert_match(self, match_info, user_id):
        '''Добавление пар для пользователя'''

        self.ins_match = insert(match)
        self.connection.execute(self.ins_match, match_info)
        self.ins_user_match = insert(user_match)
        self.connection.execute(self.ins_user_match,
                                {'user_id': user_id,
                                 'match_id': match_info['id']}
                                )

    def check_user(self, user_id):
        '''Проверка есть ли пользователь в БД'''

        self.check = select([user]).where(user.c.user_id = user_id)
        exist = self.connection.execute(self.check)
        return exist

    def delete_match(self, user_id):
        '''Удалить отношения с парами для пользователя'''

        self.delete = delete(user_match).where(user_match.c.user_id.like(user_id))
        self.connection.execute(self.delete)


# test_user = {}
# test_user['id'] = 1
# test_user['age'] = 20
# test_user['sex'] = 1
# test_user['city_id'] = 1
#
# db = DataBaseWork(URL)
# db.insert_user(test_user)