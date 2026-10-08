"""
ScamGraph AI - Emerging Scam Patterns API
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from schemas.schemas import PatternSummary
from services.emerging_engine import emerging_engine

router = APIRouter(prefix="/api/patterns", tags=["Patterns"])


@router.get("", response_model=List[PatternSummary])
def get_emerging_patterns():
    patterns = emerging_engine.discover_clusters()
    return patterns


@router.get("/{pattern_id}", response_model=PatternSummary)
def get_pattern_detail(pattern_id: str):
    pattern = emerging_engine.get_pattern_by_id(pattern_id)
    if not pattern:
        raise HTTPException(status_code=404, detail=f"Pattern {pattern_id} not found.")
    return pattern
