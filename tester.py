import pandas as pd
import random
from faker import Faker

#Initialize Faker
fake = Faker()

#Define specialties
specialties = [
    "ENT Specialist", "General Practitioner", "Allergist", "Neurologist", "Orthopedic Surgeon",
    "Cardiologist", "Rheumatologist", "Nephrologist", "Pulmonologist", "Oncologist",
    "Endocrinologist", "Pediatrician", "Dermatologist", "Gastroenterologist", "Ophthalmologist"
]

#Generate at least 30 unique cities per specialty
cities_per_specialty = {}
for specialty in specialties:
    cities_per_specialty[specialty] = list(set([fake.city() for i in range(30)]))

#Generate 1000 entries
data = []
for _ in range(1000):
    specialty = random.choice(specialties)
    city = random.choice(cities_per_specialty[specialty])
    state = "GA"  # Assuming all doctors are in Georgia
    rating = round(random.uniform(3.5, 5.0), 2)  # Random rating between 3.5 and 5.0
    doctor_name = fake.name()

    data.append([doctor_name, specialty, city, state, rating])

#Create a DataFrame
df = pd.DataFrame(data, columns=["Doctor Name", "Specialty", "City", "State", "Rating"])

#Save to CSV
df.to_csv("other_doctors.csv", index=False)

print("CSV file 'other_doctors.csv' generated successfully!")