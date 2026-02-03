"""
Multi-Agent System Orchestrator
Based on the research findings for multi-agent architectures
"""

import asyncio
from enum import Enum
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import uuid
from datetime import datetime

class AgentRole(str, Enum):
    RESEARCHER = "researcher"
    BUSINESS = "business"
    MONITORING = "monitoring"
    EMAIL = "email"
    CALENDAR = "calendar"
    TASK_MANAGER = "task_manager"

@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    role: AgentRole = AgentRole.RESEARCHER
    description: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    priority: int = 1  # 1-5, with 5 being highest priority
    deadline: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "pending"  # pending, in_progress, completed, failed

@dataclass
class AgentResponse:
    task_id: str
    success: bool
    result: Any = None
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, role: AgentRole, name: str):
        self.role = role
        self.name = name
        self.id = str(uuid.uuid4())
        
    @abstractmethod
    async def execute_task(self, task: Task) -> AgentResponse:
        """Execute a task and return the result"""
        pass

class ResearchAgent(BaseAgent):
    """Agent responsible for research and data gathering"""
    
    def __init__(self):
        super().__init__(AgentRole.RESEARCHER, "Research Agent")
        
    async def execute_task(self, task: Task) -> AgentResponse:
        """Execute research-related tasks"""
        try:
            # Import the research & analysis MCP tools
            # In a real implementation, this would connect to the MCP server
            print(f"[{self.name}] Executing research task: {task.description}")
            
            # Simulate using research tools
            if "scrape" in task.description.lower():
                # Simulate using the research & analysis server
                result = {
                    "success": True,
                    "data": f"Simulated scraped data for {task.parameters.get('url', 'unknown')}",
                    "source": "research_agent_simulation"
                }
            elif "analyze" in task.description.lower():
                # Simulate content analysis
                result = {
                    "success": True,
                    "analysis": "Simulated content analysis result",
                    "metrics": {"relevance": 0.8, "confidence": 0.9}
                }
            else:
                result = {
                    "success": True,
                    "message": f"Research task completed: {task.description}",
                    "details": task.parameters
                }
                
            return AgentResponse(
                task_id=task.id,
                success=True,
                result=result
            )
        except Exception as e:
            return AgentResponse(
                task_id=task.id,
                success=False,
                error=str(e)
            )

class BusinessAgent(BaseAgent):
    """Agent responsible for business operations"""
    
    def __init__(self):
        super().__init__(AgentRole.BUSINESS, "Business Agent")
        
    async def execute_task(self, task: Task) -> AgentResponse:
        """Execute business-related tasks"""
        try:
            print(f"[{self.name}] Executing business task: {task.description}")
            
            # Simulate using business operations tools
            if "email" in task.description.lower():
                # Simulate using the business ops server for email
                result = {
                    "success": True,
                    "action": "email_sent",
                    "recipient": task.parameters.get("recipient", "unknown"),
                    "message_id": f"email_{uuid.uuid4()}"
                }
            elif "calendar" in task.description.lower():
                # Simulate using the business ops server for calendar
                result = {
                    "success": True,
                    "action": "event_created",
                    "event_id": f"event_{uuid.uuid4()}",
                    "datetime": task.parameters.get("datetime", "unknown")
                }
            elif "contact" in task.description.lower():
                # Simulate using the business ops server for contacts
                result = {
                    "success": True,
                    "action": "contact_created",
                    "contact_id": f"contact_{uuid.uuid4()}",
                    "name": task.parameters.get("name", "unknown")
                }
            else:
                result = {
                    "success": True,
                    "message": f"Business task completed: {task.description}",
                    "details": task.parameters
                }
                
            return AgentResponse(
                task_id=task.id,
                success=True,
                result=result
            )
        except Exception as e:
            return AgentResponse(
                task_id=task.id,
                success=False,
                error=str(e)
            )

class MonitoringAgent(BaseAgent):
    """Agent responsible for monitoring and alerts"""
    
    def __init__(self):
        super().__init__(AgentRole.MONITORING, "Monitoring Agent")
        
    async def execute_task(self, task: Task) -> AgentResponse:
        """Execute monitoring tasks"""
        try:
            print(f"[{self.name}] Executing monitoring task: {task.description}")
            
            # Simulate monitoring operations
            if "status" in task.description.lower():
                result = {
                    "success": True,
                    "service": task.parameters.get("service", "unknown"),
                    "status": "operational",
                    "timestamp": datetime.now().isoformat()
                }
            elif "alert" in task.description.lower():
                result = {
                    "success": True,
                    "alert_type": task.parameters.get("type", "general"),
                    "message": task.parameters.get("message", "Monitoring alert"),
                    "severity": task.parameters.get("severity", "medium")
                }
            else:
                result = {
                    "success": True,
                    "message": f"Monitoring task completed: {task.description}",
                    "details": task.parameters
                }
                
            return AgentResponse(
                task_id=task.id,
                success=True,
                result=result
            )
        except Exception as e:
            return AgentResponse(
                task_id=task.id,
                success=False,
                error=str(e)
            )

