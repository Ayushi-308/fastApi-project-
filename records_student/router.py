from fastapi import ( APIRouter, Depends, HTTPException)
from sqlalchemy.orm import Session
from database import get_db
from records_student.schemas import (RecordCreate, RecordResponse)
from records_student.models import Records

router=APIRouter( prefix="/records", tags=["Records"])

@router.get("/", response_model=list[RecordResponse])
def get_all_records(
    db: Session = Depends(get_db)
):
    records = db.query(Records).all()
    return records

@router.post("/records", response_model=RecordResponse)
def create_record(
    data: RecordCreate,
     db: Session = Depends(get_db)
):
    new_record=Records(
        Name=data.Name,
        English=data.English,
        Maths=data.Maths,
        Science=data.Science,
        Hindi=data.Hindi,
        Social_Science=data.Social_Science
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

@router.put("/records/{Records_id}", response_model=RecordResponse)
def update_record(
    Records_id: int,
    data: RecordCreate,
    db: Session = Depends(get_db)
):
    record= db.query(Records).filter(Records.id == Records_id).first()

    if record is None:
        raise HTTPException(
            status_code=404,
            details="Record not found"
        )

    record.Name=data.Name
    record.English=data.English
    record.Maths=data.Maths
    record.Science=data.Science
    record.Hindi=data.Hindi
    record.Social_Science=data.Social_Science

    db.commit()
    db.refresh(record)
    return record

@router.delete("records/{student_id}")
def delete_record(
    records_id : int,
    db: Session = Depends(get_db)
):
    record = db.query(Records).filter(Records.id==records_id).first()
    if record is None:
        raise HTTPException(
            status_code=404,
            details="Record not found"
        )
    db.delete(record)
    db.commit()
    return {"message" : "Record deleted successfully"}

    