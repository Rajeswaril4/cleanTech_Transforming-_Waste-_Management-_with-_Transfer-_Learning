import csv
import random

# File path
output_file = "real_disease_symptoms_1000000.csv"

# Symptom pool
symptom_pool = [
    "Fever", "Cough", "Sore throat", "Headache", "Nausea", "Vomiting", "Fatigue", "Muscle pain",
    "Chest pain", "Shortness of breath", "Sneezing", "Runny nose", "Dizziness", "Sweating",
    "Chills", "Rash", "Loss of appetite", "Weight loss", "Constipation", "Diarrhea",
    "Abdominal pain", "Itchy skin", "Jaundice", "Blurred vision", "Wheezing", "Back pain",
    "Joint pain", "Swollen glands", "Night sweats", "Dry mouth", "Tingling", "Palpitations",
    "Anxiety", "Depression", "Insomnia", "Hair loss", "Hearing loss", "Red eyes", "Tremors"
]

# Real disease names
real_diseases = [
    "Diabetes", "Hypertension", "Asthma", "Tuberculosis", "COVID-19", "Influenza", "Malaria", "Dengue",
    "Pneumonia", "Typhoid", "Chickenpox", "Hepatitis A", "Migraine", "Anemia", "Arthritis", "Bronchitis",
    "Celiac Disease", "Chikungunya", "Cholera", "Conjunctivitis", "Depression", "Epilepsy", "Gastroenteritis",
    "Glaucoma", "Gonorrhea", "HIV/AIDS", "Hepatitis B", "Jaundice", "Leprosy", "Lupus", "Measles",
    "Meningitis", "Mononucleosis", "Multiple Sclerosis", "Psoriasis", "Rabies", "Scabies", "Sinusitis",
    "Syphilis", "Tetanus", "Thalassemia", "Tonsillitis", "Ulcerative Colitis", "UTI", "Vertigo", "Zika Virus"
]

# Generate dataset
entries_required = 1000000
repeat_factor = entries_required // len(real_diseases)

with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Disease", "Symptom1", "Symptom2", "Symptom3", "Symptom4", "Symptom5", "Symptom6", "Symptom7"])

    count = 1
    for i in range(repeat_factor):
        for disease in real_diseases:
            disease_name = f"{disease}_{count}"
            symptoms = random.sample(symptom_pool, random.randint(3, 7))
            row = [disease_name] + symptoms + [""] * (7 - len(symptoms))
            writer.writerow(row)
            count += 1

print(f"Dataset with 1 million entries saved as '{output_file}'")
