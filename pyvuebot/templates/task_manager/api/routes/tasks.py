from typing import List, Optional
from fastapi import APIRouter, HTTPException, Request, Query
from pydantic import BaseModel
import logging
from datetime import datetime
import uuid

from ..models import TaskCreate, TaskUpdate, TaskResponse, TaskStatus, TaskPriority
from ..db import supabase

# Setup logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("/")
@router.options("/")
async def read_tasks(
    request: Request,
    user_id: Optional[str] = None,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    sort_by: Optional[str] = Query(
        None, description="Field to sort by (created_at, deadline, priority)"),
    sort_order: Optional[str] = Query(
        "asc", description="Sort order (asc or desc)")
):
    """Get all tasks for a user"""
    # Handle CORS preflight request
    if request.method == "OPTIONS":
        return {}

    # Validate user_id
    if user_id is None:
        logger.warning("Missing user_id parameter")
        return {"error": "user_id parameter is required"}

    try:
        if supabase is None:
            raise HTTPException(
                status_code=500, detail="Database connection not available")

        query = supabase.table("tasks").select("*").eq("user_id", str(user_id))

        # Apply filters if provided
        if status:
            query = query.eq("status", status)
        if priority:
            query = query.eq("priority", priority)

        # Apply sorting
        if sort_by:
            query = query.order(sort_by, desc=(sort_order.lower() == "desc"))
        else:
            query = query.order("created_at", desc=True)

        response = query.execute()
        logger.info(f"Returning {len(response.data)} tasks for user {user_id}")
        return response.data
    except Exception as e:
        logger.error(f"Error fetching tasks: {str(e)}")
        return {"error": str(e)}


@router.post("/task")
@router.options("/task")
async def create_task(request: Request):
    """Create a new task for a user"""
    # Handle CORS preflight request
    if request.method == "OPTIONS":
        return {}

    try:
        if supabase is None:
            raise HTTPException(
                status_code=500, detail="Database connection not available")

        # Parse request manually for more flexibility
        body = await request.json()
        user_id = request.query_params.get("user_id")

        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")

        # Extract task data
        task_data = {
            "task_name": body.get("task_name"),
            "description": body.get("description"),
            "status": body.get("status", "pending"),
            "priority": body.get("priority", "medium"),
            "user_id": user_id
        }

        # Generate a proper UUID if client provided an ID based on timestamp
        # or use the provided UUID if it's valid
        client_id = body.get("id")
        if client_id:
            try:
                # Try to validate if it's already a UUID
                uuid.UUID(str(client_id))
                task_data["id"] = str(client_id)
            except ValueError:
                # If not a valid UUID, generate a new one
                task_data["id"] = str(uuid.uuid4())

        # Handle deadline if present
        if "deadline" in body and body["deadline"]:
            # Convert to ISO format if it's not already
            if isinstance(body["deadline"], str):
                task_data["deadline"] = body["deadline"]
            else:
                task_data["deadline"] = datetime.fromisoformat(
                    body["deadline"]).isoformat()

        current_time = datetime.now().isoformat()
        task_data["created_at"] = current_time
        task_data["updated_at"] = current_time

        # Validate required fields
        if not task_data.get("task_name"):
            # For backward compatibility, try using 'text' field if present
            if body.get("text"):
                task_data["task_name"] = body["text"]
            else:
                raise HTTPException(
                    status_code=400, detail="task_name is required")

        # Insert into database
        response = supabase.table("tasks").insert(task_data).execute()
        logger.info(f"Created new task for user: {user_id}")

        if response.data:
            return response.data[0]
        else:
            raise HTTPException(
                status_code=500, detail="Failed to create task")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error creating task: {str(e)}")


