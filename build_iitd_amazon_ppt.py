"""
ScamGraph - IIT Delhi Amazon Hackathon Pitch Deck Generator (9 Slides)
Aesthetic: Gen Z Minimalist Monochromatic & Subtle Pastel Vibe
Palette inspired by user's Napkin funnel graphic:
- Warm Alabaster / Cream Canvas (#FAF7F2)
- Soft Oat / Stone Bento Cards (#F2ECE4 & #FFFFFF)
- Deep Muted Plum Charcoal Typography (#3F2E46)
- Subtle Pastel Accents:
  - Sage Teal (#84C1B5)
  - Soft Matcha Mint (#B6C99B)
  - Warm Pastel Ochre (#E3C778)
  - Soft Apricot Peach (#F3A953)
  - Dusty Lavender (#D6CDEA)
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "docs", "ppt_assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

UPLOADED_FUNNEL_IMG = os.path.join(ASSETS_DIR, "ppt", "media", "image1.png")
OUTPUT_PPTX = os.path.join(BASE_DIR, "ScamGraph_IITD_Amazon_Hackathon.pptx")
OUTPUT_PPTX_MAIN = os.path.join(BASE_DIR, "ScamGraph_AI_Hackathon_Pitch.pptx")

# ==============================================================================
# GEN Z MONOCHROMATIC + SUBTLE PASTEL PALETTE
# ==============================================================================
BG_CREAM      = RGBColor(250, 247, 242)   # #FAF7F2 Warm Alabaster
CARD_WHITE    = RGBColor(255, 255, 255)   # #FFFFFF Crisp Card
CARD_OAT      = RGBColor(242, 236, 228)   # #F2ECE4 Soft Monochromatic Stone
CARD_LAVENDER = RGBColor(238, 233, 246)   # #EEE9F6 Subtle Pastel Lilac
CARD_SAGE     = RGBColor(229, 242, 239)   # #E5F2EF Subtle Pastel Sage
CARD_PEACH    = RGBColor(253, 239, 224)   # #FDEFE0 Subtle Pastel Peach
CARD_MINT     = RGBColor(236, 243, 228)   # #ECF3E4 Subtle Pastel Mint

INK_PLUM      = RGBColor(63, 46, 70)      # #3F2E46 Deep Muted Plum (Primary Ink)
INK_MUTED     = RGBColor(118, 104, 125)   # #76687D Soft Muted Mauve-Grey
BORDER_SOFT   = RGBColor(222, 214, 205)   # #DED6CD Subtle Warm Border

PASTEL_TEAL   = RGBColor(132, 193, 181)   # #84C1B5 Sage Teal
PASTEL_MINT   = RGBColor(182, 201, 155)   # #B6C99B Soft Mint
PASTEL_OCHRE  = RGBColor(227, 199, 120)   # #E3C778 Warm Ochre
PASTEL_PEACH  = RGBColor(243, 169, 83)    # #F3A953 Soft Apricot
PASTEL_MAUVE  = RGBColor(186, 166, 209)   # #BAA6D1 Dusty Mauve


def generate_visual_assets():
    """Generates high-DPI pastel charts and topology diagrams matching the deck theme."""
    plt.rcParams['font.sans-serif'] = 'Segoe UI'
    plt.rcParams['axes.edgecolor'] = '#DED6CD'
    plt.rcParams['axes.linewidth'] = 1.0

    # 1. Sequence Risk Escalation Chart (Slide 3)
    fig, ax = plt.subplots(figsize=(5.5, 3.2), dpi=240)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAF7F2')

    stages = ['1. KYC\nSMS', '2. Phish\nURL', '3. New\nDevice', '4. New\nBeneficiary', '5. UPI\nCollect', '6. ₹1.5L\nPayment']
    journey_risk = [18, 42, 61, 78, 91, 96]
    isolated_risk = [18, 35, 22, 25, 30, 45]

    x = np.arange(len(stages))
    ax.fill_between(x, journey_risk, color='#84C1B5', alpha=0.28)
    ax.plot(x, journey_risk, marker='o', color='#3F2E46', linewidth=2.8, markersize=7, label='ScamGraph Journey Score')
    ax.plot(x, isolated_risk, marker='s', linestyle='--', color='#BAA6D1', linewidth=2.0, markersize=5, label='Isolated Event Score')

    ax.axhline(75, color='#F3A953', linestyle=':', linewidth=1.5, label='Intervention Threshold')
    for i, v in enumerate(journey_risk):
        ax.annotate(f"{v}", (x[i], v + 4), ha='center', fontsize=8.5, fontweight='bold', color='#3F2E46')

    ax.set_ylim(0, 112)
    ax.set_xticks(x)
    ax.set_xticklabels(stages, fontsize=8, color='#3F2E46', fontweight='bold')
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.tick_params(axis='y', colors='#76687D', labelsize=8)
    ax.set_title('Journey Risk Escalation vs. Isolated Event Scoring', fontsize=10, fontweight='bold', color='#3F2E46', pad=10)
    ax.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#DED6CD', fontsize=7.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    chart1_path = os.path.join(ASSETS_DIR, "journey_escalation.png")
    fig.savefig(chart1_path, dpi=240)
    plt.close()

    # 2. Alert Fatigue & Risk Comparison Chart (Slide 7)
    fig, ax = plt.subplots(figsize=(5.4, 2.7), dpi=240)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAF7F2')

    examples = ['Ex 1: Legitimate\n(Known Dev + ₹2K)', 'Ex 2: Suspicious\n(New Dev + ₹30K)', 'Ex 3: AI Scam\n(Full Sequence + ₹1.5L)']
    scores = [8, 61, 96]
    colors = ['#B6C99B', '#E3C778', '#F3A953']

    bars = ax.barh(examples, scores, color=colors, height=0.52, edgecolor='#3F2E46', linewidth=1.0)
    ax.set_xlim(0, 142)
    for bar, s, act in zip(bars, scores, ['8/100 → Silent Allow', '61/100 → Verify', '96/100 → Critical Hold']):
        ax.text(s + 3, bar.get_y() + bar.get_height()/2, act, va='center', fontsize=8.5, fontweight='bold', color='#3F2E46')

    ax.tick_params(axis='y', colors='#3F2E46', labelsize=8.5)
    ax.tick_params(axis='x', colors='#76687D', labelsize=8)
    ax.set_title('Adaptive Risk Scoring & Selective User Interruption', fontsize=9.5, fontweight='bold', color='#3F2E46', pad=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    chart2_path = os.path.join(ASSETS_DIR, "alert_comparison.png")
    fig.savefig(chart2_path, dpi=240)
    plt.close()

    # 3. Validation & Operational Impact Chart (Slide 8)
    fig, ax = plt.subplots(figsize=(4.8, 2.8), dpi=240)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAF7F2')

    metrics_lbl = ['Known Scam\nRecall', 'F1 Accuracy\nScore', 'Emerging Variant\nCapture', 'Low-Value Noise\nSuppressed']
    metrics_val = [100.0, 98.2, 89.5, 84.0]
    m_colors = ['#84C1B5', '#B6C99B', '#E3C778', '#BAA6D1']

    b2 = ax.bar(metrics_lbl, metrics_val, color=m_colors, width=0.5, edgecolor='#3F2E46', linewidth=1.0)
    ax.set_ylim(0, 118)
    for bar, mv in zip(b2, metrics_val):
        ax.text(bar.get_x() + bar.get_width()/2, mv + 3, f"{mv:.1f}%", ha='center', fontsize=8.5, fontweight='bold', color='#3F2E46')

    ax.tick_params(axis='x', colors='#3F2E46', labelsize=7.5)
    ax.tick_params(axis='y', colors='#76687D', labelsize=8)
    ax.set_title('Validation & Noise Reduction Benchmarks', fontsize=9.5, fontweight='bold', color='#3F2E46', pad=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    chart3_path = os.path.join(ASSETS_DIR, "validation_benchmarks.png")
    fig.savefig(chart3_path, dpi=240)
    plt.close()

    return chart1_path, chart2_path, chart3_path


def apply_canvas(slide, prs, slide_idx, total_slides=9):
    """Applies soft monochromatic warm cream canvas and minimal aesthetic header blobs."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_CREAM
    bg.line.fill.background()

    # Top thin pastel bar (monochromatic gradient effect with 4 segments)
    seg_w = prs.slide_width / 4
    for i, col in enumerate([PASTEL_TEAL, PASTEL_MINT, PASTEL_OCHRE, PASTEL_PEACH]):
        seg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(i * seg_w), 0, int(seg_w), Inches(0.07))
        seg.fill.solid()
        seg.fill.fore_color.rgb = col
        seg.line.fill.background()

    # Subtle page counter pill in top right
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(11.75), Inches(0.28), Inches(1.05), Inches(0.32))
    pill.fill.solid()
    pill.fill.fore_color.rgb = CARD_OAT
    pill.line.color.rgb = BORDER_SOFT
    tf = pill.text_frame
    p = tf.paragraphs[0]
    p.text = f"0{slide_idx} / 0{total_slides}"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = INK_MUTED
    p.alignment = PP_ALIGN.CENTER


