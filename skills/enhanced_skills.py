"""
Enhanced Skills System for OpenClaw
Expands on the basic skills registry with advanced capabilities
"""

from typing import Dict, List, Any, Optional, Callable, Union, Type
from dataclasses import dataclass
from enum import Enum
import asyncio
import inspect
from pydantic import BaseModel, ValidationError
import time
import logging
from functools import wraps

# Enhanced enums and types
class SkillCategory(Enum):
    COMMUNICATION = "communication"
    PRODUCTIVITY = "productivity"
    RESEARCH = "research"
    SYSTEM = "system"
    BUSINESS = "business"
    DEVELOPMENT = "development"

class SkillPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

# Enhanced skill metadata
@dataclass
class EnhancedSkillMetadata:
    name: str
    description: str
    category: SkillCategory
    version: str
    author: str
    dependencies: List[str]
    priority: SkillPriority
    estimated_duration_seconds: float
    success_rate: float  # Historical success rate
    last_used: Optional[float] = None
    usage_count: int = 0

# Base skill class with enhanced functionality
class EnhancedSkill:
    """Enhanced base class for skills with additional features"""
    
    def __init__(
        self, 
        name: str, 
        description: str, 
        category: SkillCategory,
        priority: SkillPriority = SkillPriority.MEDIUM,
        estimated_duration: float = 1.0
    ):
        self.name = name
        self.description = description
        self.category = category
        self.priority = priority
        self.estimated_duration = estimated_duration
        self.metadata = EnhancedSkillMetadata(
            name=name,
            description=description,
            category=category,
            version="1.0.0",
            author="OpenClaw",
            dependencies=[],
            priority=priority,
            estimated_duration_seconds=estimated_duration,
            success_rate=0.0,
            usage_count=0
        )
        self.execution_history = []
        self.logger = logging.getLogger(f"skill.{name}")
        
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the skill with enhanced logging and error handling"""
        start_time = time.time()
        self.metadata.last_used = start_time
        self.metadata.usage_count += 1
        
        try:
            result = await self._execute_impl(**kwargs)
            
            # Calculate success rate based on history
            if not hasattr(self, '_success_count'):
                self._success_count = 0
            if result.get("success", False):
                self._success_count += 1
            self.metadata.success_rate = self._success_count / self.metadata.usage_count if self.metadata.usage_count > 0 else 0.0
            
            # Record execution
            execution_record = {
                "timestamp": start_time,
                "duration": time.time() - start_time,
                "success": result.get("success", False),
                "input": kwargs,
                "output": result
            }
            self.execution_history.append(execution_record)
            
            return result
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e),
                "skill": self.name,
                "duration": time.time() - start_time
            }
            
            # Record failure
            execution_record = {
                "timestamp": start_time,
                "duration": time.time() - start_time,
                "success": False,
                "input": kwargs,
                "output": error_result,
                "exception": str(e)
            }
            self.execution_history.append(execution_record)
            
            return error_result
    
    async def _execute_impl(self, **kwargs) -> Dict[str, Any]:
        """Implementation method to be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement _execute_impl")
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for the skill"""
        if not self.execution_history:
            return {"error": "No execution history"}
        
        durations = [record["duration"] for record in self.execution_history]
        avg_duration = sum(durations) / len(durations)
        
        successes = [record for record in self.execution_history if record["success"]]
        success_rate = len(successes) / len(self.execution_history)
        
        return {
            "total_executions": len(self.execution_history),
            "success_rate": success_rate,
            "average_duration": avg_duration,
            "min_duration": min(durations),
            "max_duration": max(durations),
            "last_execution": self.execution_history[-1]["timestamp"] if self.execution_history else None
        }

# Atomic skill with validation
class ValidatedAtomicSkill(EnhancedSkill):
    """Atomic skill with input/output validation"""
    
    def __init__(
        self, 
        name: str, 
        description: str, 
        category: SkillCategory,
        executor: Callable,
        input_schema: Optional[Type[BaseModel]] = None,
        output_schema: Optional[Type[BaseModel]] = None,
        priority: SkillPriority = SkillPriority.MEDIUM
    ):
        super().__init__(name, description, category, priority)
        self.executor = executor
        self.input_schema = input_schema
        self.output_schema = output_schema
        
        # Extract function signature for documentation
        sig = inspect.signature(executor)
        self.parameters = {name: param.annotation for name, param in sig.parameters.items()}
    
    async def _execute_impl(self, **kwargs) -> Dict[str, Any]:
        # Validate input if schema is provided
        if self.input_schema:
            try:
                validated_input = self.input_schema(**kwargs)
                validated_kwargs = validated_input.dict()
            except ValidationError as e:
                return {
                    "success": False,
                    "error": f"Input validation failed: {str(e)}",
                    "validation_errors": e.errors()
                }
        else:
            validated_kwargs = kwargs
        
        try:
            # Execute the function (could be sync or async)
            if asyncio.iscoroutinefunction(self.executor):
                result = await self.executor(**validated_kwargs)
            else:
                result = self.executor(**validated_kwargs)
            
            # Validate output if schema is provided
            if self.output_schema and result is not None:
                try:
                    validated_result = self.output_schema(**result if isinstance(result, dict) else {"result": result})
                    result = validated_result.dict()
                except ValidationError as e:
                    return {
                        "success": False,
                        "error": f"Output validation failed: {str(e)}",
                        "validation_errors": e.errors()
                    }
            
            return {
                "success": True,
                "result": result,
                "skill": self.name,
                "validated": True
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "skill": self.name
            }

# Composite skill with enhanced orchestration
class EnhancedCompositeSkill(EnhancedSkill):
    """Enhanced composite skill with better orchestration and error handling"""
    
    def __init__(
        self, 
        name: str, 
        description: str, 
        category: SkillCategory,
        skill_chain: List[Union[str, Dict]],  # Can be skill names or detailed configs
        priority: SkillPriority = SkillPriority.MEDIUM,
        continue_on_error: bool = False
    ):
        super().__init__(name, description, category, priority)
        self.skill_chain = skill_chain
        self.continue_on_error = continue_on_error
    
    async def _execute_impl(self, **kwargs) -> Dict[str, Any]:
        """Execute skills in sequence with context passing"""
        registry = EnhancedSkillsRegistry.get_instance()
        current_context = kwargs.copy()
        
        results = []
        skill_errors = []
        
        for i, skill_spec in enumerate(self.skill_chain):
            skill_name = skill_spec if isinstance(skill_spec, str) else skill_spec.get("name")
            skill_params = skill_spec if isinstance(skill_spec, dict) else {}
            
            skill = registry.get_skill(skill_name)
            if not skill:
                error = {
                    "index": i,
                    "skill_name": skill_name,
                    "error": f"Skill '{skill_name}' not found in registry"
                }
                skill_errors.append(error)
                
                if not self.continue_on_error:
                    return {
                        "success": False,
                        "error": f"Skill '{skill_name}' not found",
                        "partial_results": results,
                        "errors": skill_errors
                    }
                continue
            
            # Prepare parameters for this skill execution
            skill_kwargs = current_context.copy()
            if isinstance(skill_spec, dict):
                skill_kwargs.update({k: v for k, v in skill_spec.items() if k != "name"})
            
            # Execute the skill
            try:
                result = await skill.execute(**skill_kwargs)
                results.append({
                    "index": i,
                    "skill_name": skill_name,
                    "result": result
                })
                
                # Update context with result for next skill
                if result.get("success"):
                    # Merge result into context (avoid overwriting important context)
                    result_data = result.get("result", {})
                    if isinstance(result_data, dict):
                        current_context.update(result_data)
                
                # Check if we should continue
                if not result.get("success") and not self.continue_on_error:
                    return {
                        "success": False,
                        "error": result.get("error"),
                        "partial_results": results,
                        "failed_at": skill_name,
                        "context_at_failure": current_context
                    }
            except Exception as e:
                error = {
                    "index": i,
                    "skill_name": skill_name,
                    "error": str(e)
                }
                skill_errors.append(error)
                
                if not self.continue_on_error:
                    return {
                        "success": False,
                        "error": str(e),
                        "partial_results": results,
                        "errors": skill_errors
                    }
        
        return {
            "success": True,
            "results": results,
            "final_context": current_context,
            "skill": self.name,
            "errors": skill_errors if skill_errors else None
        }

# Adaptive skill that learns from experience
class AdaptiveSkill(EnhancedSkill):
    """Skill that adapts its behavior based on past experiences"""
    
    def __init__(
        self, 
        name: str, 
        description: str, 
        category: SkillCategory,
        executor: Callable,
        adaptation_strategy: str = "performance_based",
        priority: SkillPriority = SkillPriority.MEDIUM
    ):
        super().__init__(name, description, category, priority)
        self.executor = executor
        self.adaptation_strategy = adaptation_strategy
        self.performance_history = []
        self.adaptation_rules = []
    
    async def _execute_impl(self, **kwargs) -> Dict[str, Any]:
        # Adapt parameters based on historical performance
        adapted_kwargs = self._adapt_parameters(kwargs)
        
        try:
            if asyncio.iscoroutinefunction(self.executor):
                result = await self.executor(**adapted_kwargs)
            else:
                result = self.executor(**adapted_kwargs)
            
            # Record the execution for future adaptation
            self._record_execution(adapted_kwargs, result)
            
            return {
                "success": True,
                "result": result,
                "skill": self.name,
                "adapted": True,
                "original_params": kwargs,
                "adapted_params": adapted_kwargs
            }
        except Exception as e:
            # Record failure for adaptation
            self._record_execution(adapted_kwargs, {"success": False, "error": str(e)})
            return {
                "success": False,
                "error": str(e),
                "skill": self.name
            }
    
    def _adapt_parameters(self, original_params: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt parameters based on historical performance"""
        adapted = original_params.copy()
        
        if self.adaptation_strategy == "performance_based" and self.performance_history:
            # Example: Adjust timeout based on historical duration
            avg_duration = sum(p["duration"] for p in self.performance_history) / len(self.performance_history)
            if "timeout" in adapted and avg_duration > adapted["timeout"]:
                adapted["timeout"] = int(avg_duration * 1.5)  # Increase timeout by 50%
        
        return adapted
    
    def _record_execution(self, params: Dict[str, Any], result: Dict[str, Any]):
        """Record execution for adaptation"""
        record = {
            "timestamp": time.time(),
            "params": params,
            "result": result,
            "duration": result.get("duration", 0),
            "success": result.get("success", False)
        }
        self.performance_history.append(record)
        
        # Keep only recent history to avoid memory issues
        if len(self.performance_history) > 100:
            self.performance_history = self.performance_history[-50:]

