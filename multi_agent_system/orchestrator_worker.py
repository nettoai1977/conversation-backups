"""
Multi-Agent System: Orchestrator-Worker Pattern
Implements the orchestrator-worker architecture pattern identified in the research
"""

import asyncio
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import uuid
from datetime import datetime
import json

class AgentRole(Enum):
    ORCHESTRATOR = "orchestrator"
    WORKER = "worker"
    SPECIALIST = "specialist"

class TaskStatus(Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Task:
    id: str
    description: str
    agent_role_required: AgentRole
    priority: int = 1  # Higher number = higher priority
    assigned_to: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class Agent:
    """Base class for all agents in the system"""
    def __init__(self, agent_id: str, role: AgentRole, capabilities: List[str]):
        self.id = agent_id
        self.role = role
        self.capabilities = capabilities
        self.status = "online"
        self.current_task = None
        self.task_history = []
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute a task assigned to this agent"""
        raise NotImplementedError("Subclasses must implement execute_task")
    
    def can_handle_task(self, task: Task) -> bool:
        """Check if this agent can handle the given task"""
        return True

class WorkerAgent(Agent):
    """Worker agent that executes tasks assigned by orchestrator"""
    def __init__(self, agent_id: str, capabilities: List[str], executor_func: Callable):
        super().__init__(agent_id, AgentRole.WORKER, capabilities)
        self.executor_func = executor_func
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute the assigned task"""
        try:
            # Update task status
            task.status = TaskStatus.IN_PROGRESS
            task.assigned_to = self.id
            
            # Execute the task using the provided function
            result = await self.executor_func(task.description) if asyncio.iscoroutinefunction(self.executor_func) else self.executor_func(task.description)
            
            # Update task completion
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            task.result = result
            
            # Add to history
            self.task_history.append(task)
            
            return {
                "success": True,
                "task_id": task.id,
                "result": result,
                "agent_id": self.id
            }
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now()
            
            return {
                "success": False,
                "task_id": task.id,
                "error": str(e),
                "agent_id": self.id
            }

class SpecialistAgent(Agent):
    """Specialized agent for specific types of tasks"""
    def __init__(self, agent_id: str, capabilities: List[str], specialist_executor: Callable):
        super().__init__(agent_id, AgentRole.SPECIALIST, capabilities)
        self.specialist_executor = specialist_executor
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute specialized tasks"""
        try:
            task.status = TaskStatus.IN_PROGRESS
            task.assigned_to = self.id
            
            result = await self.specialist_executor(task.description) if asyncio.iscoroutinefunction(self.specialist_executor) else self.specialist_executor(task.description)
            
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            task.result = result
            
            self.task_history.append(task)
            
            return {
                "success": True,
                "task_id": task.id,
                "result": result,
                "agent_id": self.id,
                "specialist": True
            }
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now()
            
            return {
                "success": False,
                "task_id": task.id,
                "error": str(e),
                "agent_id": self.id,
                "specialist": True
            }

class OrchestratorAgent(Agent):
    """Orchestrator agent that coordinates worker agents"""
    def __init__(self, agent_id: str):
        super().__init__(agent_id, AgentRole.ORCHESTRATOR, ["coordination", "task_management"])
        self.worker_agents: List[WorkerAgent] = []
        self.specialist_agents: List[SpecialistAgent] = []
        self.task_queue: List[Task] = []
        self.completed_tasks: List[Task] = []
        self.failed_tasks: List[Task] = []
    
    def add_worker_agent(self, worker: WorkerAgent):
        """Add a worker agent to the pool"""
        self.worker_agents.append(worker)
    
    def add_specialist_agent(self, specialist: SpecialistAgent):
        """Add a specialist agent to the pool"""
        self.specialist_agents.append(specialist)
    
    def add_task(self, task: Task):
        """Add a task to the queue"""
        self.task_queue.append(task)
        # Sort by priority (higher first)
        self.task_queue.sort(key=lambda t: t.priority, reverse=True)
    
    async def assign_tasks(self):
        """Assign tasks to available agents"""
        # Process tasks in priority order
        for task in self.task_queue[:]:  # Create a copy to iterate over
            if task.status != TaskStatus.PENDING:
                continue
                
            # Look for a suitable agent
            assigned = False
            
            # First, try specialists if the task requires special capabilities
            if task.agent_role_required == AgentRole.SPECIALIST:
                for specialist in self.specialist_agents:
                    if specialist.status == "online" and specialist.can_handle_task(task) and not specialist.current_task:
                        await self._assign_task_to_agent(task, specialist)
                        assigned = True
                        break
            
            # If not assigned to specialist, try regular workers
            if not assigned:
                for worker in self.worker_agents:
                    if worker.status == "online" and worker.can_handle_task(task) and not worker.current_task:
                        await self._assign_task_to_agent(task, worker)
                        assigned = True
                        break
            
            # If still not assigned, check for overloaded agents
            if not assigned:
                for worker in self.worker_agents:
                    if worker.status == "online" and worker.can_handle_task(task):
                        # Agent is busy but might take another task
                        # For now, we'll just leave it queued
                        break
    
    async def _assign_task_to_agent(self, task: Task, agent: Agent):
        """Private method to assign a task to an agent"""
        task.status = TaskStatus.ASSIGNED
        task.assigned_to = agent.id
        agent.current_task = task
        
        # Execute the task asynchronously
        result = await agent.execute_task(task)
        
        # Update orchestration records
        if result["success"]:
            self.completed_tasks.append(task)
            self.task_queue.remove(task)
        else:
            self.failed_tasks.append(task)
            self.task_queue.remove(task)
    
    async def process_tasks(self):
        """Main loop to process tasks"""
        while self.task_queue:
            await self.assign_tasks()
            # Small delay to prevent busy waiting
            await asyncio.sleep(0.1)
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """As orchestrator, execute by delegating to workers"""
        self.add_task(task)
        await self.process_tasks()
        
        # Return the result of the completed task
        completed_task = next((t for t in self.completed_tasks if t.id == task.id), None)
        if completed_task:
            return {
                "success": True,
                "task_id": task.id,
                "result": completed_task.result,
                "agent_id": self.id,
                "orchestrated": True
            }
        else:
            failed_task = next((t for t in self.failed_tasks if t.id == task.id), None)
            if failed_task:
                return {
                    "success": False,
                    "task_id": task.id,
                    "error": failed_task.error,
                    "agent_id": self.id,
                    "orchestrated": True
                }
            else:
                return {
                    "success": False,
                    "task_id": task.id,
                    "error": "Task not processed",
                    "agent_id": self.id,
                    "orchestrated": True
                }

class MultiAgentSystem:
    """Main class to manage the multi-agent system"""
    def __init__(self):
        self.orchestrator: Optional[OrchestratorAgent] = None
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
    
    def setup_orchestrator(self, agent_id: str = "orchestrator_1"):
        """Set up the orchestrator agent"""
        self.orchestrator = OrchestratorAgent(agent_id)
        self.agents[agent_id] = self.orchestrator
        return self.orchestrator
    
    def add_worker_agent(self, agent_id: str, capabilities: List[str], executor: Callable):
        """Add a worker agent to the system"""
        if not self.orchestrator:
            raise ValueError("Orchestrator must be set up first")
        
        worker = WorkerAgent(agent_id, capabilities, executor)
        self.orchestrator.add_worker_agent(worker)
        self.agents[agent_id] = worker
        return worker
    
    def add_specialist_agent(self, agent_id: str, capabilities: List[str], executor: Callable):
        """Add a specialist agent to the system"""
        if not self.orchestrator:
            raise ValueError("Orchestrator must be set up first")
        
        specialist = SpecialistAgent(agent_id, capabilities, executor)
        self.orchestrator.add_specialist_agent(specialist)
        self.agents[agent_id] = specialist
        return specialist
    
    async def submit_task(self, description: str, agent_role_required: AgentRole = AgentRole.WORKER, priority: int = 1):
        """Submit a task to the system"""
        if not self.orchestrator:
            raise ValueError("Orchestrator must be set up first")
        
        task = Task(
            id=str(uuid.uuid4()),
            description=description,
            agent_role_required=agent_role_required,
            priority=priority
        )
        
        self.tasks[task.id] = task
        self.orchestrator.add_task(task)
        
        # Process the task
        result = await self.orchestrator.execute_task(task)
        return result
    
    def get_agent_status(self):
        """Get status of all agents"""
        status = {}
        for agent_id, agent in self.agents.items():
            status[agent_id] = {
                "role": agent.role.value,
                "status": agent.status,
                "capabilities": agent.capabilities,
                "current_task": agent.current_task.id if agent.current_task else None,
                "task_count": len(agent.task_history)
            }
        return status

# Example usage and test functions
async def example_worker_executor(task_description: str):
    """Example executor function for worker agents"""
    # Simulate some work
    await asyncio.sleep(0.5)
    return f"Processed: {task_description}"

async def example_specialist_executor(task_description: str):
    """Example executor function for specialist agents"""
    # Simulate specialized work
    await asyncio.sleep(0.3)
    return f"Specialized processing: {task_description}"

async def run_example():
    """Run an example of the multi-agent system"""
    print("Setting up multi-agent system...")
    
    # Create the system
    mas = MultiAgentSystem()
    
    # Set up orchestrator
    orchestrator = mas.setup_orchestrator()
    
    # Add worker agents
    worker1 = mas.add_worker_agent("worker_1", ["general", "processing"], example_worker_executor)
    worker2 = mas.add_worker_agent("worker_2", ["general", "processing"], example_worker_executor)
    
    # Add specialist agent
    specialist1 = mas.add_specialist_agent("specialist_1", ["analysis", "complex"], example_specialist_executor)
    
    # Submit tasks
    print("\nSubmitting tasks...")
    
    # Submit a general task
    result1 = await mas.submit_task("Process document 1", AgentRole.WORKER, priority=2)
    print(f"Task 1 result: {result1}")
    
    # Submit another general task
    result2 = await mas.submit_task("Process document 2", AgentRole.WORKER, priority=1)
    print(f"Task 2 result: {result2}")
    
    # Submit a specialized task
    result3 = await mas.submit_task("Analyze complex data", AgentRole.SPECIALIST, priority=3)
    print(f"Task 3 result: {result3}")
    
    # Print agent status
    print("\nAgent Status:")
    status = mas.get_agent_status()
    for agent_id, info in status.items():
        print(f"  {agent_id}: {info}")

if __name__ == "__main__":
    asyncio.run(run_example())