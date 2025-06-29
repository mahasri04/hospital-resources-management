# utils.py
import random
from datetime import datetime, timedelta

def generate_patients(count=20):
    conditions = ["Cardiac Arrest", "Pneumonia", "Stroke", "Fracture", "Sepsis",
                  "Diabetes Crisis", "Asthma Attack", "Trauma", "Appendicitis", "COVID-19"]
    departments = ["ER", "ICU", "Radiology", "Surgery", "General"]
    
    patients = []
    for i in range(1, count+1):
        admission_date = datetime.now() - timedelta(days=random.randint(0, 30))
        condition = random.choice(conditions)
        severity = random.randint(1, 10)
        department = random.choice(departments)

        patients.append({
            "id": f"P{i:03d}",
            "name": f"Patient {i}",
            "age": random.randint(18, 90),
            "gender": random.choice(["M", "F"]),
            "condition": condition,
            "severity": severity,
            "department": department,
            "admission_date": admission_date,
            "treatment_time": random.randint(1, 8),
            "resources_needed": {
                "bed": 1,
                "nurse": random.randint(1, 3),
                "doctor": 1,
                "medication": random.choice([1, 1, 1, 2]),
                "equipment": random.choice(["none", "IV", "ventilator", "monitor"])
            },
            "priority": severity * 2 + random.randint(1, 5)
        })
    return patients

def generate_resources():
    return {
        "beds": {"total": 50, "available": 35},
        "nurses": {"total": 40, "available": 25},
        "doctors": {"total": 20, "available": 12},
        "medications": {"total": 1000, "available": 650},
        "equipment": {
            "IV": {"total": 30, "available": 18},
            "ventilator": {"total": 15, "available": 8},
            "monitor": {"total": 25, "available": 15}
        }
    }

def generate_staff():
    staff = []
    roles = ["Doctor", "Nurse", "Technician", "Administrator"]
    shifts = ["Morning", "Afternoon", "Night"]
    
    for i in range(1, 41):
        staff.append({
            "id": f"S{i:03d}",
            "name": f"Staff {i}",
            "role": random.choice(roles),
            "department": random.choice(["ER", "ICU", "Radiology", "Surgery", "General"]),
            "shift": random.choice(shifts),
            "skills": random.sample(["Emergency", "Pediatrics", "Surgery", "Imaging", "Pharmacy"], k=random.randint(1, 3))
        })
    return staff

def generate_departments():
    return {
        "ER": {"capacity": 15, "adjacent": ["ICU", "Radiology"]},
        "ICU": {"capacity": 10, "adjacent": ["ER", "Surgery"]},
        "Radiology": {"capacity": 5, "adjacent": ["ER", "Surgery"]},
        "Surgery": {"capacity": 8, "adjacent": ["ICU", "Radiology"]},
        "General": {"capacity": 20, "adjacent": ["ER"]}
    }
