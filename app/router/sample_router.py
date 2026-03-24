from __future__ import annotations

from fastapi import APIRouter, Request

from app.core.response import success_response
from app.schemas.sample import SampleRequest

router = APIRouter()


@router.post("/sample")
async def create_sample(payload: SampleRequest, request: Request):
    return success_response(
        {"message": f"Hello {payload.name}"},
    )
