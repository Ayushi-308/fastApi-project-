from fastapi import FastAPI, Depends
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import Student
from schemas import StudentCreate, StudentResponse
from auth.router import router as auth_router
from records_student.router import router as records_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(records_router)

app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "API is working"}


@app.post("/students", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):

    new_student = Student(
        name=student.name,
        age=student.age,
        email=student.email
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentCreate,
    db: Session = Depends(get_db)
):
    # Find the student
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    # If student does not exist
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Update the student's data
    student.name = student_data.name
    student.age = student_data.age
    student.email = student_data.email

    # Save changes
    db.commit()

    # Get updated data
    db.refresh(student)

    return student

@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    # Find student by ID
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    # If student does not exist
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Delete the student
    db.delete(student)

    # Save changes
    db.commit()

    return {
        "message": "Student deleted successfully"
    }

@app.get("/students", response_model=list[StudentResponse])
def get_students(
    limit: int = 10,
    skip: int = 0,
     sort_by: str="age",
        order: str="asc",
    db: Session = Depends(get_db)
):
    students_query = db.query(Student)

    # Apply sorting
    if sort_by == "age":
        students_query = students_query.order_by(
            Student.age.asc() if order == "asc" else Student.age.desc()
        )
    elif sort_by == "name":
        students_query = students_query.order_by(
            Student.name.asc() if order == "asc" else Student.name.desc()
        )

    # Apply pagination
    students = students_query.limit(limit).offset(skip).all()
    return students

