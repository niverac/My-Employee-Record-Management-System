from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Employee
from models import db, Department
from models import db, Vacation
from sqlalchemy import func

app = Flask(__name__)

# MySQL configuration
app.config["SQLALCHEMY_DATABASE_URI"] = ("mysql+pymysql://carevin:060695@localhost:3306/employee_records")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Flask secret key for flash messages
app.config["SECRET_KEY"] = "dev-secret-key"
# Connect SQLAlchemy to Flask
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def dashboard():

    today = func.current_date()

    # Get currently active vacations
    current_vacations = Vacation.query.filter(
        Vacation.start_date <= today,
        Vacation.end_date >= today
    )

    # Get vacation records with employee information
    
    vacations = (
        db.session.query(
        Vacation,
        Employee.department,
        func.concat(
            Employee.first_name,
            " ",
            Employee.last_name
        ).label("name")
        )
        .outerjoin(
        Employee,
        Employee.employee_id == Vacation.employee_id
        )
        .filter(
        Vacation.end_date >= today
        )
        .order_by(Vacation.start_date.asc())
        .limit(5)
        .all()
        )
    # Dashboard statistics
    total_employees = Employee.query.count()

    total_departments = Department.query.count()

    vacation_count = current_vacations.count()

    return render_template(
        "dashboard.html",
        vacations=vacations,
        total_employees=total_employees,
        total_departments=total_departments,
        vacation_count=vacation_count
    )

@app.route("/employees")
def employees():
    employees = (
        db.session.query(
            Employee.employee_id,
            func.concat(
                Employee.first_name,
                " ",
                Employee.last_name
            ).label("name"),
            Employee.department,
            Employee.email,
            Employee.address,
            Employee.mobile_number
        )
        .order_by(Employee.employee_id.asc())
        .all()
    )

    return render_template(
        "employees.html",
        active_page="employees",
        employees=employees
    )


@app.route("/departments", methods=["GET", "POST"])
def departments():

    if request.method == "POST":

        department_id = request.form["department_id"]
        name = request.form["name"]
        manager = request.form["manager"]

        # Create department object
        new_department = Department(
            department_id=department_id,
            name=name,
            manager=manager
        )

        # Insert into database
        db.session.add(new_department)
        db.session.commit()

        return redirect(url_for("departments"))

    departments = Department.query.all()

    return render_template(
        "departments.html",
        active_page="departments",
        departments=departments
    )

@app.route("/vacations")
def vacations():
    vacations = (
            db.session.query(
                Vacation.employee_id,
                func.concat(
                    Vacation.first_name,
                    " ",
                    Vacation.last_name
                ).label("name"),
                Vacation.start_date,
                Vacation.end_date,
                Vacation.date_requested,
                Vacation.reason
            )
            .order_by(Vacation.start_date.asc())
            .all()
                )
    return render_template(
        "vacations.html",
        active_page="vacations",
        vacations=vacations
    )


@app.route("/users")
def users():
    return render_template(
        "users.html",
        active_page="users",
        users=[]
    )

@app.route("/register", methods=["GET", "POST"])
def register():
    departments = Department.query.order_by(Department.name).all()

    if request.method == "POST":
        employee_id = request.form["employee_id"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        department = request.form["department"]
        address = request.form["address"]
        mobile_number = request.form["mobile_number"]
        # Create employee object
        new_employee = Employee(
            employee_id=employee_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            department=department,
            address=address,
            mobile_number=mobile_number
        )

        # Insert into database
        db.session.add(new_employee)
        db.session.commit()

        # Redirect after successful registration
        return redirect(url_for("employees"))

    return render_template(
        "register.html",
        active_page="register",
        departments=departments
    )


@app.route("/edit_employee/<string:employee_id>", methods=["GET", "POST"])
def edit_employee(employee_id):

    # Search using employee_id, NOT auto_id
    employee = Employee.query.filter_by(
        employee_id=employee_id
    ).first_or_404()

    departments = Department.query.order_by(
        Department.name
    ).all()

    if request.method == "POST":
        employee_id = request.form["employee_id"]
        employee.first_name = request.form["first_name"]
        employee.last_name = request.form["last_name"]
        employee.email = request.form["email"]
        employee.department = request.form["department"]
        employee.address = request.form["address"]
        employee.mobile_number = request.form["mobile_number"]

        db.session.commit()

        flash("Employee updated successfully!", "success")
        return redirect(url_for("employees"))

    return render_template(
        "edit_employee.html",
        employee=employee,
        departments=departments
    )


@app.route("/vacation_request", methods=["GET", "POST"])
def vacation_request():

    employees = Employee.query.order_by(
        Employee.employee_id
    ).all()

    if request.method == "POST":

        # Create a new vacation record
        vacation = Vacation(
            employee_id=request.form["employee_id"],
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            start_date=request.form["start_date"],
            end_date=request.form["end_date"],
            date_requested=request.form["date_requested"],
            reason = request.form["reason"]
        )

        # Save to database
        db.session.add(vacation)
        db.session.commit()

        flash("Vacation request successfully added!", "success")

        return redirect(url_for("vacations"))

    return render_template(
        "vacation_request.html",
        employees=employees
    )

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)