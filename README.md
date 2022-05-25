# company-employee-information-system
The application is built using python fastapi and MySql

1. Requirements installations:
pip install uvicorn
pip install fastapi
pip install SQLAlchemy
pip install databases
pip install aiomysql
pip install mysqlclient
pip install beanie
pip install passlib
pip install python-jose
pip install python-multipart

2. Command to run the application: uvicorn main:app --reload

3. The application uses 3 tables namely:
CompanyInfo ---> To store company details.
EmployeeInfo ---> To store employee details.
user ---> To create admin

4. In order to get the bearer token go to the api link: http://127.0.0.1:8000/docs#/Auth/login_login__post
   and enter the admin username and passward. This will generate a JWT token, which you can then use to authenticate your queries.
   
Alternatively you can use Swagger UI instead of Postman for the same API's as it is much more organized.
Link to Swagger UI: http://127.0.0.1:8000/docs

5. In db.py configure the db url as per your credentials.
6. For the table EmployeeInfo, if any record has manager_id 0 thenthat means that emp_id is the head of the company.
