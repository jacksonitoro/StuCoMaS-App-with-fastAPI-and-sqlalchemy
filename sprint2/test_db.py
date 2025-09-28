from sprint2.database import Base, engine
from sprint2 import models

print("Creating tables...")
Base.metadata.create_all(bind=engine)

print(Student.__tablename__)
print(Instructor.__tablename__)
print(Course.__tablename__)
print(Enrollment.__tablename__)
print("✅ Tables created successfully!")
