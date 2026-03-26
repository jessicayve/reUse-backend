from typing import List, Literal
from pydantic import BaseModel, Field, field_validator


class ScanResponse(BaseModel):
    objectName: str
    materialType: str
    condition: str
    decision: Literal["reuse", "repair", "donate", "recycle"]
    reason: str
    reuseIdeas: List[str]
    recyclingTip: str
    recyclable: bool
    environmentalImpact: str
    disposalCategory: str
    location: str
    localDisposalGuidance: str
    confidence: float = Field(..., ge=0.0, le=1.0)

    @field_validator("reuseIdeas")
    @classmethod
    def validate_reuse_ideas(cls, value: List[str]) -> List[str]:
        if len(value) != 3:
            raise ValueError("reuseIdeas must contain exactly 3 items.")
        return value