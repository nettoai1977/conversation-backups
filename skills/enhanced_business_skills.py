"""
Enhanced Business Operations Skills for OpenClaw
Based on the research findings for multi-agent systems and skills development.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import asyncio
import json

class BusinessOperationsSkills:
    """
    Enhanced business operations skills with atomic, composite, and adaptive capabilities.
    """
    
    def __init__(self):
        # In-memory storage for demo purposes
        # In production, this would connect to persistent storage
        self.calendar_events = []
        self.contacts = {}
        self.tasks = {}
        self.email_queue = []
        self.next_task_id = 1
    
    # ATOMIC SKILLS
    async def send_email_atomic(self, recipient: str, subject: str, body: str, 
                               attachments: List[str] = []) -> Dict:
        """
        Atomic skill: Send a single email.
        """
        try:
            # Simulate email sending
            email_record = {
                "id": f"email_{len(self.email_queue) + 1}",
                "recipient": recipient,
                "subject": subject,
                "body": body[:100] + "..." if len(body) > 100 else body,  # Truncate for display
                "attachments": attachments,
                "timestamp": datetime.now().isoformat(),
                "status": "sent"
            }
            self.email_queue.append(email_record)
            
            return {
                "success": True,
                "email_id": email_record["id"],
                "message": f"Email sent to {recipient}",
                "details": email_record
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_calendar_event_atomic(self, title: str, start_time: str, 
                                        duration: int, attendees: List[str] = [], 
                                        location: str = "") -> Dict:
        """
        Atomic skill: Create a single calendar event.
        """
        try:
            event = {
                "id": f"event_{len(self.calendar_events) + 1}",
                "title": title,
                "start_time": start_time,
                "duration": duration,  # in minutes
                "attendees": attendees,
                "location": location,
                "created_at": datetime.now().isoformat()
            }
            self.calendar_events.append(event)
            
            return {
                "success": True,
                "event_id": event["id"],
                "message": f"Event '{title}' created successfully",
                "event": event
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def add_contact_atomic(self, name: str, email: str, company: str = "", 
                               notes: str = "") -> Dict:
        """
        Atomic skill: Add a single contact.
        """
        try:
            contact_id = f"contact_{len(self.contacts) + 1}"
            contact = {
                "id": contact_id,
                "name": name,
                "email": email,
                "company": company,
                "notes": notes,
                "created_at": datetime.now().isoformat()
            }
            self.contacts[contact_id] = contact
            
            return {
                "success": True,
                "contact_id": contact_id,
                "message": f"Contact '{name}' added successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_task_atomic(self, title: str, description: str, 
                               assignee: str = "", due_date: str = "") -> Dict:
        """
        Atomic skill: Create a single task.
        """
        try:
            task_id = f"task_{self.next_task_id}"
            self.next_task_id += 1
            
            task = {
                "id": task_id,
                "title": title,
                "description": description,
                "assignee": assignee,
                "due_date": due_date,
                "status": "pending",
                "created_at": datetime.now().isoformat()
            }
            self.tasks[task_id] = task
            
            return {
                "success": True,
                "task_id": task_id,
                "message": f"Task '{title}' created successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    # COMPOSITE SKILLS
    async def schedule_meeting_composite(self, client_email: str, meeting_subject: str, 
                                      preferred_times: List[str], location: str = "") -> Dict:
        """
        Composite skill: Schedule a meeting by combining multiple atomic skills.
        """
        try:
            # Step 1: Check client availability (simplified)
            available_slot = preferred_times[0] if preferred_times else datetime.now().isoformat()
            
            # Step 2: Create the calendar event
            event_result = await self.create_calendar_event_atomic(
                title=meeting_subject,
                start_time=available_slot,
                duration=60,  # 1 hour meeting
                attendees=[client_email],
                location=location
            )
            
            if not event_result["success"]:
                return event_result
            
            # Step 3: Send confirmation email to client
            email_body = f"""
Hello,

Your meeting "{meeting_subject}" has been scheduled for {available_slot}.
Location: {location}

Please let me know if you need to make any changes.

