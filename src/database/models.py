from sqlalchemy import Column, Integer, String

from .connect import Base


class UserTable(Base):
    __tablename__ = "usertable"

    userid = Column(Integer, primary_key=True, autoincrement=True)
    useremail = Column(String(255), nullable=True)
    client_name = Column(String(100), nullable=False, default="Wind Pioneers")
    first_name = Column(String(100), nullable=True)
