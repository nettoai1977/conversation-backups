"""
Skills Framework for OpenClaw
Implements the enhanced skills architecture based on research findings
"""

import asyncio
import inspect
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable, Union
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import logging
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SkillType(Enum):
    ATOMIC = "atomic"
    COMPOSITE = "composite"
    ADAPTIVE = "adaptive"

class SkillCategory(Enum):
    COMMUNICATION = "communication"
    BUSINESS = "business"
    RESEARCH = "research"
    SYSTEM = "system"
    PRODUCTIVITY = "productivity"

@dataclass
class SkillMetadata:
    """Metadata for a skill"""
    name: str
    description: str
    category: SkillCategory
    version: str = "1.0.0"
    author: str = "OpenClaw"
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class SkillInput:
    """Define input parameters for a skill"""
    name: str
    type_hint: str
    description: str
    required: bool = True
    default_value: Any = None

@dataclass
class SkillOutput:
    """Define output parameters for a skill"""
    name: str
    type_hint: str
    description: str

@dataclass
class SkillResult:
    """Result returned by a skill execution"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    skill_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

class BaseSkill(ABC):
    """Abstract base class for all skills"""
    
    def __init__(self, metadata: SkillMetadata):
        self.metadata = metadata
        self.skill_id = str(uuid.uuid4())
        self.execution_count = 0
        self.last_execution = None
        self.avg_execution_time = 0.0
        
    @abstractmethod
    async def execute(self, **kwargs) -> SkillResult:
        """Execute the skill with given parameters"""
        pass
    
    def validate_inputs(self, **kwargs) -> bool:
        """Validate input parameters"""
        # In a full implementation, this would validate against defined inputs
        return True

class AtomicSkill(BaseSkill):
    """Base class for atomic skills (single responsibility)"""
    
    def __init__(self, metadata: SkillMetadata, func: Callable):
        super().__init__(metadata)
        self.func = func
        self.type = SkillType.ATOMIC
        self.inputs = self._extract_inputs_from_func(func)
        
    def _extract_inputs_from_func(self, func: Callable) -> List[SkillInput]:
        """Extract input definitions from function signature"""
        inputs = []
        sig = inspect.signature(func)
        
        for param_name, param in sig.parameters.items():
            if param_name == 'self':  # Skip 'self' parameter for class methods
                continue
                
            input_def = SkillInput(
                name=param_name,
                type_hint=str(param.annotation) if param.annotation != inspect.Parameter.empty else "Any",
                description=f"Parameter {param_name} for {self.metadata.name}",
                required=param.default == inspect.Parameter.empty,
                default_value=param.default if param.default != inspect.Parameter.empty else None
            )
            inputs.append(input_def)
        
        return inputs
    
    async def execute(self, **kwargs) -> SkillResult:
        """Execute the atomic skill function"""
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Validate inputs
            if not self.validate_inputs(**kwargs):
                raise ValueError("Invalid input parameters")
            
            # Execute the function
            if asyncio.iscoroutinefunction(self.func):
                result = await self.func(**kwargs)
            else:
                result = self.func(**kwargs)
            
            execution_time = (asyncio.get_event_loop().time() - start_time) * 1000
            
            # Update statistics
            self.execution_count += 1
            total_time = (self.avg_execution_time * (self.execution_count - 1)) + execution_time
            self.avg_execution_time = total_time / self.execution_count
            self.last_execution = datetime.now()
            
            logger.info(f"Skill {self.metadata.name} executed successfully in {execution_time:.2f}ms")
            
            return SkillResult(
                success=True,
                data=result,
                execution_time_ms=execution_time,
                skill_id=self.skill_id
            )
            
        except Exception as e:
            execution_time = (asyncio.get_event_loop().time() - start_time) * 1000
            logger.error(f"Skill {self.metadata.name} failed: {str(e)}")
            
            return SkillResult(
                success=False,
                error=str(e),
                execution_time_ms=execution_time,
                skill_id=self.skill_id
            )

class CompositeSkill(BaseSkill):
    """Base class for composite skills (combinations of other skills)"""
    
    def __init__(self, metadata: SkillMetadata, skill_chain: List[Union[str, Callable]]):
        super().__init__(metadata)
        self.skill_chain = skill_chain  # List of skill names or functions to execute
        self.type = SkillType.COMPOSITE
        self.inputs = []  # Will be determined by the composition
        
    async def execute(self, **kwargs) -> SkillResult:
        """Execute the composite skill by running its component skills"""
        start_time = asyncio.get_event_loop().time()
        
        try:
            result_data = kwargs  # Start with initial parameters
            
            for i, skill_ref in enumerate(self.skill_chain):
                logger.info(f"Executing step {i+1}/{len(self.skill_chain)} in composite skill")
                
                # In a full implementation, this would resolve the skill reference
                # and execute it with the current result_data as input
                if callable(skill_ref):
                    # Execute directly if it's a function
                    if asyncio.iscoroutinefunction(skill_ref):
                        result_data = await skill_ref(**result_data)
                    else:
                        result_data = skill_ref(**result_data)
                else:
                    # In a real implementation, this would look up the skill by name
                    # For now, we'll simulate execution
                    logger.info(f"Would execute skill: {skill_ref}")
                    result_data[f"step_{i}_result"] = f"simulated_result_for_{skill_ref}"
            
            execution_time = (asyncio.get_event_loop().time() - start_time) * 1000
            
            # Update statistics
            self.execution_count += 1
            total_time = (self.avg_execution_time * (self.execution_count - 1)) + execution_time
            self.avg_execution_time = total_time / self.execution_count
            self.last_execution = datetime.now()
            
            logger.info(f"Composite skill {self.metadata.name} executed successfully in {execution_time:.2f}ms")
            
            return SkillResult(
                success=True,
                data=result_data,
                execution_time_ms=execution_time,
                skill_id=self.skill_id
            )
            
        except Exception as e:
            execution_time = (asyncio.get_event_loop().time() - start_time) * 1000
            logger.error(f"Composite skill {self.metadata.name} failed: {str(e)}")
            
            return SkillResult(
                success=False,
                error=str(e),
                execution_time_ms=execution_time,
                skill_id=self.skill_id
            )

class AdaptiveSkill(BaseSkill):
    """Base class for adaptive skills (learning and improving over time)"""
    
    def __init__(self, metadata: SkillMetadata, base_skill: BaseSkill):
        super().__init__(metadata)
        self.base_skill = base_skill
        self.type = SkillType.ADAPTIVE
        self.performance_history = []
        self.optimization_params = {}
        
    async def execute(self, **kwargs) -> SkillResult:
        """Execute the adaptive skill with learning capabilities"""
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Apply optimizations based on history
            optimized_kwargs = await self._apply_optimizations(kwargs)
            
            # Execute the base skill
            result = await self.base_skill.execute(**optimized_kwargs)
            
            execution_time = (asyncio.get_event_loop().time() - start_time) * 1000
            
            # Record performance for learning
            await self._record_performance(result, execution_time, kwargs)
            
            logger.info(f"Adaptive skill {self.metadata.name} executed successfully in {execution_time:.2f}ms")
            
            return result
            
        except Exception as e:
            execution_time = (asyncio.get_event_loop().time() - start_time) * 1000
            logger.error(f"Adaptive skill {self.metadata.name} failed: {str(e)}")
            
            return SkillResult(
                success=False,
                error=str(e),
                execution_time_ms=execution_time,
                skill_id=self.skill_id
            )
    
    async def _apply_optimizations(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Apply learned optimizations to input parameters"""
        # In a full implementation, this would modify parameters based on learned patterns
        return kwargs
    
    async def _record_performance(self, result: SkillResult, execution_time: float, inputs: Dict[str, Any]):
        """Record performance data for learning"""
        performance_entry = {
            "timestamp": datetime.now(),
            "execution_time_ms": execution_time,
            "success": result.success,
            "inputs": inputs,
            "result_summary": str(result.data)[:200] if result.data else None  # Truncate for storage
        }
        self.performance_history.append(performance_entry)
        
        # Keep only recent history (last 100 entries)
        if len(self.performance_history) > 100:
            self.performance_history = self.performance_history[-100:]

