"""
ScamGraph AI - Pydantic Schemas
Defines request and response models for API validation and documentation.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class AnalyzeRequest(BaseModel):
    text: str = Field(..., description="Message text, chat transcript, or email content")
    url: Optional[str] = Field(None, description="Optional suspicious URL")
    sender: Optional[str] = Field(None, description="Optional sender identifier (phone, email, handle)")
    events: Optional[List[str]] = Field(None, description="Optional manual sequence of interaction events")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Your SBI KYC will expire today. Update immediately at http://sbi-kyc-portal.xyz or account will be blocked.",
                "url": "http://sbi-kyc-portal.xyz",
                "sender": "+919876543210"
            }
        }


class GraphNode(BaseModel):
    id: str
    label: str
    type: str  # phone, message, url, domain, upi, pattern, category
    data: Dict[str, Any] = {}


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str  # SENT, CONTAINS, LINKS_TO, USES, MATCHES, BELONGS_TO


class ScamGraphData(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]


class AnalyzeResponse(BaseModel):
    risk_score: int = Field(..., description="0-100 composite risk score")
    risk_level: str = Field(..., description="LOW, MEDIUM, HIGH, CRITICAL")
    scam_type: str = Field(..., description="KYC_FRAUD, UPI_FRAUD, etc.")
    confidence: float = Field(..., description="ML/workflow confidence (0.0 to 1.0)")
    signals: List[str] = Field(..., description="Detected suspicious signals")
    workflow: List[str] = Field(..., description="Identified workflow event sequence")
    workflow_details: Dict[str, Any] = Field(..., description="Detailed workflow analysis & stages")
    scam_dna: str = Field(..., description="Unique campaign fingerprint tag, e.g. #UPI-KYC-042")
    campaign_name: str = Field(..., description="Name of matched or emerging campaign")
    recommendation: str = Field(..., description="Actionable user safety advice")
    evidence_reasons: List[str] = Field(..., description="Human-understandable evidence points")
    entities: Dict[str, Any] = Field(..., description="Preserved extracted entities (masked where appropriate)")
    url_analysis: Optional[Dict[str, Any]] = Field(None, description="Detailed URL heuristics")
    alert_details: Dict[str, Any] = Field(..., description="Adaptive fatigue & deduplication metadata")
    scam_graph: ScamGraphData = Field(..., description="React Flow nodes and edges")


class PatternSummary(BaseModel):
    dna_id: str
    title: str
    category: str
    signals: List[str]
    workflow: List[str]
    report_count: int
    growth: float
    risk: str
    phrases: List[str]
    timeline: List[Dict[str, Any]]


class DashboardStats(BaseModel):
    total_analyzed: int
    scam_detected: int
    benign_detected: int
    emerging_patterns_count: int
    critical_alerts_count: int
    high_alerts_count: int
    top_categories: List[Dict[str, Any]]
    scam_trend: List[Dict[str, Any]]
    model_metrics: Dict[str, Any]


class ReportRequest(BaseModel):
    text: str
    scam_type: Optional[str] = None
    reporter_notes: Optional[str] = None
    contact: Optional[str] = None


class ReportResponse(BaseModel):
    success: bool
    report_id: str
    message: str
