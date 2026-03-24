from __future__ import annotations

from pydantic import BaseModel, Field


class SampleRequest(BaseModel):
    name: str = Field(..., min_length=2)
    age: int = Field(..., gt=0)