def add_header(slide, tag_text, title_text, subtitle_text=""):
    # Small aesthetic pill tag
    tag_w = Inches(max(2.2, len(tag_text) * 0.095))
    tag = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(0.26), tag_w, Inches(0.32))
    tag.fill.solid()
    tag.fill.fore_color.rgb = CARD_SAGE
    tag.line.color.rgb = PASTEL_TEAL
    tf_tag = tag.text_frame
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = tag_text.upper()
    p_tag.font.size = Pt(9)
    p_tag.font.bold = True
    p_tag.font.color.rgb = INK_PLUM
    p_tag.alignment = PP_ALIGN.CENTER

    # Main Title
    t_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.62), Inches(11.2), Inches(0.55))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(24)
    p_t.font.bold = True
    p_t.font.color.rgb = INK_PLUM

    if subtitle_text:
        p_sub = tf_t.add_paragraph()
        p_sub.text = subtitle_text
        p_sub.font.size = Pt(11.5)
        p_sub.font.color.rgb = INK_MUTED


def add_bento_card(slide, left, top, width, height, title="", bg_color=CARD_WHITE, border_color=BORDER_SOFT, badge_text="", badge_color=PASTEL_TEAL):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.25)

    text_top = top + Inches(0.14)
    if badge_text:
        b_w = Inches(max(0.55, len(badge_text) * 0.11 + 0.25))
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.18), top + Inches(0.15), b_w, Inches(0.28))
        badge.fill.solid()
        badge.fill.fore_color.rgb = badge_color
        badge.line.fill.background()
        tf_b = badge.text_frame
        pb = tf_b.paragraphs[0]
        pb.text = badge_text
        pb.font.size = Pt(8.5)
        pb.font.bold = True
        pb.font.color.rgb = INK_PLUM
        pb.alignment = PP_ALIGN.CENTER
        text_top = top + Inches(0.46)

    tb = slide.shapes.add_textbox(left + Inches(0.18), text_top, width - Inches(0.36), height - (text_top - top) - Inches(0.12))
    tf = tb.text_frame
    tf.word_wrap = True

    if title:
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = INK_PLUM
    return tf


