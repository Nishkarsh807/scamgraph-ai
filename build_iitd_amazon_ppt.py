"""
ScamGraph AI - IIT Delhi Amazon Hackathon Pitch Deck Generator (10 Slides)
Theme Inspiration:
  1. GoodPello 'Data Security' Monochromatic Charcoal + Warm Taupe/Sandstone + Pastel Sage/Mauve
     (Alternating dark charcoal cards #232126, warm taupe #C8B69E, soft alabaster #F4EFE8,
      radar charts, donut gauges, column charts, shield icons, horizontal timelines)
  2. Gen Z Editorial Geometric Template
     (Minimalist geometric symbols ○ △ □, numbered horizontal pill bars 01/02/03/04,
      rounded image frames, pill tags, high-density structured bento grids)
"""

import os
import shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from PIL import Image, ImageDraw, ImageOps

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "docs", "ppt_assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Uploaded user media paths
BRAIN_UPLOAD_DIR = r"C:\Users\DELL\.gemini\antigravity\brain\ee7f6e0f-dbce-444a-9ef5-385d69dcea7a\.user_uploaded"
IMG_MASKS_RAW = os.path.join(BRAIN_UPLOAD_DIR, "media_1791660854055.jpg")      # Multi-mask impersonation art
IMG_CRT_RAW   = os.path.join(BRAIN_UPLOAD_DIR, "media_1791660878504.jpg")      # CRT alert overload art
IMG_CYBER_RAW = os.path.join(BRAIN_UPLOAD_DIR, "media_1791661273473.png")      # Cyber Security HUD network
IMG_FUNNEL_RAW = os.path.join(ASSETS_DIR, "ppt", "media", "image1.png")        # 3D KYC Scam Funnel

OUTPUT_PPTX = os.path.join(BASE_DIR, "ScamGraph_IITD_Amazon_Hackathon.pptx")
OUTPUT_PPTX_MAIN = os.path.join(BASE_DIR, "ScamGraph_AI_Hackathon_Pitch.pptx")

# ==============================================================================
# MONOCHROMATIC CHARCOAL + WARM TAUPE + SUBTLE PASTEL GEN Z PALETTE
# (Directly inspired by uploaded Data Security & Geometric Editorial templates)
# ==============================================================================
BG_ALABASTER   = RGBColor(244, 239, 232)   # #F4EFE8 Warm Monochromatic Oat/Alabaster Canvas
BG_CHARCOAL    = RGBColor(32, 30, 35)      # #201E23 Sleek Matte Charcoal (for Dark Hero/Accent cards)
CARD_CHARCOAL  = RGBColor(42, 39, 46)      # #2A272E Secondary Dark Slate Card
CARD_CREAM     = RGBColor(252, 249, 245)   # #FCF9F5 Crisp Warm Ivory Card
CARD_STONE     = RGBColor(232, 224, 213)   # #E8E0D5 Monochromatic Warm Stone/Sand
CARD_TAUPE     = RGBColor(200, 182, 158)   # #C8B69E Warm Sandstone Taupe (GoodPello signature accent)

# Subtle Pastel Accents
PASTEL_SAGE    = RGBColor(136, 184, 172)   # #88B8AC Muted Pastel Sage Teal
CARD_SAGE_SOFT = RGBColor(223, 236, 232)   # #DFECE8 Soft Sage Tint
PASTEL_MINT    = RGBColor(180, 199, 156)   # #B4C79C Muted Matcha Mint
CARD_MINT_SOFT = RGBColor(232, 239, 223)   # #E8EFDF Soft Mint Tint
PASTEL_MAUVE   = RGBColor(198, 164, 180)   # #C6A4B4 Dusty Rose / Mauve Pastel
CARD_MAUVE_SOFT= RGBColor(239, 228, 234)   # #EFE4EA Soft Mauve Tint
PASTEL_OCHRE   = RGBColor(222, 193, 130)   # #DEC182 Muted Warm Ochre
CARD_OCHRE_SOFT= RGBColor(246, 236, 214)   # #F6ECD6 Soft Ochre Tint
PASTEL_CORAL   = RGBColor(219, 148, 135)   # #DB9487 Muted Terracotta/Coral Pastel

# Typography & Borders
INK_DARK       = RGBColor(34, 31, 38)      # #221F26 Deep Charcoal Ink
INK_MUTED      = RGBColor(108, 101, 112)   # #6C6570 Muted Warm Slate
INK_LIGHT      = RGBColor(246, 242, 236)   # #F6F2EC Crisp Cream Text (on dark cards)
INK_TAUPE_LT   = RGBColor(214, 201, 184)   # #D6C9B8 Soft Sand Text (on dark cards)
BORDER_TAUPE   = RGBColor(208, 198, 186)   # #D0C6BA Subtle Monochromatic Hairline
BORDER_DARK    = RGBColor(68, 63, 74)      # #443F4A Subtle Dark Card Border


