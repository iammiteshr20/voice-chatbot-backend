import re
import json
import os
from datetime import datetime

# Get the absolute path to the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the JSON file
json_file_path = os.path.join(current_directory, "doctor_availability.json")

# Load doctor's availability from JSON file
with open(json_file_path, "r") as file:
    doctor_availability = json.load(file)

def check_booking_intent(user_input):
    booking_keywords = ['book', 'appointment', 'schedule']
    reschedule_keywords = ['reschedule', 'change']
    cancel_keywords = ['cancel']
    day_keywords = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    time_regex = re.compile(r'\d{1,2}:\d{2}\s*(?:AM|PM|am|pm|p.m.|p.m|a.m.|a.m)?')
    
    user_input = user_input.lower()
    
    # Check if input contains booking-related keywords
    booking_mentioned = any(keyword in user_input for keyword in booking_keywords)
    reschedule_mentioned = any(keyword in user_input for keyword in reschedule_keywords)
    cancel_mentioned = any(keyword in user_input for keyword in cancel_keywords)

    if booking_mentioned or reschedule_mentioned:
        # Check if both day and time are mentioned
        day_mentioned = any(day in user_input for day in day_keywords)
        time_match = time_regex.search(user_input)
        time_mentioned = bool(time_match)
        
        if day_mentioned and time_mentioned:
            # Booking details complete, proceed with booking
            day = next((day for day in day_keywords if day in user_input), None)
            time = time_match.group()
            if check_doctor_availability(day, time):
                return {"message": "Booking available for {} at {}. Please provide your name and phone number.".format(day.capitalize(), time)}
            else:
                return suggest_alternative(day, time)
        elif day_mentioned:
            # Ask for time
            return {"message": "Please specify the time for the booking."}
        elif time_mentioned:
            # Ask for day
            return {"message": "Please specify the day for the booking."}
        else:
            # Ask for both day and time
            return {"message": "Please specify both the day and time for the booking."}
    elif cancel_mentioned:
        # Canceling appointment
        return {"cancel": True}
    else:
        return {"message": "No booking or cancel intent detected in the input."}


def check_doctor_availability(day, time):
    try:
        # Attempt to parse time string in 12-hour format
        time_obj = datetime.strptime(time, "%I:%M%p")
        # Convert to military time format
        military_time_str = time_obj.strftime("%H:%M")
    except ValueError:
        return False  # Invalid time format
    
    # Check if the day and time are available
    if day.lower() in doctor_availability:
        if military_time_str in doctor_availability[day.lower()]:
            return True  # Time is available
    return False  # Time not available
    

def suggest_alternative(day, time):
    alternative_slots = []
    for alt_day, alt_times in doctor_availability.items():
        if alt_day.lower() != day.lower():
            if alt_times:
                alternative_slots.append({
                    "day": alt_day.capitalize(),
                    "times": alt_times
                })
    if alternative_slots:
        return {
            "message": "The requested time {} is not available on {}. Here are some alternative available slots:".format(time, day.capitalize()),
            "alternatives": alternative_slots
        }
    else:
        return {"message": "There are no alternative available slots."}