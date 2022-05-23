from fastapi import APIRouter, status, HTTPException, Depends
from schemas import CompanySchema, MyCompanySchema
from typing import List
from db import Company, database
from Token import get_current_user
from schemas import UserSchema

router = APIRouter(
    tags=["Company"]
)


@router.post("/company/", status_code=status.HTTP_201_CREATED, response_model=MyCompanySchema)
async def save_company(company: CompanySchema, current_user: UserSchema = Depends(get_current_user)):
    query = Company.insert().values(name=company.name, industry=company.industry, employees=company.employees,
                                    email=company.email)
    last_record_id = await database.execute(query)
    return {**company.dict(), "id": last_record_id}


@router.get("/company/", status_code=status.HTTP_200_OK, response_model=List[MyCompanySchema])
async def get_all_company(current_user: UserSchema = Depends(get_current_user)):
    query = Company.select()
    return await database.fetch_all(query=query)


@router.get("/company/{id}", status_code=status.HTTP_200_OK, response_model=MyCompanySchema)
async def get_specific_company(c_id: int, current_user: UserSchema = Depends(get_current_user)):
    query = Company.select().where(c_id == Company.c.id)
    my_company = await database.fetch_one(query=query)

    if not my_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return {**my_company}


@router.put("/company/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=MyCompanySchema)
async def update_company(c_id: int, company: CompanySchema, current_user: UserSchema = Depends(get_current_user)):
    query = Company.update().where(Company.c.id == c_id).values(name=company.name, industry=company.industry,
                                                                employees=company.employees,
                                                                email=company.email)
    await database.execute(query=query)
    return {**company.dict(), "id": c_id}


@router.delete("/company/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(c_id: int, current_user: UserSchema = Depends(get_current_user)):
    query = Company.delete().where(c_id == Company.c.id)
    await database.execute(query=query)
    return "Company deleted!"