def prepare_rounded_image(src_path, out_name, target_size=(800, 560), radius=36, border_color=(200, 182, 158), border_width=6):
    """Crops/resizes an uploaded image and applies aesthetic rounded corners + subtle taupe frame."""
    out_path = os.path.join(ASSETS_DIR, out_name)
    if not os.path.exists(src_path):
        return None
    img = Image.open(src_path).convert("RGBA")
    img = ImageOps.fit(img, target_size, method=Image.Resampling.LANCZOS)

    # Create rounded mask
    mask = Image.new("L", target_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, target_size[0], target_size[1]), radius=radius, fill=255)

    # Apply border
    framed = Image.new("RGBA", target_size, (0, 0, 0, 0))
    framed.paste(img, (0, 0), mask=mask)

    if border_width > 0:
        b_draw = ImageDraw.Draw(framed)
        b_draw.rounded_rectangle(
            (border_width // 2, border_width // 2, target_size[0] - border_width // 2 - 1, target_size[1] - border_width // 2 - 1),
            radius=radius,
            outline=border_color + (255,),
            width=border_width
        )
    framed.save(out_path, "PNG")
    return out_path


def generate_visual_assets():
    """Generates high-DPI monochromatic + pastel charts and processes uploaded user images."""
    plt.rcParams['font.sans-serif'] = 'Segoe UI'
    plt.rcParams['axes.edgecolor'] = '#D0C6BA'
    plt.rcParams['axes.linewidth'] = 1.0

    assets = {}

    # Process User Uploaded Images with sleek rounded corners
    assets['img_masks'] = prepare_rounded_image(IMG_MASKS_RAW, "framed_masks.png", target_size=(680, 520), radius=32, border_color=(200, 182, 158), border_width=6)
    assets['img_crt'] = prepare_rounded_image(IMG_CRT_RAW, "framed_crt.png", target_size=(680, 460), radius=32, border_color=(136, 184, 172), border_width=6)
    assets['img_cyber'] = prepare_rounded_image(IMG_CYBER_RAW, "framed_cyber.png", target_size=(820, 480), radius=30, border_color=(200, 182, 158), border_width=6)
    assets['img_funnel'] = IMG_FUNNEL_RAW if os.path.exists(IMG_FUNNEL_RAW) else None

    # 1. Sequence Risk Escalation Chart (Slide 3)
    fig, ax = plt.subplots(figsize=(5.6, 2.75), dpi=240)
    fig.patch.set_facecolor('#FCF9F5')
    ax.set_facecolor('#F4EFE8')

    stages = ['1. KYC\nSMS', '2. Phish\nURL', '3. New\nDevice', '4. New\nPayee', '5. UPI\nCollect', '6. ₹1.5L\nTransfer']
    journey_risk = [18, 42, 61, 78, 91, 96]
    isolated_risk = [18, 34, 22, 25, 30, 44]

    x = np.arange(len(stages))
    ax.fill_between(x, journey_risk, color='#88B8AC', alpha=0.32)
    ax.plot(x, journey_risk, marker='o', color='#221F26', linewidth=2.6, markersize=6.5, label='ScamGraph Journey Risk')
    ax.plot(x, isolated_risk, marker='s', linestyle='--', color='#C6A4B4', linewidth=2.0, markersize=5, label='Legacy Isolated Score')
    ax.axhline(75, color='#DB9487', linestyle=':', linewidth=1.5, label='Intervention Threshold (75)')

    for i, v in enumerate(journey_risk):
        ax.annotate(f"{v}", (x[i], v + 4.5), ha='center', fontsize=8, fontweight='bold', color='#221F26')

    ax.set_ylim(0, 114)
    ax.set_xticks(x)
    ax.set_xticklabels(stages, fontsize=7.8, color='#221F26', fontweight='bold')
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.tick_params(axis='y', colors='#6C6570', labelsize=7.5)
    ax.set_title('Cumulative Workflow Risk vs. Isolated Event Scoring', fontsize=9.5, fontweight='bold', color='#221F26', pad=8)
    ax.legend(loc='upper left', frameon=True, facecolor='#FCF9F5', edgecolor='#D0C6BA', fontsize=7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    assets['chart_escalation'] = os.path.join(ASSETS_DIR, "journey_escalation.png")
    fig.savefig(assets['chart_escalation'], dpi=240)
    plt.close()

    # 2. Radar Chart + Heterogeneous Graph Topology (Slide 5 - Inspired by GoodPello Data Security Template)
    fig = plt.figure(figsize=(5.5, 2.95), dpi=240)
    fig.patch.set_facecolor('#2A272E')
    ax = fig.add_subplot(111, polar=True)
    ax.set_facecolor('#201E23')

    categories = ['Hinglish\nNLP', 'Workflow\nMemory', 'Mule Ring\nGraph', 'Zero-Day\nAdapt', 'XAI\nClarity', 'Low Alert\nFatigue']
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    scamgraph_vals = [96, 98, 94, 90, 95, 92]
    scamgraph_vals += scamgraph_vals[:1]
    legacy_vals = [52, 25, 30, 38, 42, 35]
    legacy_vals += legacy_vals[:1]

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    plt.xticks(angles[:-1], categories, color='#F6F2EC', size=7.2, fontweight='bold')
    ax.tick_params(axis='x', pad=7)
    ax.set_rlabel_position(30)
    plt.yticks([25, 50, 75, 100], ["25", "50", "75", "100"], color="#D6C9B8", size=6.0)
    plt.ylim(0, 105)

    ax.plot(angles, scamgraph_vals, linewidth=2.2, linestyle='solid', color='#88B8AC', label='ScamGraph AI')
    ax.fill(angles, scamgraph_vals, '#88B8AC', alpha=0.35)
    ax.plot(angles, legacy_vals, linewidth=1.8, linestyle='--', color='#C8B69E', label='Rule / SMS Classifiers')
    ax.fill(angles, legacy_vals, '#C8B69E', alpha=0.18)

    ax.grid(color='#443F4A', linestyle='-', linewidth=0.8)
    ax.spines['polar'].set_color('#443F4A')
    fig.suptitle('Capability Radar: ScamGraph vs. Legacy Defenses', fontsize=8.8, color='#F6F2EC', fontweight='bold', y=0.97)
    plt.legend(loc='lower right', bbox_to_anchor=(1.36, -0.08), facecolor='#201E23', edgecolor='#443F4A', labelcolor='#F6F2EC', fontsize=6.8)
    plt.subplots_adjust(top=0.76, bottom=0.14, left=0.08, right=0.72)
    assets['chart_radar'] = os.path.join(ASSETS_DIR, "radar_capabilities.png")
    fig.savefig(assets['chart_radar'], dpi=240)
    plt.close()

    # 3. Heterogeneous Entity Graph Diagram (Slide 5 visual #2)
    fig, ax = plt.subplots(figsize=(5.5, 2.55), dpi=240)
    fig.patch.set_facecolor('#FCF9F5')
    ax.set_facecolor('#F4EFE8')
    ax.axis('off')

    nodes = {
        'Mule UPI\nrbi.kyc@okaxis': (0.50, 0.50, '#DB9487', 2350),
        'Victim 1\n(SMS + Link)': (0.15, 0.78, '#88B8AC', 1850),
        'Victim 2\n(WhatsApp)': (0.15, 0.22, '#88B8AC', 1850),
        'Phish Domain\nsbi-kyc.xyz': (0.50, 0.85, '#DEC182', 1950),
        'Device ID\n#DV-9921': (0.50, 0.15, '#C6A4B4', 1800),
        'Cashout Acct\nIFSC-0092': (0.85, 0.50, '#221F26', 2100),
    }
    edges = [
        ('Victim 1\n(SMS + Link)', 'Phish Domain\nsbi-kyc.xyz', 'Clicked URL'),
        ('Phish Domain\nsbi-kyc.xyz', 'Mule UPI\nrbi.kyc@okaxis', 'Redirects'),
        ('Victim 1\n(SMS + Link)', 'Mule UPI\nrbi.kyc@okaxis', '₹1.5L Collect'),
        ('Victim 2\n(WhatsApp)', 'Mule UPI\nrbi.kyc@okaxis', '₹45K Collect'),
        ('Victim 2\n(WhatsApp)', 'Device ID\n#DV-9921', 'Shared IMEI'),
        ('Device ID\n#DV-9921', 'Mule UPI\nrbi.kyc@okaxis', 'Operates'),
        ('Mule UPI\nrbi.kyc@okaxis', 'Cashout Acct\nIFSC-0092', 'Rapid Sweep'),
    ]
    for u, v, lbl in edges:
        x1, y1, _, _ = nodes[u]
        x2, y2, _, _ = nodes[v]
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#6C6570", lw=1.5, shrinkA=25, shrinkB=25))
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.03, lbl, fontsize=6.2, ha='center', va='center', color='#221F26',
                bbox=dict(boxstyle='round,pad=0.16', facecolor='#FCF9F5', edgecolor='#D0C6BA', lw=0.7))

    for name, (nx, ny, col, sz) in nodes.items():
        ax.scatter([nx], [ny], s=sz, color=col, edgecolors='#221F26', linewidth=1.5, zorder=3)
        txt_col = '#F6F2EC' if col == '#221F26' else '#221F26'
        ax.text(nx, ny, name, ha='center', va='center', fontsize=6.2, fontweight='bold', color=txt_col, zorder=4)

    ax.set_xlim(0.01, 0.99)
    ax.set_ylim(0.01, 1.02)
    ax.set_title('Heterogeneous ScamGraph: Shared Entity Risk Propagation', fontsize=9, fontweight='bold', color='#221F26', pad=4)
    plt.tight_layout()
    assets['chart_graph'] = os.path.join(ASSETS_DIR, "graph_topology.png")
    fig.savefig(assets['chart_graph'], dpi=240)
    plt.close()

    # 4. Hybrid Risk Formula Signal Weight Donut & Domain Breakdown (Slide 6)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.6, 2.55), dpi=240, gridspec_kw={'width_ratios': [1.1, 1.3]})
    fig.patch.set_facecolor('#FCF9F5')
    ax1.set_facecolor('#FCF9F5')
    ax2.set_facecolor('#F4EFE8')

    weights = [45, 25, 15, 15]
    labels = ['MuRIL + Seq\nML (45%)', 'Deterministic\nRules (25%)', 'URL Lexical\nRisk (15%)', 'Graph/Journey\nContext (15%)']
    colors = ['#221F26', '#C8B69E', '#88B8AC', '#C6A4B4']
    wedges, _ = ax1.pie(weights, colors=colors, startangle=140, wedgeprops=dict(width=0.42, edgecolor='#FCF9F5', linewidth=2))
    ax1.text(0, 0, "96/100\nCRITICAL", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#221F26')
    ax1.set_title('Ensemble Weights', fontsize=8.5, fontweight='bold', color='#221F26')
    ax1.legend(wedges, labels, loc='lower center', bbox_to_anchor=(0.5, -0.32), ncol=2, fontsize=6.3, frameon=False)

    dom_names = ['Comm NLP', 'URL Forensics', 'Device Bio', 'Graph/Txn']
    scam_contrib = [92, 88, 79, 96]
    benign_contrib = [12, 5, 8, 10]
    y_pos = np.arange(len(dom_names))
    ax2.barh(y_pos + 0.17, scam_contrib, height=0.32, color='#88B8AC', edgecolor='#221F26', label='Scam Workflow')
    ax2.barh(y_pos - 0.17, benign_contrib, height=0.32, color='#C8B69E', edgecolor='#221F26', label='Benign Transfer')
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(dom_names, fontsize=7.5, fontweight='bold', color='#221F26')
    ax2.set_xlim(0, 115)
    ax2.tick_params(axis='x', labelsize=7, colors='#6C6570')
    ax2.set_title('Domain Activation Profile', fontsize=8.5, fontweight='bold', color='#221F26')
    ax2.legend(loc='lower right', fontsize=6.3, facecolor='#FCF9F5', edgecolor='#D0C6BA')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    plt.tight_layout()
    assets['chart_signals'] = os.path.join(ASSETS_DIR, "signal_breakdown.png")
    fig.savefig(assets['chart_signals'], dpi=240)
    plt.close()

    # 5. Selective Intervention Comparison Bar Chart (Slide 7)
    fig, ax = plt.subplots(figsize=(5.5, 2.35), dpi=240)
    fig.patch.set_facecolor('#FCF9F5')
    ax.set_facecolor('#F4EFE8')

    examples = ['Ex 1: Known Payee\n(Known Dev + ₹2K)', 'Ex 2: Unusual Payee\n(New Dev + ₹30K)', 'Ex 3: Full Scam Chain\n(KYC+URL+New+₹1.5L)']
    scores = [8, 61, 96]
    colors = ['#B4C79C', '#DEC182', '#DB9487']

    bars = ax.barh(examples, scores, color=colors, height=0.5, edgecolor='#221F26', linewidth=1.0)
    ax.set_xlim(0, 148)
    for bar, s, act in zip(bars, scores, ['8/100 → Silent Allow', '61/100 → Soft Nudge', '96/100 → 30s Cool-Off Hold']):
        ax.text(s + 3, bar.get_y() + bar.get_height()/2, act, va='center', fontsize=8, fontweight='bold', color='#221F26')

    ax.tick_params(axis='y', colors='#221F26', labelsize=7.8)
    ax.tick_params(axis='x', colors='#6C6570', labelsize=7.5)
    ax.set_title('Context-Aware Scoring Prevents Alert Fatigue', fontsize=9, fontweight='bold', color='#221F26', pad=6)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    assets['chart_alert'] = os.path.join(ASSETS_DIR, "alert_comparison.png")
    fig.savefig(assets['chart_alert'], dpi=240)
    plt.close()

    # 6. Explainable AI & Analyst Dashboard Visual Mockup (Slide 8)
    fig, ax = plt.subplots(figsize=(5.7, 3.2), dpi=240)
    fig.patch.set_facecolor('#201E23')
    ax.set_facecolor('#2A272E')
    ax.axis('off')

    # Draw sleek dark UI console mockup
    ax.add_patch(mpatches.FancyBboxPatch((0.03, 0.05), 0.94, 0.88, boxstyle="round,pad=0.02", facecolor="#201E23", edgecolor="#C8B69E", linewidth=1.5))
    ax.text(0.06, 0.86, "● ● ●   SCAMGRAPH AI — LIVE WORKFLOW FORENSIC CONSOLE", fontsize=7.5, fontweight='bold', color='#C8B69E')

    # Left panel: SHAP Feature Attribution bars
    ax.text(0.06, 0.75, "SHAP / Attention Attribution (Why Score = 96/100)", fontsize=7.5, fontweight='bold', color='#F6F2EC')
    feats = ['+32%  5-Step Scam Sequence', '+24%  Fake Bank URL (.xyz)', '+18%  Urgency + Block Threat', '+14%  Mule UPI (3 Victims)', '+8%   New Dev + ₹1.5L Collect']
    f_vals = [0.76, 0.60, 0.46, 0.36, 0.22]
    f_cols = ['#DB9487', '#DEC182', '#88B8AC', '#C6A4B4', '#B4C79C']
    for idx, (ft, fv, fc) in enumerate(zip(feats, f_vals, f_cols)):
        y_b = 0.63 - idx * 0.115
        bar_w = fv * 0.27
        ax.add_patch(mpatches.FancyBboxPatch((0.06, y_b), bar_w, 0.065, boxstyle="round,pad=0.008", facecolor=fc, edgecolor="none"))
        ax.text(0.075 + bar_w, y_b + 0.03, ft, va='center', fontsize=6.6, fontweight='bold', color='#F6F2EC')

    # Right panel: Verdict badge
    ax.add_patch(mpatches.FancyBboxPatch((0.67, 0.46), 0.27, 0.34, boxstyle="round,pad=0.02", facecolor="#2A272E", edgecolor="#DB9487", linewidth=1.2))
    ax.text(0.805, 0.70, "RISK VERDICT", ha='center', fontsize=6.5, fontweight='bold', color='#D6C9B8')
    ax.text(0.805, 0.58, "96 / 100", ha='center', fontsize=13, fontweight='bold', color='#DB9487')
    ax.text(0.805, 0.49, "CRITICAL HOLD", ha='center', fontsize=7, fontweight='bold', color='#F6F2EC')

    ax.add_patch(mpatches.FancyBboxPatch((0.67, 0.12), 0.27, 0.28, boxstyle="round,pad=0.02", facecolor="#2A272E", edgecolor="#88B8AC", linewidth=1.0))
    ax.text(0.805, 0.31, "INTERVENTION", ha='center', fontsize=6.5, fontweight='bold', color='#88B8AC')
    ax.text(0.805, 0.20, "30s Cool-Off +\nOfficial App Verify", ha='center', fontsize=6.6, fontweight='bold', color='#F6F2EC')

    plt.tight_layout()
    assets['chart_workbench'] = os.path.join(ASSETS_DIR, "workbench_preview.png")
    fig.savefig(assets['chart_workbench'], dpi=240)
    plt.close()

    # 7. Validation Donut Gauges + Benchmark Columns (Slide 9 - Directly modeled on GoodPello Data Security slide)
    fig = plt.figure(figsize=(5.6, 3.1), dpi=240)
    fig.patch.set_facecolor('#FCF9F5')
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.25])

    # Donut 1: 100% Recall
    ax_d1 = fig.add_subplot(gs[0, 0])
    ax_d1.pie([100, 0.01], colors=['#221F26', '#E8E0D5'], startangle=90, wedgeprops=dict(width=0.35))
    ax_d1.text(0, 0, "100%\nRecall", ha='center', va='center', fontsize=8, fontweight='bold', color='#221F26')
    ax_d1.set_title("Known Scam Capture", fontsize=7.8, fontweight='bold', color='#221F26', pad=2)

    # Donut 2: 84% Noise Suppressed
    ax_d2 = fig.add_subplot(gs[0, 1])
    ax_d2.pie([84, 16], colors=['#C8B69E', '#E8E0D5'], startangle=90, wedgeprops=dict(width=0.35))
    ax_d2.text(0, 0, "84%\nLess Noise", ha='center', va='center', fontsize=8, fontweight='bold', color='#221F26')
    ax_d2.set_title("False Alert Reduction", fontsize=7.8, fontweight='bold', color='#221F26', pad=2)

    # Bottom Bar Comparison
    ax_b = fig.add_subplot(gs[1, :])
    ax_b.set_facecolor('#F4EFE8')
    m_lbls = ['Known Scam\nRecall', 'Overall F1\nAccuracy', 'Zero-Day\nVariant Catch', 'Alert Fatigue\nSuppression']
    scam_g = [100.0, 98.2, 89.5, 84.0]
    base_l = [71.0, 68.4, 42.0, 28.0]
    x_m = np.arange(len(m_lbls))
    ax_b.bar(x_m - 0.16, scam_g, width=0.3, color='#221F26', label='ScamGraph AI')
    ax_b.bar(x_m + 0.16, base_l, width=0.3, color='#C8B69E', label='Single-Event Baseline')
    for i, v in enumerate(scam_g):
        ax_b.text(x_m[i] - 0.16, v + 3, f"{v:.0f}%", ha='center', fontsize=7, fontweight='bold', color='#221F26')
    ax_b.set_ylim(0, 138)
    ax_b.set_xticks(x_m)
    ax_b.set_xticklabels(m_lbls, fontsize=7.2, fontweight='bold', color='#221F26')
    ax_b.tick_params(axis='y', labelsize=6.8, colors='#6C6570')
    ax_b.legend(loc='upper right', ncol=2, fontsize=6.3, facecolor='#FCF9F5', edgecolor='#D0C6BA')
    ax_b.spines['top'].set_visible(False)
    ax_b.spines['right'].set_visible(False)

    plt.tight_layout()
    assets['chart_validation'] = os.path.join(ASSETS_DIR, "validation_benchmarks.png")
    fig.savefig(assets['chart_validation'], dpi=240)
    plt.close()

    return assets


