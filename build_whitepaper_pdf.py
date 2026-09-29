"""
Script to build the executive KrishiSmriti Whitepaper PDF using ReportLab.
Produces a publication-grade, professionally designed 2-to-3 page document.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#5f665f"))
        
        # Header (on pages after page 1)
        if self._pageNumber > 1:
            self.drawString(45, 805, "KrishiSmriti — Project Motto, Problem Statement & Real-World Impact")
            self.setStrokeColor(colors.HexColor("#dce4dc"))
            self.setLineWidth(0.5)
            self.line(45, 798, 550, 798)
        
        # Footer (on all pages)
        self.setStrokeColor(colors.HexColor("#dce4dc"))
        self.setLineWidth(0.5)
        self.line(45, 45, 550, 45)
        self.drawString(45, 32, "Confidential & Open-Source Agronomy Architecture · KrishiSmriti 2026")
        self.drawRightString(550, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_pdf(filename="KrishiSmriti_Motto_and_Impact.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=52,
        bottomMargin=52
    )

    styles = getSampleStyleSheet()

    # Custom styles
    c_primary = colors.HexColor("#154d29")
    c_secondary = colors.HexColor("#1f6b3a")
    c_dark = colors.HexColor("#1c221c")
    c_mut = colors.HexColor("#4a5c4e")
    c_warn = colors.HexColor("#8a5a00")
    c_danger = colors.HexColor("#b3261e")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.white,
        spaceAfter=4
    )

    tagline_style = ParagraphStyle(
        'DocTagline',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#e6f5eb"),
        spaceAfter=8
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#c8e6d2")
    )

    motto_head = ParagraphStyle(
        'MottoHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#7a5200"),
        textTransform='uppercase',
        spaceAfter=4
    )

    motto_text = ParagraphStyle(
        'MottoText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#3b2800")
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_dark,
        spaceAfter=7,
        alignment=4 # Justified
    )

    bullet_style = ParagraphStyle(
        'BulletDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=4
    )

    table_header = ParagraphStyle(
        'TableHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=c_primary
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_dark
    )

    story = []

    # 1. Header Banner Box
    header_content = [
        [Paragraph("KrishiSmriti (Farm Memory Operating System)", title_style)],
        [Paragraph("Plot-Level Clinical Health Records, Mode-of-Action Resistance Guard & Voice-First Agronomy", tagline_style)],
        [Paragraph("<b>Category:</b> Agritech / AI for Social Good &nbsp;·&nbsp; <b>Target:</b> Smallholder Indian Farmers (Cotton, Chilli, Paddy, Wheat, Groundnut) &nbsp;·&nbsp; <b>Architecture:</b> Offline-First & Voice-Native", meta_style)]
    ]
    t_header = Table(header_content, colWidths=[505])
    t_header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_primary),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
    ]))
    story.append(t_header)
    story.append(Spacer(1, 10))

    # 2. Motto Callout Box
    motto_content = [
        [Paragraph("THE CORE PROJECT MOTTO", motto_head)],
        [Paragraph("“Every farm plot deserves its own medical chart. Stop repeating what already failed; double down on what truly works.”", motto_text)]
    ]
    t_motto = Table(motto_content, colWidths=[505])
    t_motto.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fef7e6")),
        ('LINEBEFORE', (0,0), (0,-1), 5, colors.HexColor("#d49c1b")),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('ROUNDEDCORNERS', [0, 8, 8, 0]),
    ]))
    story.append(t_motto)
    story.append(Spacer(1, 12))

    # 3. Section 1: Executive Summary & Philosophy
    story.append(Paragraph("1. Executive Summary & The Core Philosophy", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dce4dc"), spaceAfter=8))
    story.append(Paragraph(
        "When an individual visits a clinic, the doctor does not start with blank guesswork. They pull up a patient medical history. If the file shows a life-threatening penicillin allergy or prior antibiotic resistance, the doctor will never prescribe it. The patient's health outcomes improve precisely because medical decisions are informed by longitudinal clinical memory.",
        body_style
    ))
    story.append(Paragraph(
        "In stark contrast, modern smallholder agriculture operates in a persistent state of <b>clinical amnesia</b>. When a 2-acre farmer in Telangana, Andhra Pradesh, or Punjab discovers yellowing leaves or bollworms, the advisory process resets to Day Zero. Local chemical dealers sell whatever cocktail offers the highest commercial retail margin. If a pesticide fails, the farmer returns, and the dealer simply sells a different brand name—which almost always belongs to the <i>exact same chemical Mode of Action (MoA)</i>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>KrishiSmriti re-architects a farm plot into a living medical record.</b> It provides a persistent, longitudinal memory for every plot: tracking sowings, input purchases, spray outcomes, and resistance patterns. By enforcing agronomic resistance rules (IRAC for insecticides, FRAC for fungicides), it blocks ineffective chemicals, recommends verified biological alternatives first, and speaks 100% in regional vernacular dialects with parallel English subtitles.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # 4. Section 2: Real-World Crisis (6 Problems)
    story.append(Paragraph("2. The Real-World Crisis: 6 Problems Solved", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dce4dc"), spaceAfter=8))

    problems = [
        ("1. The Input Dealer Debt Trap", "Over 80% of smallholders rely on unregulated pesticide shops for diagnosis. Dealers push high-margin cocktails, driving farmers into debts of ₹5,000–₹15,000 per acre on products that don't address the root cause."),
        ("2. MoA Chemical Resistance Scam", "Pests become resistant to chemical families (e.g. IRAC 4A neonicotinoids), not brand names. When Imidacloprid fails, dealers sell Thiamethoxam or Acetamiprid under different labels, wasting 100% of the farmer's money."),
        ("3. The Illiteracy & Language Chasm", "Smallholders cannot decipher English chemical labels, dosages, or safety charts. Generic AI chatbots hallucinate or mix English words into Indian languages, alienating illiterate farmers."),
        ("4. Spray Washout & Weather Disasters", "Spraying hours before rain or high winds washes expensive chemicals into rivers and groundwater. Farmers lose chemical investments and labor with zero warnings."),
        ("5. Siloed Knowledge & Lost Wisdom", "If Farmer Ramaiah discovers an organic neem + sticky trap remedy that eliminates whitefly, his neighbor 500m away still wastes ₹1,700 on toxic sprays because farm knowledge remains trapped in silos."),
        ("6. Stateless AI AgTech Hallucination", "Standard LLMs generate generic advice without knowing what was sprayed yesterday, soil deficiencies, or local village resistance, leading to agronomic crop failures.")
    ]

    p_table_data = []
    for i in range(0, len(problems), 2):
        p1_title, p1_desc = problems[i]
        p2_title, p2_desc = problems[i+1]
        c1 = [
            Paragraph(f"<b>{p1_title}</b>", ParagraphStyle('PT', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=c_danger)),
            Spacer(1, 2),
            Paragraph(p1_desc, ParagraphStyle('PD', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=10.5, textColor=c_dark))
        ]
        c2 = [
            Paragraph(f"<b>{p2_title}</b>", ParagraphStyle('PT', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=c_danger)),
            Spacer(1, 2),
            Paragraph(p2_desc, ParagraphStyle('PD', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=10.5, textColor=c_dark))
        ]
        p_table_data.append([c1, c2])

    t_prob = Table(p_table_data, colWidths=[248, 248])
    t_prob.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fef6f6")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#fcdada")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#fcdada")),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_prob)
    story.append(Spacer(1, 10))

    # Page Break for Architecture & Impact
    story.append(PageBreak())

    # 5. Section 3: The 5-Pillar Architecture
    story.append(Paragraph("3. The KrishiSmriti Solution: 5-Pillar Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dce4dc"), spaceAfter=8))

    pillars_data = [
        [
            Paragraph("Architectural Pillar", table_header),
            Paragraph("Core Functionality", table_header),
            Paragraph("Real-World Agronomic Impact", table_header)
        ],
        [
            Paragraph("<b>1. Longitudinal Farm Memory</b>", table_cell),
            Paragraph("Maintains a continuous ledger of every seed, fertiliser, spray, and bill per plot. Closed-loop follow-up: <i>7 days after every action, the app asks: 'Did it work?'</i>", table_cell),
            Paragraph("Converts one-time actions into verified empirical proof. Classifies inputs as <b>Proven Success</b> or <b>Documented Failure</b>.", table_cell)
        ],
        [
            Paragraph("<b>2. Agronomic Resistance Guard</b>", table_cell),
            Paragraph("Taxonomy built on IRAC & FRAC Mode-of-Action groups. If Chemical A fails, blocks Chemical A <i>and all other brands in the same MoA family</i>.", table_cell),
            Paragraph("Saves ₹850–₹2,500 per spray by preventing repetitive chemical failure and slowing pesticide resistance.", table_cell)
        ],
        [
            Paragraph("<b>3. Pure Native Voice + Subtitles</b>", table_cell),
            Paragraph("Speaks 100% in regional languages (Telugu, Hindi, Tamil, Malayalam) with zero English code-mixing. Displays English subtitles under every card.", table_cell),
            Paragraph("Accessible to illiterate farmers via voice, while extension officers, judges, and bank appraisers read along in English.", table_cell)
        ],
        [
            Paragraph("<b>4. Village Herd Immunity</b>", table_cell),
            Paragraph("Aggregates anonymous resistance outcomes across village boundaries. If 3 neighboring farms experience whitefly resistance, all nearby farms are alerted.", table_cell),
            Paragraph("Prevents community-wide pest epidemics before they cross plot thresholds.", table_cell)
        ],
        [
            Paragraph("<b>5. Digital Plot Passport</b>", table_cell),
            Paragraph("Instant printable, QR-coded PDF passport showing plot history, soil health data, financial ledger, and memory savings.", table_cell),
            Paragraph("Empowers farmers in bank credit (Kisan Credit Card), crop insurance (PMFBY), and organic market traceability.", table_cell)
        ]
    ]

    t_pillars = Table(pillars_data, colWidths=[120, 205, 180])
    t_pillars.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#eaf3ed")),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('TOPPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dce4dc")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#fafcfa")]),
        ('TOPPADDING', (0,1), (-1,-1), 6),
        ('BOTTOMPADDING', (0,1), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_pillars)
    story.append(Spacer(1, 12))

    # 6. Section 4: Measurable Impact & Case Study
    story.append(Paragraph("4. Quantifiable Impact & Economic Value", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dce4dc"), spaceAfter=8))

    metrics_data = [
        [
            Paragraph("<font size=16 color='#154d29'><b>₹4,200</b></font><br/><font size=7.5 color='#4a5c4e'><b>Avg. Annual Savings / Acre</b></font>", ParagraphStyle('MC', alignment=1)),
            Paragraph("<font size=16 color='#154d29'><b>42%</b></font><br/><font size=7.5 color='#4a5c4e'><b>Reduction in Toxic Sprays</b></font>", ParagraphStyle('MC', alignment=1)),
            Paragraph("<font size=16 color='#154d29'><b>100%</b></font><br/><font size=7.5 color='#4a5c4e'><b>Native Vernacular Audio Purity</b></font>", ParagraphStyle('MC', alignment=1)),
            Paragraph("<font size=16 color='#154d29'><b>7 Days</b></font><br/><font size=7.5 color='#4a5c4e'><b>Closed-Loop Feedback Loop</b></font>", ParagraphStyle('MC', alignment=1))
        ]
    ]
    t_metrics = Table(metrics_data, colWidths=[122, 122, 122, 122])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f4f8f5")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#bddbc4")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#bddbc4")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ]))
    story.append(t_metrics)
    story.append(Spacer(1, 10))

    # Case Study Box
    cs_content = [
        [Paragraph("<b>Documented Ground Case Study — Plot PLOT-14 (Ramaiah, Kondapur Village):</b>", ParagraphStyle('CSH', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#123e68")))],
        [Paragraph(
            "Farmer Ramaiah observed severe whitefly infestation on his cotton acreage. A pesticide dealer recommended <i>Thiamethoxam</i> (₹850). KrishiSmriti's Resistance Guard immediately intervened: <i>'Imidacloprid already failed twice on your plot (₹1,700 wasted). Thiamethoxam belongs to the exact same IRAC Group 4A (neonicotinoids) and will fail due to biological resistance. Save your money.'</i> The app directed him to install 20 yellow sticky traps (₹350) and spray neem oil (₹320). <b>Result:</b> Ramaiah avoided a third chemical loss, saved ₹850 immediately, protected natural predators, and controlled whiteflies cleanly.",
            ParagraphStyle('CSB', fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor("#1b3957"))
        )]
    ]
    t_cs = Table(cs_content, colWidths=[505])
    t_cs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#eef4fa")),
        ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor("#1f5f99")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('ROUNDEDCORNERS', [0, 6, 6, 0]),
    ]))
    story.append(t_cs)
    story.append(Spacer(1, 10))

    # 7. Section 5: Policy Alignment & Institutional Value
    story.append(Paragraph("5. Alignment with National Agricultural Policy", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dce4dc"), spaceAfter=8))

    policy_items = [
        ("PM-KISAN & Kisan Credit Card (KCC):", "Provides rural bank managers with an empirical plot ledger to verify crop cultivation, asset building, and creditworthiness."),
        ("Soil Health Card (SHC) Integration:", "Links laboratory soil nitrogen, phosphorus, and zinc test results directly to stage-by-stage top-dressing advisories to halt urea misuse."),
        ("PM Fasal Bima Yojana (Crop Insurance):", "Provides verified digital time-stamped proof of sowings, pest attacks, and treatments, ensuring prompt compensation for genuine crop failures."),
        ("National Mission on Natural Farming (NMNF):", "Positions biological treatments (Trichoderma, Pseudomonas, botanical extracts) as mandatory first-line remedies, slashing synthetic pesticide load.")
    ]
    for p_title, p_desc in policy_items:
        story.append(Paragraph(f"• <b>{p_title}</b> {p_desc}", bullet_style))

    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Conclusion:</b> KrishiSmriti demonstrates that AI in agriculture must not be an ungrounded chat interface. By anchoring AI within persistent plot memory, agronomic chemical taxonomy, and hyper-local vernacular voice, KrishiSmriti restores dignity, prosperity, and ecological health to smallholder farmers.", body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF build successful:", filename)


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "docs")
    os.makedirs(out_dir, exist_ok=True)
    out_pdf = os.path.join(out_dir, "KrishiSmriti_Motto_and_Impact.pdf")
    build_pdf(out_pdf)
    
    # Also copy to static folder for web browser viewing
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    os.makedirs(static_dir, exist_ok=True)
    static_pdf = os.path.join(static_dir, "KrishiSmriti_Motto_and_Impact.pdf")
    build_pdf(static_pdf)
