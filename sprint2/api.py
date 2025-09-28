from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import sprint2.models as models
import sprint2.schemas as schemas
import sprint2.crud as crud
from sprint2.database import SessionLocal, engine

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to StuCoMaS API 🚀"}

# --- Student Routes ---

@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db=db, **student.dict())

@app.get("/students/", response_model=list[schemas.Student])
def read_students(db: Session = Depends(get_db)):
    return crud.get_students(db=db)

@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_id(db=db, student_id=student_id)
    if db_student is None:
        return {"error": "Student not found"}
    return db_student
