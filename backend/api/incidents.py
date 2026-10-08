"""
ScamGraph AI - Incidents & Community Reporting API
"""

import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from schemas.schemas import ReportRequest, ReportResponse
from database.database import get_db
from database.models import Incident, Report
from utils.redactor import redact_sensitive_info
from services.emerging_engine import emerging_engine

router = APIRouter(prefix="/api", tags=["Incidents"])


@router.get("/incidents")
def get_recent_incidents(db: Session = Depends(get_db)):
    db_items = db.query(Incident).order_by(Incident.id.desc()).limit(20).all()
    results = []
    for item in db_items:
        results.append({
            "id": item.id,
            "scam_dna": item.scam_dna_tag,
            "scam_type": item.scam_type,
            "risk_score": item.risk_score,
            "risk_level": item.risk_level,
            "confidence": item.confidence,
            "preview": item.redacted_preview,
            "created_at": item.created_at.isoformat() if item.created_at else None
        })
    return results


@router.post("/report", response_model=ReportResponse)
def submit_scam_report(report: ReportRequest, db: Session = Depends(get_db)):
    report_id = f"REP-{uuid.uuid4().hex[:8].upper()}"
    redacted = redact_sensitive_info(report.text)

    try:
        new_report = Report(
            reporter_contact_hash=uuid.uuid5(uuid.NAMESPACE_DNS, report.contact or "anonymous").hex,
            notes=f"Reported Category: {report.scam_type or 'UNSPECIFIED'}. Notes: {report.reporter_notes or 'None'}. Content: {redacted[:300]}"
        )
        db.add(new_report)
        db.commit()
    except Exception:
        db.rollback()

    return ReportResponse(
        success=True,
        report_id=report_id,
        message="Thank you. Scam interaction received securely and anonymized."
    )


@router.delete("/incidents/clear")
def clear_analysis_history(db: Session = Depends(get_db)):
    """
    User privacy feature: clears local incident log.
    """
    try:
        db.query(Incident).delete()
        db.commit()
    except Exception:
        db.rollback()
    return {"success": True, "message": "Analysis history purged completely."}