class SkillRegistry:
    """Central registry for managing all skills"""
    
    def __init__(self):
        self.skills: Dict[str, BaseSkill] = {}
        self.skill_categories: Dict[SkillCategory, List[str]] = {}
        self.skill_tags: Dict[str, List[str]] = {}
        
    def register_skill(self, skill: BaseSkill) -> str:
        """Register a skill in the registry"""
        skill_id = skill.skill_id
        self.skills[skill_id] = skill
        
        # Index by category
        category = skill.metadata.category
        if category not in self.skill_categories:
            self.skill_categories[category] = []
        self.skill_categories[category].append(skill_id)
        
        # Index by tags
        for tag in skill.metadata.tags:
            if tag not in self.skill_tags:
                self.skill_tags[tag] = []
            self.skill_tags[tag].append(skill_id)
        
        logger.info(f"Registered skill '{skill.metadata.name}' with ID: {skill_id}")
        return skill_id
    
    def get_skill(self, skill_id: str) -> Optional[BaseSkill]:
        """Retrieve a skill by ID"""
        return self.skills.get(skill_id)
    
    def find_skills_by_category(self, category: SkillCategory) -> List[BaseSkill]:
        """Find all skills in a specific category"""
        skill_ids = self.skill_categories.get(category, [])
        return [self.skills[sid] for sid in skill_ids if sid in self.skills]
    
    def find_skills_by_tag(self, tag: str) -> List[BaseSkill]:
        """Find all skills with a specific tag"""
        skill_ids = self.skill_tags.get(tag, [])
        return [self.skills[sid] for sid in skill_ids if sid in self.skills]
    
    def find_skills_by_name(self, name: str) -> List[BaseSkill]:
        """Find skills by name (partial match)"""
        matching_skills = []
        for skill in self.skills.values():
            if name.lower() in skill.metadata.name.lower():
                matching_skills.append(skill)
        return matching_skills
    
    def list_all_skills(self) -> List[BaseSkill]:
        """List all registered skills"""
        return list(self.skills.values())
    
    def execute_skill(self, skill_id: str, **kwargs) -> asyncio.Future:
        """Execute a skill asynchronously"""
        skill = self.get_skill(skill_id)
        if not skill:
            raise ValueError(f"Skill with ID {skill_id} not found")
        
        return asyncio.create_task(skill.execute(**kwargs))

