from fastapi import APIRouter, Request
from app.schemas.sample import SampleRequest
from app.core.response import success_response

router = APIRouter()

@router.post("/sample")
async def create_sample(payload: SampleRequest, request: Request):
    return success_response(
        {"message": f"Hello {payload.name}"}
    )