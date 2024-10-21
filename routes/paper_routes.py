import json
import uuid

import redis
from fastapi import APIRouter
from fastapi import (
    HTTPException,
    Body,
    UploadFile,
    File,
    BackgroundTasks,
)
from starlette.responses import JSONResponse

from ai_models.ai_api_integration.geminiApi import (
    store_file_in_local_dir,
    get_raw_data,
    determine_file_type,
)
from config.db_config import papers_collection, db
from helper.helper import CustomStandard
from models.paper_model import SamplePaper, Tasks

redis_client = redis.Redis(host="127.0.0.1", port=6379, db=0)

router = APIRouter()


@router.post("/paper", response_model=dict)
async def create_paper(paper: SamplePaper):
    """
    Create a new sample paper and store it in the database.

    Args:
        paper (SamplePaper): The data of the sample paper to be created.

    Returns:
        JSONResponse: A response indicating the success of the paper creation
                      along with the generated paper ID.

    Raises:
        HTTPException: If the paper could not be created, raises a 500 error.
    """
    paper_dict = paper.model_dump()
    paper_dict["p_id"] = str(uuid.uuid4())
    result = await papers_collection.insert_one(paper_dict)

    if result.inserted_id:
        return JSONResponse(
            content=CustomStandard.response(
                code=200,
                status="success",
                message="Sample paper created successfully",
                data={"paper_id": str(paper_dict.get("p_id"))},
            )
        )
    else:
        raise HTTPException(status_code=500, detail="Failed to create sample paper")


@router.get("/papers/{p_id}")
async def get_paper(p_id: str):
    """
    Retrieve a sample paper by its ID. Checks if the paper is available in
    the cache, and if not, fetches it from the database.

    Args:
        p_id (str): The unique identifier of the sample paper.

    Returns:
        JSONResponse: A response containing the paper data if found, either from
                      cache or the database.

    Raises:
        HTTPException: If the paper is not found, raises a 404 error.
    """
    cached_paper = redis_client.get(p_id)
    if cached_paper:
        cached_paper_data = json.loads(cached_paper)
        return JSONResponse(
            content=CustomStandard.response(
                code=200,
                status="success",
                message="Paper retrieved from cache",
                data=cached_paper_data,
            )
        )

    paper = await db.papers.find_one({"p_id": p_id})
    if paper:
        paper.pop("_id")

        redis_client.set(p_id, json.dumps(paper))
        return JSONResponse(
            content=CustomStandard.response(
                code=200,
                status="success",
                message="Paper retrieved from database",
                data=paper,
            )
        )
    raise HTTPException(status_code=404, detail="Paper not found")


@router.put("/papers/{p_id}")
async def update_paper(p_id: str, paper: dict = Body(...)):
    """
    Update an existing sample paper's details in the database.

    Args:
        p_id (str): The unique identifier of the paper to be updated.
        paper (dict): The fields to be updated along with their new values.

    Returns:
        JSONResponse: A response indicating the success of the paper update,
                      including the updated paper data.

    Raises:
        HTTPException: If the paper is not found, raises a 404 error.
    """
    existing_paper = await db.papers.find_one({"p_id": p_id})
    if not existing_paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    current_paper = SamplePaper(**existing_paper)
    for field, value in paper.items():
        if hasattr(current_paper, field):
            setattr(current_paper, field, value)
    try:
        updated_paper = current_paper.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    await db.papers.update_one({"p_id": p_id}, {"$set": paper})
    redis_client.set(p_id, json.dumps(updated_paper))

    return JSONResponse(
        content=CustomStandard.response(
            code=200,
            status="success",
            message="Paper updated successfully",
            data=updated_paper,
        )
    )


@router.delete("/papers/{p_id}")
async def delete_paper(paper_id: str):
    """
    Delete a sample paper by its ID from the database and remove it from the cache.

    Args:
        paper_id (str): The unique identifier of the paper to be deleted.

    Returns:
        JSONResponse: A response indicating the success of the deletion.

    Raises:
        HTTPException: If the paper is not found, raises a 404 error.
    """
    result = await db.papers.delete_one({"p_id": paper_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Paper not found")
    redis_client.delete(paper_id)
    return JSONResponse(
        content=CustomStandard.response(
            code=200, status="success", message="Paper deleted successfully"
        )
    )


async def process_Data(file_path, task_id, file_type):
    """
    Process the data from a file and update the task status in the database.

    Args:
        file_path (str): The path to the file to be processed.
        task_id (str): The unique identifier of the task.
        file_type (str): The type of the file (e.g., text, PDF).

    Updates:
        Updates the task status to 'completed' or 'failed' based on the processing outcome.
    """
    try:
        extract_data = await get_raw_data(file_path, file_type)
        await db.Tasks.update_one(
            {"t_id": task_id},
            {
                "$set": Tasks(
                    task_status="completed", extract_data=extract_data
                ).model_dump(exclude_unset=True)
            },
        )
    except Exception as e:
        await db.Tasks.update_one(
            {"t_id": task_id},
            {
                "$set": Tasks(
                    task_status="failed", extract_data={"error": str(e)}
                ).model_dump(exclude_unset=True)
            },
        )


@router.post("/extract/text")
async def extract_text(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    """
    Extract text data from a file and process it asynchronously.

    Args:
        background_tasks (BackgroundTasks): The background task manager for asynchronous processing.
        file (UploadFile): The file to be processed.

    Returns:
        JSONResponse: A response indicating the start of the text extraction process.
    """
    task_id = str(uuid.uuid4())
    file_content = await file.read()

    file_path = await store_file_in_local_dir(file_content, file.filename)

    file_type = determine_file_type(file.filename)

    await db.Tasks.insert_one(
        Tasks(
            t_id=task_id,
            task_status="processing",
            file_path=file_path,
            file_type=file_type,
        ).model_dump(exclude={"extract_data"})
    )

    background_tasks.add_task(process_Data, file_path, task_id, file_type)

    return JSONResponse(
        content=CustomStandard.response(
            code=202,
            status="processing",
            message=f"{file_type.upper()} extraction started",
            data={"task_id": task_id},
        ),
    )


@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    """
    Retrieve the status of a specific task.

    Args:
        task_id (str): The unique identifier of the task.

    Returns:
        JSONResponse: A response containing the current status of the task.

    Raises:
        HTTPException: If the task is not found, raises a 404 error.
    """
    task = await db.Tasks.find_one({"t_id": task_id})
    if task:
        return JSONResponse(
            content=CustomStandard.response(
                code=200,
                status="success",
                message="Task status retrieved",
                data={"status": task["task_status"]},
            )
        )
    raise HTTPException(status_code=404, detail="Task not found")