# Enhanced skills registry
class EnhancedSkillsRegistry:
    """Enhanced registry with advanced features"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.skills: Dict[str, EnhancedSkill] = {}
            self.categories: Dict[SkillCategory, List[str]] = {cat: [] for cat in SkillCategory}
            self.priority_queue: List[str] = []
            self.initialized = True
    
    @classmethod
    def get_instance(cls):
        return cls()
    
    def register_skill(self, skill: EnhancedSkill) -> bool:
        """Register a skill with enhanced validation"""
        if skill.name in self.skills:
            print(f"Warning: Skill '{skill.name}' already exists, overwriting")
        
        self.skills[skill.name] = skill
        
        # Add to category mapping
        if skill.name not in self.categories[skill.category]:
            self.categories[skill.category].append(skill.name)
        
        # Add to priority queue (sorted by priority)
        self.priority_queue.append(skill.name)
        self.priority_queue.sort(key=lambda x: self.skills[x].priority.value, reverse=True)
        
        return True
    
    def get_skill(self, skill_name: str) -> Optional[EnhancedSkill]:
        """Retrieve a skill by name"""
        return self.skills.get(skill_name)
    
    def get_skills_by_category(self, category: SkillCategory) -> List[EnhancedSkill]:
        """Get all skills in a specific category"""
        skill_names = self.categories.get(category, [])
        return [self.skills[name] for name in skill_names if name in self.skills]
    
    def get_skills_by_priority(self, min_priority: SkillPriority) -> List[EnhancedSkill]:
        """Get skills with priority equal to or higher than specified"""
        return [self.skills[name] for name in self.priority_queue 
                if self.skills[name].priority.value >= min_priority.value]
    
    def get_all_skills(self) -> Dict[str, EnhancedSkill]:
        """Get all registered skills"""
        return self.skills.copy()
    
    def execute_skill(self, skill_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a skill by name"""
        skill = self.get_skill(skill_name)
        if not skill:
            return {
                "success": False,
                "error": f"Skill '{skill_name}' not found",
                "available_skills": list(self.skills.keys())
            }
        
        # Use asyncio.run if not already in an event loop
        try:
            loop = asyncio.get_running_loop()
            return skill.execute(**kwargs)
        except RuntimeError:
            # No event loop running
            return asyncio.run(skill.execute(**kwargs))
    
    def get_recommendations(self, category: SkillCategory, max_results: int = 5) -> List[Dict[str, Any]]:
        """Get recommended skills based on performance metrics"""
        skills = self.get_skills_by_category(category)
        recommendations = []
        
        for skill in skills:
            metrics = skill.get_performance_metrics()
            if "error" not in metrics:
                recommendations.append({
                    "skill_name": skill.name,
                    "success_rate": metrics["success_rate"],
                    "avg_duration": metrics["average_duration"],
                    "total_executions": metrics["total_executions"]
                })
        
        # Sort by success rate and execution count
        recommendations.sort(key=lambda x: (x["success_rate"], x["total_executions"]), reverse=True)
        return recommendations[:max_results]