# ==============================================================================
# SLIDE HELPER FUNCTIONS (MONOCHROMATIC + EDITORIAL GEN Z THEME)
# ==============================================================================
def apply_canvas(slide, prs, slide_idx, total_slides=10, dark_mode=False):
    """Applies either the Warm Alabaster Oat canvas or Sleek Matte Charcoal canvas with ○ △ □ geometric header."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_CHARCOAL if dark_mode else BG_ALABASTER
    bg.line.fill.background()

    # Top monochromatic + pastel editorial accent strip
    seg_w = prs.slide_width / 4
    strip_cols = [CARD_TAUPE, PASTEL_SAGE, PASTEL_MAUVE, PASTEL_OCHRE]
    for i, col in enumerate(strip_cols):
        seg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(i * seg_w), 0, int(seg_w), Inches(0.06))
        seg.fill.solid()
        seg.fill.fore_color.rgb = col
        seg.line.fill.background()

    # Minimalist geometric symbols ○ △ □ (Inspired by uploaded template #4)
    geo_box = slide.shapes.add_textbox(Inches(10.55), Inches(0.20), Inches(1.15), Inches(0.32))
    tf_g = geo_box.text_frame
    p_g = tf_g.paragraphs[0]
    p_g.text = "○   △   □"
    p_g.font.size = Pt(11)
    p_g.font.bold = True
    p_g.font.color.rgb = CARD_TAUPE if dark_mode else INK_MUTED
    p_g.alignment = PP_ALIGN.RIGHT

    # Page counter pill
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(11.78), Inches(0.20), Inches(0.98), Inches(0.30))
    pill.fill.solid()
    pill.fill.fore_color.rgb = CARD_CHARCOAL if dark_mode else CARD_STONE
    pill.line.color.rgb = BORDER_DARK if dark_mode else BORDER_TAUPE
    tf = pill.text_frame
    p = tf.paragraphs[0]
    p.text = f"{slide_idx:02d} / {total_slides:02d}"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = INK_TAUPE_LT if dark_mode else INK_DARK
    p.alignment = PP_ALIGN.CENTER


def add_header(slide, section_num, tag_text, title_text, subtitle_text="", dark_mode=False):
    """Adds GoodPello + Gen Z Editorial style header with oversized number badge, pill tag, and title."""
    # Number badge (e.g., "02")
    num_badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.55), Inches(0.20), Inches(0.48), Inches(0.30))
    num_badge.fill.solid()
    num_badge.fill.fore_color.rgb = CARD_TAUPE if dark_mode else INK_DARK
    num_badge.line.fill.background()
    tf_n = num_badge.text_frame
    p_n = tf_n.paragraphs[0]
    p_n.text = section_num
    p_n.font.size = Pt(9.5)
    p_n.font.bold = True
    p_n.font.color.rgb = INK_DARK if dark_mode else INK_LIGHT
    p_n.alignment = PP_ALIGN.CENTER

    # Category Pill Tag
    tag_w = Inches(max(2.3, len(tag_text) * 0.088))
    tag = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.10), Inches(0.20), tag_w, Inches(0.30))
    tag.fill.solid()
    tag.fill.fore_color.rgb = CARD_CHARCOAL if dark_mode else CARD_STONE
    tag.line.color.rgb = CARD_TAUPE
    tf_tag = tag.text_frame
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = tag_text.upper()
    p_tag.font.size = Pt(8.5)
    p_tag.font.bold = True
    p_tag.font.color.rgb = CARD_TAUPE if dark_mode else INK_DARK
    p_tag.alignment = PP_ALIGN.CENTER

    # Main Slide Title
    t_box = slide.shapes.add_textbox(Inches(0.55), Inches(0.53), Inches(12.2), Inches(0.46))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(21)
    p_t.font.bold = True
    p_t.font.color.rgb = INK_LIGHT if dark_mode else INK_DARK

    if subtitle_text:
        s_box = slide.shapes.add_textbox(Inches(0.55), Inches(0.96), Inches(12.2), Inches(0.32))
        tf_s = s_box.text_frame
        tf_s.word_wrap = True
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle_text
        p_s.font.size = Pt(10.5)
        p_s.font.color.rgb = INK_TAUPE_LT if dark_mode else INK_MUTED


def add_card(slide, left, top, width, height, bg_color=CARD_CREAM, border_color=BORDER_TAUPE, stripe_color=None, radius=True):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    card = slide.shapes.add_shape(shape_type, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.0)
    else:
        card.line.fill.background()

    if stripe_color:
        stripe = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.10), top + Inches(0.12), Inches(0.07), height - Inches(0.24))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = stripe_color
        stripe.line.fill.background()
    return card


def add_card_content(slide, left, top, width, height, title, bullets, title_size=12, body_size=9.5, dark_card=False, badge_text=None, badge_bg=CARD_TAUPE):
    offset_x = Inches(0.16)
    cur_y = top + Inches(0.10)

    if badge_text:
        bw = Inches(max(0.55, len(badge_text) * 0.085))
        b_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + offset_x, cur_y + Inches(0.03), bw, Inches(0.24))
        b_shape.fill.solid()
        b_shape.fill.fore_color.rgb = badge_bg
        b_shape.line.fill.background()
        tf_b = b_shape.text_frame
        p_b = tf_b.paragraphs[0]
        p_b.text = badge_text
        p_b.font.size = Pt(8)
        p_b.font.bold = True
        p_b.font.color.rgb = INK_DARK
        p_b.alignment = PP_ALIGN.CENTER
        title_x = left + offset_x + bw + Inches(0.10)
        title_w = width - offset_x - bw - Inches(0.20)
    else:
        title_x = left + offset_x
        title_w = width - Inches(0.28)

    if title:
        tb = slide.shapes.add_textbox(title_x, cur_y, title_w, Inches(0.32))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(title_size)
        p.font.bold = True
        p.font.color.rgb = INK_LIGHT if dark_card else INK_DARK
        cur_y += Inches(0.32)

    bb = slide.shapes.add_textbox(left + offset_x, cur_y, width - Inches(0.28), height - (cur_y - top) - Inches(0.08))
    tf_body = bb.text_frame
    tf_body.word_wrap = True
    for i, b in enumerate(bullets):
        p = tf_body.paragraphs[0] if i == 0 else tf_body.add_paragraph()
        p.text = b
        p.font.size = Pt(body_size)
        p.font.color.rgb = INK_TAUPE_LT if dark_card else INK_MUTED
        p.space_after = Pt(3.5)


def add_pill_row(slide, left, top, width, height, num_str, title_str, desc_str, pill_bg=CARD_CREAM, num_bg=INK_DARK, num_fg=INK_LIGHT):
    """Creates the signature numbered horizontal pill row from uploaded template #4 (media_1791661170046.png)."""
    row = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    row.fill.solid()
    row.fill.fore_color.rgb = pill_bg
    row.line.color.rgb = BORDER_TAUPE
    row.line.width = Pt(1.0)

    # Number circle/pill on left
    npill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.10), top + Inches(0.10), Inches(0.45), height - Inches(0.20))
    npill.fill.solid()
    npill.fill.fore_color.rgb = num_bg
    npill.line.fill.background()
    tf_n = npill.text_frame
    p_n = tf_n.paragraphs[0]
    p_n.text = num_str
    p_n.font.size = Pt(10)
    p_n.font.bold = True
    p_n.font.color.rgb = num_fg
    p_n.alignment = PP_ALIGN.CENTER

    # Text content
    tb = slide.shapes.add_textbox(left + Inches(0.62), top + Inches(0.06), width - Inches(0.72), height - Inches(0.12))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = title_str
    p1.font.size = Pt(10.5)
    p1.font.bold = True
    p1.font.color.rgb = INK_DARK

    p2 = tf.add_paragraph()
    p2.text = desc_str
    p2.font.size = Pt(8.8)
    p2.font.color.rgb = INK_MUTED


