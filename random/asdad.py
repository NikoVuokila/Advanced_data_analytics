import random
import mysql.connector


# ============================
# MySQL connection settings
# ============================

DB_CONFIG = {
    "host": "3306",
    "user": "root",
    "password": "Perttikalevi1",
    "database": "nf_test"
}


# ============================
# Sample data
# ============================

departments = [
    (1, "Human Resources"),
    (2, "Finance"),
    (3, "IT"),
    (4, "Marketing"),
    (5, "Sales")
]

skills = [
    (1, "Python"),
    (2, "SQL"),
    (3, "Project Management"),
    (4, "Data Analysis"),
    (5, "Communication")
]


# ============================
# Generate employees
# ============================

first_names = [
    "Anna", "Mark", "John", "Emma", "Michael",
    "Sarah", "David", "Laura", "James", "Linda",
    "Robert", "Maria", "Daniel", "Sophie", "Thomas",
    "Emily", "Peter", "Olivia", "William", "Mia"
]

last_names = [
    "Smith", "Johnson", "Brown", "Taylor", "Anderson",
    "Wilson", "Moore", "Martin", "Jackson", "White",
    "Harris", "Thompson", "Garcia", "Martinez", "Robinson"
]


employees = []

for employee_id in range(1, 101):

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)

    employee_name = f"{first_name} {last_name}"
    email = f"{first_name.lower()}.{last_name.lower()}{employee_id}@company.com"

    department_id = random.randint(1, 5)

    employees.append(
        (
            employee_id,
            employee_name,
            email,
            department_id
        )
    )


# ============================
# Generate employee skills
# ============================

employee_skills = []

for employee_id in range(1, 101):

    # Each employee gets 1–3 skills
    number_of_skills = random.randint(1, 3)

    selected_skills = random.sample(
        range(1, 6),
        number_of_skills
    )

    for skill_id in selected_skills:
        employee_skills.append(
            (
                skill_id,
                employee_id
            )
        )


# ============================
# Connect to MySQL
# ============================

connection = mysql.connector.connect(**DB_CONFIG)

cursor = connection.cursor()


try:

    # ============================
    # Insert departments
    # ============================

    cursor.executemany(
        """
        INSERT INTO departments
            (department_id, department_name)
        VALUES
            (%s, %s)
        """,
        departments
    )


    # ============================
    # Insert skills
    # ============================

    cursor.executemany(
        """
        INSERT INTO skills
            (skill_id, skill_name)
        VALUES
            (%s, %s)
        """,
        skills
    )


    # ============================
    # Insert employees
    # ============================

    cursor.executemany(
        """
        INSERT INTO employees
            (employee_id, employee_name, email, department_id)
        VALUES
            (%s, %s, %s, %s)
        """,
        employees
    )


    # ============================
    # Insert employee skills
    # ============================

    cursor.executemany(
        """
        INSERT INTO skills_has_employees
            (skills_skill_id, employees_employee_id)
        VALUES
            (%s, %s)
        """,
        employee_skills
    )


    # Commit all changes
    connection.commit()

    print("Data inserted successfully!")
    print(f"Departments: {len(departments)}")
    print(f"Skills: {len(skills)}")
    print(f"Employees: {len(employees)}")
    print(f"Employee-skill relationships: {len(employee_skills)}")


except mysql.connector.Error as error:

    print("Error:", error)

    # Undo changes if something went wrong
    connection.rollback()


finally:

    cursor.close()
    connection.close()