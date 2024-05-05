from fastapi import FastAPI, Depends

from db import get_db
from api.models.log_entry import LogEntry

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/logs/")
def create_log_entry(message: str, db=Depends(get_db)):
    # Create a new LogEntry instance
    log_entry = LogEntry(message=message)

    # Add the log entry to the database session
    db.add(log_entry)

    # Commit the changes to the database
    db.commit()

    # Return the created log entry
    return {"id": log_entry.id, "message": log_entry.message}


@app.get("/logs/")
def get_log_entries(db=Depends(get_db)):
    # Query the log entries from the database
    log_entries = db.query(LogEntry).all()

    # Convert the log entries to a list of dictionaries
    logs = [{"id": entry.id, "message": entry.message} for entry in log_entries]

    # Return the log entries
    return logs
