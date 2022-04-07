from sqlalchemy import MetaData, Table, String, Integer, Column, ForeignKey, insert
import sqlalchemy



class DataBase:

    def __init__(self):
        self.engine = sqlalchemy.create_engine('postgresql://postgres:postgre@localhost:5432/postgres')
        self.connection = self.engine.connect()
        self.metadata = MetaData()
        self.metadata.drop_all(self.engine)

        user = Table('user', self.metadata,
                       Column('id', Integer(), primary_key=True),
                       Column('age', Integer(), nullable=False),
                       Column('sex', String(), nullable=False),
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

    def insert_user(self, user_info):
        self.ins_user = insert(user)
        self.connection.execute(self.ins_user, user_info)

    def insert_desired(self, match_info, user_id):
        self.ins_match = insert(match)
        self.connection.execute(self.ins_match, match_info)
        self.ins_user_match = insert(user_match)
        self.connection.execute(self.ins_user_match,
                                {'user_id': user_id,
                                 'match_id': match_info['id']}
                                )




# db = DataBase()