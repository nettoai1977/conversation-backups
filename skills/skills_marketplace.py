"""
Skills Marketplace for OpenClaw
Implements the skill marketplace and orchestration engine concepts from the research
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import logging
from pathlib import Path
import aiofiles
from pydantic import BaseModel, Field

# Enums for the marketplace
class SkillStatus(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"

class SkillRating(Enum):
    ONE_STAR = 1
    TWO_STARS = 2
    THREE_STARS = 3
    FOUR_STARS = 4
    FIVE_STARS = 5

# Data models for the marketplace
@dataclass
class SkillPackage:
    """Represents a packaged skill with metadata"""
    id: str
    name: str
    description: str
    version: str
    author: str
    category: str
    status: SkillStatus
    created_at: datetime
    updated_at: datetime
    downloads: int
    rating: float
    tags: List[str]
    dependencies: List[str]
    code: str  # Serialized skill code
    schema: Dict[str, Any]  # Input/output schema
    documentation: str
    license: str

class Review(BaseModel):
    """Skill review model"""
    user_id: str
    rating: SkillRating
    comment: str = ""
    created_at: datetime = Field(default_factory=datetime.now)

class SkillMarketplace:
    """Skills marketplace implementation"""
    
    def __init__(self, storage_path: str = "./marketplace_storage"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        
        self.skills: Dict[str, SkillPackage] = {}
        self.reviews: Dict[str, List[Review]] = {}  # skill_id -> [reviews]
        self.downloads: Dict[str, List[Tuple[str, datetime]]] = {}  # skill_id -> [(user_id, timestamp)]
        self.user_ratings: Dict[str, Dict[str, SkillRating]] = {}  # user_id -> {skill_id: rating}
        
        self.logger = logging.getLogger("skills.marketplace")
        self._load_from_storage()
    
    def _get_skill_path(self, skill_id: str) -> Path:
        """Get the file path for a skill package"""
        return self.storage_path / f"{skill_id}.json"
    
    def _get_reviews_path(self, skill_id: str) -> Path:
        """Get the file path for skill reviews"""
        return self.storage_path / f"{skill_id}_reviews.json"
    
    async def _load_from_storage(self):
        """Load skills and reviews from storage"""
        for skill_file in self.storage_path.glob("*.json"):
            if not skill_file.name.endswith("_reviews.json"):
                try:
                    async with aiofiles.open(skill_file, 'r') as f:
                        data = json.loads(await f.read())
                        
                    skill = SkillPackage(
                        id=data['id'],
                        name=data['name'],
                        description=data['description'],
                        version=data['version'],
                        author=data['author'],
                        category=data['category'],
                        status=SkillStatus(data['status']),
                        created_at=datetime.fromisoformat(data['created_at']),
                        updated_at=datetime.fromisoformat(data['updated_at']),
                        downloads=data['downloads'],
                        rating=data['rating'],
                        tags=data['tags'],
                        dependencies=data['dependencies'],
                        code=data['code'],
                        schema=data['schema'],
                        documentation=data['documentation'],
                        license=data['license']
                    )
                    
                    self.skills[skill.id] = skill
                    
                    # Load reviews if they exist
                    reviews_path = self._get_reviews_path(skill.id)
                    if reviews_path.exists():
                        async with aiofiles.open(reviews_path, 'r') as f:
                            reviews_data = json.loads(await f.read())
                        
                        self.reviews[skill.id] = [
                            Review(
                                user_id=r['user_id'],
                                rating=SkillRating(r['rating']),
                                comment=r.get('comment', ''),
                                created_at=datetime.fromisoformat(r['created_at'])
                            ) for r in reviews_data
                        ]
                        
                        # Calculate average rating
                        if self.reviews[skill.id]:
                            total_rating = sum(review.rating.value for review in self.reviews[skill.id])
                            avg_rating = total_rating / len(self.reviews[skill.id])
                            skill.rating = round(avg_rating, 2)
                
                except Exception as e:
                    self.logger.error(f"Failed to load skill from {skill_file}: {e}")
    
    async def _save_skill(self, skill: SkillPackage):
        """Save a skill package to storage"""
        skill_data = {
            "id": skill.id,
            "name": skill.name,
            "description": skill.description,
            "version": skill.version,
            "author": skill.author,
            "category": skill.category,
            "status": skill.status.value,
            "created_at": skill.created_at.isoformat(),
            "updated_at": skill.updated_at.isoformat(),
            "downloads": skill.downloads,
            "rating": skill.rating,
            "tags": skill.tags,
            "dependencies": skill.dependencies,
            "code": skill.code,
            "schema": skill.schema,
            "documentation": skill.documentation,
            "license": skill.license
        }
        
        skill_path = self._get_skill_path(skill.id)
        async with aiofiles.open(skill_path, 'w') as f:
            await f.write(json.dumps(skill_data, indent=2))
    
    async def _save_reviews(self, skill_id: str):
        """Save reviews for a skill to storage"""
        if skill_id in self.reviews:
            reviews_data = [
                {
                    "user_id": r.user_id,
                    "rating": r.rating.value,
                    "comment": r.comment,
                    "created_at": r.created_at.isoformat()
                } for r in self.reviews[skill_id]
            ]
            
            reviews_path = self._get_reviews_path(skill_id)
            async with aiofiles.open(reviews_path, 'w') as f:
                await f.write(json.dumps(reviews_data, indent=2))
    
    async def publish_skill(self, 
                           name: str, 
                           description: str, 
                           category: str, 
                           code: str, 
                           schema: Dict[str, Any],
                           documentation: str = "",
                           version: str = "1.0.0",
                           author: str = "unknown",
                           tags: List[str] = None,
                           dependencies: List[str] = None,
                           license: str = "MIT") -> str:
        """Publish a new skill to the marketplace"""
        
        skill_id = str(uuid.uuid4())
        
        skill = SkillPackage(
            id=skill_id,
            name=name,
            description=description,
            version=version,
            author=author,
            category=category,
            status=SkillStatus.PUBLISHED,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            downloads=0,
            rating=0.0,
            tags=tags or [],
            dependencies=dependencies or [],
            code=code,
            schema=schema,
            documentation=documentation,
            license=license
        )
        
        self.skills[skill_id] = skill
        self.reviews[skill_id] = []
        
        await self._save_skill(skill)
        await self._save_reviews(skill_id)
        
        self.logger.info(f"Published skill: {name} (ID: {skill_id})")
        
        return skill_id
    
    async def get_skill(self, skill_id: str) -> Optional[SkillPackage]:
        """Get a skill by ID"""
        return self.skills.get(skill_id)
    
    async def search_skills(self, 
                           query: str = "", 
                           category: str = "", 
                           tags: List[str] = None,
                           min_rating: float = 0.0,
                           sort_by: str = "relevance") -> List[SkillPackage]:
        """Search for skills in the marketplace"""
        
        results = []
        
        for skill in self.skills.values():
            if skill.status != SkillStatus.PUBLISHED:
                continue
            
            # Apply filters
            if query and query.lower() not in skill.name.lower() and query.lower() not in skill.description.lower():
                continue
            
            if category and category.lower() != skill.category.lower():
                continue
            
            if tags:
                if not any(tag.lower() in [t.lower() for t in skill.tags] for tag in tags):
                    continue
            
            if skill.rating < min_rating:
                continue
            
            results.append(skill)
        
        # Sort results
        if sort_by == "rating":
            results.sort(key=lambda s: s.rating, reverse=True)
        elif sort_by == "downloads":
            results.sort(key=lambda s: s.downloads, reverse=True)
        elif sort_by == "newest":
            results.sort(key=lambda s: s.created_at, reverse=True)
        else:  # relevance
            results.sort(key=lambda s: s.rating * s.downloads, reverse=True)
        
        return results
    
    async def download_skill(self, skill_id: str, user_id: str) -> Optional[SkillPackage]:
        """Download a skill and record the download"""
        skill = self.skills.get(skill_id)
        if not skill or skill.status != SkillStatus.PUBLISHED:
            return None
        
        # Record download
        if skill_id not in self.downloads:
            self.downloads[skill_id] = []
        
        self.downloads[skill_id].append((user_id, datetime.now()))
        skill.downloads += 1
        skill.updated_at = datetime.now()
        
        # Save updated skill
        await self._save_skill(skill)
        
        self.logger.info(f"Downloaded skill {skill.name} by user {user_id}")
        
        return skill
    
    async def add_review(self, skill_id: str, user_id: str, rating: SkillRating, comment: str = "") -> bool:
        """Add a review for a skill"""
        if skill_id not in self.skills:
            return False
        
        if skill_id not in self.reviews:
            self.reviews[skill_id] = []
        
        # Check if user already reviewed this skill
        existing_review = next((r for r in self.reviews[skill_id] if r.user_id == user_id), None)
        if existing_review:
            # Update existing review
            existing_review.rating = rating
            existing_review.comment = comment
            existing_review.created_at = datetime.now()
        else:
            # Add new review
            review = Review(user_id=user_id, rating=rating, comment=comment)
            self.reviews[skill_id].append(review)
        
        # Update user ratings tracking
        if user_id not in self.user_ratings:
            self.user_ratings[user_id] = {}
        self.user_ratings[user_id][skill_id] = rating
        
        # Recalculate average rating
        total_rating = sum(r.rating.value for r in self.reviews[skill_id])
        avg_rating = total_rating / len(self.reviews[skill_id])
        self.skills[skill_id].rating = round(avg_rating, 2)
        
        # Save reviews
        await self._save_reviews(skill_id)
        
        self.logger.info(f"Added review for skill {skill_id} by user {user_id}")
        
        return True
    
    async def get_top_skills(self, limit: int = 10) -> List[SkillPackage]:
        """Get top-rated skills"""
        published_skills = [s for s in self.skills.values() if s.status == SkillStatus.PUBLISHED]
        sorted_skills = sorted(published_skills, key=lambda s: (s.rating, s.downloads), reverse=True)
        return sorted_skills[:limit]
    
    async def get_new_skills(self, limit: int = 10) -> List[SkillPackage]:
        """Get recently published skills"""
        published_skills = [s for s in self.skills.values() if s.status == SkillStatus.PUBLISHED]
        sorted_skills = sorted(published_skills, key=lambda s: s.created_at, reverse=True)
        return sorted_skills[:limit]

class SkillsOrchestrationEngine:
    """Skills orchestration engine for composing and executing skill workflows"""
    
    def __init__(self, marketplace: SkillMarketplace):
        self.marketplace = marketplace
        self.active_workflows = {}
        self.workflow_history = []
        self.logger = logging.getLogger("skills.orchestration")
    
    async def compose_workflow(self, 
                              name: str, 
                              description: str,
                              skill_chain: List[Dict[str, Any]],
                              input_schema: Dict[str, Any] = None,
                              output_schema: Dict[str, Any] = None) -> str:
        """Compose a workflow from multiple skills"""
        
        workflow_id = str(uuid.uuid4())
        
        workflow = {
            "id": workflow_id,
            "name": name,
            "description": description,
            "skill_chain": skill_chain,
            "input_schema": input_schema or {},
            "output_schema": output_schema or {},
            "created_at": datetime.now().isoformat(),
            "status": "ready"
        }
        
        self.active_workflows[workflow_id] = workflow
        
        self.logger.info(f"Composed workflow: {name} (ID: {workflow_id})")
        
        return workflow_id
    
    async def execute_workflow(self, 
                              workflow_id: str, 
                              input_data: Dict[str, Any],
                              user_id: str = "system") -> Dict[str, Any]:
        """Execute a workflow with given input data"""
        
        if workflow_id not in self.active_workflows:
            return {"success": False, "error": f"Workflow {workflow_id} not found"}
        
        workflow = self.active_workflows[workflow_id]
        
        if workflow["status"] != "ready":
            return {"success": False, "error": f"Workflow {workflow_id} is not ready for execution"}
        
        start_time = datetime.now()
        
        # Validate input against schema
        if workflow["input_schema"]:
            # In a real implementation, we would validate against the schema
            pass
        
        execution_result = {
            "workflow_id": workflow_id,
            "user_id": user_id,
            "start_time": start_time.isoformat(),
            "steps": [],
            "success": True,
            "final_output": {},
            "duration": 0
        }
        
        current_context = input_data.copy()
        step_results = []
        
        try:
            for i, step in enumerate(workflow["skill_chain"]):
                step_start = datetime.now()
                
                skill_id = step["skill_id"]
                step_params = step.get("parameters", {})
                
                # Download and execute the skill
                skill_package = await self.marketplace.download_skill(skill_id, user_id)
                if not skill_package:
                    error_result = {
                        "step": i,
                        "skill_id": skill_id,
                        "success": False,
                        "error": f"Skill {skill_id} not found or unavailable",
                        "duration": (datetime.now() - step_start).total_seconds()
                    }
                    step_results.append(error_result)
                    execution_result["success"] = False
                    break
                
                # Prepare parameters for the skill
                skill_params = current_context.copy()
                skill_params.update(step_params)
                
                # In a real implementation, we would execute the skill code
                # For now, we'll simulate execution
                import time
                time.sleep(0.1)  # Simulate processing time
                
                step_result = {
                    "step": i,
                    "skill_id": skill_id,
                    "skill_name": skill_package.name,
                    "success": True,
                    "output": {"simulated": True, "step": i},  # Real implementation would execute skill
                    "duration": (datetime.now() - step_start).total_seconds()
                }
                
                step_results.append(step_result)
                
                # Update context with step result for next step
                if step_result["success"] and "output" in step_result:
                    current_context.update(step_result["output"])
                
                # Check if we should continue
                if not step_result["success"] and step.get("continue_on_error", False) is False:
                    execution_result["success"] = False
                    break
            
            execution_result["steps"] = step_results
            execution_result["final_output"] = current_context
            execution_result["duration"] = (datetime.now() - start_time).total_seconds()
            
        except Exception as e:
            execution_result["success"] = False
            execution_result["error"] = str(e)
            execution_result["duration"] = (datetime.now() - start_time).total_seconds()
        
        # Record execution in history
        self.workflow_history.append(execution_result.copy())
        
        # Keep only recent history
        if len(self.workflow_history) > 100:
            self.workflow_history = self.workflow_history[-50:]
        
        self.logger.info(f"Executed workflow {workflow_id} by user {user_id}, success: {execution_result['success']}")
        
        return execution_result
    
    async def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a workflow"""
        return self.active_workflows.get(workflow_id)
    
    async def list_workflows(self) -> List[Dict[str, Any]]:
        """List all available workflows"""
        return list(self.active_workflows.values())
    
    async def get_workflow_performance(self, workflow_id: str) -> Dict[str, Any]:
        """Get performance metrics for a workflow"""
        if workflow_id not in self.active_workflows:
            return {"error": f"Workflow {workflow_id} not found"}
        
        # Find executions for this workflow
        executions = [e for e in self.workflow_history if e["workflow_id"] == workflow_id]
        
        if not executions:
            return {"workflow_id": workflow_id, "total_executions": 0}
        
        total_executions = len(executions)
        successful_executions = sum(1 for e in executions if e["success"])
        success_rate = successful_executions / total_executions if total_executions > 0 else 0
        
        durations = [e["duration"] for e in executions]
        avg_duration = sum(durations) / len(durations) if durations else 0
        min_duration = min(durations) if durations else 0
        max_duration = max(durations) if durations else 0
        
        return {
            "workflow_id": workflow_id,
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "success_rate": success_rate,
            "average_duration": avg_duration,
            "min_duration": min_duration,
            "max_duration": max_duration
        }