Best regards,
Your Assistant
"""
            email_result = await self.send_email_atomic(
                recipient=client_email,
                subject=f"Meeting Confirmation: {meeting_subject}",
                body=email_body
            )
            
            return {
                "success": True,
                "event_result": event_result,
                "email_result": email_result,
                "message": f"Meeting scheduled and confirmation sent to {client_email}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_client_profile_composite(self, name: str, email: str, 
                                           company: str = "", notes: str = "") -> Dict:
        """
        Composite skill: Create a comprehensive client profile.
        """
        try:
            # Step 1: Add contact
            contact_result = await self.add_contact_atomic(name, email, company, notes)
            
            if not contact_result["success"]:
                return contact_result
            
            # Step 2: Create initial task to follow up
            followup_task = await self.create_task_atomic(
                title=f"Follow up with {name}",
                description=f"Initial follow up with new contact {name}",
                assignee="account_manager",
                due_date=(datetime.now() + timedelta(days=7)).isoformat()
            )
            
            # Step 3: Send welcome email (if company provided)
            email_result = None
            if company:
                welcome_email = await self.send_email_atomic(
                    recipient=email,
                    subject=f"Welcome, {name}!",
                    body=f"Thank you for connecting with us, {name} from {company}."
                )
                email_result = welcome_email
            
            return {
                "success": True,
                "contact_result": contact_result,
                "followup_task": followup_task,
                "welcome_email": email_result,
                "message": f"Client profile for {name} created successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def generate_client_report_composite(self, client_id: str, 
                                            report_period_days: int = 30) -> Dict:
        """
        Composite skill: Generate a comprehensive client report.
        """
        try:
            if client_id not in self.contacts:
                return {
                    "success": False,
                    "error": f"Contact with ID {client_id} not found"
                }
            
            client = self.contacts[client_id]
            
            # Find related events and tasks
            client_events = [
                event for event in self.calendar_events 
                if client["email"] in event.get("attendees", [])
            ]
            
            client_tasks = [
                task for task_id, task in self.tasks.items()
                if task.get("assignee", "").lower() == client["email"].lower() or 
                   client["name"].lower() in task.get("description", "").lower()
            ]
            
            # Generate report
            report = {
                "client": client,
                "period_days": report_period_days,
                "events_count": len(client_events),
                "tasks_count": len(client_tasks),
                "recent_events": client_events[-5:],  # Last 5 events
                "pending_tasks": [task for task in client_tasks if task.get("status") == "pending"],
                "completed_tasks": [task for task in client_tasks if task.get("status") == "completed"],
                "generated_at": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "report": report,
                "message": f"Report generated for {client['name']}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    # ADAPTIVE SKILLS
    async def prioritize_tasks_adaptive(self, user_preferences: Dict = None) -> Dict:
        """
        Adaptive skill: Prioritize tasks based on learned patterns and preferences.
        """
        try:
            # In a real implementation, this would use ML models to learn from past behavior
            # For now, we'll implement basic prioritization logic
            
            all_tasks = list(self.tasks.values())
            
            # Basic prioritization algorithm
            for task in all_tasks:
                priority_score = 0
                
                # Factor 1: Due date proximity (higher score for closer deadlines)
                if task.get("due_date"):
                    try:
                        due_dt = datetime.fromisoformat(task["due_date"].replace('Z', '+00:00'))
                        time_diff = (due_dt - datetime.now()).days
                        if time_diff <= 1:  # Due today or overdue
                            priority_score += 50
                        elif time_diff <= 7:  # Due this week
                            priority_score += 30
                        elif time_diff <= 30:  # Due this month
                            priority_score += 10
                    except:
                        pass  # Invalid date format
                
                # Factor 2: Task status (higher score for pending tasks)
                if task.get("status") == "pending":
                    priority_score += 20
                elif task.get("status") == "in_progress":
                    priority_score += 10
                
                # Factor 3: Task assignment (higher score for personally assigned)
                if task.get("assignee"):  # Assuming current user is primary assignee
                    priority_score += 15
                
                task["priority_score"] = priority_score
            
            # Sort by priority score (highest first)
            sorted_tasks = sorted(all_tasks, key=lambda x: x.get("priority_score", 0), reverse=True)
            
            # Apply user preferences if provided
            if user_preferences:
                # Adjust priorities based on user preferences
                for task in sorted_tasks:
                    if user_preferences.get("high_priority_projects"):
                        for project in user_preferences["high_priority_projects"]:
                            if project.lower() in task.get("title", "").lower() or \
                               project.lower() in task.get("description", "").lower():
                                task["priority_score"] += 25
                                task["adjusted_for_preference"] = True
            
            return {
                "success": True,
                "prioritized_tasks": sorted_tasks,
                "total_tasks": len(sorted_tasks),
                "preferences_applied": bool(user_preferences)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def optimize_workflow_adaptive(self, workflow_type: str, 
                                       performance_data: Dict = None) -> Dict:
        """
        Adaptive skill: Optimize workflow based on performance data and usage patterns.
        """
        try:
            # In a real implementation, this would analyze workflow performance
            # and suggest optimizations based on ML analysis
            optimization_suggestions = []
            
            if workflow_type == "meeting_scheduling":
                # Analyze meeting scheduling patterns
                meeting_count = len([e for e in self.calendar_events if "meeting" in e["title"].lower()])
                
                if meeting_count > 0:
                    avg_duration = sum(e["duration"] for e in self.calendar_events) / len(self.calendar_events)
                    optimization_suggestions.extend([
                        f"Average meeting duration is {avg_duration:.0f} minutes - consider optimizing for efficiency",
                        "Schedule buffer time between meetings to account for overruns",
                        "Batch similar meetings together to minimize context switching"
                    ])
            
            elif workflow_type == "client_communication":
                # Analyze email patterns
                email_count = len(self.email_queue)
                
                if email_count > 0:
                    # Calculate average response time if we had that data
                    optimization_suggestions.extend([
                        f"You've sent {email_count} emails recently - consider batching for efficiency",
                        "Use templates for common responses to save time",
                        "Schedule specific times for email processing rather than constant checking"
                    ])
            
            elif workflow_type == "task_management":
                # Analyze task completion patterns
                pending_tasks = [t for t in self.tasks.values() if t.get("status") == "pending"]
                completed_tasks = [t for t in self.tasks.values() if t.get("status") == "completed"]
                
                completion_rate = len(completed_tasks) / (len(pending_tasks) + len(completed_tasks)) if (len(pending_tasks) + len(completed_tasks)) > 0 else 0
                
                optimization_suggestions.extend([
                    f"Current task completion rate is {completion_rate:.1%}",
                    "Break larger tasks into smaller, manageable chunks",
                    "Set realistic deadlines to improve completion rates"
                ])
            
            # Apply performance data if provided
            if performance_data:
                # Adjust suggestions based on actual performance
                if performance_data.get("missed_deadlines", 0) > 3:
                    optimization_suggestions.insert(0, "⚠️ High number of missed deadlines detected - prioritize deadline management")
                
                if performance_data.get("response_time_avg", 0) > 24:  # hours
                    optimization_suggestions.insert(0, "⚠️ Slow response times detected - consider faster response protocols")
            
            return {
                "success": True,
                "workflow_type": workflow_type,
                "optimization_suggestions": optimization_suggestions,
                "suggestions_count": len(optimization_suggestions),
                "performance_data_considered": bool(performance_data)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Initialize the skills instance
business_skills = BusinessOperationsSkills()

# Define the functions that will be exposed as skills
async def send_email_skill(recipient: str, subject: str, body: str, 
                          attachments: List[str] = []) -> Dict:
    """Send an email to a recipient."""
    return await business_skills.send_email_atomic(recipient, subject, body, attachments)

async def schedule_meeting_skill(client_email: str, meeting_subject: str, 
                               preferred_times: List[str], location: str = "") -> Dict:
    """Schedule a meeting with a client."""
    return await business_skills.schedule_meeting_composite(
        client_email, meeting_subject, preferred_times, location
    )

async def create_client_profile_skill(name: str, email: str, 
                                    company: str = "", notes: str = "") -> Dict:
    """Create a comprehensive client profile."""
    return await business_skills.create_client_profile_composite(name, email, company, notes)

async def prioritize_tasks_skill(user_preferences: Dict = None) -> Dict:
    """Prioritize tasks based on learned patterns and preferences."""
    return await business_skills.prioritize_tasks_adaptive(user_preferences)

async def optimize_workflow_skill(workflow_type: str, 
                                performance_data: Dict = None) -> Dict:
    """Optimize workflow based on performance data and usage patterns."""
    return await business_skills.optimize_workflow_adaptive(workflow_type, performance_data)

# Export the skills
__all__ = [
    'send_email_skill',
    'schedule_meeting_skill',
    'create_client_profile_skill',
    'prioritize_tasks_skill',
    'optimize_workflow_skill'
]