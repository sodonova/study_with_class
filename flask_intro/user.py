from mysqlx import Column
from app import db


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {"extend_existing":True}

    email = db.Column()