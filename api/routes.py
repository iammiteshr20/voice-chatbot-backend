import os
import uuid
import requests
from pydantic import BaseModel
from shutil import copyfileobj
from pydantic import BaseModel
from datetime import datetime
from typing import List

from fastapi import Depends, APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

import assemblyai as aai
from database import engine, SessionLocal
from functions.appointment import check_booking_intent
from functions.text_to_speech import convert_text_to_speech
from settings import settings
from models.doctor import Base, User, DoctorSchedule, Doctor, Appointment
from schemas.doctor_schema import UserSchema, DoctorSchema, DoctorResponse, DoctorWithSchedule, AppointmentSchema

Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


router = APIRouter()
user_router = APIRouter()
doctor_router = APIRouter()
ai_router = APIRouter()


# ----- Router -------------------------------------------
@router.get("/")
async def read_root():
    return {"message": "Hello, world!"}


# ----- AI Router ----------------------------------------
@ai_router.get("/welcome-doctor")
async def welcome():
    text= "Hello, thanks for calling Dr. Archer’s office. How may I assist you today?",
    
    return {
        "message": text,
        "result_audio_path": f"{settings.base_url}/audios/welcome.mp3"
    }

@ai_router.post("/voice-chat/book-appointment")
async def book_appointment(file: UploadFile = File(...)):
    input_random_filename = str(uuid.uuid4()) + ".wav"

    # Directory to save uploaded files
    UPLOAD_DIR = "audios/input"

    # Create the upload directory if it doesn't exist
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_path = os.path.join(UPLOAD_DIR, input_random_filename)

    # Save the uploaded file to the specified directory
    with open(file_path, "wb") as buffer:
        copyfileobj(file.file, buffer)

    # Transcribe the uploaded audio file using AssemblyAI
    aai.settings.api_key = settings.assemblyai_api_key
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path)
    text = transcript.text

    print(text, "test")

    # Process the transcribed text and check booking intent
    result = check_booking_intent(transcript.text)

    # Raise an exception if the booking intent is not valid
    if not result:
        raise HTTPException(status_code=400, detail="Invalid booking input")
    
    # Convert chat response to audio  
    audio_output = convert_text_to_speech(result['message'])

    return {
        "file":{
            "name": file.filename, 
            "content_type": file.content_type, 
            "size": os.path.getsize(file_path), 
        },
        "transcription": text, 
        "booking_result": result,
        "result_audio_path": f"{settings.base_url}/{audio_output}"
    }


# ----- User Router --------------------------------------
@user_router.post("/get-users")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@user_router.post("/add-user")
async def add_user(request:UserSchema, db: Session = Depends(get_db)):
    user = User(name=request.name, email=request.email, nickname=request.nickname)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ----- Doctor Router -----------------------------------
# @doctor_router.post("/get-doctors")
# async def get__all_doctors(db: Session = Depends(get_db)):
#     doctors = db.query(Doctor).all()
#     return doctors

@doctor_router.get("/get-doctors", response_model=List[DoctorWithSchedule])
async def get_all_doctors_with_schedule(db: Session = Depends(get_db)):
    doctors_with_schedule = []
    doctors = db.query(Doctor).all()
    for doctor in doctors:
        doctor_schedule = db.query(DoctorSchedule).filter(DoctorSchedule.doctor_id == doctor.id).first()
        if doctor_schedule:
            doctors_with_schedule.append(DoctorWithSchedule(
                id=doctor.id,
                name=doctor.name,
                specialty=doctor.specialty,
                created_at=doctor.created_at,
                updated_at=doctor.updated_at,
                schedule=doctor_schedule.schedule
            ))
        else:
            doctors_with_schedule.append(DoctorWithSchedule(
                id=doctor.id,
                name=doctor.name,
                specialty=doctor.specialty,
                created_at=doctor.created_at,
                updated_at=doctor.updated_at,
                schedule={}
            ))
    return doctors_with_schedule

@doctor_router.get("/get-doctor/{doctor_id}", response_model=DoctorResponse)
async def get_doctor_by_id(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Fetch the doctor's schedule if available
    doctor_schedule = db.query(DoctorSchedule).filter(DoctorSchedule.doctor_id == doctor_id).first()
    schedule = doctor_schedule.schedule if doctor_schedule else None
    
    # Construct the DoctorResponse object with doctor details and schedule
    doctor_response = DoctorResponse(
        id=doctor.id,
        name=doctor.name,
        specialty=doctor.specialty,
        created_at=doctor.created_at,
        updated_at=doctor.updated_at,
        schedule=schedule
    )
    
    return doctor_response

@doctor_router.post("/add-doctor")
async def add_doctor(request:DoctorSchema, db: Session = Depends(get_db)):
    doctor = Doctor(name=request.name, specialty=request.specialty)
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor

# Endpoint to create or update doctor's schedule
@doctor_router.post("/doctor-schedule/")
async def create_or_update_doctor_schedule(doctor_id: int, schedule: dict, db: Session = Depends(get_db)):
    # Check if the schedule already exists for the doctor
    existing_schedule = db.query(DoctorSchedule).filter(DoctorSchedule.doctor_id == doctor_id).first()
    if existing_schedule:
        existing_schedule.schedule = schedule
    else:
        new_schedule = DoctorSchedule(doctor_id=doctor_id, schedule=schedule)
        db.add(new_schedule)
    db.commit()
    return {"message": "Doctor's schedule updated successfully"}

# Endpoint to get doctor's schedule
@doctor_router.get("/doctor-schedule/{doctor_id}")
async def get_doctor_schedule(doctor_id: int, db: Session = Depends(get_db)):
    doctor_schedule = db.query(DoctorSchedule).filter(DoctorSchedule.doctor_id == doctor_id).first()
    if not doctor_schedule:
        return {"message": "Doctor's schedule not found"}
    return doctor_schedule.schedule

@router.get("/appointments")
def get_all_appointments(db: Session = Depends(get_db)):
    appointments = db.query(Appointment).all()
    return appointments
