import asyncio
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

class EmailOperation(BaseModel):
    recipient: str = Field(description="Email recipient")
    subject: str = Field(description="Email subject")
    body: str = Field(description="Email body content")
    attachments: List[str] = Field(default=[], description="List of attachment file paths")

class CalendarEvent(BaseModel):
    title: str = Field(description="Event title")
    start_time: str = Field(description="Start time in ISO format")
    duration_minutes: int = Field(description="Duration in minutes")
    attendees: List[str] = Field(default=[], description="List of attendee emails")
    location: str = Field(default="", description="Event location")

class ContactInfo(BaseModel):
    name: str = Field(description="Contact name")
    email: str = Field(description="Contact email")
    company: str = Field(default="", description="Contact company")
    notes: str = Field(default="", description="Additional notes")

class TaskInfo(BaseModel):
    title: str = Field(description="Task title")
    description: str = Field(description="Task description")
    assignee: str = Field(default="", description="Person assigned to task")
    due_date: str = Field(default="", description="Due date in ISO format")

class BusinessOperationsMCP:
    def __init__(self):
        self.app = FastMCP("business-ops")
        # In a real implementation, these would connect to actual services
        # For now, we'll simulate the operations
        
    async def send_email(self, recipient: str, subject: str, body: str, attachments: List[str] = []) -> dict:
        """Send an email to the specified recipient."""
        try:
            # Simulate email sending - in reality, this would connect to an email service
            print(f"Simulating email send to {recipient}: {subject}")
            return {
                "success": True,
                "message_id": f"email_{hash(recipient + subject)}",
                "timestamp": datetime.now().isoformat(),
                "message": f"Email sent to {recipient}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def create_calendar_event(self, title: str, start_time: str, duration_minutes: int, 
                                   attendees: List[str] = [], location: str = "") -> dict:
        """Create a calendar event."""
        try:
            # Simulate calendar event creation - in reality, this would connect to a calendar service
            event_id = f"event_{hash(title + start_time)}"
            print(f"Simulating calendar event creation: {title} at {start_time}")
            return {
                "success": True,
                "event_id": event_id,
                "title": title,
                "start_time": start_time,
                "end_time": (datetime.fromisoformat(start_time.replace('Z', '+00:00')) + 
                            timedelta(minutes=duration_minutes)).isoformat(),
                "attendees": attendees,
                "location": location,
                "status": "confirmed"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def create_contact(self, name: str, email: str, company: str = "", notes: str = "") -> dict:
        """Create a new contact."""
        try:
            # Simulate contact creation - in reality, this would connect to a CRM
            contact_id = f"contact_{hash(email)}"
            print(f"Simulating contact creation: {name} ({email})")
            return {
                "success": True,
                "contact_id": contact_id,
                "name": name,
                "email": email,
                "company": company,
                "notes": notes
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def create_task(self, title: str, description: str, assignee: str = "", due_date: str = "") -> dict:
        """Create a new task."""
        try:
            # Simulate task creation - in reality, this would connect to a task management system
            task_id = f"task_{hash(title + assignee)}"
            print(f"Simulating task creation: {title} assigned to {assignee}")
            return {
                "success": True,
                "task_id": task_id,
                "title": title,
                "description": description,
                "assignee": assignee,
                "due_date": due_date,
                "status": "pending"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

def create_business_ops_server():
    server = BusinessOperationsMCP()
    
    @server.app.tool("send_email", "Send an email to the specified recipient")
    async def handle_send_email(op: EmailOperation) -> dict:
        return await server.send_email(
            op.recipient, op.subject, op.body, op.attachments
        )
    
    @server.app.tool("create_calendar_event", "Create a calendar event")
    async def handle_create_event(event: CalendarEvent) -> dict:
        return await server.create_calendar_event(
            event.title, event.start_time, event.duration_minutes,
            event.attendees, event.location
        )
    
    @server.app.tool("create_contact", "Create a new contact in the system")
    async def handle_create_contact(contact: ContactInfo) -> dict:
        return await server.create_contact(
            contact.name, contact.email, contact.company, contact.notes
        )
    
    @server.app.tool("create_task", "Create a new task")
    async def handle_create_task(task: TaskInfo) -> dict:
        return await server.create_task(
            task.title, task.description, task.assignee, task.due_date
        )
    
    return server

if __name__ == "__main__":
    import uvicorn
    server = create_business_ops_server()
    
    async def run_server():
        config_obj = uvicorn.Config(app=server.app, host="127.0.0.1", port=3003)
        server_instance = uvicorn.Server(config_obj)
        await server_instance.serve()
    
    asyncio.run(run_server())