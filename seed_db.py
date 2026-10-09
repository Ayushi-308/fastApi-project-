import random
from database import SessionLocal, engine, Base
from models import Student

# Ensure tables are created
Base.metadata.create_all(bind=engine)

def seed_students(n=100):
    db = SessionLocal()
    
    first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Hannah", "Isaac", "Jack", "Kevin", "Liam", "Mia", "Noah", "Olivia", "Peter", "Quinn", "Rachel", "Sam", "Tom", "Ursula", "Victor", "Wendy", "Xavier", "Yvonne", "Zack"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White"]
    
    try:
        students_to_add = []
        for i in range(n):
            first = random.choice(first_names)
            last = random.choice(last_names)
            name = f"{first} {last}"
            email = f"{first.lower()}.{last.lower()}{i}@example.com"
            age = random.randint(18, 25)
            
            new_student = Student(
                name=name,
                age=age,
                email=email
            )
            students_to_add.append(new_student)
        
        # Bulk save for better performance
        db.add_all(students_to_add)
        db.commit()
        print(f"Successfully added {n} student records to the database.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_students(100)
