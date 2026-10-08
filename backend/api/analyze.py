"""
ScamGraph AI - Analyze Endpoint
Executes the end-to-end scam intelligence pipeline:
Preprocessing -> ML -> Signals -> URL Analysis -> Workflow Playbooks -> Scam DNA -> Risk Scoring -> Scam Graph.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from schemas.schemas import AnalyzeRequest, AnalyzeResponse, ScamGraphData
from database.database import get_db
from database.models import Incident, Message, Signal, WorkflowEvent, Alert
from utils.redactor import redact_sensitive_info
from services.preprocessing import preprocess_service
from services.signal_engine import signal_engine
from services.url_analyzer import url_analyzer
from services.workflow_engine import workflow_engine
from services.scam_dna import scam_dna_engine
from services.emerging_engine import emerging_engine
from services.risk_engine import risk_engine
from services.alert_engine import alert_engine
from services.graph_builder import build_scam_graph

# ML Inference import
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(BASE_DIR, "ml"))
from inference import inference_engine

router = APIRouter(prefix="/api", tags=["Analysis"])


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_interaction(request: AnalyzeRequest, db: Session = Depends(get_db)):
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")

    raw_text = request.text
    explicit_url = request.url

    # 1. Preprocessing & Entity Extraction
    prep_data = preprocess_service.process(raw_text)
    entities = prep_data["entities"]
    if explicit_url and explicit_url not in entities["urls"]:
        entities["urls"].append(explicit_url)

    # 2. ML Prediction (Binary Fraud Prob + Multi-class Category)
    ml_res = inference_engine.predict(raw_text)
    ml_prob = ml_res["scam_probability"]
    ml_category = ml_res["category"]

    # 3. Rule / Signal Extraction
    signal_res = signal_engine.analyze(raw_text, entities)
    rule_score = signal_res["rule_score"]
    detected_signals = signal_res["detected_signals"]

    # 4. URL Threat Analysis
    url_res = url_analyzer.analyze_urls(entities["urls"])
    url_score = url_res["url_risk_score"]

    # 5. Scam Workflow Intelligence
    extracted_events = request.events or workflow_engine.extract_events_from_text(
        raw_text, entities, signal_res["signals"]
    )
    workflow_res = workflow_engine.evaluate_workflow(extracted_events, ml_category)
    workflow_score = workflow_res["workflow_score"]

    # 6. Scam DNA & Semantic Matching
    dna_res = scam_dna_engine.match_scam_dna(raw_text, ml_category, detected_signals)
    scam_dna_tag = dna_res["scam_dna"]
    campaign_name = dna_res["campaign_name"]

    # 7. Composite Risk Engine
    risk_res = risk_engine.calculate_risk(
        ml_prob=ml_prob,
        rule_score=rule_score,
        url_score=url_score,
        workflow_score=workflow_score,
        signals_detected=detected_signals
    )
    final_risk_score = risk_res["risk_score"]
    risk_level = risk_res["risk_level"]

    # Final category adjustment if workflow is high confidence
    final_category = ml_category
    if workflow_res.get("workflow_detected") and workflow_res.get("playbook_id") != "GENERIC_SUSPICIOUS":
        final_category = workflow_res["playbook_id"]

    # 8. Explainable AI & Actionable Safety Recommendation
    explanation_res = risk_engine.generate_explanation(
        scam_type=final_category,
        risk_level=risk_level,
        signals=detected_signals,
        events=extracted_events,
        url_report=url_res
    )

    # 9. Alert Fatigue & Campaign Deduplication
    alert_res = alert_engine.process_alert(
        risk_level=risk_level,
        scam_dna=scam_dna_tag,
        risk_score=final_risk_score
    )

    # 10. Scam Graph Construction
    sender_identifier = request.sender or (entities["phone_numbers"][0] if entities["phone_numbers"] else "Unknown Number")
    redacted_preview = redact_sensitive_info(raw_text)
    scam_graph = build_scam_graph(
        sender=sender_identifier,
        text_preview=redacted_preview,
        entities=entities,
        workflow_events=extracted_events,
        scam_dna=scam_dna_tag,
        category=final_category
    )

    # 11. Record Incident in DB & Emerging Incident Pool (Privacy-Sanitized)
    incident_record = {
        "text": redacted_preview,
        "scam_type": final_category,
        "risk_score": final_risk_score,
        "signals": detected_signals,
        "workflow": extracted_events,
        "scam_dna": scam_dna_tag
    }
    emerging_engine.record_incident(incident_record)

    try:
        db_incident = Incident(
            scam_dna_tag=scam_dna_tag,
            scam_type=final_category,
            risk_score=final_risk_score,
            risk_level=risk_level,
            confidence=round(max(ml_prob, workflow_res["confidence"]), 2),
            redacted_preview=redacted_preview[:400]
        )
        db.add(db_incident)
        db.commit()
        db.refresh(db_incident)

        db_msg = Message(
            incident_id=db_incident.id,
            sender_masked=sender_identifier,
            redacted_content=redacted_preview,
            detected_language=prep_data["language"]
        )
        db.add(db_msg)
        db.commit()
    except Exception as e:
        db.rollback()
        # Non-blocking database write error fallback

    return AnalyzeResponse(
        risk_score=final_risk_score,
        risk_level=risk_level,
        scam_type=final_category,
        confidence=round(max(ml_prob, workflow_res["confidence"]), 2),
        signals=detected_signals,
        workflow=extracted_events,
        workflow_details=workflow_res,
        scam_dna=scam_dna_tag,
        campaign_name=campaign_name,
        recommendation=explanation_res["recommended_action"],
        evidence_reasons=explanation_res["evidence_reasons"],
        entities=entities,
        url_analysis=url_res,
        alert_details=alert_res,
        scam_graph=scam_graph
    )
