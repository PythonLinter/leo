from sqlalchemy import create_engine, Column, String, Integer, Unicode, Text, Index, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from restfulpy.orm import FullTextSearchMixin, Field, to_tsvector

db_string = "postgresql://postgres:postgres@localhost/baghali"
db = create_engine(db_string, echo=True)
DeclarativeBase = declarative_base()


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


Session = sessionmaker(db)
session = Session()
# session.execute('CREATE EXTENSION pg_trgm;')
# session.commit()

DeclarativeBase.metadata.create_all(db)


if __name__ == '__main__':
    # Create
    # noinspection PyArgumentList
    # session.add(
    #     Person(first_name='mohammad', last_name='borghei', description='python developer in backend team')
    # )
    # session.commit()

    people = session.query(Person)
    for person in people:
        print(person.first_name)