@router.put("/{task_id}")
@router.options("/{task_id}")
async def update_task(request: Request, task_id: str):
    """Update a task's details"""
    # Handle CORS preflight request
    if request.method == "OPTIONS":
        return {}

    try:
        if supabase is None:
            raise HTTPException(
                status_code=500, detail="Database connection not available")

        # Parse parameters
        user_id = request.query_params.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")

        # Get request body
        body = await request.json()

        # First check if the task exists and belongs to the user
        check_response = supabase.table("tasks").select("id").eq(
            "id", task_id).eq("user_id", str(user_id)).execute()

        if not check_response.data:
            # If task not found, create a new one with the specified ID
            logger.warning(
                f"Task {task_id} not found for user {user_id} - creating new task")

            # Try to use a valid UUID
            try:
                uuid.UUID(task_id)
            except ValueError:
                # If not a valid UUID, use it as a reference but generate a new UUID
                new_task_id = str(uuid.uuid4())
                logger.info(
                    f"Converted invalid UUID {task_id} to {new_task_id}")
                task_id = new_task_id

            # Extract task data
            task_data = {
                "id": task_id,
                # Use part of UUID for readability
                "task_name": body.get("task_name", f"Task {task_id[:8]}"),
                "description": body.get("description"),
                "status": body.get("status", "pending"),
                "priority": body.get("priority", "medium"),
                "user_id": user_id
            }

            # For backward compatibility
            if "text" in body and not task_data.get("task_name"):
                task_data["task_name"] = body["text"]

            # Handle deadline if present
            if "deadline" in body and body["deadline"]:
                if isinstance(body["deadline"], str):
                    task_data["deadline"] = body["deadline"]
                else:
                    task_data["deadline"] = datetime.fromisoformat(
                        body["deadline"]).isoformat()

            current_time = datetime.now().isoformat()
            task_data["created_at"] = current_time
            task_data["updated_at"] = current_time

            # Insert new task
            response = supabase.table("tasks").insert(task_data).execute()
            logger.info(
                f"Created new task with ID {task_id} for user: {user_id}")

            if response.data:
                return response.data[0]
            else:
                raise HTTPException(
                    status_code=500, detail="Failed to create task")

        # Prepare update data
        update_data = {}

        # Handle update fields
        if "task_name" in body:
            update_data["task_name"] = body["task_name"]
        elif "text" in body:  # Backward compatibility
            update_data["task_name"] = body["text"]

        if "description" in body:
            update_data["description"] = body["description"]

        if "status" in body:
            update_data["status"] = body["status"]

        if "priority" in body:
            update_data["priority"] = body["priority"]

        if "deadline" in body:
            if body["deadline"] is None:
                update_data["deadline"] = None
            elif isinstance(body["deadline"], str):
                update_data["deadline"] = body["deadline"]
            else:
                update_data["deadline"] = datetime.fromisoformat(
                    body["deadline"]).isoformat()

        # Handle special case for completed status from old API
        if "completed" in body:
            update_data["status"] = "completed" if body["completed"] else "pending"

        update_data["updated_at"] = datetime.now().isoformat()

        # Update the task
        response = supabase.table("tasks").update(update_data).eq(
            "id", task_id).eq("user_id", str(user_id)).execute()

        logger.info(f"Updated task {task_id} for user {user_id}")

        if response.data:
            return response.data[0]
        else:
            raise HTTPException(
                status_code=500, detail="Failed to update task")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}")
        # Return 200 with error info instead of raising exception
        # This makes the API more robust for frontend use
        return {"success": False, "error": str(e)}

@router.delete("/{task_id}")
@router.options("/{task_id}")
async def delete_task(request: Request, task_id: str):
    """Delete a task"""
    # Handle CORS preflight request
    if request.method == "OPTIONS":
        return {}

    try:
        if supabase is None:
            raise HTTPException(
                status_code=500, detail="Database connection not available")

        user_id = request.query_params.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")

        logger.info(f"DELETE /api/tasks/{task_id} - User ID: {user_id}")

        # Check if the task exists and belongs to the user
        check_response = supabase.table("tasks").select("id").eq(
            "id", task_id).eq("user_id", str(user_id)).execute()

        if not check_response.data:
            logger.warning(
                f"Task {task_id} not found for user {user_id} - ignoring delete")
            # Return success even if not found to be idempotent
            return {"success": True, "message": "Task not found but operation considered successful"}

        # Delete the task
        response = supabase.table("tasks").delete().eq(
            "id", task_id).eq("user_id", str(user_id)).execute()

        logger.info(f"Deleted task {task_id} for user {user_id}")
        return {"success": True, "message": f"Task {task_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting task: {str(e)}")
        # Return 200 with error info instead of raising exception
        return {"success": False, "error": str(e)}
