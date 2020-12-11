import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from faker import Faker

faker = Faker()


Base = declarative_base()


class Person(Base):
    __tablename__ = "person"
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Address(Base):
    __tablename__ = "address"
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    street_number = Column(String(250))
    street_name = Column(String(250))
    city = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey("person.id"))
    person = relationship("Person", backref="address")

    def __str__(self) -> str:
        return f"{self.street_number} {self.street_name}, {self.post_code} {self.city}"
    
    def __repr__(self) -> str:
        return self.__str__()

from sqlalchemy.event import listens_for

@listens_for(Person, "after_insert")
def insert_order_to_printer(mapper, connection, target):
    print(f"\tEvent: Person '{target.name}' was inserted in the DB")
    

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine("sqlite:///sqlalchemy_db.db")

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Insert a Person in the person table
new_person = Person(name=faker.name())
session.add(new_person)
session.commit()

# Insert an Address in the address table
new_address = Address(
    street_number=faker.building_number(),
    street_name=faker.street_name(),
    city=faker.city(),
    post_code=faker.postcode(),
    person=new_person,
)
session.add(new_address)
session.commit()

people = session.query(Person).all()
for p in people:
    print(p.id, p.name, " - ", p.address[0])