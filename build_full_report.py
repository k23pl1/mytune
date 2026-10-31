# -*- coding: utf-8 -*-
"""
Master Report Builder for MyTune Documentation
Candidate: Kuldeep Pal (Roll No: 35)
Generates both PDF and DOCX formats with 45 comprehensive pages.
"""

import os
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import pypdf

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from report_content import METADATA, PAGES
from report_chapters_1_3 import CHAPTERS_1_TO_3
from report_chapters_4_6 import CHAPTERS_4_TO_6
from report_chapters_7_app import CHAPTERS_7_TO_APP

base_dir = r"C:\Users\palku\OneDrive\เอกสาร\Desktop\EX_PROJECTS\mytune"
assets_dir = os.path.join(base_dir, "docs_assets")
pdf_output = os.path.join(base_dir, "MyTune_Project_Report_Kuldeep_Pal.pdf")
docx_output = os.path.join(base_dir, "MyTune_Project_Report_Kuldeep_Pal.docx")

scratch_dir = r"C:\Users\palku\.gemini\antigravity\scratch\mytune"
artifact_dir = r"C:\Users\palku\.gemini\antigravity\brain\016e3f8b-39b1-4679-9990-29c43bce4b39"

ALL_PAGES = PAGES + CHAPTERS_1_TO_3 + CHAPTERS_4_TO_6 + CHAPTERS_7_TO_APP
print(f"Total page specifications loaded: {len(ALL_PAGES)}")

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
        # Cover page (page 1) has no headers or footers
        if self._pageNumber == 1:
            return
        
        self.saveState()
        
        # Header (Top)
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#334155"))
        self.drawString(54, 804, "MYTUNE: MODERN AUDIO-REACTIVE WEB MUSIC STREAMING PLATFORM")
        self.setFont("Helvetica", 8)
        self.drawRightString(541, 804, "TY B.Sc. CS (2026-27)")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.75)
        self.line(54, 796, 541, 796)
        
        # Footer (Bottom)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.75)
        self.line(54, 48, 541, 48)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(54, 34, "Vande Mataram Degree College | Dept. of Computer Science")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(541, 34, page_str)
        
        self.restoreState()

