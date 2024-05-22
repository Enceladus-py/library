from app.database import SessionLocal


# Create session when accessing database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