# Example skill implementations based on research categories
def create_example_skills(registry: SkillRegistry):
    """Create example skills based on the research findings"""
    
    # Communication Skills
    def send_email(to: str, subject: str, body: str, attachments: List[str] = None) -> Dict[str, Any]:
        """Send an email to the specified recipient"""
        import time
        time.sleep(0.1)  # Simulate API call
        return {
            "success": True,
            "message_id": f"msg_{uuid.uuid4()}",
            "recipients": [to],
            "timestamp": datetime.now().isoformat()
        }
    
    email_metadata = SkillMetadata(
        name="send_email",
        description="Send an email to the specified recipient",
        category=SkillCategory.COMMUNICATION,
        tags=["email", "communication", "notification"]
    )
    
    send_email_skill = AtomicSkill(email_metadata, send_email)
    registry.register_skill(send_email_skill)
    
    # Business Operations Skills
    def create_calendar_event(title: str, start_time: str, duration_minutes: int, 
                           attendees: List[str] = None, location: str = "") -> Dict[str, Any]:
        """Create a calendar event"""
        import time
        time.sleep(0.1)  # Simulate API call
        return {
            "success": True,
            "event_id": f"event_{uuid.uuid4()}",
            "title": title,
            "start_time": start_time,
            "attendees": attendees or [],
            "status": "confirmed"
        }
    
    calendar_metadata = SkillMetadata(
        name="create_calendar_event",
        description="Create a calendar event with specified details",
        category=SkillCategory.BUSINESS,
        tags=["calendar", "scheduling", "meeting"]
    )
    
    calendar_skill = AtomicSkill(calendar_metadata, create_calendar_event)
    registry.register_skill(calendar_skill)
    
    # Research & Analysis Skills
    def analyze_content(text: str, analysis_types: List[str] = None) -> Dict[str, Any]:
        """Analyze content based on specified analysis types"""
        import time
        time.sleep(0.1)  # Simulate processing
        
        analysis_types = analysis_types or ["sentiment"]
        results = {}
        
        if "sentiment" in analysis_types:
            results["sentiment"] = "positive"  # Simplified analysis
        if "keywords" in analysis_types:
            results["keywords"] = ["example", "keyword", "analysis"]
        
        return {
            "success": True,
            "analysis_results": results,
            "word_count": len(text.split()),
            "analysis_types": analysis_types
        }
    
    analysis_metadata = SkillMetadata(
        name="analyze_content",
        description="Analyze content with various analysis techniques",
        category=SkillCategory.RESEARCH,
        tags=["analysis", "content", "text-processing"]
    )
    
    analysis_skill = AtomicSkill(analysis_metadata, analyze_content)
    registry.register_skill(analysis_skill)
    
    # System Skills
    def get_system_stats(cpu: bool = True, memory: bool = True, 
                        disk: bool = True, network: bool = False) -> Dict[str, Any]:
        """Get system statistics"""
        import psutil
        import time
        time.sleep(0.05)  # Simulate quick check
        
        stats = {"timestamp": datetime.now().isoformat()}
        
        if cpu:
            stats["cpu_percent"] = psutil.cpu_percent(interval=0.1)
        if memory:
            mem = psutil.virtual_memory()
            stats["memory_percent"] = mem.percent
        if disk:
            disk_usage = psutil.disk_usage('/')
            stats["disk_percent"] = (disk_usage.used / disk_usage.total) * 100
        if network:
            net_io = psutil.net_io_counters()
            stats["network_bytes_sent"] = net_io.bytes_sent
            stats["network_bytes_recv"] = net_io.bytes_recv
        
        return {
            "success": True,
            "stats": stats
        }
    
    system_metadata = SkillMetadata(
        name="get_system_stats",
        description="Get system statistics (CPU, memory, disk, network)",
        category=SkillCategory.SYSTEM,
        tags=["system", "monitoring", "performance"]
    )
    
    system_skill = AtomicSkill(system_metadata, get_system_stats)
    registry.register_skill(system_skill)
    
    # Productivity Skills
    def create_task(title: str, description: str, assignee: str = "", 
                   due_date: str = "", tags: List[str] = None) -> Dict[str, Any]:
        """Create a new task in the system"""
        import time
        time.sleep(0.05)  # Simulate API call
        
        return {
            "success": True,
            "task_id": f"task_{uuid.uuid4()}",
            "title": title,
            "description": description,
            "assignee": assignee,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
    
    task_metadata = SkillMetadata(
        name="create_task",
        description="Create a new task with specified details",
        category=SkillCategory.PRODUCTIVITY,
        tags=["task", "productivity", "management"]
    )
    
    task_skill = AtomicSkill(task_metadata, create_task)
    registry.register_skill(task_skill)
    
    # Create a composite skill that combines multiple operations
    def schedule_meeting_with_followup(client_email: str, meeting_time: str, 
                                     topic: str = "Meeting") -> Dict[str, Any]:
        """Schedule a meeting and send a confirmation email"""
        # This would actually call other skills in sequence
        # For demonstration, we'll simulate the process
        event_result = create_calendar_event(
            title=f"{topic} with Client",
            start_time=meeting_time,
            duration_minutes=60,
            attendees=[client_email]
        )
        
        if event_result["success"]:
            email_result = send_email(
                to=client_email,
                subject=f"Confirmed: {topic} on {meeting_time}",
                body=f"Your {topic} has been scheduled for {meeting_time}. Event ID: {event_result['event_id']}"
            )
        else:
            email_result = {"success": False, "error": "Could not create calendar event"}
        
        return {
            "success": event_result["success"] and email_result["success"],
            "calendar_result": event_result,
            "email_result": email_result,
            "overall_status": "scheduled" if event_result["success"] and email_result["success"] else "failed"
        }
    
    meeting_metadata = SkillMetadata(
        name="schedule_meeting_with_followup",
        description="Schedule a meeting and send confirmation email",
        category=SkillCategory.BUSINESS,
        tags=["meeting", "scheduling", "automation"],
        dependencies=["create_calendar_event", "send_email"]
    )
    
    meeting_skill = CompositeSkill(meeting_metadata, [
        create_calendar_event,
        send_email
    ])
    registry.register_skill(meeting_skill)
    
    logger.info("Example skills registered successfully")

# Example usage
async def demo_skills_framework():
    """Demonstrate the skills framework"""
    print("🚀 Starting Skills Framework Demo")
    print("=" * 50)
    
    # Create registry and register example skills
    registry = SkillRegistry()
    create_example_skills(registry)
    
    # List all skills
    print(f"\n📋 Registered Skills ({len(registry.list_all_skills())}):")
    for skill in registry.list_all_skills():
        print(f"  - {skill.metadata.name} ({skill.metadata.category.value}) [{skill.type.value}]")
    
    # Test executing an atomic skill
    print(f"\n🧪 Testing atomic skill execution...")
    send_email_skill = registry.find_skills_by_name("send_email")[0]
    
    result = await send_email_skill.execute(
        to="test@example.com",
        subject="Test Email",
        body="This is a test email from the skills framework"
    )
    
    print(f"Email skill result: {result.success}")
    print(f"Execution time: {result.execution_time_ms:.2f}ms")
    print(f"Result data: {result.data}")
    
    # Test executing a composite skill
    print(f"\n🧪 Testing composite skill execution...")
    meeting_skill = registry.find_skills_by_name("schedule_meeting_with_followup")[0]
    
    result = await meeting_skill.execute(
        client_email="client@example.com",
        meeting_time="2024-01-15T10:00:00",
        topic="Project Discussion"
    )
    
    print(f"Meeting skill result: {result.success}")
    print(f"Execution time: {result.execution_time_ms:.2f}ms")
    print(f"Overall status: {result.data['overall_status']}")
    
    # Test finding skills by category
    print(f"\n🔍 Finding skills by category...")
    business_skills = registry.find_skills_by_category(SkillCategory.BUSINESS)
    print(f"Business skills: {[s.metadata.name for s in business_skills]}")
    
    # Test finding skills by tag
    print(f"\n🏷️  Finding skills by tag...")
    communication_skills = registry.find_skills_by_tag("communication")
    print(f"Communication skills: {[s.metadata.name for s in communication_skills]}")
    
    print(f"\n🎯 Skills Framework Demo Complete!")

if __name__ == "__main__":
    asyncio.run(demo_skills_framework())