# Example skill implementations with schemas
from pydantic import BaseModel, Field

class EmailInput(BaseModel):
    recipient: str = Field(..., description="Email recipient")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body content", max_length=10000)

class EmailOutput(BaseModel):
    success: bool
    message_id: str
    sent_at: str

class CalendarInput(BaseModel):
    title: str = Field(..., description="Event title")
    start_time: str = Field(..., description="Start time in ISO format")
    duration_minutes: int = Field(..., ge=15, le=1440, description="Duration in minutes")

class CalendarOutput(BaseModel):
    success: bool
    event_id: str
    status: str

def example_email_executor(input_data: EmailInput) -> EmailOutput:
    """Example email executor function"""
    import uuid
    from datetime import datetime
    
    # Simulate email sending
    return EmailOutput(
        success=True,
        message_id=f"msg_{uuid.uuid4()}",
        sent_at=datetime.now().isoformat()
    )

def example_calendar_executor(input_data: CalendarInput) -> CalendarOutput:
    """Example calendar executor function"""
    import uuid
    
    # Simulate calendar event creation
    return CalendarOutput(
        success=True,
        event_id=f"evt_{uuid.uuid4()}",
        status="confirmed"
    )

# Initialize the enhanced registry with example skills
def initialize_enhanced_skills_registry():
    """Initialize the enhanced skills registry with example skills"""
    registry = EnhancedSkillsRegistry.get_instance()
    
    # Register validated atomic skills
    registry.register_skill(ValidatedAtomicSkill(
        name="send_validated_email",
        description="Send an email with full validation",
        category=SkillCategory.COMMUNICATION,
        executor=example_email_executor,
        input_schema=EmailInput,
        output_schema=EmailOutput,
        priority=SkillPriority.HIGH
    ))
    
    registry.register_skill(ValidatedAtomicSkill(
        name="create_calendar_event_validated",
        description="Create a calendar event with validation",
        category=SkillCategory.PRODUCTIVITY,
        executor=example_calendar_executor,
        input_schema=CalendarInput,
        output_schema=CalendarOutput,
        priority=SkillPriority.HIGH
    ))
    
    # Register adaptive skills
    registry.register_skill(AdaptiveSkill(
        name="adaptive_web_search",
        description="Web search that adapts based on query complexity",
        category=SkillCategory.RESEARCH,
        executor=lambda query, timeout=10: {"results": [f"Result for {query}"], "query": query, "timeout_used": timeout},
        adaptation_strategy="performance_based"
    ))
    
    # Register composite skills
    registry.register_skill(EnhancedCompositeSkill(
        name="schedule_meeting_complete",
        description="Complete meeting scheduling workflow",
        category=SkillCategory.BUSINESS,
        skill_chain=[
            {
                "name": "create_calendar_event_validated",
                "title": "Meeting",
                "start_time": "2024-01-01T10:00:00",
                "duration_minutes": 60
            },
            {
                "name": "send_validated_email",
                "recipient": "attendee@example.com",
                "subject": "Meeting Confirmation",
                "body": "Your meeting has been scheduled."
            }
        ]
    ))

