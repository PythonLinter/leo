import unittest

from sqlalchemy import Integer, Unicode, Text, Index, text, func, desc
from nanohttp import settings
from restfulpy.db import DatabaseManager

from restfulpy.testing import WebAppTestCase
from restfulpy.tests.helpers import MockupApplication
from restfulpy.orm import DeclarativeBase, Field, FullTextSearchMixin, fts_escape, to_tsvector, create_engine, \
    session_factory, setup_schema


class Person(FullTextSearchMixin, DeclarativeBase):
    __tablename__ = 'person'

    id = Field(Integer, primary_key=True)
    first_name = Field(Unicode(50))
    last_name = Field(Unicode(50))
    description = Field(Text)

    __ts_vector__ = to_tsvector(
        first_name, last_name, description
    )

    __table_args__ = (
        Index('idx_person_fts', __ts_vector__, postgresql_using='gin'),
        Index('idx_first_name_trgm', text("first_name gin_trgm_ops"), postgresql_using='gin')
    )

    @classmethod
    def search(cls, expressions, query=None):
        expressions = expressions.replace(' ', '|')
        query = (query or cls.query).filter(
            cls.__ts_vector__.match(expressions)
        )
        return query


class FullTextSearchTestCase(WebAppTestCase):
    application = MockupApplication('MockupApplication', None)
    __configuration__ = '''
    db:
      url: postgresql://postgres:postgres@localhost/baghali
      echo: false
    '''

    @classmethod
    def prepare_database(cls):
        with DatabaseManager() as m:
            m.drop_database()
            m.create_database()

        cls.engine = create_engine(echo=True)
        cls.session = session = session_factory(bind=cls.engine, expire_on_commit=False)
        cls.session.execute('CREATE EXTENSION pg_trgm;')
        session.commit()
        setup_schema(session)
        session.commit()

    @classmethod
    def configure_app(cls):
        cls.application.configure(force=True)
        settings.merge(cls.__configuration__)

    @classmethod
    def tearDownClass(cls):
        pass


    @classmethod
    def mockup(cls):
        # noinspection PyArgumentList
        cls.session.add(
            Person(first_name='mohammad', last_name='borghei', description='python developer in backend team')
        )
        # noinspection PyArgumentList
        cls.session.add(
            Person(first_name='mehdi', last_name='aali', description='mehdi is perfect')
        )
        # noinspection PyArgumentList
        cls.session.add(
            Person(first_name='mohammad hasan', last_name='vakili', description='This is a test description')
        )

        cls.session.commit()

    def test_search_results(self):
        result = Person.search('ali')
        similarity_result = Person.query.filter(Person.first_name % 'mohammad').all()
        similarity_result = Person.query.order_by(desc(func.similarity(Person.first_name, 'mhmd'))).first()
        similarity_result = Person.query.order_by(desc(func.similarity(Person.first_name, 'oh'))).first()



        a = 10


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
