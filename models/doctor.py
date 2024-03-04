from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    nickname = Column(String)


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    specialty = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define the relationship with DoctorSchedule
    schedule = relationship("DoctorSchedule", uselist=False, back_populates="doctor")

    # Define the relationship with appointments
    appointments = relationship("Appointment", back_populates="doctor")


# Define SQLAlchemy model for doctor's availability schedule
class DoctorSchedule(Base):
    __tablename__ = "doctor_schedule"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'))  # Foreign key relationship
    schedule = Column(JSON)

    # Define the relationship with Doctor
    doctor = relationship("Doctor", back_populates="schedule")

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    patient_token_number = Column(String)  # Assuming token number is a string
    schedule = Column(String)
    status = Column(String, default="scheduled")  # Added status field with default value "scheduled"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    doctor = relationship("Doctor", back_populates="appointments")




# class DoctorAvailability(Base):
#     __tablename__ = "doctor_availability"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     doctor_id = Column(Integer, ForeignKey('doctors.id'))
#     # doctor = relationship("Doctor", back_populates="appointments")
#     # available_date = Column(DateTime, index=True)
#     available_date = Column(String, index=True)
#     start_time = Column(DateTime)
#     end_time = Column(DateTime)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# class Appointment(Base):
#     __tablename__ = "appointments"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     doctor_id = Column(Integer, ForeignKey('doctors.id'))
#     doctor = relationship("Doctor", back_populates="appointments")
#     appointment_datetime = Column(DateTime, index=True)
#     patient_token = Column(String, unique=True)
