from sqlalchemy import (Column, Integer, String, Table, MetaData, create_engine, ForeignKey)
from databases import Database
from sqlalchemy.orm import relationship


DATABASE_URL = "mysql://root:*********@localhost/Company"

database = Database(DATABASE_URL)

metadata = MetaData()

engine = create_engine(DATABASE_URL)

Company = Table(
    "CompanyInfo",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("name", String(50)),
    Column("industry", String(100)),
    Column("employees", Integer()),
    Column("email", String(50))
)

Employee = Table(
    "EmployeeInfo",
    metadata,
    Column("emp_id", Integer(), primary_key=True),
    Column("name", String(50)),
    Column("phone_no", String(100)),
    Column("manager_id", Integer()),
    Column("email", String(50)),
    Column("company_id", Integer(), ForeignKey("CompanyInfo.id")),
    company_relation=relationship("CompanyInfo", back_populates="EmployeeInfo")
)

User = Table(
    "user",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("username", String(100)),
    Column("password", String(300)),
)