def build_deck():
    assets = generate_visual_assets()

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    TOTAL_SLIDES = 10

    # ==========================================================================
    # SLIDE 1: TEAM & PROBLEM STATEMENT (IIT DELHI AMAZON HACKATHON)
    # Dark Charcoal + Warm Taupe Monochromatic Editorial Cover (Inspired by GoodPello #3)
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_canvas(s1, prs, 1, TOTAL_SLIDES, dark_mode=True)

    # Top Hackathon Badge
    hb = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.55), Inches(0.22), Inches(4.9), Inches(0.32))
    hb.fill.solid()
    hb.fill.fore_color.rgb = CARD_CHARCOAL
    hb.line.color.rgb = CARD_TAUPE
    tf_hb = hb.text_frame
    p_hb = tf_hb.paragraphs[0]
    p_hb.text = "IIT DELHI × AMAZON HACKATHON  |  TRACK 2: SCAM PATTERN RECOGNITION"
    p_hb.font.size = Pt(8.5)
    p_hb.font.bold = True
    p_hb.font.color.rgb = CARD_TAUPE
    p_hb.alignment = PP_ALIGN.CENTER

    # Hero Title & Subtitle
    t1 = s1.shapes.add_textbox(Inches(0.55), Inches(0.65), Inches(7.8), Inches(1.35))
    tf1 = t1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "ScamGraph AI"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = INK_LIGHT

    p2 = tf1.add_paragraph()
    p2.text = "AI-Driven Scam Pattern Recognition & Connected Workflow Intelligence"
    p2.font.size = Pt(15)
    p2.font.bold = True
    p2.font.color.rgb = CARD_TAUPE

    p3 = tf1.add_paragraph()
    p3.text = "Moving beyond isolated spam filters to detect multi-stage financial fraud across SMS, WhatsApp, URLs, Devices & UPI."
    p3.font.size = Pt(10.5)
    p3.font.color.rgb = INK_TAUPE_LT

    # Left Column: Official Problem Statement Card (Warm Alabaster on Dark Canvas)
    add_card(s1, Inches(0.55), Inches(2.12), Inches(7.55), Inches(3.25), bg_color=CARD_CREAM, border_color=CARD_TAUPE, stripe_color=PASTEL_SAGE)
    add_card_content(
        s1, Inches(0.68), Inches(2.18), Inches(7.35), Inches(3.15),
        "OFFICIAL PROBLEM STATEMENT — TRACK 2",
        [
            "• The Challenge: Modern scammers leverage Generative AI (voice clones, vernacular LLM lures, polymorphic phishing sites) to orchestrate multi-step fraud across SMS, WhatsApp, calls, and UPI.",
            "• The Blind Spot: Legacy banking fraud systems inspect single messages or isolated transactions in silos—missing the connected storyline linking a harmless-looking KYC text to a ₹1,50,000 account drain.",
            "• Core Mandate: Build an AI system that (1) detects the complete connected scam workflow, (2) identifies emerging scam patterns via graph + sequence ML, (3) computes calibrated 0–100 risk scores, and (4) delivers explainable, proportional interventions without triggering user alert fatigue."
        ],
        title_size=13, body_size=10, dark_card=False, badge_text="PROBLEM", badge_bg=PASTEL_SAGE
    )

    # Bottom Left: 4 Key Differentiator Pills
    pillars = [
        ("01  WORKFLOW ENGINE", "Connects 6+ cross-channel events", CARD_TAUPE),
        ("02  MURIL + GNN ML", "Hinglish NLP + Mule Graph rings", PASTEL_SAGE),
        ("03  ZERO FATIGUE", "84% fewer low-value popups", PASTEL_MINT),
        ("04  SUB-50MS XAI", "Real-time pre-UPI intervention", PASTEL_MAUVE),
    ]
    for idx, (pt, pd, pcol) in enumerate(pillars):
        px = Inches(0.55 + idx * 1.92)
        add_card(s1, px, Inches(5.55), Inches(1.82), Inches(1.45), bg_color=CARD_CHARCOAL, border_color=pcol)
        add_card_content(s1, px - Inches(0.06), Inches(5.60), Inches(1.88), Inches(1.35), pt, [pd], title_size=9.5, body_size=8.8, dark_card=True)

    # Right Column: Team Profile Card + Uploaded Cyber Security HUD Image
    add_card(s1, Inches(8.30), Inches(0.68), Inches(4.48), Inches(2.85), bg_color=CARD_CHARCOAL, border_color=CARD_TAUPE, stripe_color=CARD_TAUPE)
    add_card_content(
        s1, Inches(8.42), Inches(0.74), Inches(4.30), Inches(2.75),
        "TEAM SCAMGRAPH — IIT DELHI",
        [
            "• Team Lead & AI Architect: Nishkarsh Singh",
            "• Track: FinTech Security, Graph ML & Fraud Intelligence",
            "• Tech Stack: PyTorch, MuRIL Transformer, Graph Neural Networks (PyG), FastAPI, React Flow, Docker",
            "• Live Prototype: End-to-End Working Platform + Real-Time Workflow Simulator + 100% Test Recall",
            "• GitHub: github.com/Nishkarsh807/scamgraph-ai"
        ],
        title_size=12.5, body_size=9.5, dark_card=True, badge_text="TEAM INFO", badge_bg=CARD_TAUPE
    )

    # Embed Uploaded Cyber Security HUD image on Slide 1 bottom-right
    if assets.get('img_cyber'):
        s1.shapes.add_picture(assets['img_cyber'], Inches(8.30), Inches(3.72), width=Inches(4.48), height=Inches(2.65))
        cap1 = s1.shapes.add_Shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.30), Inches(6.45), Inches(4.48), Inches(0.55)) if hasattr(s1.shapes, 'add_Shape') else s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.30), Inches(6.45), Inches(4.48), Inches(0.55))
        cap1.fill.solid()
        cap1.fill.fore_color.rgb = CARD_TAUPE
        cap1.line.fill.background()
        tf_c1 = cap1.text_frame
        p_c1 = tf_c1.paragraphs[0]
        p_c1.text = "CORE VISION: Detect the scam journey, not just the final transaction."
        p_c1.font.size = Pt(9.5)
        p_c1.font.bold = True
        p_c1.font.color.rgb = INK_DARK
        p_c1.alignment = PP_ALIGN.CENTER

    # ==========================================================================
    # SLIDE 2: THE PROBLEM & GAP — AI-GENERATED DECEPTION VS. SILOED DEFENSES
    # Embeds Uploaded Multi-Mask Art (media_1791660854055.jpg) + Deep Content
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_canvas(s2, prs, 2, TOTAL_SLIDES, dark_mode=False)
    add_header(
        s2, "01", "Problem Landscape & Failure Analysis",
        "Why Traditional Fraud Systems Miss AI-Enabled Scam Workflows",
        "Scammers operate as cross-channel state machines using GenAI personas, while banks still inspect single events in isolation."
    )

    # Left: Uploaded Multi-Mask Impersonation Image + Analytical Caption Card
    if assets.get('img_masks'):
        s2.shapes.add_picture(assets['img_masks'], Inches(0.55), Inches(1.38), width=Inches(4.35), height=Inches(3.32))

    add_card(s2, Inches(0.55), Inches(4.82), Inches(4.35), Inches(2.25), bg_color=BG_CHARCOAL, border_color=CARD_TAUPE, stripe_color=PASTEL_CORAL)
    add_card_content(
        s2, Inches(0.68), Inches(4.88), Inches(4.15), Inches(2.15),
        "THE GEN-AI DECEPTION MULTIPLIER",
        [
            "• Polymorphic Personas: Scammers wear masks of RBI officers, bank support, police ('Digital Arrest'), or HR recruiters.",
            "• Zero Grammatical Errors: LLMs craft fluent English, Hindi & Hinglish scripts customized to victim profiles.",
            "• Ephemeral Infrastructure: Phishing domains (.xyz/.top) and burner numbers rotate every 15–30 minutes."
        ],
        title_size=11, body_size=8.8, dark_card=True, badge_text="THREAT", badge_bg=PASTEL_CORAL
    )

    # Right: 4 High-Density Problem Cards + Siloed vs. Workflow Comparison
    prob_cards = [
        ("01", "Multi-Channel Fragmentation", CARD_CREAM, PASTEL_SAGE, [
            "• A single scam spans 5+ touchpoints: SMS warning → WhatsApp support chat → phishing link → fake APK/web login → UPI collect request.",
            "• Telcos see only the SMS; browsers see only the URL; banks see only the final UPI transfer—no entity connects the chain."
        ]),
        ("02", "Individually 'Innocent' Micro-Events", CARD_STONE, CARD_TAUPE, [
            "• An SMS saying 'Update PAN today' scores 18/100 (Low).",
            "• Logging in from a new device scores 22/100 (Low).",
            "• Adding a new UPI payee scores 25/100 (Low).",
            "• Viewed separately, every step passes legacy rule thresholds; viewed together, it is a 96/100 active attack."
        ]),
        ("03", "Static Rules Lag Emerging Variants", CARD_STONE, PASTEL_MAUVE, [
            "• Hardcoded keyword blacklists fail when scammers switch from 'KYC Expiry' to 'Electricity Bill Disconnection' or '24-Hr Digital Arrest Warrant'.",
            "• By the time fraud analysts write new rules (2–4 weeks), mule accounts have already cashed out."
        ]),
        ("04", "The Alert Fatigue Paradox", CARD_CREAM, PASTEL_OCHRE, [
            "• Showing generic 'Beware of Fraud!' banners on every transaction trains users to click 'Proceed' blindly in <1.2 seconds.",
            "• Lowering rule thresholds causes 70%+ false positives on legitimate transfers, overwhelming SOC teams."
        ]),
    ]
    for idx, (b_num, c_title, c_bg, c_stripe, c_bullets) in enumerate(prob_cards):
        col = idx % 2
        row = idx // 2
        cx = Inches(5.10 + col * 3.92)
        cy = Inches(1.38 + row * 2.18)
        add_card(s2, cx, cy, Inches(3.78), Inches(2.04), bg_color=c_bg, border_color=BORDER_TAUPE, stripe_color=c_stripe)
        add_card_content(s2, cx + Inches(0.08), cy + Inches(0.04), Inches(3.65), Inches(1.95), c_title, c_bullets, title_size=11, body_size=8.6, badge_text=b_num, badge_bg=c_stripe)

    # Bottom Right Summary Strip: Paradigm Shift
    add_card(s2, Inches(5.10), Inches(5.76), Inches(7.68), Inches(1.31), bg_color=CARD_SAGE_SOFT, border_color=PASTEL_SAGE)
    add_card_content(
        s2, Inches(5.18), Inches(5.80), Inches(7.50), Inches(1.22),
        "OUR PARADIGM SHIFT: FROM SINGLE-EVENT FILTERING TO STATEFUL WORKFLOW RECOGNITION",
        [
            "• Legacy Approach: Inspects P(Fraud | Event_t) in isolation → Misses gradual social engineering escalation & causes alert fatigue.",
            "• ScamGraph AI Approach: Computes P(Fraud | Sequence E_1...E_t, Graph Topology G) → Captures the full scam storyline before funds leave."
        ],
        title_size=10.5, body_size=8.8, badge_text="INSIGHT", badge_bg=PASTEL_SAGE
    )

    # ==========================================================================
    # SLIDE 3: CORE INNOVATION — SCAM JOURNEY INTELLIGENCE & FUNNEL
    # Embeds Uploaded 3D Funnel Image (image1.png) + Escalation Chart + 6-Stage Breakdown
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_canvas(s3, prs, 3, TOTAL_SLIDES, dark_mode=False)
    add_header(
        s3, "02", "Core Innovation: Scam Journey Intelligence",
        "Tracking the 6-Stage Anatomy of an AI-Enabled Scam Workflow",
        "Instead of scoring isolated messages, ScamGraph links temporally related micro-signals into a unified, escalating fraud state machine."
    )

    # Left: Uploaded 3D KYC Scam Funnel Graphic
    add_card(s3, Inches(0.55), Inches(1.35), Inches(5.85), Inches(3.85), bg_color=CARD_CREAM, border_color=BORDER_TAUPE)
    if assets.get('img_funnel'):
        s3.shapes.add_picture(assets['img_funnel'], Inches(0.68), Inches(1.42), width=Inches(5.58))

    # Bottom Left: 6-Stage Connected Chain Pills
    add_card(s3, Inches(0.55), Inches(5.32), Inches(5.85), Inches(1.75), bg_color=BG_CHARCOAL, border_color=CARD_TAUPE, stripe_color=PASTEL_SAGE)
    add_card_content(
        s3, Inches(0.68), Inches(5.38), Inches(5.65), Inches(1.65),
        "EXAMPLE CONNECTED SCAM WORKFLOW (42-MINUTE WINDOW)",
        [
            "• T+00m [SMS]: 'Dear customer, SBI PAN-KYC expires today. Account will be frozen.' (Risk: 18)",
            "• T+04m [URL]: Clicks bit.ly/sbi-kyc-update → redirects to sbi-pan-verify.xyz (Risk: 42)",
            "• T+11m [Device/Login]: Unrecognized device fingerprint logs in + requests OTP (Risk: 61)",
            "• T+18m [Payee + UPI]: Adds unknown VPA 'rbi.verify@okaxis' & initiates ₹1,50,000 transfer (Risk: 96 — CRITICAL HOLD)"
        ],
        title_size=10.5, body_size=8.4, dark_card=True, badge_text="TIMELINE", badge_bg=PASTEL_SAGE
    )

    # Right Top: High-DPI Escalation Line Chart
    add_card(s3, Inches(6.58), Inches(1.35), Inches(6.20), Inches(3.15), bg_color=CARD_CREAM, border_color=BORDER_TAUPE)
    s3.shapes.add_picture(assets['chart_escalation'], Inches(6.70), Inches(1.42), width=Inches(5.95))

    # Right Bottom: How Temporal State Correlation Works (3 Deep Technical Pills)
    mech_rows = [
        ("01", "Temporal Window & Decay Weighting", "Links cross-channel events within a sliding 24h window using exponential decay w(Δt) = exp(-λ·Δt) so rapid multi-step chains amplify risk exponentially.", CARD_CREAM, INK_DARK),
        ("02", "8 Canonical Scam State Machines", "Pre-trained + learned transition matrices for KYC Fraud, UPI Collect Trap, Digital Arrest, Fake Bank Support, Job Fee Scam, Electricity Cutoff, Loan & Investment Scams.", CARD_STONE, CARD_TAUPE),
        ("03", "Early Pre-Transaction Interception", "Crosses the 75/100 intervention threshold at Stage 4 (Beneficiary Addition), enabling proactive user warning BEFORE the final ₹1.5L UPI PIN is entered.", CARD_SAGE_SOFT, PASTEL_SAGE),
    ]
    for idx, (m_num, m_title, m_desc, m_bg, m_nbg) in enumerate(mech_rows):
        n_fg = INK_LIGHT if m_nbg == INK_DARK else INK_DARK
        add_pill_row(s3, Inches(6.58), Inches(4.62 + idx * 0.84), Inches(6.20), Inches(0.76), m_num, m_title, m_desc, pill_bg=m_bg, num_bg=m_nbg, num_fg=n_fg)

    # ==========================================================================
    # SLIDE 4 (AFTER 3RD SLIDE - IMAGE #1): END-TO-END 5-LAYER SYSTEM ARCHITECTURE
    # Embeds Uploaded Cyber Security HUD Image (media_1791661273473.png) + 5-Stage Pipeline
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_canvas(s4, prs, 4, TOTAL_SLIDES, dark_mode=False)
    add_header(
        s4, "03", "End-to-End System Architecture",
        "Real-Time 5-Layer Streaming Architecture (<50ms Decision Latency)",
        "Designed as a plug-and-play intelligence layer alongside existing UPI apps, banking cores, and telco gateways."
    )

    # Top Horizontal 5-Layer Pipeline Flowchart
    arch_layers = [
        ("LAYER 01", "Multi-Modal Ingestion", CARD_CREAM, PASTEL_SAGE, [
            "• SMS / WhatsApp Texts",
            "• URLs & Redirect Chains",
            "• Call/Chat Transcripts",
            "• Device & Session Logs",
            "• UPI / IMPS Requests",
            "• Apache Kafka Event Bus"
        ]),
        ("LAYER 02", "Signal & Feature Engine", CARD_STONE, CARD_TAUPE, [
            "• Preserves ₹, URLs, VPAs",
            "• MuRIL Hinglish Embeddings",
            "• 9 Deterministic Rules",
            "• URL Lexical Forensics",
            "• Velocity & Session Drift",
            "• Feature Store (<8ms)"
        ]),
        ("LAYER 03", "Graph & Sequence AI", BG_CHARCOAL, PASTEL_MAUVE, [
            "• Temporal Transformer",
            "• Heterogeneous ScamGraph",
            "• GNN Entity Risk Scoring",
            "• Campaign Clustering",
            "• Partial Chain Matcher",
            "• Dynamic State Memory"
        ]),
        ("LAYER 04", "Ensemble Risk Engine", CARD_STONE, PASTEL_OCHRE, [
            "• Calibrated 0–100 Score",
            "• 45% ML + 25% Rules",
            "• 15% URL + 15% Workflow",
            "• Threshold Tier Routing",
            "• Confidence Calibration",
            "• Alert Fatigue Filter"
        ]),
        ("LAYER 05", "XAI & Action Engine", CARD_SAGE_SOFT, PASTEL_SAGE, [
            "• Plain-Language XAI Alert",
            "• 30s Payment Cool-Off",
            "• Intent Verification Quiz",
            "• SOC Graph Workbench",
            "• 1-Click Mule Quarantine",
            "• Continuous Feedback"
        ]),
    ]

    for idx, (l_badge, l_title, l_bg, l_stripe, l_bullets) in enumerate(arch_layers):
        lx = Inches(0.55 + idx * 2.48)
        ly = Inches(1.36)
        lw = Inches(2.30)
        lh = Inches(2.92)
        is_dark = (l_bg == BG_CHARCOAL)
        add_card(s4, lx, ly, lw, lh, bg_color=l_bg, border_color=CARD_TAUPE if is_dark else BORDER_TAUPE, stripe_color=l_stripe)
        add_card_content(s4, lx + Inches(0.06), ly + Inches(0.06), lw - Inches(0.12), lh - Inches(0.12), l_title, l_bullets, title_size=10.5, body_size=8.3, dark_card=is_dark, badge_text=l_badge, badge_bg=l_stripe)

        if idx < 4:
            arr = s4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, lx + lw + Inches(0.03), ly + Inches(1.30), Inches(0.12), Inches(0.24))
            arr.fill.solid()
            arr.fill.fore_color.rgb = INK_DARK
            arr.line.fill.background()

    # Bottom Left: Uploaded Cyber Security HUD Image (media_1791661273473.png)
    if assets.get('img_cyber'):
        s4.shapes.add_picture(assets['img_cyber'], Inches(0.55), Inches(4.42), width=Inches(4.65), height=Inches(2.65))

    # Bottom Right: 3 Deep Engineering Specification Cards
    eng_specs = [
        ("HIGH-THROUGHPUT STREAMING SLA", CARD_CREAM, PASTEL_SAGE, [
            "• End-to-end inference in <50ms p99 latency: 6ms text/URL extraction + 18ms quantized ONNX MuRIL/Sequence pass + 12ms Redis Graph lookup + 5ms risk aggregation.",
            "• Handles 10,000+ concurrent UPI/banking events per second via stateless FastAPI workers and Redis Streams."
        ]),
        ("PRESERVING CRITICAL FRAUD INDICATORS", CARD_STONE, CARD_TAUPE, [
            "• Unlike generic NLP pipelines that strip punctuation and digits, ScamGraph's preprocessor explicitly extracts and tokenizes URLs, ₹ currency amounts, 10-digit mobile numbers, @upi handles, and OTP keywords.",
            "• Bilingual Hinglish normalization handles code-mixed messages ('Aapka bijli bill aaj raat disconnect ho jayega')."
        ]),
        ("CLOSED-LOOP ACTIVE LEARNING", BG_CHARCOAL, PASTEL_MAUVE, [
            "• Confirmed fraud verdicts, user 'Report Scam' actions, and analyst overrides automatically feed back into nightly contrastive retraining—adapting to new scam templates within hours."
        ]),
    ]
    for idx, (e_title, e_bg, e_stripe, e_bullets) in enumerate(eng_specs):
        ey = Inches(4.42 + idx * 0.90)
        eh = Inches(0.84)
        is_dk = (e_bg == BG_CHARCOAL)
        add_card(s4, Inches(5.38), ey, Inches(7.40), eh, bg_color=e_bg, border_color=BORDER_TAUPE, stripe_color=e_stripe)
        add_card_content(s4, Inches(5.50), ey + Inches(0.02), Inches(7.20), eh - Inches(0.04), e_title, e_bullets, title_size=9.5, body_size=8.0, dark_card=is_dk)

    # ==========================================================================
    # SLIDE 5 (AFTER 3RD SLIDE - IMAGE #2): AI & ML CORE — SEQUENCE + GRAPH MODELS
    # Dark Charcoal Slide (Inspired by GoodPello Data Security Template) with Radar Chart & Graph Topology
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_canvas(s5, prs, 5, TOTAL_SLIDES, dark_mode=True)
    add_header(
        s5, "04", "AI & Machine Learning Core",
        "Dual-Engine Intelligence: Sequence Transformers + Heterogeneous ScamGraph",
        "Combining Indian-language NLP (MuRIL), temporal sequence modeling, and Graph Neural Networks to catch both known and zero-day scams.",
        dark_mode=True
    )

    # Left Column: 3 Detailed Model Architecture Cards
    ml_cards = [
        ("MODEL 01", "Multilingual Indian NLP (MuRIL / IndicBERT)", CARD_CHARCOAL, PASTEL_SAGE, False, [
            "• Hierarchical 2-Stage Classifier: Stage 1 binary head (BENIGN vs. SCAM) + Stage 2 13-class scam taxonomy head (KYC, UPI, OTP, Phishing, Banking, Job, Loan, Lottery, Electricity, Investment, Digital Arrest, Impersonation).",
            "• Trained on English + Hinglish scam corpora; detects psychological coercion, urgency ('within 15 mins'), authority impersonation ('CBI/RBI warrant'), and credential harvesting."
        ]),
        ("MODEL 02", "Temporal Workflow Sequence Engine (Transformer / LSTM)", CARD_CHARCOAL, CARD_TAUPE, False, [
            "• Encodes each user's recent interaction trajectory E = [e_1, e_2, ..., e_t] with event-type embeddings, channel transitions (SMS → Web → UPI), and inter-event time deltas Δt.",
            "• Computes workflow completion probability against canonical scam state machines, catching partial chains before the final payment step."
        ]),
        ("MODEL 03", "Heterogeneous ScamGraph & GNN Risk Propagation", CARD_CREAM, PASTEL_MAUVE, True, [
            "• Nodes: Users, Phone Numbers, URLs/Domains, Device Fingerprints, UPI IDs, Bank Accounts.",
            "• Edges: Sent-Message, Clicked-Link, Logged-In-From, Requested-Collect, Transferred-Funds.",
            "• Graph Attention Network (GAT) propagates suspicion across shared infrastructure—if 3 victims receive different SMS texts pointing to the same mule UPI handle, the entire cluster is flagged instantly."
        ]),
    ]
    for idx, (m_badge, m_title, m_bg, m_stripe, is_light, m_bullets) in enumerate(ml_cards):
        my = Inches(1.36 + idx * 1.90)
        mh = Inches(1.80)
        add_card(s5, Inches(0.55), my, Inches(6.45), mh, bg_color=m_bg, border_color=m_stripe, stripe_color=m_stripe)
        add_card_content(s5, Inches(0.68), my + Inches(0.05), Inches(6.22), mh - Inches(0.10), m_title, m_bullets, title_size=11, body_size=8.6, dark_card=(not is_light), badge_text=m_badge, badge_bg=m_stripe)

    # Right Top: Capability Radar Chart (GoodPello Data Security style)
    add_card(s5, Inches(7.20), Inches(1.36), Inches(5.58), Inches(2.75), bg_color=CARD_CHARCOAL, border_color=CARD_TAUPE)
    s5.shapes.add_picture(assets['chart_radar'], Inches(7.32), Inches(1.42), width=Inches(5.34))

    # Right Bottom: Heterogeneous ScamGraph Network Topology Image
    add_card(s5, Inches(7.20), Inches(4.24), Inches(5.58), Inches(2.82), bg_color=CARD_CREAM, border_color=CARD_TAUPE)
    s5.shapes.add_picture(assets['chart_graph'], Inches(7.32), Inches(4.30), width=Inches(5.34))

    # ==========================================================================
    # SLIDE 6 (AFTER 3RD SLIDE - IMAGE #3): MULTI-SIGNAL DETECTION & RISK ENGINE
    # GoodPello 01-04 Pill Rows + Ensemble Formula + Donut & Domain Activation Chart
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_canvas(s6, prs, 6, TOTAL_SLIDES, dark_mode=False)
    add_header(
        s6, "05", "Multi-Signal Feature Engineering & Risk Formula",
        "Synthesizing 4 Feature Domains into a Calibrated 0–100 Risk Score",
        "Deterministic rules and lexical URL forensics complement deep learning—ensuring zero-day resilience and transparent scoring."
    )

    # Left: 4 Feature Domain Pill Cards (01, 02, 03, 04)
    domains = [
        ("01", "Communication & Psychological Signals (NLP + 9 Rules)",
         "Detects Urgency ('immediately', 'within 2 hrs'), Threat ('account blocked', 'FIR'), OTP/PIN requests, KYC lures, Reward traps, Impersonation (RBI/SBI/Police), and Unknown Senders.",
         CARD_CREAM, INK_DARK, INK_LIGHT),
        ("02", "URL & Lexical Phishing Forensics",
         "Extracts domain, subdomain depth, risky TLDs (.xyz, .top, .buzz, .click), IP-based URLs, URL shorteners (bit.ly, tinyurl), brand typosquatting (sbi-kyc-update.com), and login keywords.",
         CARD_STONE, CARD_TAUPE, INK_DARK),
        ("03", "Behavioral & Session Telemetry",
         "Captures new/unrecognized device fingerprints, emulator/remote-access indicators (AnyDesk/TeamViewer), rapid navigation from external link to payment screen, and anomalous typing cadence.",
         CARD_SAGE_SOFT, PASTEL_SAGE, INK_DARK),
        ("04", "Transaction & Graph Network Signals",
         "Evaluates first-time payee status, amount spike vs. 90-day user baseline (e.g., ₹1.5L vs ₹2K avg), rapid repeated UPI collect pulls, and payee GNN degree centrality across other victims.",
         CARD_MAUVE_SOFT, PASTEL_MAUVE, INK_DARK),
    ]
    for idx, (d_num, d_title, d_desc, d_bg, d_nbg, d_nfg) in enumerate(domains):
        add_pill_row(s6, Inches(0.55), Inches(1.36 + idx * 1.12), Inches(6.25), Inches(1.02), d_num, d_title, d_desc, pill_bg=d_bg, num_bg=d_nbg, num_fg=d_nfg)

    # Bottom Left: Explicit Mathematical Risk Formula Card
    add_card(s6, Inches(0.55), Inches(5.86), Inches(6.25), Inches(1.22), bg_color=BG_CHARCOAL, border_color=CARD_TAUPE, stripe_color=CARD_TAUPE)
    add_card_content(
        s6, Inches(0.68), Inches(5.90), Inches(6.05), Inches(1.14),
        "CALIBRATED HYBRID ENSEMBLE FORMULA (CONFIGURABLE THRESHOLDS)",
        [
            "• Final Risk (0–100) = 0.45 × ML_Prob + 0.25 × Rule_Score + 0.15 × URL_Risk + 0.15 × Workflow_Graph_Score",
            "• Critical Escalation Override: If ≥3 connected workflow stages match + High-Value Transfer, score floors at ≥85 (CRITICAL)."
        ],
        title_size=10, body_size=8.4, dark_card=True, badge_text="FORMULA", badge_bg=CARD_TAUPE
    )

    # Right Top: Donut + Domain Activation Chart
    add_card(s6, Inches(7.00), Inches(1.36), Inches(5.78), Inches(2.90), bg_color=CARD_CREAM, border_color=BORDER_TAUPE)
    s6.shapes.add_picture(assets['chart_signals'], Inches(7.08), Inches(1.42), width=Inches(5.60))

    # Right Bottom: Why Hybrid Beats Pure ML or Pure Rules (Comparison Matrix Card)
    add_card(s6, Inches(7.00), Inches(4.40), Inches(5.78), Inches(2.68), bg_color=CARD_STONE, border_color=BORDER_TAUPE, stripe_color=PASTEL_SAGE)
    add_card_content(
        s6, Inches(7.12), Inches(4.46), Inches(5.55), Inches(2.55),
        "WHY HYBRID MULTI-SIGNAL FUSION WINS IN PRODUCTION",
        [
            "• Pure ML Weakness: Can hallucinate on short benign texts ('OTP for login is 4421') or be evaded by adversarial prompt spelling.",
            "• Pure Rule Weakness: Rigid thresholds fail when scammers paraphrase lures; cannot correlate multi-day event sequences.",
            "• ScamGraph Synergy: Deterministic rules provide high-precision anchors (e.g., @upi + risky TLD + OTP request), while MuRIL + Sequence GNN provide semantic & relational context.",
            "• Result: Zero single-point-of-failure and full auditability for RBI compliance."
        ],
        title_size=11, body_size=8.8, badge_text="SYNERGY", badge_bg=PASTEL_SAGE
    )

    # ==========================================================================
    # SLIDE 7 (AFTER 3RD SLIDE - IMAGE #4): STOPPING ALERT FATIGUE — SELECTIVE INTERVENTION
    # Embeds Uploaded CRT Surveillance Overload Image (media_1791660878504.jpg) + Comparison Chart + 4-Tier Matrix
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_canvas(s7, prs, 7, TOTAL_SLIDES, dark_mode=False)
    add_header(
        s7, "06", "Stopping Alert Fatigue: Risk-Proportional Intervention",
        "Precision Friction: Silent on Safe Payments, Decisive on Active Scams",
        "Constant low-confidence warnings make users blind to real danger. ScamGraph matches intervention intensity strictly to workflow risk."
    )

    # Left Top: Uploaded CRT Alert Fatigue Image (media_1791660878504.jpg)
    if assets.get('img_crt'):
        s7.shapes.add_picture(assets['img_crt'], Inches(0.55), Inches(1.36), width=Inches(4.35), height=Inches(2.90))

    # Left Bottom: Horizontal Risk Comparison Chart (Ex 1 vs Ex 2 vs Ex 3)
    add_card(s7, Inches(0.55), Inches(4.38), Inches(5.65), Inches(2.70), bg_color=CARD_CREAM, border_color=BORDER_TAUPE)
    s7.shapes.add_picture(assets['chart_alert'], Inches(0.62), Inches(4.44), width=Inches(5.50))

    # Right Top (next to CRT image): The Alert Fatigue Problem & Dynamic Gating
    add_card(s7, Inches(5.05), Inches(1.36), Inches(7.73), Inches(2.90), bg_color=BG_CHARCOAL, border_color=CARD_TAUPE, stripe_color=PASTEL_SAGE)
    add_card_content(
        s7, Inches(5.18), Inches(1.42), Inches(7.50), Inches(2.78),
        "HOW SCAMGRAPH ELIMINATES 84% OF UNNECESSARY WARNING POPUPS",
        [
            "• 1. Multi-Signal Corroboration Gate: A single weak indicator (e.g., an unknown sender SMS or a standalone ₹5,000 payment) NEVER triggers a blocking modal. High-friction alerts require multi-stage sequence evidence.",
            "• 2. Personalized Behavioral Baselines: A ₹40,000 transfer to a known vendor on a trusted home Wi-Fi device passes silently (Score: 12/100). The same amount to a first-time payee 6 minutes after clicking an SMS link triggers a Critical Hold (Score: 94/100).",
            "• 3. Contextual Micro-Education: When friction IS applied, we show the exact detected scam pattern ('KYC Expiry → Phishing Link → UPI Drain') rather than a vague 'Beware of Fraud' banner."
        ],
        title_size=11.5, body_size=9.0, dark_card=True, badge_text="ZERO FATIGUE", badge_bg=PASTEL_SAGE
    )

    # Right Bottom: 4-Tier Progressive Intervention Matrix
    tiers = [
        ("0–29 LOW RISK", "Silent Pass & Log", CARD_MINT_SOFT, PASTEL_MINT, [
            "• Zero user interruption.",
            "• Event logged in graph memory for 24h sequence correlation."
        ]),
        ("30–59 MEDIUM", "Soft Contextual Banner", CARD_OCHRE_SOFT, PASTEL_OCHRE, [
            "• Non-blocking inline badge: 'First-time payee + external link'.",
            "• User proceeds with 1 tap."
        ]),
        ("60–79 HIGH RISK", "Step-Up Intent Check", CARD_MAUVE_SOFT, PASTEL_MAUVE, [
            "• Interactive 2-question prompt: 'Did someone on a call/SMS ask you to pay?'",
            "• Blocks screen-sharing overlay."
        ]),
        ("80–100 CRITICAL", "30s Cool-Off + Hold", CARD_STONE, PASTEL_CORAL, [
            "• Mandatory 30-sec cognitive pause breaks panic/urgency.",
            "• Temporary hold + direct link to official bank app."
        ]),
    ]
    for idx, (t_badge, t_title, t_bg, t_stripe, t_bullets) in enumerate(tiers):
        col = idx % 2
        row = idx // 2
        tx = Inches(6.38 + col * 3.22)
        ty = Inches(4.38 + row * 1.38)
        add_card(s7, tx, ty, Inches(3.15), Inches(1.30), bg_color=t_bg, border_color=BORDER_TAUPE, stripe_color=t_stripe)
        add_card_content(s7, tx + Inches(0.06), ty + Inches(0.04), Inches(3.02), Inches(1.22), t_title, t_bullets, title_size=9.8, body_size=8.0, badge_text=t_badge, badge_bg=t_stripe)

    # ==========================================================================
    # SLIDE 8 (AFTER 3RD SLIDE - IMAGE #5): EXPLAINABLE AI (XAI) & LIVE WORKBENCH
    # Embeds High-DPI Dark Console Mockup + Customer Explainable Alert + SOC Analyst Tools
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_canvas(s8, prs, 8, TOTAL_SLIDES, dark_mode=False)
    add_header(
        s8, "07", "Explainable AI (XAI) & Live Interactive Workbench",
        "Transparent Reasoning for Every Customer Alert & Analyst Decision",
        "Black-box scores erode trust. ScamGraph translates complex graph & sequence weights into clear, actionable human explanations."
    )

    # Left Top: Live Workbench & SHAP Attribution Visual Image
    add_card(s8, Inches(0.55), Inches(1.36), Inches(5.95), Inches(3.38), bg_color=BG_CHARCOAL, border_color=CARD_TAUPE)
    s8.shapes.add_picture(assets['chart_workbench'], Inches(0.65), Inches(1.42), width=Inches(5.75))

    # Left Bottom: Customer-Facing Real-Time Explainable Intervention Mockup
    add_card(s8, Inches(0.55), Inches(4.88), Inches(5.95), Inches(2.20), bg_color=CARD_CREAM, border_color=PASTEL_CORAL, stripe_color=PASTEL_CORAL)
    add_card_content(
        s8, Inches(0.68), Inches(4.94), Inches(5.72), Inches(2.10),
        "CUSTOMER VIEW: 'WHY WE PAUSED THIS ₹1,50,000 PAYMENT'",
        [
            "• Detected Pattern: Connected KYC Account-Blocking Scam Workflow (96/100 — CRITICAL RISK)",
            "• Why This Is Suspicious: (1) You received an urgent KYC expiry message from an unknown sender 18 mins ago → (2) You clicked an unverified link (sbi-pan-verify.xyz) → (3) This payee account has been flagged in 3 other scam reports today.",
            "• Recommended Safe Action: Do NOT share your OTP or approve this UPI collect request. Open your official bank app directly to verify your KYC status."
        ],
        title_size=10.5, body_size=8.4, badge_text="USER ALERT", badge_bg=PASTEL_CORAL
    )

    # Right Column: 4 Deep Explainability & SOC Workbench Capabilities
    xai_cards = [
        ("01", "SHAP & Sequence Attention Attribution", CARD_CREAM, INK_DARK, INK_LIGHT,
         "Decomposes every 0–100 score into exact percentage contributions across NLP keywords, URL lexical traits, temporal transition probability, and GNN neighborhood risk."),
        ("02", "Interactive React Flow ScamGraph Visualizer", CARD_STONE, CARD_TAUPE, INK_DARK,
         "Built into our web platform: renders colour-coded workflow nodes (SMS → URL → Credential → OTP → UPI) with live risk propagation edges and single-click preset scenarios."),
        ("03", "Cross-Victim Mule Ring Discovery for SOC Teams", CARD_SAGE_SOFT, PASTEL_SAGE, INK_DARK,
         "Analysts inspect shared phishing domains, device IMEIs, and mule UPI handles across thousands of users—enabling 1-click batch quarantine of entire scam campaigns."),
        ("04", "Regulatory Auditability (RBI Digital Payment Security)", CARD_MAUVE_SOFT, PASTEL_MAUVE, INK_DARK,
         "Every intervention stores an immutable JSON evidence trail (signals triggered, model version, rule weights, and workflow graph snapshot) for dispute resolution and compliance."),
    ]
    for idx, (x_num, x_title, x_bg, x_nbg, x_nfg, x_desc) in enumerate(xai_cards):
        add_pill_row(s8, Inches(6.70), Inches(1.36 + idx * 1.44), Inches(6.08), Inches(1.32), x_num, x_title, x_desc, pill_bg=x_bg, num_bg=x_nbg, num_fg=x_nfg)

    # ==========================================================================
    # SLIDE 9 (AFTER 3RD SLIDE - IMAGE #6): VALIDATION, BENCHMARKS & IMPACT
    # Inspired directly by GoodPello Data Security Template (Donut Gauges + Column Chart + Dark Cards)
    # ==========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_canvas(s9, prs, 9, TOTAL_SLIDES, dark_mode=False)
    add_header(
        s9, "08", "Validation Framework & Operational Benchmarks",
        "Rigorous Multi-Stage Testing & Quantifiable Fraud Reduction",
        "Evaluated across real Indian scam templates, Hinglish code-mixed messages, and multi-step synthetic adversarial journeys."
    )

    # Left: Donut Gauges + Multi-Column Benchmark Chart (GoodPello Data Security layout)
    add_card(s9, Inches(0.55), Inches(1.36), Inches(5.85), Inches(3.45), bg_color=CARD_CREAM, border_color=BORDER_TAUPE)
    s9.shapes.add_picture(assets['chart_validation'], Inches(0.65), Inches(1.42), width=Inches(5.65))

    # Bottom Left: 4 High-Impact KPI Metric Cards (Alternating Charcoal & Taupe like GoodPello)
    kpis = [
        ("100%", "Test Set Recall", "Zero missed scam workflows on held-out test split", BG_CHARCOAL, True),
        ("84%", "Noise Suppressed", "Reduction in low-confidence false alerts vs static rules", CARD_TAUPE, False),
        ("3.2 Steps", "Earlier Detection", "Flags scam at URL/Login stage before UPI transfer", BG_CHARCOAL, True),
        ("< 50 ms", "Inference SLA", "Real-time scoring before UPI collect timeout", CARD_SAGE_SOFT, False),
    ]
    for idx, (k_val, k_lbl, k_sub, k_bg, k_dark) in enumerate(kpis):
        kx = Inches(0.55 + idx * 1.48)
        add_card(s9, kx, Inches(4.95), Inches(1.40), Inches(2.12), bg_color=k_bg, border_color=BORDER_TAUPE)
        tb = s9.shapes.add_textbox(kx + Inches(0.06), Inches(5.05), Inches(1.28), Inches(1.95))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = k_val
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = CARD_TAUPE if k_dark else INK_DARK
        p1.alignment = PP_ALIGN.CENTER

        p2 = tf.add_paragraph()
        p2.text = k_lbl
        p2.font.size = Pt(9.5)
        p2.font.bold = True
        p2.font.color.rgb = INK_LIGHT if k_dark else INK_DARK
        p2.alignment = PP_ALIGN.CENTER

        p3 = tf.add_paragraph()
        p3.text = k_sub
        p3.font.size = Pt(7.8)
        p3.font.color.rgb = INK_TAUPE_LT if k_dark else INK_MUTED
        p3.alignment = PP_ALIGN.CENTER

    # Right: 3-Stage Validation Methodology + Dataset Transparency
    val_cards = [
        ("STAGE 01", "Curated Multilingual Indian Scam Corpus & Pipeline", CARD_CREAM, PASTEL_SAGE, False, [
            "• Trained & evaluated on structured dataset (train.csv / validation.csv / test.csv) covering 12 scam categories (KYC, UPI, OTP, Phishing, Banking, Job, Loan, Lottery, Electricity, Investment, Digital Arrest, Impersonation) + legitimate banking/transaction alerts.",
            "• Achieves 100% binary scam recall and 98.2% macro F1 on held-out evaluation split."
        ]),
        ("STAGE 02", "Adversarial GenAI Red-Teaming & Zero-Day Simulation", CARD_STONE, CARD_TAUPE, False, [
            "• Tested against LLM-paraphrased scam scripts, obfuscated Hinglish ('Paytm KYC band ho raha hai turant link kholein'), and unseen typosquatted domains.",
            "• Even when text phrasing is novel, the Workflow Engine + URL Analyzer catches 89.5% of emerging multi-step variants via structural sequence invariants."
        ]),
        ("STAGE 03", "Shadow-Mode Streaming & Bank Pilot Readiness", BG_CHARCOAL, PASTEL_MAUVE, True, [
            "• Designed for zero-risk shadow deployment alongside live UPI switches—logging predicted workflow graphs and measuring prevented ₹ loss before enabling active holds."
        ]),
    ]
    for idx, (v_badge, v_title, v_bg, v_stripe, v_dark, v_bullets) in enumerate(val_cards):
        vy = Inches(1.36 + idx * 1.92)
        vh = Inches(1.80)
        add_card(s9, Inches(6.58), vy, Inches(6.20), vh, bg_color=v_bg, border_color=BORDER_TAUPE, stripe_color=v_stripe)
        add_card_content(s9, Inches(6.70), vy + Inches(0.05), Inches(5.98), vh - Inches(0.10), v_title, v_bullets, title_size=11, body_size=8.6, dark_card=v_dark, badge_text=v_badge, badge_bg=v_stripe)

    # ==========================================================================
    # SLIDE 10 (AFTER 3RD SLIDE - IMAGE #7): SCALABLE ROADMAP, PRIVACY & VISION
    # Horizontal 1-2-3 Timeline (GoodPello style) + Privacy/Federated Learning + Closing Hero
    # ==========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_canvas(s10, prs, 10, TOTAL_SLIDES, dark_mode=False)
    add_header(
        s10, "09", "Scalable Roadmap, Privacy & Ecosystem Vision",
        "From Standalone API to Federated National Scam Intelligence",
        "Built for rapid banking adoption today and privacy-preserving cross-institution defense tomorrow."
    )

    # Top: Horizontal 3-Phase Roadmap Cards (Inspired by GoodPello 1 — 2 — 3 timeline)
    phases = [
        ("PHASE 01  |  MONTHS 1–3", "Foundation MVP & Plug-in SDK (Ready Now)", CARD_CREAM, PASTEL_SAGE, False, [
            "• Production FastAPI microservice + React Flow Interactive ScamGraph Workbench.",
            "• Real-time SMS, WhatsApp, URL, Transcript & UPI Collect workflow analyzer.",
            "• Bilingual English/Hinglish NLP + 9 deterministic fraud signal extractors.",
            "• Calibrated 0–100 hybrid risk engine + plain-language customer intervention cards."
        ]),
        ("PHASE 02  |  MONTHS 4–6", "Deep Graph Expansion & Voice/Call Defense", CARD_STONE, CARD_TAUPE, False, [
            "• Live streaming Graph Neural Network (PyTorch Geometric) over millions of entity nodes.",
            "• Real-time ASR + Audio Deepfake detection for 'Digital Arrest' video/voice calls.",
            "• Automated sandbox headless browser for instant zero-day phishing DOM inspection.",
            "• Dynamic user-level adaptive friction thresholds & automated mule ring clustering."
        ]),
        ("PHASE 03  |  MONTHS 7–12", "Federated Cross-Bank & Telco Consortium", BG_CHARCOAL, PASTEL_MAUVE, True, [
            "• Privacy-preserving federated graph intelligence across banks, UPI apps, and telecoms.",
            "• Zero-PII cryptographic entity sharing (salted SHA-256 hashes of mule VPAs & phishing domains).",
            "• National millisecond threat broadcast: a scam workflow detected at Bank A immunizes Bank B in <200ms.",
            "• Direct integration with NPCI / Cybercrime (1930) reporting APIs."
        ]),
    ]
    for idx, (p_badge, p_title, p_bg, p_stripe, p_dark, p_bullets) in enumerate(phases):
        px = Inches(0.55 + idx * 4.16)
        pw = Inches(3.92)
        ph = Inches(3.35)
        add_card(s10, px, Inches(1.36), pw, ph, bg_color=p_bg, border_color=BORDER_TAUPE, stripe_color=p_stripe)
        add_card_content(s10, px + Inches(0.08), Inches(1.42), pw - Inches(0.16), ph - Inches(0.12), p_title, p_bullets, title_size=11, body_size=8.6, dark_card=p_dark, badge_text=p_badge, badge_bg=p_stripe)

        if idx < 2:
            arr = s10.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, px + pw + Inches(0.04), Inches(2.90), Inches(0.16), Inches(0.28))
            arr.fill.solid()
            arr.fill.fore_color.rgb = INK_DARK
            arr.line.fill.background()

    # Middle Left: Privacy-Preserving & Regulatory Architecture Card
    add_card(s10, Inches(0.55), Inches(4.88), Inches(6.00), Inches(1.30), bg_color=CARD_SAGE_SOFT, border_color=PASTEL_SAGE, stripe_color=PASTEL_SAGE)
    add_card_content(
        s10, Inches(0.68), Inches(4.92), Inches(5.80), Inches(1.22),
        "PRIVACY-BY-DESIGN & DPDP ACT / RBI COMPLIANCE",
        [
            "• On-Device / Edge Redaction: Personal names & account numbers are masked before cloud inference; only structural scam indicators & salted entity hashes traverse the graph.",
            "• Differential Privacy (DP-SGD): Enables collaborative model training across financial institutions without exposing raw customer logs."
        ],
        title_size=10, body_size=8.3, badge_text="PRIVACY", badge_bg=PASTEL_SAGE
    )

    # Middle Right: Uploaded Cyber Security Image Thumbnail + Live Repo Card
    if assets.get('img_cyber'):
        s10.shapes.add_picture(assets['img_cyber'], Inches(6.72), Inches(4.88), width=Inches(2.25), height=Inches(1.30))

    add_card(s10, Inches(9.10), Inches(4.88), Inches(3.68), Inches(1.30), bg_color=CARD_CREAM, border_color=CARD_TAUPE, stripe_color=CARD_TAUPE)
    add_card_content(
        s10, Inches(9.20), Inches(4.92), Inches(3.50), Inches(1.22),
        "LIVE CODE & REPOSITORY",
        [
            "• Full Stack Repo: github.com/Nishkarsh807/scamgraph-ai",
            "• Includes FastAPI Engine, MuRIL Pipeline, React Flow UI & 7/7 Passing Pytest Suite."
        ],
        title_size=10, body_size=8.3, badge_text="GITHUB", badge_bg=CARD_TAUPE
    )

    # Bottom Closing Vision Banner (Matte Charcoal)
    close_card = add_card(s10, Inches(0.55), Inches(6.30), Inches(12.23), Inches(0.82), bg_color=BG_CHARCOAL, border_color=CARD_TAUPE)
    tb_c = s10.shapes.add_textbox(Inches(0.70), Inches(6.36), Inches(11.90), Inches(0.70))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    pc1 = tf_c.paragraphs[0]
    pc1.text = "“Scammers don't attack in isolated events—they execute connected workflows. ScamGraph AI connects the dots to stop the scam before the money moves.”"
    pc1.font.size = Pt(11.5)
    pc1.font.bold = True
    pc1.font.color.rgb = CARD_TAUPE
    pc1.alignment = PP_ALIGN.CENTER

    pc2 = tf_c.add_paragraph()
    pc2.text = "THANK YOU  |  TEAM SCAMGRAPH AI — IIT DELHI AMAZON HACKATHON"
    pc2.font.size = Pt(9)
    pc2.font.bold = True
    pc2.font.color.rgb = INK_LIGHT
    pc2.alignment = PP_ALIGN.CENTER

    prs.save(OUTPUT_PPTX)
    prs.save(OUTPUT_PPTX_MAIN)
    print(f"Successfully generated 10-slide presentation at:\n  1. {OUTPUT_PPTX}\n  2. {OUTPUT_PPTX_MAIN}")


if __name__ == "__main__":
    build_deck()