class EmailAgent(BaseAgent):
    """Agent responsible for email operations"""
    
    def __init__(self):
        super().__init__(AgentRole.EMAIL, "Email Agent")
        
    async def execute_task(self, task: Task) -> AgentResponse:
        """Execute email-related tasks"""
        try:
            print(f"[{self.name}] Executing email task: {task.description}")
            
            # Simulate using email MCP tools
            if "send" in task.description.lower():
                result = {
                    "success": True,
                    "action": "email_sent",
                    "to": task.parameters.get("to", []),
                    "subject": task.parameters.get("subject", ""),
                    "message_id": f"email_{uuid.uuid4()}",
                    "timestamp": datetime.now().isoformat()
                }
            elif "read" in task.description.lower():
                result = {
                    "success": True,
                    "action": "emails_fetched",
                    "count": task.parameters.get("limit", 5),
                    "folder": task.parameters.get("folder", "INBOX")
                }
            else:
                result = {
                    "success": True,
                    "message": f"Email task completed: {task.description}",
                    "details": task.parameters
                }
                
            return AgentResponse(
                task_id=task.id,
                success=True,
                result=result
            )
        except Exception as e:
            return AgentResponse(
                task_id=task.id,
                success=False,
                error=str(e)
            )

class CalendarAgent(BaseAgent):
    """Agent responsible for calendar operations"""
    
    def __init__(self):
        super().__init__(AgentRole.CALENDAR, "Calendar Agent")
        
    async def execute_task(self, task: Task) -> AgentResponse:
        """Execute calendar-related tasks"""
        try:
            print(f"[{self.name}] Executing calendar task: {task.description}")
            
            # Simulate using calendar MCP tools
            if "schedule" in task.description.lower() or "create" in task.description.lower():
                result = {
                    "success": True,
                    "action": "event_created",
                    "event_id": f"event_{uuid.uuid4()}",
                    "title": task.parameters.get("title", ""),
                    "datetime": task.parameters.get("datetime", ""),
                    "attendees": task.parameters.get("attendees", [])
                }
            elif "check" in task.description.lower() or "availability" in task.description.lower():
                result = {
                    "success": True,
                    "action": "availability_checked",
                    "available_slots": ["2024-01-15T10:00:00", "2024-01-15T14:00:00"],
                    "requested_dates": task.parameters.get("dates", [])
                }
            else:
                result = {
                    "success": True,
                    "message": f"Calendar task completed: {task.description}",
                    "details": task.parameters
                }
                
            return AgentResponse(
                task_id=task.id,
                success=True,
                result=result
            )
        except Exception as e:
            return AgentResponse(
                task_id=task.id,
                success=False,
                error=str(e)
            )

class TaskManagerAgent(BaseAgent):
    """Agent responsible for task coordination and management"""
    
    def __init__(self):
        super().__init__(AgentRole.TASK_MANAGER, "Task Manager Agent")
        
    async def execute_task(self, task: Task) -> AgentResponse:
        """Execute task management tasks"""
        try:
            print(f"[{self.name}] Executing task management: {task.description}")
            
            # Simulate task management operations
            result = {
                "success": True,
                "action": "task_managed",
                "task_id": task.id,
                "operation": task.description,
                "parameters": task.parameters
            }
                
            return AgentResponse(
                task_id=task.id,
                success=True,
                result=result
            )
        except Exception as e:
            return AgentResponse(
                task_id=task.id,
                success=False,
                error=str(e)
            )

