"""
ScamGraph AI - Enhanced Visual 15-Slide Hackathon Pitch Deck Generator
Builds a rich PowerPoint presentation (.pptx) featuring:
- Visual Architecture Flowchart Shapes
- Structured Comparison & Workflow Content Tables
- Step-by-Step Playbook Deep-Dives (KYC, UPI, Digital Arrest, Electricity)
- Embedded Confusion Matrix Image (ml/reports/confusion_matrix.png)
- Visual Scam Graph Node-Link Diagram
- KPI Metric Cards & Partial-Match Formula Breakdown
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CM_IMAGE_PATH = os.path.join(BASE_DIR, "ml", "reports", "confusion_matrix.png")
OUTPUT_PPTX = os.path.join(BASE_DIR, "ScamGraph_AI_Hackathon_Pitch.pptx")

# Color Palette (Modern Dark Security UI)
BG_DARK = RGBColor(11, 17, 32)         # #0B1120
CARD_BG = RGBColor(19, 28, 49)         # #131C31
CARD_ALT = RGBColor(15, 23, 42)        # #0F172A
EMERALD = RGBColor(16, 185, 129)       # #10B981
DARK_EMERALD = RGBColor(6, 78, 59)     # #064E3B
CYAN = RGBColor(56, 189, 248)          # #38BDF8
AMBER = RGBColor(245, 158, 11)         # #F59E0B
ROSE = RGBColor(244, 63, 94)           # #F43F5E
DARK_ROSE = RGBColor(76, 5, 25)        # #4C0519
PURPLE = RGBColor(168, 85, 247)        # #A855F7
WHITE = RGBColor(255, 255, 255)
SLATE_LIGHT = RGBColor(226, 232, 240)
SLATE_MUTED = RGBColor(148, 163, 184)
BORDER_SLATE = RGBColor(30, 41, 59)


def set_slide_bg(slide, prs):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_DARK
    bg.line.fill.background()
    # Subtle top accent bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.06))
    bar.fill.solid()
    bar.fill.fore_color.rgb = EMERALD
    bar.line.fill.background()


def add_slide_header(slide, title_text, subtitle_text="SCAMGRAPH AI • TRACK 2: AI-DRIVEN SCAM PATTERN RECOGNITION", slide_num=None):
    # Tagline pill
    cat_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.25), Inches(10.5), Inches(0.35))
    tf_cat = cat_box.text_frame
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = subtitle_text.upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = EMERALD

    # Slide Number badge
    if slide_num:
        num_box = slide.shapes.add_textbox(Inches(11.8), Inches(0.25), Inches(1.0), Inches(0.35))
        tf_num = num_box.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.text = f"{slide_num:02d} / 15"
        p_num.font.size = Pt(10)
        p_num.font.bold = True
        p_num.font.color.rgb = SLATE_MUTED
        p_num.alignment = PP_ALIGN.RIGHT

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.55), Inches(12.0), Inches(0.55))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(24)
    p_t.font.bold = True
    p_t.font.color.rgb = WHITE


def add_box_card(slide, left, top, width, height, title="", border_color=BORDER_SLATE, fill_color=CARD_BG, title_color=CYAN):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)

    tb = slide.shapes.add_textbox(left + Inches(0.18), top + Inches(0.15), width - Inches(0.36), height - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    if title:
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = title_color
    return tf


def add_bullet(tf, bold_prefix, text, size=11, color=SLATE_LIGHT, prefix_color=WHITE, space_before=6):
    p = tf.add_paragraph()
    p.space_before = Pt(space_before)
    if bold_prefix:
        run_b = p.add_run()
        run_b.text = bold_prefix + " "
        run_b.font.bold = True
        run_b.font.size = Pt(size)
        run_b.font.color.rgb = prefix_color
    run_t = p.add_run()
    run_t.text = text
    run_t.font.size = Pt(size)
    run_t.font.color.rgb = color


def style_table_cell(cell, text, font_size=10, bold=False, text_color=WHITE, bg_color=CARD_BG, align=PP_ALIGN.LEFT):
    cell.fill.solid()
    cell.fill.fore_color.rgb = bg_color
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf = cell.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = text_color
    p.alignment = align


def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: COVER SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank)
    set_slide_bg(s1, prs)

    # Track Pill Shape
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.8), Inches(1.2), Inches(5.7), Inches(0.45))
    pill.fill.solid()
    pill.fill.fore_color.rgb = DARK_EMERALD
    pill.line.color.rgb = EMERALD
    tf_p = pill.text_frame
    p = tf_p.paragraphs[0]
    p.text = "TRACK 2 • AI-DRIVEN SCAM PATTERN RECOGNITION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p.alignment = PP_ALIGN.CENTER

    # Hero Title
    hero_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(11.3), Inches(2.6))
    tf_h = hero_box.text_frame
    tf_h.word_wrap = True
    p1 = tf_h.paragraphs[0]
    p1.text = "ScamGraph AI"
    p1.font.size = Pt(60)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.alignment = PP_ALIGN.CENTER

    p2 = tf_h.add_paragraph()
    p2.text = "From suspicious messages to complete scam workflows."
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = CYAN
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf_h.add_paragraph()
    p3.text = "\nDetect Multi-Stage Scam Workflows  •  Fingerprint Scam DNA  •  Stop Fraud Before Money Moves"
    p3.font.size = Pt(13)
    p3.font.color.rgb = SLATE_MUTED
    p3.alignment = PP_ALIGN.CENTER

    # 4 Bottom Metric Cards on Cover
    cover_kpis = [
        ("100% Recall", "Zero Missed Scams on Test Set", EMERALD),
        ("8 Playbooks", "Multi-Event Workflow Tracking", CYAN),
        ("Scam DNA", "Semantic Vector Fingerprinting", PURPLE),
        ("React Flow", "Interactive Scam Graph Topology", AMBER)
    ]
    for i, (k_val, k_sub, k_col) in enumerate(cover_kpis):
        left = Inches(1.0 + i * 2.9)
        c = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(4.8), Inches(2.7), Inches(1.3))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = k_col
        c.line.width = Pt(1.5)
        tf_c = c.text_frame
        tf_c.word_wrap = True
        pk1 = tf_c.paragraphs[0]
        pk1.text = k_val
        pk1.font.size = Pt(20)
        pk1.font.bold = True
        pk1.font.color.rgb = k_col
        pk1.alignment = PP_ALIGN.CENTER
        pk2 = tf_c.add_paragraph()
        pk2.text = k_sub
        pk2.font.size = Pt(10)
        pk2.font.color.rgb = SLATE_LIGHT
        pk2.alignment = PP_ALIGN.CENTER

    # Presenter Footer
    foot = s1.shapes.add_textbox(Inches(1.0), Inches(6.45), Inches(11.3), Inches(0.5))
    tf_f = foot.text_frame
    pf = tf_f.paragraphs[0]
    pf.text = "Author: Nishkarsh Singh  |  GitHub: github.com/Nishkarsh807/scamgraph-ai"
    pf.font.size = Pt(12)
    pf.font.bold = True
    pf.font.color.rgb = SLATE_MUTED
    pf.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 2: THE PROBLEM STATEMENT
    # =========================================================================
    s2 = prs.slides.add_slide(blank)
    set_slide_bg(s2, prs)
    add_slide_header(s2, "The Problem: Fraudsters Execute Workflows, Not Single Texts", slide_num=2)

    tf_left = add_box_card(s2, Inches(0.6), Inches(1.3), Inches(5.9), Inches(4.1), "How a Real Scam Unfolds Across Channels", border_color=ROSE, title_color=ROSE)
    add_bullet(tf_left, "Step 1 (SMS):", "'Dear customer, your SBI KYC expires today.' — Appears benign in isolation.", 11)
    add_bullet(tf_left, "Step 2 (Link):", "'Update PAN immediately at http://sbi-kyc-update.xyz' — Phishing lure.", 11)
    add_bullet(tf_left, "Step 3 (Web):", "Fake banking page harvests NetBanking username & password.", 11)
    add_bullet(tf_left, "Step 4 (Call/WhatsApp):", "'Tell our executive the 6-digit OTP to unfreeze your account.'", 11)
    add_bullet(tf_left, "Step 5 (UPI):", "'Approve ₹1 verification collect request' -> Drains ₹95,000.", 11, color=ROSE)

    tf_right = add_box_card(s2, Inches(6.8), Inches(1.3), Inches(5.9), Inches(4.1), "Why Traditional Spam Classifiers Fail", border_color=BORDER_SLATE, title_color=CYAN)
    add_bullet(tf_right, "1. Zero State Memory:", "Evaluates each SMS independently without linking previous messages.", 11)
    add_bullet(tf_right, "2. High Alert Fatigue:", "Flags harmless marketing promos while missing subtle social engineering.", 11)
    add_bullet(tf_right, "3. Hinglish Evasion:", "Fails on Romanized Hindi ('Aapka khata band ho jayega turant').", 11)
    add_bullet(tf_right, "4. Black-Box Output:", "Shows 'Spam: 80%' without explaining why or what the user should do.", 11)
    add_bullet(tf_right, "5. No Campaign Vision:", "Cannot connect 100 slightly reworded texts to one fraud ring.", 11)

    # Bottom Visual Chain Flow
    chain_steps = ["Unknown Sender", "KYC Expiry Threat", "Suspicious URL", "Credential Theft", "OTP Request", "UPI Account Drain"]
    for idx, st in enumerate(chain_steps):
        left = Inches(0.6 + idx * 2.05)
        box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(5.75), Inches(1.75), Inches(0.95))
        box.fill.solid()
        box.fill.fore_color.rgb = DARK_ROSE if idx >= 3 else CARD_BG
        box.line.color.rgb = ROSE if idx >= 3 else CYAN
        tf_b = box.text_frame
        tf_b.word_wrap = True
        p = tf_b.paragraphs[0]
        p.text = f"Event {idx+1}\n{st}"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

        if idx < len(chain_steps) - 1:
            arr = s2.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, left + Inches(1.8), Inches(6.1), Inches(0.2), Inches(0.25))
            arr.fill.solid()
            arr.fill.fore_color.rgb = EMERALD
            arr.line.fill.background()

    # =========================================================================
    # SLIDE 3: CORE INNOVATION & PARADIGM SHIFT TABLE
    # =========================================================================
    s3 = prs.slides.add_slide(blank)
    set_slide_bg(s3, prs)
    add_slide_header(s3, "Core Innovation: The ScamGraph AI Paradigm Shift", slide_num=3)

    # Principle Banner
    prin = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.25), Inches(12.1), Inches(1.15))
    prin.fill.solid()
    prin.fill.fore_color.rgb = DARK_EMERALD
    prin.line.color.rgb = EMERALD
    prin.line.width = Pt(2)
    tf_pr = prin.text_frame
    tf_pr.word_wrap = True
    p = tf_pr.paragraphs[0]
    p.text = "CORE PRODUCT PRINCIPLE"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p2 = tf_pr.add_paragraph()
    p2.text = "Do NOT ask: \"Is this message spam?\"   ➔   Ask: \"What scam workflow is unfolding, how risky is it, what evidence supports that conclusion, and what should the user do next?\""
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = WHITE

    # Comparison Table
    rows, cols = 7, 3
    table_shape = s3.shapes.add_table(rows, cols, Inches(0.6), Inches(2.6), Inches(12.1), Inches(4.4))
    table = table_shape.table
    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(4.5)
    table.columns[2].width = Inches(5.0)

    headers = ["Capability", "Legacy Spam Classifiers", "ScamGraph AI Platform"]
    for c_idx, h in enumerate(headers):
        style_table_cell(table.cell(0, c_idx), h, font_size=11, bold=True, text_color=BG_DARK if c_idx==2 else WHITE, bg_color=EMERALD if c_idx==2 else BORDER_SLATE)

    comp_data = [
        ("Detection Scope", "Isolated single-message text classification", "Multi-event Scam Workflow State Machine (8 Playbooks)"),
        ("Campaign Tracking", "None — treats every reworded SMS as new", "Scam DNA Semantic Vectors (#UPI-KYC-042)"),
        ("Emerging Threats", "Static rule updates weeks after outbreak", "Unsupervised DBSCAN Clustering (+64% velocity alerts)"),
        ("Language Support", "English keyword matching", "Multilingual MuRIL + Hinglish Subword N-grams"),
        ("Alert Fatigue", "High false alarms on benign bank alerts", "Adaptive 4-Tier Intervention + Campaign Deduplication"),
        ("Explainability", "Black-box probability score only", "Plain-English Evidence + Next Attacker Move + Action")
    ]
    for r_idx, (cap, leg, sg) in enumerate(comp_data, start=1):
        bg = CARD_BG if r_idx % 2 == 1 else CARD_ALT
        style_table_cell(table.cell(r_idx, 0), cap, font_size=10, bold=True, text_color=CYAN, bg_color=bg)
        style_table_cell(table.cell(r_idx, 1), leg, font_size=10, bold=False, text_color=SLATE_MUTED, bg_color=bg)
        style_table_cell(table.cell(r_idx, 2), sg, font_size=10, bold=True, text_color=EMERALD, bg_color=bg)

    # =========================================================================
    # SLIDE 4: VISUAL SYSTEM ARCHITECTURE DIAGRAM
    # =========================================================================
    s4 = prs.slides.add_slide(blank)
    set_slide_bg(s4, prs)
    add_slide_header(s4, "System Architecture: Multi-Engine Fraud Intelligence Pipeline", slide_num=4)

    # Draw visual layered architecture using shapes
    # Layer 1: Input & Preprocessing
    b_in = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.3), Inches(12.1), Inches(0.8))
    b_in.fill.solid()
    b_in.fill.fore_color.rgb = CARD_BG
    b_in.line.color.rgb = CYAN
    tf = b_in.text_frame
    p = tf.paragraphs[0]
    p.text = "1. INPUT & ENTITY PRESERVATION LAYER  —  SMS • WhatsApp • Email • UPI Request • URL • Call/Chat Transcript"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = CYAN
    p.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph()
    p2.text = "Preserves URLs, ₹ Amounts, Phone Numbers, UPI Handles, OTP Keywords & Detects English / Hinglish"
    p2.font.size = Pt(10)
    p2.font.color.rgb = SLATE_LIGHT
    p2.alignment = PP_ALIGN.CENTER

    # Layer 2: 4 Parallel Intelligence Engines
    engines = [
        ("2A. NLP ML Engine", "MuRIL + Word/Char N-Grams\nBinary + 13-Class Taxonomy\n(Weight: 0.45)", EMERALD),
        ("2B. Signal Rule Engine", "11 Deterministic Indicators\nUrgency, Threat, KYC, OTP\n(Weight: 0.25)", CYAN),
        ("2C. URL Threat Analyzer", "Typosquatting, High-Abuse TLD\nHTTP, Brand Impersonation\n(Weight: 0.15)", AMBER),
        ("2D. Workflow Engine", "8 Attack Playbooks\nPartial Sequence Alignment\n(Weight: 0.15)", PURPLE)
    ]
    for idx, (e_title, e_desc, e_col) in enumerate(engines):
        left = Inches(0.6 + idx * 3.1)
        eb = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.35), Inches(2.8), Inches(1.55))
        eb.fill.solid()
        eb.fill.fore_color.rgb = CARD_BG
        eb.line.color.rgb = e_col
        eb.line.width = Pt(1.5)
        tfe = eb.text_frame
        tfe.word_wrap = True
        pe1 = tfe.paragraphs[0]
        pe1.text = e_title
        pe1.font.size = Pt(12)
        pe1.font.bold = True
        pe1.font.color.rgb = e_col
        pe1.alignment = PP_ALIGN.CENTER
        pe2 = tfe.add_paragraph()
        pe2.text = "\n" + e_desc
        pe2.font.size = Pt(10)
        pe2.font.color.rgb = WHITE
        pe2.alignment = PP_ALIGN.CENTER

    # Layer 3: Scam DNA & Risk Engine
    b_mid1 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(4.15), Inches(5.9), Inches(1.2))
    b_mid1.fill.solid()
    b_mid1.fill.fore_color.rgb = CARD_BG
    b_mid1.line.color.rgb = PURPLE
    tfm1 = b_mid1.text_frame
    tfm1.word_wrap = True
    pm1 = tfm1.paragraphs[0]
    pm1.text = "3. SCAM DNA & DBSCAN EMERGING ENGINE"
    pm1.font.size = Pt(12)
    pm1.font.bold = True
    pm1.font.color.rgb = PURPLE
    pm1.alignment = PP_ALIGN.CENTER
    pm1_sub = tfm1.add_paragraph()
    pm1_sub.text = "SentenceTransformer Cosine Similarity -> Campaign Tag (#UPI-KYC-042)\nUnsupervised DBSCAN Clusters -> Weekly Growth Velocity Alerts"
    pm1_sub.font.size = Pt(10)
    pm1_sub.font.color.rgb = SLATE_LIGHT
    pm1_sub.alignment = PP_ALIGN.CENTER

    b_mid2 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.15), Inches(5.9), Inches(1.2))
    b_mid2.fill.solid()
    b_mid2.fill.fore_color.rgb = DARK_EMERALD
    b_mid2.line.color.rgb = EMERALD
    tfm2 = b_mid2.text_frame
    tfm2.word_wrap = True
    pm2 = tfm2.paragraphs[0]
    pm2.text = "4. COMPOSITE RISK & ALERT FATIGUE ENGINE"
    pm2.font.size = Pt(12)
    pm2.font.bold = True
    pm2.font.color.rgb = EMERALD
    pm2.alignment = PP_ALIGN.CENTER
    pm2_sub = tfm2.add_paragraph()
    pm2_sub.text = "Risk = 0.45*ML + 0.25*Rule + 0.15*URL + 0.15*Workflow (0-100)\nTiers: LOW (0-29) • MEDIUM (30-59) • HIGH (60-79) • CRITICAL (80-100)"
    pm2_sub.font.size = Pt(10)
    pm2_sub.font.color.rgb = WHITE
    pm2_sub.alignment = PP_ALIGN.CENTER

    # Layer 4: Output Deliverables
    b_out = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(5.6), Inches(12.1), Inches(1.3))
    b_out.fill.solid()
    b_out.fill.fore_color.rgb = CARD_ALT
    b_out.line.color.rgb = EMERALD
    tfo = b_out.text_frame
    tfo.word_wrap = True
    po1 = tfo.paragraphs[0]
    po1.text = "5. ACTIONABLE OUTPUT & VISUALIZATION LAYER"
    po1.font.size = Pt(12)
    po1.font.bold = True
    po1.font.color.rgb = EMERALD
    po1.alignment = PP_ALIGN.CENTER
    po2 = tfo.add_paragraph()
    po2.text = "✓ Calibrated Risk Score (91/100)    ✓ Explainable 'Why' Evidence    ✓ Predicted Next Attacker Step\n" \
               "✓ React Flow Scam Graph Topology    ✓ Deduplicated Campaign Notice    ✓ Privacy-Redacted Storage"
    po2.font.size = Pt(11)
    po2.font.color.rgb = WHITE
    po2.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 5: UNIVERSAL FRAUD EVENT TAXONOMY (WORKFLOW CONTENT PART 1)
    # =========================================================================
    s5 = prs.slides.add_slide(blank)
    set_slide_bg(s5, prs)
    add_slide_header(s5, "Workflow Intelligence: Universal Fraud Event Taxonomy", slide_num=5)

    t_shape5 = s5.shapes.add_table(11, 4, Inches(0.6), Inches(1.3), Inches(12.1), Inches(5.7))
    t5 = t_shape5.table
    t5.columns[0].width = Inches(2.8)
    t5.columns[1].width = Inches(2.2)
    t5.columns[2].width = Inches(3.6)
    t5.columns[3].width = Inches(3.5)

    for c_i, h in enumerate(["Atomic Event Token", "Stage Role", "Detection Trigger Mechanism", "Real Message / Transcript Example"]):
        style_table_cell(t5.cell(0, c_i), h, 10, True, BG_DARK, EMERALD)

    events_rows = [
        ("KYC_WARNING", "Initial Hook", "Keywords: kyc, pan, aadhaar, yono, suspended", "'Your SBI YONO account KYC expired today'"),
        ("DISCONNECTION_THREAT", "Panic Hook", "Utility keywords + tonight / 9:30 PM outage", "'Electricity power will be cut tonight at 9:30 PM'"),
        ("LAW_ENFORCEMENT_IMP", "Fear Coercion", "CBI, Cyber Crime, Customs, FedEx, Warrant", "'Inspector Rajesh from Mumbai Cyber Crime'"),
        ("JOB_OR_LOTTERY_LURE", "Greed Hook", "Daily income, YouTube task, KBC 25 Lakhs", "'Earn ₹5,000 daily liking YouTube videos'"),
        ("URGENCY", "Psychological", "Immediately, turant, 24 hours, final notice", "'Update within 2 hours or account freezes'"),
        ("EXTERNAL_LINK", "Vector Delivery", "Regex URL extraction + suspicious TLD check", "'Click http://sbi-kyc-verify.xyz/login'"),
        ("REMOTE_ACCESS_REQ", "Device Takeover", "AnyDesk, TeamViewer, QuickSupport, APK", "'Install QuickSupport APK and share 9-digit code'"),
        ("CREDENTIAL_REQUEST", "Data Harvest", "CVV, NetBanking password, card details", "'Enter your username and card CVV to verify'"),
        ("OTP_REQUEST", "Auth Bypass", "6-digit OTP, verification code, share token", "'Tell the 6-digit OTP sent to your mobile'"),
        ("UPI_REQUEST", "Financial Drain", "Collect request, scan QR, enter UPI PIN", "'Scan QR and enter UPI PIN to receive ₹5,000'")
    ]
    for r_i, row_vals in enumerate(events_rows, start=1):
        bg = CARD_BG if r_i % 2 == 1 else CARD_ALT
        style_table_cell(t5.cell(r_i, 0), row_vals[0], 9, True, CYAN, bg)
        style_table_cell(t5.cell(r_i, 1), row_vals[1], 9, True, AMBER, bg)
        style_table_cell(t5.cell(r_i, 2), row_vals[2], 9, False, SLATE_LIGHT, bg)
        style_table_cell(t5.cell(r_i, 3), row_vals[3], 9, False, WHITE, bg)

    # =========================================================================
    # SLIDE 6: THE 8 CANONICAL SCAM WORKFLOW PLAYBOOKS
    # =========================================================================
    s6 = prs.slides.add_slide(blank)
    set_slide_bg(s6, prs)
    add_slide_header(s6, "Scam Workflow Engine: 8 Canonical Attack Playbooks", slide_num=6)

    playbooks_grid = [
        ("1. KYC Account Takeover (#UPI-KYC-042)", "KYC_WARNING ➔ URGENCY ➔ EXTERNAL_LINK ➔ CREDENTIAL_REQUEST ➔ OTP_REQUEST ➔ UNAUTHORIZED_TXN", "Exploits fear of bank account freeze to harvest NetBanking credentials and OTPs.", ROSE),
        ("2. Reverse UPI Collect Scam (#UPI-COLLECT-019)", "PAYMENT_LURE ➔ UPI_LINK ➔ URGENCY ➔ PIN_OR_OTP_REQUEST ➔ FINANCIAL_DRAIN", "Deceives victim into entering their secret UPI PIN under the guise of receiving a refund or OLX payment.", AMBER),
        ("3. Remote Tech/Bank Support (#SUPP-REMOTE-007)", "BANK_SUPPORT_IMPERSONATION ➔ DISPUTE_CLAIM ➔ REMOTE_ACCESS (AnyDesk) ➔ CREDENTIAL_REQUEST", "Tricks victim into installing screen-sharing tools to silently read SMS OTPs.", CYAN),
        ("4. Part-Time Job & VIP Task Trap (#TASK-JOB-088)", "JOB_OFFER ➔ INITIAL_REWARD (₹150) ➔ VIP_TASK_FEE ➔ ESCALATING_PAYMENT ➔ LOCKOUT", "Builds trust with micro-payouts before demanding large crypto/UPI deposits to unlock earnings.", EMERALD),
        ("5. Electricity Outage Panic (#ELEC-DISCONN-019)", "DISCONNECTION_THREAT ➔ URGENCY (Tonight) ➔ FAKE_OFFICER_CALL ➔ APK_OR_FEE ➔ OTP_DRAIN", "Creates evening panic about power disconnection to force interaction with a fake officer.", AMBER),
        ("6. Law Enforcement Digital Arrest (#CYBER-ARREST-104)", "POLICE_IMPERSONATION ➔ CONTRABAND_ACCUSATION ➔ SKYPE_ARREST_THREAT ➔ ESCROW_TRANSFER", "Coerces victims on video call into transferring savings to a fake 'RBI verification account'.", ROSE),
        ("7. Pre-Approved Loan Advance Fee (#LOAN-ADVANCE-031)", "LOAN_OFFER ➔ INSTANT_APPROVAL ➔ PROCESSING_OR_GST_FEE ➔ PAYMENT_REQUEST ➔ GHOSTING", "Offers 0% CIBIL-free loans and steals upfront processing/insurance fees.", PURPLE),
        ("8. KBC / Lucky Draw Prize Scam (#KBC-LUCKY-055)", "LOTTERY_WIN_ANNOUNCEMENT ➔ WHATSAPP_DIRECTIVE ➔ TAX_CLEARANCE_FEE ➔ PAYMENT_REQUEST", "Promises ₹25 Lakh lottery wins and demands advance government tax transfer via UPI.", CYAN)
    ]

    for idx, (pb_title, pb_chain, pb_desc, pb_col) in enumerate(playbooks_grid):
        col = idx % 2
        row = idx // 2
        left = Inches(0.6 + col * 6.15)
        top = Inches(1.3 + row * 1.42)
        tf_pb = add_box_card(s6, left, top, Inches(5.95), Inches(1.3), pb_title, border_color=pb_col, title_color=pb_col)
        p_ch = tf_pb.add_paragraph()
        p_ch.text = pb_chain
        p_ch.font.size = Pt(8.5)
        p_ch.font.bold = True
        p_ch.font.color.rgb = WHITE
        p_ds = tf_pb.add_paragraph()
        p_ds.text = pb_desc
        p_ds.font.size = Pt(8.5)
        p_ds.font.color.rgb = SLATE_MUTED

    # =========================================================================
    # SLIDE 7: WORKFLOW CONTENT DEEP-DIVE #1 (KYC & UPI COLLECT)
    # =========================================================================
    s7 = prs.slides.add_slide(blank)
    set_slide_bg(s7, prs)
    add_slide_header(s7, "Workflow Content Deep-Dive: KYC Fraud & Reverse UPI Scams", slide_num=7)

    # Table 1: KYC Workflow
    lbl1 = s7.shapes.add_textbox(Inches(0.6), Inches(1.2), Inches(12.0), Inches(0.35))
    lbl1.text_frame.paragraphs[0].text = "PLAYBOOK 1: KYC ACCOUNT TAKEOVER WORKFLOW (#UPI-KYC-042)"
    lbl1.text_frame.paragraphs[0].font.size = Pt(12)
    lbl1.text_frame.paragraphs[0].font.bold = True
    lbl1.text_frame.paragraphs[0].font.color.rgb = ROSE

    t_kyc = s7.shapes.add_table(5, 4, Inches(0.6), Inches(1.55), Inches(12.1), Inches(2.4)).table
    t_kyc.columns[0].width = Inches(1.8)
    t_kyc.columns[1].width = Inches(5.3)
    t_kyc.columns[2].width = Inches(2.5)
    t_kyc.columns[3].width = Inches(2.5)
    for ci, h in enumerate(["Workflow Stage", "Actual Scammer Content (English / Hinglish)", "Extracted Signals", "Engine State & Risk"]):
        style_table_cell(t_kyc.cell(0, ci), h, 9.5, True, WHITE, DARK_ROSE)

    kyc_steps = [
        ("Stage 1: Threat", "'Dear SBI Customer, your YONO account is suspended due to pending KYC.'", "kyc_request, threat", "Stage 1 Matched (Risk: 48)"),
        ("Stage 2: Link", "'Aapka khata band ho jayega. Click http://sbi-kyc-verify.xyz to update PAN.'", "urgency, suspicious_url", "Stage 3 Matched (Risk: 76)"),
        ("Stage 3: Harvest", "'Enter your NetBanking Username, Password & Date of Birth on portal.'", "credential_request", "Stage 4 Matched (Risk: 86)"),
        ("Stage 4: OTP", "'Share the 6-digit high-security OTP sent to your mobile to restore access.'", "otp_request", "WORKFLOW DETECTED (91/100)")
    ]
    for ri, rdata in enumerate(kyc_steps, start=1):
        bg = CARD_BG if ri % 2 == 1 else CARD_ALT
        style_table_cell(t_kyc.cell(ri, 0), rdata[0], 9, True, CYAN, bg)
        style_table_cell(t_kyc.cell(ri, 1), rdata[1], 9, False, WHITE, bg)
        style_table_cell(t_kyc.cell(ri, 2), rdata[2], 9, False, AMBER, bg)
        style_table_cell(t_kyc.cell(ri, 3), rdata[3], 9, True, EMERALD if ri<4 else ROSE, bg)

    # Table 2: UPI Collect Workflow
    lbl2 = s7.shapes.add_textbox(Inches(0.6), Inches(4.15), Inches(12.0), Inches(0.35))
    lbl2.text_frame.paragraphs[0].text = "PLAYBOOK 2: REVERSE UPI COLLECT / REFUND TRAP (#UPI-COLLECT-019)"
    lbl2.text_frame.paragraphs[0].font.size = Pt(12)
    lbl2.text_frame.paragraphs[0].font.bold = True
    lbl2.text_frame.paragraphs[0].font.color.rgb = AMBER

    t_upi = s7.shapes.add_table(5, 4, Inches(0.6), Inches(4.5), Inches(12.1), Inches(2.4)).table
    t_upi.columns[0].width = Inches(1.8)
    t_upi.columns[1].width = Inches(5.3)
    t_upi.columns[2].width = Inches(2.5)
    t_upi.columns[3].width = Inches(2.5)
    for ci, h in enumerate(["Workflow Stage", "Actual Scammer Content (English / Hinglish)", "Extracted Signals", "Engine State & Risk"]):
        style_table_cell(t_upi.cell(0, ci), h, 9.5, True, BG_DARK, AMBER)

    upi_steps = [
        ("Stage 1: Lure", "'You have won a PhonePe cashback scratch card of ₹4,999! Claim now.'", "reward_lure", "Stage 1 Matched (Risk: 42)"),
        ("Stage 2: Collect", "'Bhai maine galti se ₹5,000 bhej diye, approve collect link: http://upi-claim.in'", "payment_request, url", "Stage 2 Matched (Risk: 68)"),
        ("Stage 3: Urgency", "'Cashback link expires in 10 minutes. Open Google Pay immediately.'", "urgency", "Stage 3 Matched (Risk: 78)"),
        ("Stage 4: PIN Trap", "'Paise account mein receive karne ke liye QR scan karein aur 6-digit UPI PIN dalein.'", "otp_request, upi_pin", "WORKFLOW DETECTED (93/100)")
    ]
    for ri, rdata in enumerate(upi_steps, start=1):
        bg = CARD_BG if ri % 2 == 1 else CARD_ALT
        style_table_cell(t_upi.cell(ri, 0), rdata[0], 9, True, CYAN, bg)
        style_table_cell(t_upi.cell(ri, 1), rdata[1], 9, False, WHITE, bg)
        style_table_cell(t_upi.cell(ri, 2), rdata[2], 9, False, AMBER, bg)
        style_table_cell(t_upi.cell(ri, 3), rdata[3], 9, True, EMERALD if ri<4 else ROSE, bg)

    # =========================================================================
    # SLIDE 8: WORKFLOW CONTENT DEEP-DIVE #2 (DIGITAL ARREST & ELECTRICITY)
    # =========================================================================
    s8 = prs.slides.add_slide(blank)
    set_slide_bg(s8, prs)
    add_slide_header(s8, "Workflow Content Deep-Dive: Digital Arrest & Electricity Scams", slide_num=8)

    # Table 1: Digital Arrest
    lbl3 = s8.shapes.add_textbox(Inches(0.6), Inches(1.2), Inches(12.0), Inches(0.35))
    lbl3.text_frame.paragraphs[0].text = "PLAYBOOK 3: LAW ENFORCEMENT DIGITAL ARREST EXTORTION (#CYBER-ARREST-104)"
    lbl3.text_frame.paragraphs[0].font.size = Pt(12)
    lbl3.text_frame.paragraphs[0].font.bold = True
    lbl3.text_frame.paragraphs[0].font.color.rgb = PURPLE

    t_da = s8.shapes.add_table(5, 4, Inches(0.6), Inches(1.55), Inches(12.1), Inches(2.4)).table
    t_da.columns[0].width = Inches(1.8)
    t_da.columns[1].width = Inches(5.3)
    t_da.columns[2].width = Inches(2.5)
    t_da.columns[3].width = Inches(2.5)
    for ci, h in enumerate(["Workflow Stage", "Actual Scammer Content (Call / Chat Transcript)", "Extracted Signals", "Engine State & Risk"]):
        style_table_cell(t_da.cell(0, ci), h, 9.5, True, WHITE, PURPLE)

    da_steps = [
        ("Stage 1: Authority", "'This is Inspector Rajesh Kumar from Mumbai Cyber Crime / CBI Headquarters.'", "impersonation", "Stage 1 Matched (Risk: 52)"),
        ("Stage 2: Contraband", "'A FedEx parcel in your name containing 5 passports & 160g MDMA drugs was seized.'", "threat, contraband", "Stage 2 Matched (Risk: 79)"),
        ("Stage 3: Isolation", "'Non-bailable warrant issued on your Aadhaar. Stay on Skype video call under Digital Arrest.'", "urgency, arrest_threat", "Stage 4 Matched (Risk: 90)"),
        ("Stage 4: Escrow", "'Transfer all funds to RBI Safety Escrow Account for audit to prove innocence.'", "payment_request", "WORKFLOW DETECTED (98/100)")
    ]
    for ri, rdata in enumerate(da_steps, start=1):
        bg = CARD_BG if ri % 2 == 1 else CARD_ALT
        style_table_cell(t_da.cell(ri, 0), rdata[0], 9, True, CYAN, bg)
        style_table_cell(t_da.cell(ri, 1), rdata[1], 9, False, WHITE, bg)
        style_table_cell(t_da.cell(ri, 2), rdata[2], 9, False, AMBER, bg)
        style_table_cell(t_da.cell(ri, 3), rdata[3], 9, True, EMERALD if ri<4 else ROSE, bg)

    # Table 2: Electricity Disconnection
    lbl4 = s8.shapes.add_textbox(Inches(0.6), Inches(4.15), Inches(12.0), Inches(0.35))
    lbl4.text_frame.paragraphs[0].text = "PLAYBOOK 4: NIGHT ELECTRICITY DISCONNECTION PANIC (#ELEC-DISCONN-019)"
    lbl4.text_frame.paragraphs[0].font.size = Pt(12)
    lbl4.text_frame.paragraphs[0].font.bold = True
    lbl4.text_frame.paragraphs[0].font.color.rgb = CYAN

    t_el = s8.shapes.add_table(5, 4, Inches(0.6), Inches(4.5), Inches(12.1), Inches(2.4)).table
    t_el.columns[0].width = Inches(1.8)
    t_el.columns[1].width = Inches(5.3)
    t_el.columns[2].width = Inches(2.5)
    t_el.columns[3].width = Inches(2.5)
    for ci, h in enumerate(["Workflow Stage", "Actual Scammer Content (English / Hinglish)", "Extracted Signals", "Engine State & Risk"]):
        style_table_cell(t_el.cell(0, ci), h, 9.5, True, BG_DARK, CYAN)

    el_steps = [
        ("Stage 1: Outage", "'Dear Consumer, aapki bijli aaj raat 9:30 baje sub-station se kaat di jayegi.'", "threat, utility", "Stage 1 Matched (Risk: 55)"),
        ("Stage 2: Urgency", "'Previous month bill was not updated. Only 1 hour remaining before disconnection.'", "urgency", "Stage 2 Matched (Risk: 70)"),
        ("Stage 3: Fake SDO", "'Immediately contact Electricity SDO Officer Sharma at +91-9876543210.'", "phone_contact, impersonation", "Stage 3 Matched (Risk: 83)"),
        ("Stage 4: APK/Fee", "'Pay ₹10 meter update charge at http://bses-portal.in and share SMS OTP.'", "payment, url, otp", "WORKFLOW DETECTED (92/100)")
    ]
    for ri, rdata in enumerate(el_steps, start=1):
        bg = CARD_BG if ri % 2 == 1 else CARD_ALT
        style_table_cell(t_el.cell(ri, 0), rdata[0], 9, True, CYAN, bg)
        style_table_cell(t_el.cell(ri, 1), rdata[1], 9, False, WHITE, bg)
        style_table_cell(t_el.cell(ri, 2), rdata[2], 9, False, AMBER, bg)
        style_table_cell(t_el.cell(ri, 3), rdata[3], 9, True, EMERALD if ri<4 else ROSE, bg)

    # =========================================================================
    # SLIDE 9: PARTIAL MATCHING & PREDICTIVE INTERVENTION
    # =========================================================================
    s9 = prs.slides.add_slide(blank)
    set_slide_bg(s9, prs)
    add_slide_header(s9, "Predictive Workflow Engine: Stopping Scams Mid-Flight", slide_num=9)

    tf_pm = add_box_card(s9, Inches(0.6), Inches(1.3), Inches(5.8), Inches(3.2), "Partial-Order Sequence Alignment Math", border_color=EMERALD, title_color=EMERALD)
    add_bullet(tf_pm, "Why Partial Matching?", "Users rarely paste all 6 steps at once. We must detect the workflow when only 2 or 3 events have occurred.", 11)
    add_bullet(tf_pm, "Overlap Ratio:", "|Detected_Events ∩ Playbook_Steps| / |Playbook_Steps|", 11, color=CYAN)
    add_bullet(tf_pm, "Category Synergy Bonus:", "+0.20 boost when ML classifier category aligns with the playbook category.", 11)
    add_bullet(tf_pm, "Formula:", "Confidence = min(0.99, 0.50 + 0.45 * Overlap + Category_Bonus)", 11, color=EMERALD)

    tf_pr = add_box_card(s9, Inches(6.8), Inches(1.3), Inches(5.9), Inches(3.2), "Example: Partial Match at Stage 3 (82% Confidence)", border_color=AMBER, title_color=AMBER)
    add_bullet(tf_pr, "Observed Events:", "[KYC_WARNING]  ➔  [URGENCY]  ➔  [EXTERNAL_LINK]", 11, color=WHITE)
    add_bullet(tf_pr, "Missing Future Events:", "[CREDENTIAL_REQUEST]  ➔  [OTP_REQUEST]  ➔  [DRAIN]", 11, color=SLATE_MUTED)
    add_bullet(tf_pr, "Classification:", "Potential KYC Scam Workflow — 82% Confidence", 11, color=AMBER)
    add_bullet(tf_pr, "Next Move Prediction:", "'Attacker will attempt Credential & OTP Harvesting next. Do not open link.'", 11, color=EMERALD)

    # Visual Stepper showing Observed vs Predicted
    stepper_title = s9.shapes.add_textbox(Inches(0.6), Inches(4.7), Inches(12.0), Inches(0.35))
    stepper_title.text_frame.paragraphs[0].text = "LIVE STAGE PROGRESSION TRACKER (OBSERVED VS. PREDICTED ATTACKER MOVES)"
    stepper_title.text_frame.paragraphs[0].font.size = Pt(11)
    stepper_title.text_frame.paragraphs[0].font.bold = True
    stepper_title.text_frame.paragraphs[0].font.color.rgb = CYAN

    st_items = [
        ("Stage 1: KYC Warning", "✓ OBSERVED", DARK_EMERALD, EMERALD),
        ("Stage 2: Urgency Threat", "✓ OBSERVED", DARK_EMERALD, EMERALD),
        ("Stage 3: Phishing Link", "✓ CURRENT STAGE", DARK_EMERALD, CYAN),
        ("Stage 4: Credential Input", "⚡ PREDICTED NEXT", DARK_ROSE, ROSE),
        ("Stage 5: OTP Theft", "⚡ PREDICTED", CARD_BG, SLATE_MUTED),
        ("Stage 6: Account Drain", "🛑 PREVENTED", CARD_BG, SLATE_MUTED)
    ]
    for idx, (st_name, st_stat, bg_c, br_c) in enumerate(st_items):
        left = Inches(0.6 + idx * 2.05)
        sb = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(5.15), Inches(1.85), Inches(1.5))
        sb.fill.solid()
        sb.fill.fore_color.rgb = bg_c
        sb.line.color.rgb = br_c
        sb.line.width = Pt(2)
        tfs = sb.text_frame
        tfs.word_wrap = True
        p1 = tfs.paragraphs[0]
        p1.text = st_stat
        p1.font.size = Pt(9)
        p1.font.bold = True
        p1.font.color.rgb = br_c
        p1.alignment = PP_ALIGN.CENTER
        p2 = tfs.add_paragraph()
        p2.text = "\n" + st_name
        p2.font.size = Pt(10.5)
        p2.font.bold = True
        p2.font.color.rgb = WHITE
        p2.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 10: SCAM DNA & EMERGING PATTERN DISCOVERY
    # =========================================================================
    s10 = prs.slides.add_slide(blank)
    set_slide_bg(s10, prs)
    add_slide_header(s10, "Scam DNA Fingerprinting & Emerging Pattern Discovery", slide_num=10)

    tf_dna = add_box_card(s10, Inches(0.6), Inches(1.3), Inches(5.8), Inches(5.5), "Scam DNA: Semantic Campaign Fingerprinting", border_color=PURPLE, title_color=PURPLE)
    add_bullet(tf_dna, "The Problem:", "Scammers mutate bank names (SBI -> HDFC) and URLs every hour to bypass hash filters.", 11)
    add_bullet(tf_dna, "Our Solution:", "We encode messages using SentenceTransformer ('all-MiniLM-L6-v2') + structural signal vectors.", 11)
    add_bullet(tf_dna, "Variant A:", "'Your SBI KYC will expire today. Update now.'", 10.5, color=CYAN)
    add_bullet(tf_dna, "Variant B:", "'Dear customer, your bank KYC is pending. Verify immediately.'", 10.5, color=CYAN)
    add_bullet(tf_dna, "Variant C (Hinglish):", "'Aapka SBI account block ho jayega, KYC update karein.'", 10.5, color=CYAN)
    add_bullet(tf_dna, "Shared Fingerprint:", "All 3 resolve to Scam DNA: #UPI-KYC-042 (Cosine Sim > 0.78)", 11, color=EMERALD)

    tf_em = add_box_card(s10, Inches(6.8), Inches(1.3), Inches(5.9), Inches(2.5), "Unsupervised Emerging Discovery (DBSCAN)", border_color=CYAN, title_color=CYAN)
    add_bullet(tf_em, "Incident Vector:", "[Embedding + Category + Signals + Workflow + Timestamp]", 10.5)
    add_bullet(tf_em, "Density Clustering:", "DBSCAN groups unknown scam waves without requiring pre-labeled classes.", 10.5)
    add_bullet(tf_em, "Growth Alert:", "Clusters growing >30% WoW trigger '⚠️ Emerging Scam Pattern Detected'.", 10.5, color=AMBER)

    # 4 Emerging Cluster Cards
    clusters = [
        ("#UPI-KYC-042", "YONO / Bank KYC APK Wave", "117 Reports", "+64% this week", "CRITICAL", ROSE),
        ("#ELEC-DISCONN-019", "Night Power Outage Scam", "83 Reports", "+41% this week", "HIGH", AMBER),
        ("#CYBER-ARREST-104", "FedEx / CBI Digital Arrest", "64 Reports", "+78% this week", "CRITICAL", ROSE),
        ("#TASK-JOB-088", "Telegram YouTube Like Tasks", "142 Reports", "+55% this week", "HIGH", EMERALD)
    ]
    for idx, (c_id, c_name, c_rep, c_gr, c_rk, c_col) in enumerate(clusters):
        col = idx % 2
        row = idx // 2
        left = Inches(6.8 + col * 3.0)
        top = Inches(4.0 + row * 1.45)
        cb = add_box_card(s10, left, top, Inches(2.9), Inches(1.35), f"{c_id} ({c_rk})", border_color=c_col, title_color=c_col)
        p = cb.add_paragraph()
        p.text = f"{c_name}\n{c_rep}  •  {c_gr}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 11: MACHINE LEARNING PIPELINE & REAL CONFUSION MATRIX
    # =========================================================================
    s11 = prs.slides.add_slide(blank)
    set_slide_bg(s11, prs)
    add_slide_header(s11, "Machine Learning Pipeline & Real Test Evaluation", slide_num=11)

    tf_ml = add_box_card(s11, Inches(0.6), Inches(1.3), Inches(6.6), Inches(5.5), "Trained Model Architecture & Dataset Splits", border_color=EMERALD, title_color=EMERALD)
    add_bullet(tf_ml, "Multilingual Architecture:", "Google MuRIL ('google/muril-base-cased') + Dual TF-IDF FeatureUnion (Word 1-2 + Char 2-5 subwords) with Sigmoid Platt Calibration.", 10.5)
    add_bullet(tf_ml, "Authentic Dataset:", "276 unique curated Indian scam & benign samples (80.4% English, 19.6% Hinglish) across 13 categories.", 10.5)
    add_bullet(tf_ml, "Stratified Splits:", "70% Train (193 rows) • 15% Validation (41 rows) • 15% Held-Out Test (42 rows).", 10.5, color=CYAN)
    add_bullet(tf_ml, "Test Recall (Fraud Capture):", "100.00% — Zero false negatives on held-out test set.", 11, color=EMERALD)
    add_bullet(tf_ml, "Test Precision:", "96.43% — Minimal false alarms on legitimate bank alerts.", 11, color=EMERALD)
    add_bullet(tf_ml, "Test F1 Score:", "98.18%  |  ROC-AUC: 1.0000  |  Accuracy: 97.62%", 11, color=WHITE)
    add_bullet(tf_ml, "13 Category Head:", "87.80% Validation Accuracy across KYC, UPI, OTP, Phishing, Banking, Job, Loan, Lottery, Electricity, Investment, Digital Arrest, Impersonation, Other.", 10)

    # Embed actual confusion_matrix.png image on the right card!
    cm_card = add_box_card(s11, Inches(7.5), Inches(1.3), Inches(5.2), Inches(5.5), "Held-Out Test Confusion Matrix", border_color=CYAN, title_color=CYAN)
    if os.path.exists(CM_IMAGE_PATH):
        s11.shapes.add_picture(CM_IMAGE_PATH, Inches(7.85), Inches(1.95), width=Inches(4.5))
    else:
        add_bullet(cm_card, "Confusion Matrix:", "TN=14, FP=1, FN=0, TP=27", 12)

    # =========================================================================
    # SLIDE 12: ZERO ALERT FATIGUE & EXPLAINABLE AI
    # =========================================================================
    s12 = prs.slides.add_slide(blank)
    set_slide_bg(s12, prs)
    add_slide_header(s12, "Alert Fatigue Prevention & Explainable AI", slide_num=12)

    # 4 Adaptive Alert Tiers
    tiers = [
        ("LOW (0–29)", "Passive Monitoring", "No interruption. Shown as verified or normal message.", EMERALD),
        ("MEDIUM (30–59)", "Advisory Caution", "'Be careful before interacting. Verify sender independently.'", CYAN),
        ("HIGH (60–79)", "Strong Warning", "'Multiple scam indicators & partial workflow detected.'", AMBER),
        ("CRITICAL (80–100)", "Blocking Intervention", "'STOP — Active multi-stage financial scam workflow.'", ROSE)
    ]
    for idx, (t_rng, t_type, t_msg, t_col) in enumerate(tiers):
        left = Inches(0.6 + idx * 3.1)
        tc = add_box_card(s12, left, Inches(1.3), Inches(2.85), Inches(1.9), t_rng, border_color=t_col, title_color=t_col)
        p1 = tc.add_paragraph()
        p1.text = t_type
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = WHITE
        p2 = tc.add_paragraph()
        p2.text = "\n" + t_msg
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = SLATE_LIGHT

    tf_dedup = add_box_card(s12, Inches(0.6), Inches(3.5), Inches(5.8), Inches(3.4), "Campaign Deduplication (Anti-Fatigue)", border_color=PURPLE, title_color=PURPLE)
    add_bullet(tf_dedup, "The Nuisance Problem:", "Victims often receive 5 identical SMS messages from different numbers in 10 minutes.", 11)
    add_bullet(tf_dedup, "Scam DNA Suppression:", "Instead of firing 5 separate blocking popups, ScamGraph AI matches the Scam DNA (#UPI-KYC-042) and groups them:", 11)
    add_bullet(tf_dedup, "Grouped Banner:", "'🛡️ 118 similar messages detected from active campaign (#UPI-KYC-042).'", 11, color=EMERALD)

    tf_xai = add_box_card(s12, Inches(6.8), Inches(3.5), Inches(5.9), Inches(3.4), "Explainable AI Output Structure", border_color=EMERALD, title_color=EMERALD)
    add_bullet(tf_xai, "Risk Score:", "91 / 100 — CRITICAL RISK (KYC Fraud)", 11, color=ROSE)
    add_bullet(tf_xai, "Why? (Evidence):", "✓ Account freeze threat  ✓ Urgency pressure  ✓ Brand typosquatting URL (sbi-kyc-verify.xyz)  ✓ Requests OTP", 10.5)
    add_bullet(tf_xai, "Actionable Advice:", "'Do NOT click the verification link or share your OTP. Open your bank's official YONO app directly.'", 10.5, color=EMERALD)

    # =========================================================================
    # SLIDE 13: VISUAL SCAM GRAPH TOPOLOGY (REACT FLOW)
    # =========================================================================
    s13 = prs.slides.add_slide(blank)
    set_slide_bg(s13, prs)
    add_slide_header(s13, "Interactive Scam Graph: Visual Attack Topology", slide_num=13)

    # Draw visual node-link diagram on left
    graph_nodes = [
        ("Sender Node", "+91-9823419821 (Unknown Origin)", DARK_EMERALD, EMERALD, "SENT"),
        ("Payload Node", "'Dear SBI Customer, KYC suspended...'", CARD_BG, SLATE_LIGHT, "CONTAINS"),
        ("Phishing URL Node", "http://sbi-kyc-update.xyz/login", DARK_ROSE, ROSE, "LINKS_TO"),
        ("Impersonated Domain", "Fake Bank Portal (.xyz TLD)", CARD_BG, AMBER, "USES"),
        ("Workflow Stage Node", "Credential & OTP Request", CARD_BG, PURPLE, "MATCHES"),
        ("Scam DNA & Category", "#UPI-KYC-042  ➔  KYC Fraud Category", DARK_EMERALD, CYAN, None)
    ]
    for idx, (n_type, n_val, n_bg, n_col, edge_lbl) in enumerate(graph_nodes):
        top = Inches(1.3 + idx * 0.92)
        nb = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(5.5), Inches(0.62))
        nb.fill.solid()
        nb.fill.fore_color.rgb = n_bg
        nb.line.color.rgb = n_col
        nb.line.width = Pt(1.5)
        tfn = nb.text_frame
        p = tfn.paragraphs[0]
        p.text = f"[{n_type.upper()}]   {n_val}"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

        if edge_lbl:
            lbl_box = s13.shapes.add_textbox(Inches(2.8), top + Inches(0.61), Inches(1.5), Inches(0.3))
            pl = lbl_box.text_frame.paragraphs[0]
            pl.text = f"↓ {edge_lbl}"
            pl.font.size = Pt(8.5)
            pl.font.bold = True
            pl.font.color.rgb = EMERALD
            pl.alignment = PP_ALIGN.CENTER

    tf_gi = add_box_card(s13, Inches(6.8), Inches(1.3), Inches(5.9), Inches(5.5), "Why Graph Topology Matters for Security Teams", border_color=CYAN, title_color=CYAN)
    add_bullet(tf_gi, "1. Powered by React Flow 12:", "Interactive pan, zoom, animated edges, and live node attribute inspection.", 11)
    add_bullet(tf_gi, "2. Entity-Relationship Mapping:", "Connects Phone Numbers, Messages, URLs, Domains, UPI Handles, Scam DNA, and Categories.", 11)
    add_bullet(tf_gi, "3. Fraud Ring Attribution:", "Reveals when 50 different phone numbers link to the exact same UPI ID or phishing domain.", 11)
    add_bullet(tf_gi, "4. One-Click Investigation:", "Security analysts click any node to inspect its TLD flags, protocol status, and campaign history.", 11)

    # =========================================================================
    # SLIDE 14: 5-STEP GUIDED DEMO WALKTHROUGH (SECTION 28)
    # =========================================================================
    s14 = prs.slides.add_slide(blank)
    set_slide_bg(s14, prs)
    add_slide_header(s14, "Live Demo Story: Watching a Scam Workflow Unfold", slide_num=14)

    demo_steps = [
        ("STEP 1", "Suspicious Threat", "'Your bank KYC will expire today. Update immediately.'", "Detects urgency & account threat signals -> Risk: 52 (MEDIUM)", CYAN),
        ("STEP 2", "Phishing URL Added", "Adds link: 'http://sbi-kyc-verify.xyz/login'", "URL Analyzer flags .xyz TLD, HTTP, & SBI impersonation -> Risk: 76 (HIGH)", AMBER),
        ("STEP 3", "OTP Harvest Added", "Adds: 'Enter PAN and share 6-digit OTP to verify.'", "Workflow Engine aligns 4 stages of KYC Playbook -> Risk: 88 (CRITICAL)", ROSE),
        ("STEP 4", "Workflow Detected", "Full multi-step attack + ₹1 UPI mandate", "Triggers SCAM WORKFLOW DETECTED (91/100) + Scam DNA: #UPI-KYC-042", ROSE),
        ("STEP 5", "Emerging Cluster", "Opens Emerging Patterns & Scam Graph", "Displays 117 linked reports (+64% weekly growth) & full React Flow graph", EMERALD)
    ]
    for idx, (d_st, d_title, d_in, d_out, d_col) in enumerate(demo_steps):
        top = Inches(1.3 + idx * 1.12)
        card = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), top, Inches(12.1), Inches(0.98))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = d_col
        card.line.width = Pt(1.5)
        tfd = card.text_frame
        tfd.word_wrap = True
        p1 = tfd.paragraphs[0]
        p1.text = f"{d_st}: {d_title.upper()}   |   Input: {d_in}"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = d_col
        p2 = tfd.add_paragraph()
        p2.text = f"System Response:  {d_out}"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 15: PRIVACY, IMPACT & FUTURE ROADMAP
    # =========================================================================
    s15 = prs.slides.add_slide(blank)
    set_slide_bg(s15, prs)
    add_slide_header(s15, "Privacy by Design, Deployment & Future Roadmap", slide_num=15)

    tf_priv = add_box_card(s15, Inches(0.6), Inches(1.3), Inches(3.8), Inches(5.5), "1. Security & Privacy Core", border_color=EMERALD, title_color=EMERALD)
    add_bullet(tf_priv, "Auto PII Redaction:", "Masks 16-digit cards, CVVs, passwords, and OTPs in-memory before logging.", 10.5)
    add_bullet(tf_priv, "Identifier Hashing:", "Sender numbers & contacts hashed via SHA-256 / UUID5.", 10.5)
    add_bullet(tf_priv, "Zero Raw Archival:", "Stores only redacted previews & signal vectors.", 10.5)
    add_bullet(tf_priv, "One-Click Purge:", "DELETE /api/incidents/clear wipes local history immediately.", 10.5)

    tf_dep = add_box_card(s15, Inches(4.75), Inches(1.3), Inches(3.8), Inches(5.5), "2. Production Stack", border_color=CYAN, title_color=CYAN)
    add_bullet(tf_dep, "Backend:", "FastAPI + SQLAlchemy (SQLite / PostgreSQL) + Pytest (7/7 Passing).", 10.5)
    add_bullet(tf_dep, "Frontend:", "React 18 + Vite + Tailwind CSS + Recharts + React Flow 12.", 10.5)
    add_bullet(tf_dep, "ML Stack:", "PyTorch + Transformers (MuRIL) + Scikit-Learn + SentenceTransformers.", 10.5)
    add_bullet(tf_dep, "Dockerized:", "Multi-container docker-compose.yml with Nginx reverse proxy.", 10.5)

    tf_road = add_box_card(s15, Inches(8.9), Inches(1.3), Inches(3.8), Inches(5.5), "3. Future Impact & Scale", border_color=PURPLE, title_color=PURPLE)
    add_bullet(tf_road, "Banking SDK:", "Pre-transaction warning hook inside UPI & NetBanking apps.", 10.5)
    add_bullet(tf_road, "Live Call Audio:", "Real-time Indic speech-to-text stream interception for Digital Arrest calls.", 10.5)
    add_bullet(tf_road, "1930 Cyber Crime Sync:", "Automated Scam DNA feed for national takedowns.", 10.5)
    add_bullet(tf_road, "GitHub Repo:", "github.com/Nishkarsh807/scamgraph-ai", 10.5, color=EMERALD)

    prs.save(OUTPUT_PPTX)
    print(f"Presentation saved successfully: {OUTPUT_PPTX} (Total Slides: {len(prs.slides)})")


if __name__ == "__main__":
    build_presentation()
