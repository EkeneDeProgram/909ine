# Import third party libraries
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Boolean, UniqueConstraint, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Define the database connection and session
connection_string = "sqlite:///909ine.db"
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)
session = Session()

# Create a base class for declarative models
Base = declarative_base()

# Defin users model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, unique=True, nullable=False)
    salt = Column(String, nullable=False)
    logins = relationship("Login", back_populates="user")


    # Initialize the attributes (or properties) of the object
    def __init__(self, username, password, salt):
        self.username = username
        self.password = password
        self.salt = salt


    # Insert user details into database
    def insert(self):
        session.add(self)
        session.commit()


    # Update user deatils in database
    def update(self):
        session.commit()


    # Using __str__() for a human-readable representation
    def __str__(self):
        platform = ", ".join([logs.platform for logs in self.logins])
        email = ", ".join([logs.email for logs in self.logins])
        password = ", ".join([logs.password.decode('utf-8') for logs in self.logins])
        return f"{website}, {email}, {password}"

    # Using __repr__() for unambiguous representation
    def __repr__(self):
        return f"<id: {self.id}, username: {self.username}, password: {self.password}, salt: {self.salt}"


# Defind logins model
class Login(Base):
    __tablename__ = "logins"
    id = Column(Integer, primary_key=True, autoincrement=True)
    platform = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    key = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="logins")



    # Initialize the attributes (or properties) of the object
    def __init__(self, platform, email, password, key, user):
        self.platform = platform
        self.email = email
        self.password = password
        self.key = key
        self.user = user


    # Insert user logins details into database
    def insert(self):
        session.add(self)
        session.commit()


    # Update user logins details in database
    def update(self):
        session.commit()


    # Delete user logins details from database
    def delete(self):
        session.delete(self)
        session.commit()


    # Using __str__() for a human-readable representation
    def __str__(self):
        return f"<website: {self.platform}, email: {self.email},\
                  password {self.password}"


    # Using __repr__() for unambiguous representation
    def __repr__(self):
        return f"<id: {self.id}, website: {self.platform}, \
                  email: {self.email}, password: {self.password},\
                  key: {self.key}, user_id: {self.user_id}>"


# Create the table in the database
Base.metadata.create_all(bind=engine)



