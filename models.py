from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):

    __tablename__ = "Employees"

    auto_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)

class Department(db.Model):

    __tablename__ = "Department"

    auto_id = db.Column(db.Integer,primary_key=True)
    department_id = db.Column(db.String(100),nullable=False,unique=True)
    name = db.Column(db.String(100),nullable=False,unique=True)
    manager = db.Column(db.String(100),nullable=False,unique=True)

class Vacation(db.Model):

    __tablename__ = "Vacations"

    vacation_id = db.Column(db.Integer,primary_key=True)
    employee_id = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    start_date = db.Column(db.Date,nullable=False)
    end_date = db.Column(db.Date,nullable=False)
    date_requested = db.Column(db.Date,nullable=False)
    reason = db.Column(db.String(200),nullable=False)