# Example usage and testing
async def demo_marketplace_and_engine():
    """Demonstrate the skills marketplace and orchestration engine"""
    
    print("=== Skills Marketplace and Orchestration Demo ===\n")
    
    # Initialize marketplace
    marketplace = SkillMarketplace("./demo_marketplace")
    
    # Publish some example skills
    print("1. Publishing example skills...")
    
    email_skill_id = await marketplace.publish_skill(
        name="Email Sender",
        description="Sends emails to specified recipients",
        category="communication",
        code="# Email sending skill code",
        schema={
            "input": {"recipient": "string", "subject": "string", "body": "string"},
            "output": {"success": "boolean", "message_id": "string"}
        },
        documentation="Sends emails using SMTP",
        tags=["email", "communication", "notification"]
    )
    print(f"   Published Email Sender (ID: {email_skill_id})")
    
    calendar_skill_id = await marketplace.publish_skill(
        name="Calendar Event Creator",
        description="Creates calendar events",
        category="productivity",
        code="# Calendar event creation skill code",
        schema={
            "input": {"title": "string", "date": "string", "attendees": "array"},
            "output": {"success": "boolean", "event_id": "string"}
        },
        documentation="Creates calendar events",
        tags=["calendar", "scheduling", "productivity"]
    )
    print(f"   Published Calendar Event Creator (ID: {calendar_skill_id})")
    
    # Search for skills
    print("\n2. Searching for skills...")
    search_results = await marketplace.search_skills(query="email", category="communication")
    print(f"   Found {len(search_results)} email-related skills")
    
    # Add reviews
    print("\n3. Adding reviews...")
    await marketplace.add_review(email_skill_id, "user1", SkillRating.FIVE_STARS, "Great email skill!")
    await marketplace.add_review(email_skill_id, "user2", SkillRating.FOUR_STARS, "Works well")
    print(f"   Added reviews for Email Sender (Rating: {(await marketplace.get_skill(email_skill_id)).rating})")
    
    # Get top skills
    print("\n4. Top-rated skills:")
    top_skills = await marketplace.get_top_skills(limit=5)
    for skill in top_skills:
        print(f"   - {skill.name} (Rating: {skill.rating}, Downloads: {skill.downloads})")
    
    # Initialize orchestration engine
    print("\n5. Initializing orchestration engine...")
    engine = SkillsOrchestrationEngine(marketplace)
    
    # Compose a workflow
    workflow_id = await engine.compose_workflow(
        name="Meeting Scheduler",
        description="Schedule a meeting by creating calendar event and sending notification",
        skill_chain=[
            {
                "skill_id": calendar_skill_id,
                "parameters": {"title": "Team Meeting", "date": "2024-01-01"},
                "continue_on_error": False
            },
            {
                "skill_id": email_skill_id,
                "parameters": {"subject": "Meeting Reminder", "body": "Your meeting is scheduled."},
                "continue_on_error": True
            }
        ],
        input_schema={"attendees": "array", "meeting_details": "object"},
        output_schema={"calendar_event_id": "string", "email_sent": "boolean"}
    )
    print(f"   Composed workflow 'Meeting Scheduler' (ID: {workflow_id})")
    
    # Execute the workflow
    print("\n6. Executing workflow...")
    execution_result = await engine.execute_workflow(
        workflow_id,
        {"attendees": ["john@example.com", "jane@example.com"], "meeting_details": {"topic": "Project Update"}}
    )
    print(f"   Workflow execution result: Success = {execution_result['success']}")
    print(f"   Duration: {execution_result['duration']:.2f} seconds")
    
    # Get workflow performance
    print("\n7. Workflow performance metrics:")
    perf_metrics = await engine.get_workflow_performance(workflow_id)
    print(f"   Success rate: {perf_metrics['success_rate']:.2%}")
    print(f"   Avg duration: {perf_metrics['average_duration']:.2f}s")
    
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    asyncio.run(demo_marketplace_and_engine())