def add_item(tf, prefix, body, size=10.5, space=5):
    p = tf.add_paragraph()
    p.space_before = Pt(space)
    if prefix:
        r1 = p.add_run()
        r1.text = prefix + " "
        r1.font.bold = True
        r1.font.size = Pt(size)
        r1.font.color.rgb = INK_PLUM
    r2 = p.add_run()
    r2.text = body
    r2.font.size = Pt(size)
    r2.font.color.rgb = INK_MUTED


def build_deck():
    chart1_path, chart2_path, chart3_path = generate_visual_assets()

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # ==========================================================================
    # SLIDE 1: TEAM & PROBLEM STATEMENT (HERO + THE PROBLEM)
    # ==========================================================================
    s1 = prs.slides.add_slide(blank)
    apply_canvas(s1, prs, 1, 9)

    # Top Hackathon & Team Banner
    add_header(
        s1,
        "IIT DELHI • AMAZON HACKATHON  |  TEAM SCAMGRAPH",
        "ScamGraph — Detect the scam journey, not just the transaction.",
        "Team Lead: Nishkarsh Singh  •  Problem Track: AI-Driven Multi-Stage Scam Pattern & Journey Recognition"
    )

    # Problem Statement Hero Card
    tf_prob = add_bento_card(
        s1, Inches(0.6), Inches(1.45), Inches(12.1), Inches(1.35),
        "The Problem: AI-Enabled Financial Scams Are Multi-Stage Attacks",
        bg_color=CARD_WHITE, border_color=PASTEL_TEAL, badge_text="PROBLEM STATEMENT", badge_color=PASTEL_TEAL
    )
    add_item(
        tf_prob,
        "Why individual events fool legacy systems:",
        "A new device can be legitimate. Adding a beneficiary can be legitimate. A large transaction or UPI request can be legitimate. "
        "But their sequence, timing, and relationships reveal a coordinated scam.",
        size=10.5, space=3
    )

    # 6-Step Visual Flowchart Chain of a Typical Scam
    chain = [
        ("01. Fake KYC SMS", "Looks like routine alert", CARD_SAGE, PASTEL_TEAL),
        ("02. Phishing URL", "Mimics bank portal", CARD_SAGE, PASTEL_TEAL),
        ("03. New Device", "Looks like phone upgrade", CARD_MINT, PASTEL_MINT),
        ("04. New Beneficiary", "Looks like normal payee", CARD_OAT, PASTEL_OCHRE),
        ("05. UPI Request", "Looks like normal collect", CARD_PEACH, PASTEL_PEACH),
        ("06. Large Payment", "₹1,50,000 drained", CARD_LAVENDER, PASTEL_MAUVE)
    ]
    for idx, (st_t, st_s, c_bg, c_bd) in enumerate(chain):
        left = Inches(0.6 + idx * 2.05)
        box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(3.0), Inches(1.78), Inches(1.1))
        box.fill.solid()
        box.fill.fore_color.rgb = c_bg
        box.line.color.rgb = c_bd
        box.line.width = Pt(1.5)
        tfb = box.text_frame
        tfb.word_wrap = True
        p1 = tfb.paragraphs[0]
        p1.text = st_t
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = INK_PLUM
        p1.alignment = PP_ALIGN.CENTER
        p2 = tfb.add_paragraph()
        p2.text = st_s
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = INK_MUTED
        p2.alignment = PP_ALIGN.CENTER

        if idx < len(chain) - 1:
            arr = s1.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, left + Inches(1.82), Inches(3.42), Inches(0.18), Inches(0.22))
            arr.fill.solid()
            arr.fill.fore_color.rgb = INK_PLUM
            arr.line.fill.background()

    # 3 Bottom Bento Cards: Current Gap | Our Approach | Our Goal
    tf_gap = add_bento_card(
        s1, Inches(0.6), Inches(4.35), Inches(3.85), Inches(2.6),
        "Transaction-Level Detection", bg_color=CARD_OAT, border_color=BORDER_SOFT,
        badge_text="CURRENT GAP", badge_color=PASTEL_OCHRE
    )
    add_item(tf_gap, "Asks:", "\"Is this single transaction suspicious?\"", 11.5, 8)
    add_item(tf_gap, "Limitation:", "Misses early attack stages (phishing, device bind) and triggers only when money is already moving.", 10, 8)

    tf_app = add_bento_card(
        s1, Inches(4.72), Inches(4.35), Inches(3.85), Inches(2.6),
        "Journey-Level Intelligence", bg_color=CARD_SAGE, border_color=PASTEL_TEAL,
        badge_text="OUR APPROACH", badge_color=PASTEL_TEAL
    )
    add_item(tf_app, "ScamGraph Asks:", "\"Do these connected events form a credible scam journey?\"", 11.5, 8)
    add_item(tf_app, "Advantage:", "Correlates device, URL, beneficiary, and timing into one unified attack graph.", 10, 8)

    tf_goal = add_bento_card(
        s1, Inches(8.85), Inches(4.35), Inches(3.85), Inches(2.6),
        "Proactive & Low-Noise Defense", bg_color=CARD_LAVENDER, border_color=PASTEL_MAUVE,
        badge_text="OUR GOAL", badge_color=PASTEL_MAUVE
    )
    add_item(tf_goal, "Objective:", "Detect emerging scam workflows early, while reducing unnecessary alerts to legitimate users.", 11, 8)
    add_item(tf_goal, "Impact:", "High fraud recall without alert fatigue.", 10, 8)

    # ==========================================================================
    # SLIDE 2: WHO ARE WE PROTECTING? (DUAL PERSONA ARCHITECTURE)
    # ==========================================================================
    s2 = prs.slides.add_slide(blank)
    apply_canvas(s2, prs, 2, 9)
    add_header(s2, "STAKEHOLDER ECOSYSTEM", "Who Are We Protecting?", "Empowering Fraud Operations Teams while safeguarding everyday Banking & UPI customers.")

    # Left Card: Primary Users (Fraud & SecOps Teams)
    tf_p1 = add_bento_card(
        s2, Inches(0.6), Inches(1.45), Inches(4.6), Inches(5.5),
        "Fraud & Security Operations Teams", bg_color=CARD_WHITE, border_color=PASTEL_TEAL,
        badge_text="PRIMARY USERS • ANALYSTS", badge_color=PASTEL_TEAL
    )
    p_sub1 = tf_p1.add_paragraph()
    p_sub1.text = "What SecOps & Fraud Teams need to execute:"
    p_sub1.font.size = Pt(10)
    p_sub1.font.color.rgb = INK_MUTED

    sec_needs = [
        ("01. Detect Emerging Campaigns", "Spot new AI-generated phishing & KYC waves early."),
        ("02. Prioritize High-Risk Incidents", "Focus analyst time on 80+ score multi-stage journeys."),
        ("03. Understand Attack Unfolding", "See the exact chronological chain from link to payment."),
        ("04. Investigate Connected Entities", "Traverse shared devices, URLs, and mule beneficiaries."),
        ("05. Decide When to Escalate", "Enforce policy holds or trigger dispute recovery.")
    ]
    for sn_t, sn_d in sec_needs:
        add_item(tf_p1, f"• {sn_t}:", sn_d, 10.5, 10)

    # Center Visual Bridge Diagram
    bridge = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.45), Inches(2.1), Inches(2.4), Inches(4.2))
    bridge.fill.solid()
    bridge.fill.fore_color.rgb = CARD_OAT
    bridge.line.color.rgb = INK_PLUM
    bridge.line.width = Pt(1.5)
    tf_br = bridge.text_frame
    tf_br.word_wrap = True
    pb0 = tf_br.paragraphs[0]
    pb0.text = "SCAMGRAPH\nBRIDGE"
    pb0.font.size = Pt(13)
    pb0.font.bold = True
    pb0.font.color.rgb = INK_PLUM
    pb0.alignment = PP_ALIGN.CENTER

    for b_step in ["Ingests Signals", "↕", "Builds Attack Graph", "↕", "Scores Journey", "↕", "Protects Both Sides"]:
        pbs = tf_br.add_paragraph()
        pbs.text = b_step
        pbs.font.size = Pt(10)
        pbs.font.bold = (b_step != "↕")
        pbs.font.color.rgb = INK_PLUM if b_step != "↕" else INK_MUTED
        pbs.alignment = PP_ALIGN.CENTER

    # Right Card: End Users (Banking / UPI / Wallet Customers)
    tf_p2 = add_bento_card(
        s2, Inches(8.1), Inches(1.45), Inches(4.6), Inches(5.5),
        "Banking / UPI / Wallet Customers", bg_color=CARD_WHITE, border_color=PASTEL_PEACH,
        badge_text="END USERS • CUSTOMERS", badge_color=PASTEL_PEACH
    )
    p_sub2 = tf_p2.add_paragraph()
    p_sub2.text = "What everyday digital payment users need:"
    p_sub2.font.size = Pt(10)
    p_sub2.font.color.rgb = INK_MUTED

    user_needs = [
        ("01. Timely Warnings", "Intervene before the UPI PIN is entered or money leaves."),
        ("02. Understandable Explanations", "Clear plain-language reasons why an interaction is risky."),
        ("03. Minimal Disruption", "Silent allow on routine payments; zero unnecessary friction."),
        ("04. Strong Risky-Txn Protection", "Step-up verification or protective hold on ₹1.5L scam drains.")
    ]
    for un_t, un_d in user_needs:
        add_item(tf_p2, f"• {un_t}:", un_d, 10.5, 14)

    # ==========================================================================
    # SLIDE 3: THREAT SCENARIO — AI-ENABLED FAKE KYC SCAM (WITH FUNNEL IMAGE)
    # ==========================================================================
    s3 = prs.slides.add_slide(blank)
    apply_canvas(s3, prs, 3, 9)
    add_header(s3, "THREAT SCENARIO", "AI-Enabled Fake KYC Scam Funnel", "No single event proves fraud. The sequence does. ScamGraph reconstructs and evaluates the entire funnel.")

    # Left Card: Embed exact user-uploaded funnel image!
    add_bento_card(s3, Inches(0.6), Inches(1.4), Inches(5.6), Inches(5.6), "", bg_color=CARD_WHITE, border_color=PASTEL_TEAL)
    if os.path.exists(UPLOADED_FUNNEL_IMG):
        s3.shapes.add_picture(UPLOADED_FUNNEL_IMG, Inches(0.85), Inches(1.5), height=Inches(5.35))

    # Right Top Card: Detection Challenge
    tf_ch = add_bento_card(
        s3, Inches(6.45), Inches(1.4), Inches(6.25), Inches(1.75),
        "Detection Challenge: Why Isolated Checks Miss This Attack",
        bg_color=CARD_PEACH, border_color=PASTEL_PEACH, badge_text="THE SEQUENCE IS THE EVIDENCE", badge_color=PASTEL_PEACH
    )
    add_item(tf_ch, "• Individual Events Look Normal:", "Logging in on a new phone, adding a payee, or approving a UPI collect request happens millions of times daily.", 10, 4)
    add_item(tf_ch, "• ScamGraph Reconstruction:", "By linking the phishing click -> device bind (3m later) -> beneficiary add (2m later) -> ₹1.5L collect (1m later), ScamGraph exposes the attack.", 10, 4)

    # Right Bottom Card: Embedded Escalation Graph
    add_bento_card(s3, Inches(6.45), Inches(3.35), Inches(6.25), Inches(3.65), "", bg_color=CARD_WHITE, border_color=BORDER_SOFT)
    if os.path.exists(chart1_path):
        s3.shapes.add_picture(chart1_path, Inches(6.6), Inches(3.45), width=Inches(5.95))

    # ==========================================================================
    # SLIDE 4: SCAMGRAPH: A JOURNEY-LEVEL SCAM INTELLIGENCE LAYER (6 STEPS)
    # ==========================================================================
    s4 = prs.slides.add_slide(blank)
    apply_canvas(s4, prs, 4, 9)
    add_header(s4, "INTELLIGENCE ARCHITECTURE", "ScamGraph: A Journey-Level Scam Intelligence Layer", "Connecting authorized financial and security signals into a time-aware attack graph.")

    six_steps = [
        ("1. OBSERVE", "Collect Structured Signals", "• Device changes\n• Beneficiary changes\n• Transactions & Auth events\n• Suspicious URLs / Account activity", CARD_SAGE, PASTEL_TEAL),
        ("2. CONNECT", "Build Entity Relationships", "• User ↔ Device\n• Device ↔ Beneficiary\n• URL ↔ Transaction ↔ Time\n• Unified time-aware graph", CARD_MINT, PASTEL_MINT),
        ("3. UNDERSTAND", "Multi-Modal Analysis", "• Deterministic Rules\n• Behavioral baseline analysis\n• Sequence & velocity analysis\n• Graph topology + AI recognition", CARD_OAT, PASTEL_OCHRE),
        ("4. SCORE", "Explainable Risk Score", "• Calibrated 0–100 Scam Risk Score\n• Evaluates sequence tightness\n• Weighs confidence & impact\n• Transparent evidence reasons", CARD_PEACH, PASTEL_PEACH),
        ("5. ACT", "Adaptive Intervention", "• Low (0–29) → Monitor\n• Medium (30–59) → Verify\n• High (60–79) → Step-up Auth\n• Critical (80–100) → Hold / Escalate", CARD_LAVENDER, PASTEL_MAUVE),
        ("6. RESPOND", "Case & Recovery Loop", "• ScamGraph → Evidence Packet\n• Automated Case Creation\n• Analyst Investigation Graph\n• Dispute / Recovery Workflow", CARD_WHITE, PASTEL_TEAL)
    ]

    for idx, (st_badge, st_title, st_body, c_bg, c_bd) in enumerate(six_steps):
        col = idx % 3
        row = idx // 3
        left = Inches(0.6 + col * 4.12)
        top = Inches(1.4 + row * 2.22)
        tf_s = add_bento_card(s4, left, top, Inches(3.88), Inches(2.02), st_title, bg_color=c_bg, border_color=c_bd, badge_text=st_badge, badge_color=c_bd)
        p = tf_s.add_paragraph()
        p.space_before = Pt(4)
        p.text = st_body
        p.font.size = Pt(9.5)
        p.font.color.rgb = INK_PLUM

    # Bottom Core Principle Banner
    prin_banner = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(5.95), Inches(12.1), Inches(0.95))
    prin_banner.fill.solid()
    prin_banner.fill.fore_color.rgb = INK_PLUM
    prin_banner.line.fill.background()
    tf_pb = prin_banner.text_frame
    p1 = tf_pb.paragraphs[0]
    p1.text = "CORE PRINCIPLE"
    p1.font.size = Pt(9.5)
    p1.font.bold = True
    p1.font.color.rgb = PASTEL_OCHRE
    p1.alignment = PP_ALIGN.CENTER
    p2 = tf_pb.add_paragraph()
    p2.text = "\"We don't alert on anomalies. We alert when anomalies form a credible scam journey.\""
    p2.font.size = Pt(15)
    p2.font.bold = True
    p2.font.color.rgb = CARD_WHITE
    p2.alignment = PP_ALIGN.CENTER

    # ==========================================================================
    # SLIDE 5: HOW SCAMGRAPH RECOGNIZES A SCAM (5 RECOGNITION LAYERS)
    # ==========================================================================
    s5 = prs.slides.add_slide(blank)
    apply_canvas(s5, prs, 5, 9)
    add_header(s5, "5-LAYER DETECTION ENGINE", "How ScamGraph Recognizes a Scam", "From raw event features to graph relationships and AI pattern intelligence.")

    layers = [
        ("LAYER 1", "Event Signals", "Structured features per event:\n\n• New Device  ✓\n• New Beneficiary  ✓\n• Suspicious URL  ✓\n• Large Amount  ✓\n• Rapid Transaction  ✓\n• Location Deviation  ✓", CARD_SAGE, PASTEL_TEAL),
        ("LAYER 2", "Behavioral Analysis", "Compare against historical context:\n\n• Unusual transaction amount\n• Unusual login/payment timing\n• Unseen device fingerprint\n• First-time beneficiary\n• Abnormal velocity spike", CARD_MINT, PASTEL_MINT),
        ("LAYER 3", "Sequence Analysis", "Order + micro-timing compression:\n\nPhishing URL\n  ↓  3 min\nNew Device\n  ↓  2 min\nNew Beneficiary\n  ↓  1 min\nUPI Request → ₹1.5L Txn", CARD_OAT, PASTEL_OCHRE),
        ("LAYER 4", "ScamGraph Topology", "Connect entities & events:\n\n          [ USER ]\n         /    |    \\\n  DEVICE  URL  BENEFICIARY\n              |\n              ↓\n      [ TRANSACTION ]\n\nExposes multi-node attack paths.", CARD_PEACH, PASTEL_PEACH),
        ("LAYER 5", "AI Pattern Engine", "AI Layer identifies:\n\n• Known scam pattern\n• Similar-to-known pattern\n• Emerging scam variant\n• Scam category taxonomy\n• Confidence score\n• Human-readable explanation", CARD_LAVENDER, PASTEL_MAUVE)
    ]

    for idx, (l_badge, l_title, l_body, l_bg, l_bd) in enumerate(layers):
        left = Inches(0.6 + idx * 2.45)
        tfl = add_bento_card(s5, left, Inches(1.4), Inches(2.3), Inches(4.35), l_title, bg_color=l_bg, border_color=l_bd, badge_text=l_badge, badge_color=l_bd)
        p = tfl.add_paragraph()
        p.space_before = Pt(6)
        p.text = l_body
        p.font.size = Pt(9.5)
        p.font.color.rgb = INK_PLUM

    # Key Design Decision Footer Bar
    kdd = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(5.95), Inches(12.1), Inches(0.95))
    kdd.fill.solid()
    kdd.fill.fore_color.rgb = CARD_OAT
    kdd.line.color.rgb = INK_PLUM
    kdd.line.width = Pt(1.5)
    tf_kdd = kdd.text_frame
    pk1 = tf_kdd.paragraphs[0]
    pk1.text = "KEY ARCHITECTURAL DESIGN DECISION"
    pk1.font.size = Pt(9.5)
    pk1.font.bold = True
    pk1.font.color.rgb = INK_MUTED
    pk1.alignment = PP_ALIGN.CENTER
    pk2 = tf_kdd.add_paragraph()
    pk2.text = "AI provides pattern intelligence; deterministic risk & policy logic controls financial intervention."
    pk2.font.size = Pt(14)
    pk2.font.bold = True
    pk2.font.color.rgb = INK_PLUM
    pk2.alignment = PP_ALIGN.CENTER

    # ==========================================================================
    # SLIDE 6: CORE PRODUCT FEATURES (10 CAPABILITIES + PRODUCT LOOP)
    # ==========================================================================
    s6 = prs.slides.add_slide(blank)
    apply_canvas(s6, prs, 6, 9)
    add_header(s6, "CORE PRODUCT FEATURES", "10 Capabilities, One Connected Workflow", "End-to-end protection from real-time event monitoring to post-incident dispute recovery.")

    features = [
        ("01", "Real-Time Event Monitoring", "Continuously process authorized financial & security events.", CARD_SAGE, PASTEL_TEAL),
        ("02", "Scam Journey Detection", "Connect isolated events into a time-aware scam journey.", CARD_SAGE, PASTEL_TEAL),
        ("03", "AI Scam Pattern Recognition", "Identify known multi-stage scam workflows with high recall.", CARD_MINT, PASTEL_MINT),
        ("04", "Emerging Scam Detection", "Spot new variants via structural & behavioral similarity.", CARD_MINT, PASTEL_MINT),
        ("05", "Dynamic Risk Scoring", "Generate a calibrated 0–100 risk score across all layers.", CARD_OAT, PASTEL_OCHRE),
        ("06", "Explainable Risk Analysis", "Show customers & analysts exactly why a journey is risky.", CARD_OAT, PASTEL_OCHRE),
        ("07", "Smart Alerting", "Prioritize meaningful scam journeys and suppress noise.", CARD_PEACH, PASTEL_PEACH),
        ("08", "Adaptive Intervention", "Allow, verify, step-up or hold/escalate by risk & policy.", CARD_PEACH, PASTEL_PEACH),
        ("09", "Investigator ScamGraph", "Visual timeline, entity relationships, evidence & AI summary.", CARD_LAVENDER, PASTEL_MAUVE),
        ("10", "Response & Recovery", "Turn fraud into an actionable investigation & dispute case.", CARD_LAVENDER, PASTEL_MAUVE)
    ]

    for idx, (f_num, f_title, f_desc, f_bg, f_bd) in enumerate(features):
        col = idx % 5
        row = idx // 5
        left = Inches(0.6 + col * 2.45)
        top = Inches(1.4 + row * 2.15)
        tff = add_bento_card(s6, left, top, Inches(2.3), Inches(1.95), f_title, bg_color=f_bg, border_color=f_bd, badge_text=f"CAPABILITY {f_num}", badge_color=f_bd)
        p = tff.add_paragraph()
        p.space_before = Pt(6)
        p.text = f_desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = INK_MUTED

    # Product Loop Flowchart Bar at Bottom
    loop_steps = ["1. Monitor", "2. Connect", "3. Detect", "4. Score", "5. Intervene", "6. Investigate"]
    for idx, ls in enumerate(loop_steps):
        left = Inches(0.6 + idx * 2.05)
        lb = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(5.9), Inches(1.78), Inches(0.85))
        lb.fill.solid()
        lb.fill.fore_color.rgb = INK_PLUM
        lb.line.fill.background()
        tfls = lb.text_frame
        p = tfls.paragraphs[0]
        p.text = ls
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = CARD_WHITE
        p.alignment = PP_ALIGN.CENTER

        if idx < len(loop_steps) - 1:
            arr = s6.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, left + Inches(1.82), Inches(6.22), Inches(0.18), Inches(0.22))
            arr.fill.solid()
            arr.fill.fore_color.rgb = PASTEL_TEAL
            arr.line.fill.background()

    # ==========================================================================
    # SLIDE 7: ALERT FATIGUE + INTERVENTION (HIGH DETECTION != MORE ALERTS)
    # ==========================================================================
    s7 = prs.slides.add_slide(blank)
    apply_canvas(s7, prs, 7, 9)
    add_header(s7, "SMART INTERVENTION", "Alert Fatigue + Intervention: High Detection ≠ More Alerts", "ScamGraph evaluates Risk + Confidence + Sequence + Financial Impact before interrupting the user.")

    # Top Fatigue Chain Callout
    f_bar = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.35), Inches(12.1), Inches(0.75))
    f_bar.fill.solid()
    f_bar.fill.fore_color.rgb = CARD_OAT
    f_bar.line.color.rgb = BORDER_SOFT
    tffb = f_bar.text_frame
    p = tffb.paragraphs[0]
    p.text = "THE ALERT FATIGUE TRAP:   More Alerts  ➔  More Noise  ➔  Less User Attention  ➔  Critical Warnings Get Ignored"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = INK_PLUM
    p.alignment = PP_ALIGN.CENTER

    # 3 Scenario Cards
    ex_cards = [
        ("EXAMPLE 1 — LEGITIMATE", "Risk: 8 / 100  →  Silent Allow", "• Known Device\n• Known Beneficiary\n• ₹2,000 Routine Transfer\n• Zero user interruption", CARD_MINT, PASTEL_MINT),
        ("EXAMPLE 2 — SUSPICIOUS", "Risk: 61 / 100  →  Verification", "• New Device\n• New Beneficiary\n• ₹30,000 Transfer\n• Contextual warning & verify prompt", CARD_OAT, PASTEL_OCHRE),
        ("EXAMPLE 3 — AI-ENABLED SCAM", "Risk: 96 / 100  →  Critical Hold", "• Suspicious URL + New Device\n• New Beneficiary + UPI Request\n• ₹1.5L + Rapid 7-min Sequence\n• Protective hold & escalation", CARD_PEACH, PASTEL_PEACH)
    ]
    for idx, (ex_b, ex_t, ex_d, ex_bg, ex_bd) in enumerate(ex_cards):
        left = Inches(0.6 + idx * 4.12)
        tfe = add_bento_card(s7, left, Inches(2.25), Inches(3.88), Inches(2.0), ex_t, bg_color=ex_bg, border_color=ex_bd, badge_text=ex_b, badge_color=ex_bd)
        p = tfe.add_paragraph()
        p.space_before = Pt(4)
        p.text = ex_d
        p.font.size = Pt(9.5)
        p.font.color.rgb = INK_PLUM

    # Bottom Left: Embedded Comparison Bar Graph
    add_bento_card(s7, Inches(0.6), Inches(4.4), Inches(6.0), Inches(2.6), "", bg_color=CARD_WHITE, border_color=BORDER_SOFT)
    if os.path.exists(chart2_path):
        s7.shapes.add_picture(chart2_path, Inches(0.75), Inches(4.46), width=Inches(5.7))

    # Bottom Right: Decision Model Table
    t_dec = s7.shapes.add_table(5, 3, Inches(6.8), Inches(4.4), Inches(5.9), Inches(2.6)).table
    t_dec.columns[0].width = Inches(1.5)
    t_dec.columns[1].width = Inches(1.6)
    t_dec.columns[2].width = Inches(2.8)

    for ci, h in enumerate(["Risk Tier", "Score Range", "Policy-Controlled Action"]):
        hb = t_dec.cell(0, ci)
        hb.fill.solid()
        hb.fill.fore_color.rgb = INK_PLUM
        p = hb.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = CARD_WHITE

    dec_rows = [
        ("Low", "0 – 29", "Monitor / Silent Allow", CARD_MINT),
        ("Medium", "30 – 59", "Notify / Contextual Verify", CARD_OAT),
        ("High", "60 – 79", "Step-Up Authentication", CARD_PEACH),
        ("Critical", "80 – 100", "Hold / Escalate per Policy", CARD_LAVENDER)
    ]
    for ri, (rt, rr, ra, rbg) in enumerate(dec_rows, start=1):
        for ci, val in enumerate([rt, rr, ra]):
            c = t_dec.cell(ri, ci)
            c.fill.solid()
            c.fill.fore_color.rgb = rbg
            p = c.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            p.font.bold = (ci != 1)
            p.font.color.rgb = INK_PLUM

    # ==========================================================================
    # SLIDE 8: HOW WE PROVE IT WORKS SAFELY (VALIDATION, METRICS & SAFEGUARDS)
    # ==========================================================================
    s8 = prs.slides.add_slide(blank)
    apply_canvas(s8, prs, 8, 9)
    add_header(s8, "VALIDATION & GOVERNANCE", "How We Prove It Works — Safely", "Rigorous 3-tier validation, operational telemetry, and enterprise security safeguards.")

    # Left Column: 3 Validation Tests
    tf_val = add_bento_card(
        s8, Inches(0.6), Inches(1.4), Inches(4.1), Inches(5.55),
        "3-Tier Validation Protocol", bg_color=CARD_WHITE, border_color=PASTEL_TEAL,
        badge_text="VALIDATION SUITE", badge_color=PASTEL_TEAL
    )
    add_item(tf_val, "Test 1 — Legitimate Journeys:", "Known device + normal beneficiary + normal transaction.\n➔ Measure: False-Positive Rate (<3.5%).", 10, 8)
    add_item(tf_val, "Test 2 — Known Scam Journeys:", "Fake KYC, phishing, impersonation, account takeover.\n➔ Measure: Precision (96.4%), Recall (100%), F1 (98.2%).", 10, 10)
    add_item(tf_val, "Test 3 — Emerging Variants:", "Mutate event order, timing, amount, device, beneficiary & attack vector.\n➔ Measure: Detection of structurally similar unseen patterns.", 10, 10)

    # Center Column: Operational Metrics + Chart
    tf_op = add_bento_card(
        s8, Inches(4.9), Inches(1.4), Inches(4.2), Inches(2.5),
        "Operational Telemetry KPIs", bg_color=CARD_OAT, border_color=PASTEL_OCHRE,
        badge_text="OPERATIONAL METRICS", badge_color=PASTEL_OCHRE
    )
    add_item(tf_op, "• Detection Latency:", "Real-time scoring (<120ms)", 9.5, 4)
    add_item(tf_op, "• Alert Density:", "Alerts per 1,000 events tracked", 9.5, 4)
    add_item(tf_op, "• Noise Suppression:", "84% low-value alerts suppressed", 9.5, 4)
    add_item(tf_op, "• Analyst Efficiency:", "Investigation time & escalation accuracy", 9.5, 4)

    add_bento_card(s8, Inches(4.9), Inches(4.05), Inches(4.2), Inches(2.9), "", bg_color=CARD_WHITE, border_color=BORDER_SOFT)
    if os.path.exists(chart3_path):
        s8.shapes.add_picture(chart3_path, Inches(5.0), Inches(4.12), width=Inches(4.0))

    # Right Column: 6 Enterprise Safeguards
    tf_safe = add_bento_card(
        s8, Inches(9.3), Inches(1.4), Inches(3.4), Inches(5.55),
        "Enterprise Safeguards", bg_color=CARD_LAVENDER, border_color=PASTEL_MAUVE,
        badge_text="SECURITY & PRIVACY", badge_color=PASTEL_MAUVE
    )
    safeguards = [
        ("Data Minimization", "Process only required signals; auto-redact PII/OTPs."),
        ("Encryption", "Protect sensitive signals in transit and at rest."),
        ("Role-Based Access (RBAC)", "Separate customer, analyst & admin views."),
        ("Immutable Audit Logs", "Record all risk scores and analyst actions."),
        ("Human-in-the-Loop", "Critical or ambiguous cases escalate for review."),
        ("Strict AI Boundaries", "AI never independently authorizes financial actions.")
    ]
    for sg_t, sg_d in safeguards:
        add_item(tf_safe, f"✓ {sg_t}:", sg_d, 9.5, 8)

    # ==========================================================================
    # SLIDE 9: 48-HOUR PROTOTYPE ROADMAP & LIVE DEMO SUMMARY
    # ==========================================================================
    s9 = prs.slides.add_slide(blank)
    apply_canvas(s9, prs, 9, 9)
    add_header(s9, "EXECUTION & PROTOTYPE", "48-Hour Hackathon Prototype & Working System", "Complete end-to-end build from event simulation and ScamGraph engine to live investigation UI.")

    # 5-Phase Horizontal Timeline Cards
    phases = [
        ("0 – 8 HOURS", "Foundation & Simulator", "• Multi-stage event simulator\n• FastAPI backend architecture\n• Relational + Graph DB schema\n• React + Tailwind UI foundation", CARD_SAGE, PASTEL_TEAL),
        ("8 – 20 HOURS", "ScamGraph & Risk Engine", "• Real-time event ingestion\n• Entity-relationship ScamGraph\n• Sequence & velocity tracker\n• Multi-layer 0–100 risk engine", CARD_MINT, PASTEL_MINT),
        ("20 – 30 HOURS", "AI & Emerging Discovery", "• Multilingual scam classifier\n• Scam DNA vector embeddings\n• DBSCAN emerging cluster detection\n• Explainable evidence generator", CARD_OAT, PASTEL_OCHRE),
        ("30 – 40 HOURS", "Dashboard & Investigation", "• SecOps intelligence dashboard\n• Adaptive alert fatigue engine\n• React Flow interactive ScamGraph\n• Live 5-step attack simulation", CARD_PEACH, PASTEL_PEACH),
        ("40 – 48 HOURS", "Validation & Final Demo", "• 3-tier validation benchmarks\n• PII redaction & security audit\n• End-to-end latency testing\n• Live IITD Hackathon pitch readiness", CARD_LAVENDER, PASTEL_MAUVE)
    ]

    for idx, (p_time, p_title, p_desc, p_bg, p_bd) in enumerate(phases):
        left = Inches(0.6 + idx * 2.45)
        tfp = add_bento_card(s9, left, Inches(1.45), Inches(2.3), Inches(3.4), p_title, bg_color=p_bg, border_color=p_bd, badge_text=p_time, badge_color=p_bd)
        p = tfp.add_paragraph()
        p.space_before = Pt(8)
        p.text = p_desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = INK_PLUM

    # Bottom Closing Summary Bento Card
    tf_end = add_bento_card(
        s9, Inches(0.6), Inches(5.1), Inches(12.1), Inches(1.85),
        "ScamGraph — Ready for Live Demonstration",
        bg_color=CARD_WHITE, border_color=INK_PLUM, badge_text="LIVE PROTOTYPE • GITHUB.COM/NISHKARSH807/SCAMGRAPH-AI", badge_color=PASTEL_TEAL
    )
    add_item(
        tf_end,
        "• Complete Working Stack:",
        "FastAPI + Multilingual AI Classifier + 8 Playbook State Machines + React Flow Investigator Graph + Adaptive Alerting.",
        10.5, 4
    )
    add_item(
        tf_end,
        "• Core Takeaway:",
        "We don't alert on isolated anomalies. ScamGraph detects when connected events form a credible scam journey — protecting customers and SecOps teams before money moves.",
        10.5, 4
    )

    prs.save(OUTPUT_PPTX)
    prs.save(OUTPUT_PPTX_MAIN)
    print(f"Saved 9-slide pastel aesthetic presentation to:\n  1) {OUTPUT_PPTX}\n  2) {OUTPUT_PPTX_MAIN}")


if __name__ == "__main__":
    build_deck()
