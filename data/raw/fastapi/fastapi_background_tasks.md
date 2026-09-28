# Background Tasks for Asynchronous Execution

**Doc ID:** `fastapi_background_tasks`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Execute non-blocking tasks (email dispatch, log flushing, notifications) after sending HTTP responses.

---

## Using BackgroundTasks
```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def send_notification_email(email: str, message: str):
    # Simulated background task (runs after HTTP response is returned to client)
    with open("notifications.log", "a") as f:
        f.write(f"Notified {email}: {message}\n")

@app.post("/send-alert/")
async def send_alert(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_notification_email, email, message="Security alert")
    return {"message": "Notification scheduled"}
```