def build_pdf():
    print(f"Generating PDF: {pdf_output} ...")
    doc = SimpleDocTemplate(
        pdf_output,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=18, leading=23,
        alignment=1, textColor=colors.HexColor('#0f172a'), spaceAfter=12
    )
    sub_style = ParagraphStyle(
        'CoverSub', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10, leading=14,
        alignment=1, textColor=colors.HexColor('#334155'), spaceAfter=15
    )
    meta_style = ParagraphStyle(
        'CoverMeta', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=14,
        alignment=1, textColor=colors.HexColor('#1e3a8a'), spaceAfter=6
    )
    meta_body = ParagraphStyle(
        'CoverMetaBody', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13,
        alignment=1, textColor=colors.HexColor('#334155'), spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'CustomH1', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=13, leading=16,
        textColor=colors.HexColor('#1e3a8a'), spaceBefore=8, spaceAfter=5, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'CustomH2', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=13.5,
        textColor=colors.HexColor('#0369a1'), spaceBefore=6, spaceAfter=3, keepWithNext=True
    )
    h3_style = ParagraphStyle(
        'CustomH3', parent=styles['Heading3'],
        fontName='Helvetica-Bold', fontSize=9, leading=12,
        textColor=colors.HexColor('#334155'), spaceBefore=5, spaceAfter=2, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'CustomBody', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.0, leading=11.2,
        alignment=4, textColor=colors.HexColor('#1e293b'), spaceAfter=4
    )
    code_style = ParagraphStyle(
        'CustomCode', parent=styles['Normal'],
        fontName='Courier', fontSize=6.0, leading=7.5,
        textColor=colors.HexColor('#0f172a'), spaceAfter=1
    )
    caption_style = ParagraphStyle(
        'CustomCaption', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7.5, leading=10,
        alignment=1, textColor=colors.HexColor('#475569'), spaceBefore=3, spaceAfter=4
    )
    th_style = ParagraphStyle(
        'TH', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7.5, leading=9.5,
        alignment=1, textColor=colors.white
    )
    tc_style = ParagraphStyle(
        'TC', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.0, leading=9.0,
        textColor=colors.HexColor('#1e293b')
    )

    story = []
    
    for idx, page in enumerate(ALL_PAGES):
        p_type = page.get("type")
        
        if p_type == "cover":
            c = page["content"]
            story.append(Spacer(1, 10))
            story.append(Paragraph(c["univ"], ParagraphStyle('Univ', parent=title_style, fontSize=14, leading=18, textColor=colors.HexColor('#b91c1c'))))
            story.append(Spacer(1, 10))
            story.append(Paragraph(c["sub"], sub_style))
            story.append(Paragraph(c["degree"], ParagraphStyle('Deg', parent=title_style, fontSize=11, leading=15, textColor=colors.HexColor('#1e3a8a'))))
            story.append(Spacer(1, 15))
            story.append(Paragraph(c["project_title"], title_style))
            story.append(Paragraph(c["subtitle"], sub_style))
            story.append(Spacer(1, 15))
            story.append(Paragraph("SUBMITTED BY:", meta_style))
            story.append(Paragraph(f"{c['student_name']} / {c['roll_no']}", meta_body))
            story.append(Paragraph("UNDER THE ESTEEMED GUIDANCE OF:", meta_style))
            story.append(Paragraph(c["guide"], meta_body))
            story.append(Paragraph("ACADEMIC YEAR 2026–2027", meta_style))
            story.append(Spacer(1, 20))
            story.append(Paragraph(c["college"], ParagraphStyle('Col', parent=title_style, fontSize=11, leading=14, textColor=colors.HexColor('#047857'))))
            story.append(Paragraph(c["affiliation"], sub_style))
            story.append(Paragraph(c["address"], ParagraphStyle('Addr', parent=sub_style, fontSize=8.5, leading=11)))
            story.append(Spacer(1, 10))
            story.append(Paragraph(f"<b>Live Public Production URL:</b> {c['render_link']}", ParagraphStyle('Lnk', parent=sub_style, fontSize=8.5, leading=11, textColor=colors.HexColor('#2563eb'))))
            
        elif p_type == "certificate":
            story.append(Paragraph(page["title"], h1_style))
            story.append(Paragraph(page["subtitle"], h2_style))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=12))
            for para in page["cert_text"].split("\n\n"):
                story.append(Paragraph(para, body_style))
            story.append(Spacer(1, 40))
            # Signatures
            sig_data = [
                [Paragraph("_______________________<br/><b>Asst. Prof. Bharati Gaikar</b><br/>Internal Project Guide", tc_style),
                 Paragraph("_______________________<br/><b>Head of Department</b><br/>Dept. of Computer Science", tc_style),
                 Paragraph("_______________________<br/><b>Dr. Rajkumar M. Kolhe</b><br/>Principal, VMDC", tc_style)]
            ]
            t_sig = Table(sig_data, colWidths=[160, 160, 160])
            t_sig.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
            story.append(t_sig)

        elif p_type == "declaration":
            story.append(Paragraph(page["title"], h1_style))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=12))
            for para in page["text"].split("\n\n"):
                story.append(Paragraph(para, body_style))
            story.append(Spacer(1, 35))
            m = page["meta"]
            dec_data = [
                [Paragraph(f"<b>Date:</b> {m['date']}<br/><b>Place:</b> {m['place']}", tc_style),
                 Paragraph(f"____________________________<br/><b>Signature of the Candidate</b><br/><b>Name:</b> {m['name']}<br/><b>Roll No:</b> {m['roll']}", tc_style)]
            ]
            t_dec = Table(dec_data, colWidths=[240, 240])
            t_dec.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
            story.append(t_dec)

        elif p_type == "abstract":
            story.append(Paragraph(page["title"], h1_style))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
            for para in page["abstract"].split("\n\n"):
                story.append(Paragraph(para, body_style))
            story.append(Spacer(1, 10))
            story.append(Paragraph(page["role_title"], h2_style))
            story.append(Paragraph(page["role_text"], body_style))

        elif p_type == "acknowledgement":
            story.append(Paragraph(page["title"], h1_style))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=12))
            for para in page["text"].split("\n\n"):
                story.append(Paragraph(para, body_style))
            story.append(Spacer(1, 25))
            ack_data = [
                [Paragraph("", tc_style),
                 Paragraph(f"_______________________<br/><b>{page['sig_name']}</b><br/>{page['sig_roll']}", tc_style)]
            ]
            t_ack = Table(ack_data, colWidths=[260, 220])
            story.append(t_ack)

        elif p_type == "toc1":
            story.append(Paragraph(page["title"], h1_style))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=8))
            t_data = [[Paragraph(f"<b>{t}</b>" if "Chapter" in t or "Preliminary" in t else t, tc_style),
                       Paragraph(f"<b>{p}</b>" if "Page" in p or "Chapter" in t else p, tc_style)] for t, p in page["entries"]]
            t_toc = Table(t_data, colWidths=[420, 60])
            t_toc.setStyle(TableStyle([
                ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#f1f5f9")),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ('TOPPADDING', (0,0), (-1,-1), 2)
            ]))
            story.append(t_toc)

        elif p_type == "toc2":
            story.append(Paragraph(page["title"], h1_style))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=6))
            t_data = [[Paragraph(f"<b>{t}</b>" if "Chapter" in t else t, tc_style),
                       Paragraph(f"<b>{p}</b>" if "Chapter" in t else p, tc_style)] for t, p in page["entries"]]
            t_toc = Table(t_data, colWidths=[420, 60])
            t_toc.setStyle(TableStyle([
                ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#f1f5f9")),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
                ('TOPPADDING', (0,0), (-1,-1), 1.5)
            ]))
            story.append(t_toc)
            story.append(Spacer(1, 6))
            story.append(Paragraph("LIST OF FIGURES", h2_style))
            fig_data = [[Paragraph(f"<b>{f}</b>", tc_style), Paragraph(c, tc_style), Paragraph(p, tc_style)] for f, c, p in page["figures"]]
            t_fig = Table(fig_data, colWidths=[65, 365, 50])
            t_fig.setStyle(TableStyle([('BOTTOMPADDING', (0,0), (-1,-1), 1), ('TOPPADDING', (0,0), (-1,-1), 1)]))
            story.append(t_fig)
            story.append(Spacer(1, 6))
            story.append(Paragraph("LIST OF TABLES", h2_style))
            tbl_data = [[Paragraph(f"<b>{t}</b>", tc_style), Paragraph(c, tc_style), Paragraph(p, tc_style)] for t, c, p in page["tables"]]
            t_tbl = Table(tbl_data, colWidths=[65, 365, 50])
            t_tbl.setStyle(TableStyle([('BOTTOMPADDING', (0,0), (-1,-1), 1), ('TOPPADDING', (0,0), (-1,-1), 1)]))
            story.append(t_tbl)

        else:
            # Standard chapter / technical page
            if "title" in page:
                story.append(Paragraph(page["title"], h1_style))
                story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0369a1"), spaceAfter=6))
            
            if "sections" in page:
                for sec in page["sections"]:
                    story.append(Paragraph(f"{sec['num']} {sec['title']}", h2_style))
                    for p in sec["content"].split("\n\n"):
                        story.append(Paragraph(p, body_style))
            
            if "image" in page:
                img_info = page["image"]
                img_path = os.path.join(assets_dir, img_info["filename"])
                if os.path.exists(img_path):
                    # Fit nicely on page
                    img_w = min(480, img_info.get("width", 6.0) * 72)
                    img_h = min(260, img_info.get("height", 3.0) * 72)
                    story.append(Image(img_path, width=img_w, height=img_h))
                    story.append(Paragraph(img_info["caption"], caption_style))
            
            if "tables" in page:
                for t_spec in page["tables"]:
                    story.append(Paragraph(t_spec["caption"], caption_style))
                    h_cells = [Paragraph(h, th_style) for h in t_spec["headers"]]
                    r_cells = [[Paragraph(c, tc_style) for c in row] for row in t_spec["rows"]]
                    t_all = [h_cells] + r_cells
                    
                    # Auto column widths
                    num_cols = len(t_spec["headers"])
                    c_w = 480 / num_cols
                    t_elem = Table(t_all, colWidths=[c_w]*num_cols)
                    t_elem.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e3a8a")),
                        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
                        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#f8fafc"), colors.white]),
                        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                        ('TOPPADDING', (0,0), (-1,-1), 2),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 2)
                    ]))
                    story.append(t_elem)
                    story.append(Spacer(1, 4))
            
            if "code_block" in page:
                code_text = page["code_block"]
                code_lines = [Paragraph(line.replace(" ", "&nbsp;").replace("<", "&lt;").replace(">", "&gt;"), code_style) for line in code_text.split("\n")]
                t_code = Table([[code_lines]], colWidths=[480])
                t_code.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
                    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
                    ('TOPPADDING', (0,0), (-1,-1), 2),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                    ('LEFTPADDING', (0,0), (-1,-1), 5)
                ]))
                story.append(t_code)
                story.append(Spacer(1, 4))

            if "extra_text" in page:
                for p in page["extra_text"].split("\n\n"):
                    story.append(Paragraph(p, body_style))

        # Enforce page break between logical document pages
        if idx < len(ALL_PAGES) - 1:
            story.append(PageBreak())

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF build complete.")

