import meta as meta
import sqlalchemy as db
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy import null, select
from schemas import UserSchema
from schemas import EmployeeSchema, MyEmployeeSchema
from typing import List
from db import Employee, database, engine
from Token import get_current_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import aliased
from sqlalchemy.sql import alias, select, text

router = APIRouter(
    tags=["Employee"]
)

Session = sessionmaker(bind=engine)
session = Session()


@router.post("/employee/", status_code=status.HTTP_201_CREATED, response_model=MyEmployeeSchema)
async def save_employee(employee: EmployeeSchema, current_user: UserSchema = Depends(get_current_user)):
    query = Employee.insert().values(name=employee.name, phone_no=employee.phone_no, manager_id=employee.manager_id,
                                     email=employee.email, company_id=employee.company_id)
    last_record_id = await database.execute(query)
    return {**employee.dict(), "emp_id": last_record_id}


@router.get("/employee/", status_code=status.HTTP_200_OK, response_model=List[MyEmployeeSchema])
async def get_all_employee(current_user: UserSchema = Depends(get_current_user)):
    query = Employee.select()
    return await database.fetch_all(query=query)


@router.get("/employee/{id}/", status_code=status.HTTP_200_OK, response_model=MyEmployeeSchema)
async def get_specific_employee(e_id: int, current_user: UserSchema = Depends(get_current_user)):
    query = Employee.select().where(e_id == Employee.c.emp_id)
    my_employee = await database.fetch_one(query=query)

    if not my_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return {**my_employee}


@router.put("/employee/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=MyEmployeeSchema)
async def update_employee(id: int, employee: EmployeeSchema, current_user: UserSchema = Depends(get_current_user)):
    query = Employee.update().where(id == Employee.c.emp_id).values(name=employee.name, phone_no=employee.phone_no,
                                                                    manager_id=employee.manager_id,
                                                                    email=employee.email,
                                                                    company_id=employee.company_id)
    await database.execute(query=query)
    return {**employee.dict(), "emp_id": id}


@router.delete("/employee/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(e_id: int, current_user: UserSchema = Depends(get_current_user)):
    query = Employee.delete().where(e_id == Employee.c.emp_id)
    await database.execute(query=query)
    return "Employee deleted!"


@router.get("/emp/{id}/", status_code=status.HTTP_200_OK, response_model=MyEmployeeSchema)
async def get_specific_employee(name: str | None = None, phno: str | None = None, e_id: int | None = None,
                                current_user: UserSchema = Depends(get_current_user)):
    if e_id:
        query = Employee.select().where(e_id == Employee.c.emp_id)
        my_employee = await database.fetch_one(query=query)
        if not my_employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
        return {**my_employee}

    elif name:
        query = Employee.select().where(name == Employee.c.name)
        my_employee = await database.fetch_one(query=query)
        if not my_employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
        return {**my_employee}
    elif phno:
        query = Employee.select().where(phno == Employee.c.phone_no)
        my_employee = await database.fetch_one(query=query)
        if not my_employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
        return {**my_employee}


async def find_subordinates(e_id: int):
    query = Employee.select().where(e_id == Employee.c.manager_id)
    employees = await database.fetch_all(query=query)
    return employees


async def find_manager(e_id: int):
    query1 = Employee.select().where(Employee.c.emp_id == e_id)
    query2 = Employee.select().where(Employee.c.emp_id == query1.c.manager_id)
    manager = await database.fetch_one(query=query2)
    return manager


@router.get("/employee_hierarchy/{id}/", status_code=status.HTTP_200_OK)
async def find_hierarchy(e_id: int, current_user: UserSchema = Depends(get_current_user)):
    subordinates = await find_subordinates(e_id=e_id)
    manager = await find_manager(e_id=e_id)
    if not manager:
        return {"manger": "Head of the company"}
    return subordinates, {**manager}