class Orchestrator:
    """Main orchestrator for the multi-agent system"""
    
    def __init__(self):
        self.agents: Dict[AgentRole, BaseAgent] = {}
        self.task_queue: List[Task] = []
        self.completed_tasks: List[AgentResponse] = []
        self.running = False
        
        # Initialize all agents
        self._initialize_agents()
        
    def _initialize_agents(self):
        """Initialize all specialized agents"""
        self.agents[AgentRole.RESEARCHER] = ResearchAgent()
        self.agents[AgentRole.BUSINESS] = BusinessAgent()
        self.agents[AgentRole.MONITORING] = MonitoringAgent()
        self.agents[AgentRole.EMAIL] = EmailAgent()
        self.agents[AgentRole.CALENDAR] = CalendarAgent()
        self.agents[AgentRole.TASK_MANAGER] = TaskManagerAgent()
        
        print("Initialized agents:")
        for role, agent in self.agents.items():
            print(f"  - {agent.name} ({role.value})")
    
    def add_task(self, task: Task) -> str:
        """Add a task to the queue"""
        self.task_queue.append(task)
        print(f"Added task {task.id} for {task.role.value}: {task.description}")
        return task.id
    
    def create_task(self, role: AgentRole, description: str, parameters: Dict[str, Any] = None, 
                   priority: int = 1) -> str:
        """Convenience method to create and add a task"""
        task = Task(
            role=role,
            description=description,
            parameters=parameters or {},
            priority=priority
        )
        return self.add_task(task)
    
    async def execute_next_task(self) -> Optional[AgentResponse]:
        """Execute the next highest priority task in the queue"""
        if not self.task_queue:
            return None
            
        # Sort tasks by priority (highest first) and take the first one
        self.task_queue.sort(key=lambda t: t.priority, reverse=True)
        task = self.task_queue.pop(0)
        
        print(f"Executing task {task.id} with priority {task.priority}")
        
        # Find the appropriate agent
        if task.role not in self.agents:
            error_msg = f"No agent available for role: {task.role}"
            response = AgentResponse(
                task_id=task.id,
                success=False,
                error=error_msg
            )
            self.completed_tasks.append(response)
            return response
        
        agent = self.agents[task.role]
        response = await agent.execute_task(task)
        
        # Update task status
        task.status = "completed" if response.success else "failed"
        
        self.completed_tasks.append(response)
        return response
    
    async def execute_all_tasks(self):
        """Execute all tasks in the queue"""
        print(f"Starting execution of {len(self.task_queue)} tasks")
        
        while self.task_queue:
            response = await self.execute_next_task()
            if response:
                status = "SUCCESS" if response.success else "FAILED"
                print(f"Task {response.task_id} completed with status: {status}")
        
        print(f"All tasks executed. Total completed: {len(self.completed_tasks)}")
    
    async def run_worker_cycle(self, max_tasks: int = 10):
        """Run a cycle of task execution (for continuous operation)"""
        tasks_executed = 0
        while self.task_queue and tasks_executed < max_tasks:
            response = await self.execute_next_task()
            if response:
                tasks_executed += 1
                status = "SUCCESS" if response.success else "FAILED"
                print(f"Task {response.task_id} completed with status: {status}")
    
    def get_agent_by_role(self, role: AgentRole) -> Optional[BaseAgent]:
        """Get an agent by its role"""
        return self.agents.get(role)
    
    def get_completed_tasks(self) -> List[AgentResponse]:
        """Get all completed tasks"""
        return self.completed_tasks.copy()
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status"""
        role_counts = {}
        for task in self.task_queue:
            role_counts[task.role.value] = role_counts.get(task.role.value, 0) + 1
        
        return {
            "queue_size": len(self.task_queue),
            "completed_count": len(self.completed_tasks),
            "by_role": role_counts
        }

# Example usage and testing
async def demo_multi_agent_system():
    """Demonstrate the multi-agent system"""
    print("🚀 Starting Multi-Agent System Demo")
    print("=" * 50)
    
    # Create orchestrator
    orchestrator = Orchestrator()
    
    # Add various tasks to demonstrate different agents
    print("\n📋 Adding tasks to the system...")
    
    # Research tasks
    orchestrator.create_task(
        AgentRole.RESEARCHER,
        "Scrape website content",
        {"url": "https://example.com", "format": "markdown"},
        priority=3
    )
    
    orchestrator.create_task(
        AgentRole.RESEARCHER,
        "Analyze article sentiment",
        {"text": "This is a very positive article about technology advances", "type": "sentiment"},
        priority=2
    )
    
    # Business tasks
    orchestrator.create_task(
        AgentRole.BUSINESS,
        "Send follow-up email to client",
        {"recipient": "client@example.com", "subject": "Project Update", "body": "Here's the latest update..."},
        priority=4
    )
    
    orchestrator.create_task(
        AgentRole.BUSINESS,
        "Create new contact in CRM",
        {"name": "John Doe", "email": "john@example.com", "company": "Acme Corp"},
        priority=2
    )
    
    # Email tasks
    orchestrator.create_task(
        AgentRole.EMAIL,
        "Send notification email",
        {"to": ["team@company.com"], "subject": "System Alert", "body": "Important system notification"},
        priority=5
    )
    
    # Calendar tasks
    orchestrator.create_task(
        AgentRole.CALENDAR,
        "Schedule team meeting",
        {"title": "Weekly Team Sync", "datetime": "2024-01-15T10:00:00", "attendees": ["team@company.com"]},
        priority=3
    )
    
    # Monitoring tasks
    orchestrator.create_task(
        AgentRole.MONITORING,
        "Check system status",
        {"service": "web_server", "endpoint": "/health"},
        priority=1
    )
    
    # Display queue status
    status = orchestrator.get_queue_status()
    print(f"\n📊 Queue Status: {status}")
    
    # Execute all tasks
    print(f"\n⚙️  Executing {status['queue_size']} tasks...")
    await orchestrator.execute_all_tasks()
    
    # Show completion results
    print(f"\n📈 Execution Results:")
    results = orchestrator.get_completed_tasks()
    successful = sum(1 for r in results if r.success)
    failed = len(results) - successful
    
    print(f"  - Successful: {successful}")
    print(f"  - Failed: {failed}")
    print(f"  - Total: {len(results)}")
    
    print(f"\n🎯 Multi-Agent System Demo Complete!")

if __name__ == "__main__":
    asyncio.run(demo_multi_agent_system())