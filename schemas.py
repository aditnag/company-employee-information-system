from pydantic import BaseModel


class CompanySchema(BaseModel):
    name: str
    industry: str
    employees: int
    email: str


class MyCompanySchema(BaseModel):
    id: int
    name: str
    industry: str
    employees: int
    email: str

    class Config:
        orm_mode = True


class EmployeeSchema(BaseModel):
    name: str
    phone_no: str
    manager_id: int
    email: str
    company_id: int


class MyEmployeeSchema(BaseModel):
    emp_id: int
    name: str
    phone_no: str
    manager_id: int
    email: str
    company_id: int

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    username: str
    password: str


class MyUserSchema(BaseModel):
    id: int
    username: str


class LoginSchema(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: str | None = None