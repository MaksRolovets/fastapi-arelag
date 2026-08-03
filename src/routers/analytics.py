from fastapi import APIRouter
from tasks.analytics import generate_transaction_analysis, get_task_result


router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.post("/transactions")
async def create_analysis():
    task = generate_transaction_analysis.delay()
    return {"task_id": task.id}


@router.get("/tasks/{task_id}")
async def get_analysis(task_id: str):
    task = get_task_result(task_id)

    response = {
        "task_id": task.id,
        "status": task.status,
    }

    if task.ready():
        response["result"] = task.result

    return response