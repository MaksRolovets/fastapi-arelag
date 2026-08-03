from tasks.analytics import generate_transaction_analysis
from fastapi import APIRouter, HTTPException
from core.broker import broker
from schemas.analytics import TransactionAnalyticsModel
from services.analytics import get_transaction_events_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.post("/transactions")
async def generate():
    task = await generate_transaction_analysis.kiq()

    return {"task_id": task.task_id}

@router.get("/tasks/{task_id}")
async def get_task_result(task_id: str):
    ready = await broker.result_backend.is_result_ready(task_id)

    if not ready:
        return {
            "task_id": task_id,
            "status": "PENDING",
        }

    result = await broker.result_backend.get_result(task_id)

    return {
        "task_id": task_id,
        "status": "SUCCESS",
        "result": result.return_value,
    }

@router.get(
    "/transactions-clickhouse",
    response_model=list[TransactionAnalyticsModel],
)
async def get_transactions():
    return await get_transaction_events_service()