def build_docx():
    print(f"Generating DOCX: {docx_output} ...")
    doc = docx.Document()
    
    # Page setup: A4 with 1 inch (72 pt) margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        
        # Header & Footer setup
        header = section.header
        hp = header.paragraphs[0]
        hp.text = "MYTUNE: MODERN AUDIO-REACTIVE WEB MUSIC STREAMING PLATFORM | TY B.Sc. CS"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.runs[0].font.size = Pt(8)
        hp.runs[0].font.color.rgb = RGBColor(71, 85, 105)

        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "Vande Mataram Degree College | Dept. of Computer Science | Kuldeep Pal (Roll No: 35)"
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        fp.runs[0].font.size = Pt(8)
        fp.runs[0].font.color.rgb = RGBColor(71, 85, 105)

    for idx, page in enumerate(ALL_PAGES):
        p_type = page.get("type")
        
        if p_type == "cover":
            c = page["content"]
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(c["univ"] + "\n\n")
            run.font.bold = True
            run.font.size = Pt(16)
            run.font.color.rgb = RGBColor(185, 28, 28)

            run = p.add_run(c["sub"] + "\n")
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(71, 85, 105)

            run = p.add_run(c["degree"] + "\n\n")
            run.font.bold = True
            run.font.size = Pt(12)
            run.font.color.rgb = RGBColor(30, 58, 138)

            run = p.add_run(c["project_title"] + "\n\n")
            run.font.bold = True
            run.font.size = Pt(18)
            run.font.color.rgb = RGBColor(15, 23, 42)

            run = p.add_run(c["subtitle"] + "\n\n")
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(51, 65, 85)

            run = p.add_run("SUBMITTED BY:\n")
            run.font.bold = True
            run.font.size = Pt(10)
            run = p.add_run(f"{c['student_name']} / {c['roll_no']}\n\n")
            run.font.size = Pt(11)

            run = p.add_run("UNDER THE GUIDANCE OF:\n")
            run.font.bold = True
            run.font.size = Pt(10)
            run = p.add_run(c["guide"] + "\n\n")
            run.font.size = Pt(11)

            run = p.add_run(c["college"] + "\n")
            run.font.bold = True
            run.font.size = Pt(12)
            run.font.color.rgb = RGBColor(4, 120, 87)

            run = p.add_run(c["affiliation"] + "\n" + c["address"] + "\n\n")
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor(71, 85, 105)

            run = p.add_run(f"Live Public Deployment: {c['render_link']}\n")
            run.font.bold = True
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(37, 99, 235)

        elif p_type == "certificate":
            h = doc.add_heading(page["title"], level=1)
            h.runs[0].font.color.rgb = RGBColor(30, 58, 138)
            doc.add_paragraph(page["subtitle"])
            for para in page["cert_text"].split("\n\n"):
                doc.add_paragraph(para)
            doc.add_paragraph("\n\n")
            table = doc.add_table(rows=1, cols=3)
            hdr = table.rows[0].cells
            hdr[0].text = "______________________\nAsst. Prof. Bharati Gaikar\nInternal Guide"
            hdr[1].text = "______________________\nHead of Department\nComputer Science"
            hdr[2].text = "______________________\nDr. Rajkumar M. Kolhe\nPrincipal, VMDC"

        elif p_type == "declaration":
            h = doc.add_heading(page["title"], level=1)
            h.runs[0].font.color.rgb = RGBColor(30, 58, 138)
            for para in page["text"].split("\n\n"):
                doc.add_paragraph(para)
            doc.add_paragraph("\n\n")
            m = page["meta"]
            table = doc.add_table(rows=1, cols=2)
            hdr = table.rows[0].cells
            hdr[0].text = f"Date: {m['date']}\nPlace: {m['place']}"
            hdr[1].text = f"____________________________\nCandidate Signature\nName: {m['name']}\nRoll No: {m['roll']}"

        elif p_type == "abstract":
            h = doc.add_heading(page["title"], level=1)
            h.runs[0].font.color.rgb = RGBColor(30, 58, 138)
            for para in page["abstract"].split("\n\n"):
                doc.add_paragraph(para)
            doc.add_heading(page["role_title"], level=2)
            doc.add_paragraph(page["role_text"])

        elif p_type == "acknowledgement":
            h = doc.add_heading(page["title"], level=1)
            h.runs[0].font.color.rgb = RGBColor(30, 58, 138)
            for para in page["text"].split("\n\n"):
                doc.add_paragraph(para)
            doc.add_paragraph("\n\n")
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p.add_run(f"_______________________\n{page['sig_name']}\n{page['sig_roll']}")

        elif p_type in ["toc1", "toc2"]:
            h = doc.add_heading(page["title"], level=1)
            h.runs[0].font.color.rgb = RGBColor(30, 58, 138)
            table = doc.add_table(rows=len(page["entries"]), cols=2)
            for r_idx, (item, p_num) in enumerate(page["entries"]):
                cells = table.rows[r_idx].cells
                cells[0].text = item
                cells[1].text = p_num

        else:
            if "title" in page:
                h = doc.add_heading(page["title"], level=1)
                h.runs[0].font.color.rgb = RGBColor(30, 58, 138)
            
            if "sections" in page:
                for sec in page["sections"]:
                    h2 = doc.add_heading(f"{sec['num']} {sec['title']}", level=2)
                    h2.runs[0].font.color.rgb = RGBColor(3, 105, 161)
                    for p_text in sec["content"].split("\n\n"):
                        doc.add_paragraph(p_text)
            
            if "image" in page:
                img_info = page["image"]
                img_path = os.path.join(assets_dir, img_info["filename"])
                if os.path.exists(img_path):
                    doc.add_paragraph()
                    doc.add_picture(img_path, width=Inches(min(6.2, img_info.get("width", 6.0))))
                    cap = doc.add_paragraph(img_info["caption"])
                    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    cap.runs[0].font.italic = True
                    cap.runs[0].font.size = Pt(8.5)
            
            if "tables" in page:
                for t_spec in page["tables"]:
                    cap = doc.add_paragraph(t_spec["caption"])
                    cap.runs[0].font.bold = True
                    cap.runs[0].font.size = Pt(9)
                    
                    table = doc.add_table(rows=len(t_spec["rows"]) + 1, cols=len(t_spec["headers"]))
                    hdr_cells = table.rows[0].cells
                    for c_idx, head in enumerate(t_spec["headers"]):
                        hdr_cells[c_idx].text = head
                        hdr_cells[c_idx].paragraphs[0].runs[0].font.bold = True
                        hdr_cells[c_idx].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
                        shd = parse_xml(r'<w:shd {} w:fill="1E3A8A"/>'.format(nsdecls('w')))
                        hdr_cells[c_idx]._tc.get_or_add_tcPr().append(shd)

                    for r_idx, row in enumerate(t_spec["rows"]):
                        row_cells = table.rows[r_idx + 1].cells
                        for c_idx, val in enumerate(row):
                            row_cells[c_idx].text = str(val)
                            row_cells[c_idx].paragraphs[0].runs[0].font.size = Pt(8)
                            if r_idx % 2 == 1:
                                shd = parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w')))
                                row_cells[c_idx]._tc.get_or_add_tcPr().append(shd)
            
            if "code_block" in page:
                p_code = doc.add_paragraph()
                p_code.paragraph_format.left_indent = Inches(0.2)
                run_code = p_code.add_run(page["code_block"])
                run_code.font.name = 'Consolas'
                run_code.font.size = Pt(7.5)
                run_code.font.color.rgb = RGBColor(15, 23, 42)

            if "extra_text" in page:
                for p_text in page["extra_text"].split("\n\n"):
                    doc.add_paragraph(p_text)

        # Enforce page break between logical document pages
        if idx < len(ALL_PAGES) - 1:
            doc.add_page_break()

    doc.save(docx_output)
    print("DOCX build complete.")

if __name__ == "__main__":
    build_pdf()
    build_docx()

    # Verify generated PDF page count
    reader = pypdf.PdfReader(pdf_output)
    actual_pages = len(reader.pages)
    print(f"VERIFICATION: Generated PDF has {actual_pages} pages!")

    # Mirror output files to scratch and artifact directories
    for out_f in [pdf_output, docx_output]:
        base_name = os.path.basename(out_f)
        shutil.copy2(out_f, os.path.join(scratch_dir, base_name))
        shutil.copy2(out_f, os.path.join(artifact_dir, base_name))
        print(f"Copied {base_name} to scratch and artifact directories.")

    print("ALL DOCUMENTATION GENERATED AND VERIFIED SUCCESSFULLY!")