# Singleton instance
enhanced_skills_registry = EnhancedSkillsRegistry.get_instance()
initialize_enhanced_skills_registry()

# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def test_enhanced_skills():
        registry = EnhancedSkillsRegistry.get_instance()
        
        # Test validated atomic skill
        print("Testing validated atomic skill...")
        result = await registry.skills["send_validated_email"].execute(
            recipient="test@example.com",
            subject="Test Subject",
            body="This is a test email body."
        )
        print(f"Email result: {result}")
        
        # Test adaptive skill
        print("\nTesting adaptive skill...")
        result = await registry.skills["adaptive_web_search"].execute(query="OpenClaw")
        print(f"Search result: {result}")
        
        # Test composite skill
        print("\nTesting composite skill...")
        result = await registry.skills["schedule_meeting_complete"].execute()
        print(f"Meeting result: {result}")
        
        # Get recommendations
        print("\nGetting recommendations...")
        recs = registry.get_recommendations(SkillCategory.COMMUNICATION)
        print(f"Communication skill recommendations: {recs}")
        
        # Get performance metrics
        print("\nGetting performance metrics...")
        metrics = registry.skills["send_validated_email"].get_performance_metrics()
        print(f"Email skill metrics: {metrics}")
    
    asyncio.run(test_enhanced_skills())