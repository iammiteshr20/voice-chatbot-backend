from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List, Dict
from typing import Dict, Optional, List

class UserSchema(BaseModel):
    name: str
    email: str
    nickname: str

class DoctorSchema(BaseModel):
    name: str
    specialty: str
    
class DoctorWithSchedule(BaseModel):
    id: int
    name: str
    specialty: str
    created_at: datetime
    updated_at: datetime
    schedule: Optional[Dict[str, List[str]]]
    
class DoctorResponse(BaseModel):
    id: int
    name: str
    specialty: str
    created_at: datetime
    updated_at: datetime
    schedule: Optional[dict] = None
    
class AppointmentSchema(BaseModel):
    id: int
    doctor_id: int
    patient_token_number: str
    schedule: dict
    status: str
    created_at: datetime
    updated_at: datetime
