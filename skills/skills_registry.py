"""
Skills Registry for OpenClaw
Implements the enhanced skills architecture with atomic, composite, and adaptive skills
"""

from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass
from enum import Enum
import inspect
import asyncio
from pydantic import BaseModel

class SkillType(Enum):
    ATOMIC = "atomic"
    COMPOSITE = "composite"
    ADAPTIVE = "adaptive"

@dataclass
class SkillMetadata:
    name: str
    description: str
    skill_type: SkillType
    category: str
    version: str
    author: str
    dependencies: List[str]

class Skill:
    """Base class for all skills"""
    def __init__(self, name: str, description: str, skill_type: SkillType, category: str):
        self.name = name
        self.description = description
        self.skill_type = skill_type
        self.category = category
        self.metadata = SkillMetadata(
            name=name,
            description=description,
            skill_type=skill_type,
            category=category,
            version="1.0.0",
            author="OpenClaw",
            dependencies=[]
        )
        self.input_schema = None
        self.output_schema = None
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the skill with given parameters"""
        raise NotImplementedError("Subclasses must implement execute method")
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input against schema"""
        return True  # Simplified for this implementation

class AtomicSkill(Skill):
    """Atomic skills perform single, specific functions"""
    def __init__(self, name: str, description: str, category: str, executor: Callable):
        super().__init__(name, description, SkillType.ATOMIC, category)
        self.executor = executor
        # Extract function signature for input validation
        sig = inspect.signature(executor)
        self.parameters = list(sig.parameters.keys())
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        try:
            # Filter kwargs to only include valid parameters
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in self.parameters}
            
            # Execute the function (could be sync or async)
            if asyncio.iscoroutinefunction(self.executor):
                result = await self.executor(**filtered_kwargs)
            else:
                result = self.executor(**filtered_kwargs)
            
            return {
                "success": True,
                "result": result,
                "skill": self.name
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "skill": self.name
            }

class CompositeSkill(Skill):
    """Composite skills combine multiple atomic skills"""
    def __init__(self, name: str, description: str, category: str, skill_chain: List[str]):
        super().__init__(name, description, SkillType.COMPOSITE, category)
        self.skill_chain = skill_chain  # Ordered list of skill names to execute
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute skills in sequence, passing results between them"""
        registry = SkillsRegistry.get_instance()
        current_context = kwargs.copy()
        
        try:
            results = []
            for skill_name in self.skill_chain:
                skill = registry.get_skill(skill_name)
                if not skill:
                    return {
                        "success": False,
                        "error": f"Skill '{skill_name}' not found in registry",
                        "failed_at": skill_name
                    }
                
                # Execute the skill with current context
                result = await skill.execute(**current_context)
                results.append(result)
                
                # Update context with result for next skill
                if result.get("success"):
                    current_context.update(result.get("result", {}))
                
                # Check if we should continue
                if not result.get("success"):
                    return {
                        "success": False,
                        "error": result.get("error"),
                        "partial_results": results,
                        "failed_at": skill_name
                    }
            
            return {
                "success": True,
                "results": results,
                "final_context": current_context,
                "skill": self.name
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "skill": self.name
            }

class SkillsRegistry:
    """Central registry for managing all skills"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.skills: Dict[str, Skill] = {}
            self.categories: Dict[str, List[str]] = {}
            self.initialized = True
    
    @classmethod
    def get_instance(cls):
        return cls()
    
    def register_skill(self, skill: Skill) -> bool:
        """Register a new skill in the registry"""
        if skill.name in self.skills:
            print(f"Warning: Skill '{skill.name}' already exists, overwriting")
        
        self.skills[skill.name] = skill
        
        # Add to category mapping
        if skill.category not in self.categories:
            self.categories[skill.category] = []
        if skill.name not in self.categories[skill.category]:
            self.categories[skill.category].append(skill.name)
        
        return True
    
    def get_skill(self, skill_name: str) -> Optional[Skill]:
        """Retrieve a skill by name"""
        return self.skills.get(skill_name)
    
    def get_skills_by_category(self, category: str) -> List[Skill]:
        """Get all skills in a specific category"""
        skill_names = self.categories.get(category, [])
        return [self.skills[name] for name in skill_names if name in self.skills]
    
    def get_all_skills(self) -> Dict[str, Skill]:
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
        
        return asyncio.run(skill.execute(**kwargs))

# Example skill implementations
def send_email_atomic(recipient: str, subject: str, body: str) -> Dict[str, Any]:
    """Example atomic skill: send an email"""
    # This would integrate with actual email service
    return {
        "status": "sent",
        "recipient": recipient,
        "subject": subject,
        "message_id": f"msg_{hash(recipient + subject)}"
    }

def check_calendar_atomic(date_range: str) -> Dict[str, Any]:
    """Example atomic skill: check calendar availability"""
    # This would integrate with actual calendar service
    return {
        "available_times": ["10:00", "14:00", "16:00"],
        "date_range": date_range
    }

def schedule_meeting_composite(recipient: str, preferred_times: List[str]) -> Dict[str, Any]:
    """Example composite skill: schedule a meeting by combining email and calendar skills"""
    # In a real implementation, this would call the skills registry
    # For now, we'll simulate the behavior
    return {
        "meeting_scheduled": True,
        "recipient": recipient,
        "time": preferred_times[0] if preferred_times else "10:00",
        "confirmation_code": f"conf_{hash(recipient + preferred_times[0] if preferred_times else 'default')}"
    }

# Initialize the registry with example skills
def initialize_skills_registry():
    """Initialize the skills registry with example skills"""
    registry = SkillsRegistry.get_instance()
    
    # Register atomic skills
    registry.register_skill(AtomicSkill(
        name="send_email",
        description="Send an email to a recipient",
        category="communication",
        executor=send_email_atomic
    ))
    
    registry.register_skill(AtomicSkill(
        name="check_calendar",
        description="Check calendar availability in a date range",
        category="productivity",
        executor=check_calendar_atomic
    ))
    
    # Register composite skills
    registry.register_skill(CompositeSkill(
        name="schedule_meeting",
        description="Schedule a meeting by coordinating email and calendar",
        category="productivity",
        skill_chain=["check_calendar", "send_email"]
    ))
    
    # Register more example skills
    registry.register_skill(AtomicSkill(
        name="search_web",
        description="Search the web for information",
        category="research",
        executor=lambda query: {"results": [f"Result for {query}"], "query": query}
    ))
    
    registry.register_skill(AtomicSkill(
        name="create_note",
        description="Create a note in the note-taking system",
        category="productivity",
        executor=lambda title, content: {"note_id": f"note_{hash(title)}", "title": title}
    ))
    
    registry.register_skill(CompositeSkill(
        name="research_and_summarize",
        description="Research a topic and create a summary note",
        category="research",
        skill_chain=["search_web", "create_note"]
    ))

# Singleton instance
skills_registry = SkillsRegistry.get_instance()
initialize_skills_registry()