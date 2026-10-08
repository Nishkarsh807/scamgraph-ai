"""
ScamGraph AI - SQLAlchemy ORM Models
Defines relational schema for users, incidents, messages, signals,
scam_patterns, workflow_events, scam_dna, reports, and alerts.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email_hash = Column(String(64), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    reports = relationship("Report", back_populates="user")


class ScamPattern(Base):
    __tablename__ = "scam_patterns"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True)  # e.g., UPI-KYC-042
    title = Column(String(200))
    category = Column(String(50), index=True)  # KYC, UPI, OTP, etc.
    description = Column(Text)
    risk_level = Column(String(20))  # LOW, MEDIUM, HIGH, CRITICAL
    active_incidents_count = Column(Integer, default=1)
    weekly_growth_rate = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    incidents = relationship("Incident", back_populates="pattern")
    dna_records = relationship("ScamDNA", back_populates="pattern")


class ScamDNA(Base):
    __tablename__ = "scam_dna"

    id = Column(Integer, primary_key=True, index=True)
    dna_id = Column(String(50), unique=True, index=True)  # #UPI-KYC-042
    pattern_id = Column(Integer, ForeignKey("scam_patterns.id"), nullable=True)
    vector_hash = Column(String(64))
    canonical_signals = Column(Text)  # JSON or comma-separated
    first_detected = Column(DateTime, default=datetime.utcnow)
    last_detected = Column(DateTime, default=datetime.utcnow)

    pattern = relationship("ScamPattern", back_populates="dna_records")


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    pattern_id = Column(Integer, ForeignKey("scam_patterns.id"), nullable=True)
    scam_dna_tag = Column(String(50), index=True)
    scam_type = Column(String(50), index=True)
    risk_score = Column(Integer)  # 0-100
    risk_level = Column(String(20))  # LOW, MEDIUM, HIGH, CRITICAL
    confidence = Column(Float)
    redacted_preview = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    pattern = relationship("ScamPattern", back_populates="incidents")
    messages = relationship("Message", back_populates="incident", cascade="all, delete-orphan")
    signals = relationship("Signal", back_populates="incident", cascade="all, delete-orphan")
    workflow_events = relationship("WorkflowEvent", back_populates="incident", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="incident", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    sender_masked = Column(String(100), nullable=True)
    redacted_content = Column(Text)
    content_hash = Column(String(64), index=True)
    detected_language = Column(String(20), default="english")
    created_at = Column(DateTime, default=datetime.utcnow)

    incident = relationship("Incident", back_populates="messages")


class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    signal_name = Column(String(100), index=True)
    signal_value = Column(Integer, default=1)
    weight = Column(Float, default=1.0)

    incident = relationship("Incident", back_populates="signals")


class WorkflowEvent(Base):
    __tablename__ = "workflow_events"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    event_order = Column(Integer, default=1)
    event_type = Column(String(100))  # KYC_WARNING, URGENCY, EXTERNAL_LINK, etc.
    event_timestamp = Column(DateTime, default=datetime.utcnow)

    incident = relationship("Incident", back_populates="workflow_events")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    alert_level = Column(String(20))  # LOW, MEDIUM, HIGH, CRITICAL
    intervention_type = Column(String(50))
    is_suppressed_for_fatigue = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    incident = relationship("Incident", back_populates="alerts")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=True)
    reporter_contact_hash = Column(String(64), nullable=True)
    notes = Column(Text, nullable=True)
    reported_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reports")
