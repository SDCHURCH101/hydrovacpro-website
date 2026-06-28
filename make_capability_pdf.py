#!/usr/bin/env python3
"""Generate the Hydrovac Pro one-page Capability Statement PDF.

Pulls all verified facts (legal name, UEI, CAGE, USDOT, NAICS, POC, addresses)
straight from build.py so the PDF can never drift from the website.

Run:  ./make_capability_pdf.py        (needs reportlab + Pillow)
Output: assets/hydrovac-pro-capability-statement.pdf
"""
import os
import build  # verified business constants live here

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.utils import ImageReader, simpleSplit
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "assets", "hydrovac-pro-capability-statement.pdf")

# ---- brand palette
NAVY   = (0x0b/255, 0x18/255, 0x2b/255)
BLUE   = (0x15/255, 0x59/255, 0xa8/255)
ORANGE = (0xf5/255, 0x82/255, 0x1f/255)
MIST   = (0xee/255, 0xf2/255, 0xf7/255)
INK    = (0x21/255, 0x2b/255, 0x39/255)
GRAY   = (0x5a/255, 0x6b/255, 0x80/255)
WHITE  = (1, 1, 1)
LINE   = (0xd4/255, 0xdd/255, 0xe7/255)

W, H = LETTER  # 612 x 792
M = 36         # page margin

# ---- content (marketing copy; facts come from build.py)
OVERVIEW = (
    f"{build.NAME}, a dba of {build.LEGAL_NAME}, is a Fairbanks-based hydro-excavation and "
    "vacuum-truck contractor serving utilities, government agencies, mining, oil & gas, and "
    "industrial clients across Interior Alaska and the North Slope. We expose and clear buried "
    "infrastructure without the strike risk of mechanical digging, backed by 13 years of Arctic "
    "and North Dakota oil-field experience, a hot-water hydrovac that cuts frozen ground, and a "
    "perfect safety record of zero utility strikes."
)
COMPETENCIES = [
    "Hydro excavation: daylighting & potholing",
    "Slot trenching & precision excavation",
    "Vactor 2100 jetter: culvert, storm & sewer cleaning",
    "Service pit, sump & tank cleanouts",
    "Cold-weather & frozen-ground excavation / thawing",
    "Emergency & spill response, liquid recovery",
]
DIFFERENTIATORS = [
    "Perfect safety record: zero utility strikes",
    "Hot-water hydrovac for permafrost & frozen ground",
    "One crew, two trucks: Tornado F4 + Vactor 2100",
    "24/7 emergency & after-hours mobilization",
    "Licensed, bonded, insured · OSHA · DOT registered",
    "Documented digs for engineering & procurement",
]
INDUSTRIES = ("Utilities & Telecom · Government & Municipal (DOT, FAA, boroughs) · Mining · "
              "Oil, Gas & Pipeline · Construction & GC · Environmental & Industrial")


def rect(c, x, y, w, h, fill):
    c.setFillColorRGB(*fill)
    c.rect(x, y, w, h, stroke=0, fill=1)


def section_head(c, x, y, w, text, color=NAVY):
    c.setFillColorRGB(*color)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(x, y, text.upper())
    c.setStrokeColorRGB(*ORANGE)
    c.setLineWidth(1.4)
    c.line(x, y - 5, x + 22, y - 5)
    c.setStrokeColorRGB(*LINE)
    c.setLineWidth(0.6)
    c.line(x + 26, y - 5, x + w, y - 5)
    return y - 18


def paragraph(c, x, y, w, text, size=9, leading=12.4, color=INK):
    c.setFillColorRGB(*color)
    c.setFont("Helvetica", size)
    for ln in simpleSplit(text, "Helvetica", size, w):
        c.drawString(x, y, ln)
        y -= leading
    return y


def bullets(c, x, y, w, items, size=9, leading=14.5):
    for it in items:
        c.setFillColorRGB(*ORANGE)
        c.rect(x, y + 1.3, 3.2, 3.2, stroke=0, fill=1)
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica", size)
        lines = simpleSplit(it, "Helvetica", size, w - 12)
        c.drawString(x + 10, y, lines[0])
        for extra in lines[1:]:
            y -= 11
            c.drawString(x + 10, y, extra)
        y -= leading
    return y


def field(c, x, y, w, label, value):
    c.setFillColorRGB(*GRAY)
    c.setFont("Helvetica-Bold", 6.8)
    c.drawString(x, y, label.upper())
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 9.3)
    yy = y - 11
    for ln in simpleSplit(value, "Helvetica-Bold", 9.3, w):
        c.drawString(x, yy, ln)
        yy -= 10.5
    return yy - 5


def build_pdf():
    c = canvas.Canvas(OUT, pagesize=LETTER)
    c.setTitle("Hydrovac Pro Capability Statement")
    c.setAuthor(build.NAME)
    c.setSubject("Hydro excavation & vacuum truck services in Fairbanks, Alaska")
    c.setKeywords("hydro excavation, hydrovac, capability statement, UEI, CAGE, NAICS, Alaska")

    # ---------- header band
    band_h = 86
    rect(c, 0, H - band_h, W, band_h, NAVY)
    rect(c, 0, H - band_h - 6, W, 6, ORANGE)  # hazard stripe

    # white wordmark logo (png preferred, else webp via PIL)
    logo = None
    for cand in ("logo-wordmark-white.png", "logo-wordmark-white.webp"):
        p = os.path.join(HERE, "assets", "img", cand)
        if os.path.exists(p):
            logo = p
            break
    if logo:
        im = Image.open(logo).convert("RGBA")
        ar = im.width / im.height
        lw = 218
        lh = lw / ar
        c.drawImage(ImageReader(im), 40, H - band_h + (band_h - lh) / 2,
                    width=lw, height=lh, mask="auto")

    c.setFillColorRGB(*WHITE)
    c.setFont("Helvetica-Bold", 15)
    c.drawRightString(W - 40, H - 38, "CAPABILITY STATEMENT")
    c.setFillColorRGB(*ORANGE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawRightString(W - 40, H - 52, "DIG SAFE.")
    c.setFillColorRGB(0.8, 0.86, 0.93)
    c.setFont("Helvetica", 8)
    c.drawRightString(W - 40, H - 65, "Hydro Excavation · Vacuum Trucks · Fairbanks, Alaska")

    # ---------- columns geometry
    top = H - band_h - 26
    foot_h = 40
    col_gap = 18
    right_w = 212
    right_x = W - M - right_w
    left_x = M
    left_w = right_x - col_gap - left_x

    # ---------- right sidebar panel
    panel_top = top + 10
    panel_bot = foot_h + 10
    rect(c, right_x - 12, panel_bot, right_w + 12, panel_top - panel_bot, MIST)

    # ---------- LEFT column
    y = top
    y = section_head(c, left_x, y, left_w, "Company Overview")
    y = paragraph(c, left_x, y, left_w, OVERVIEW)
    y -= 10
    y = section_head(c, left_x, y, left_w, "Core Competencies")
    y = bullets(c, left_x, y, left_w, COMPETENCIES)
    y -= 6
    y = section_head(c, left_x, y, left_w, "Differentiators")
    y = bullets(c, left_x, y, left_w, DIFFERENTIATORS)
    y -= 6
    y = section_head(c, left_x, y, left_w, "Industries Served")
    y = paragraph(c, left_x, y, left_w, INDUSTRIES, size=8.6, leading=12.6, color=GRAY)

    # ---------- RIGHT sidebar content
    rx = right_x
    rw = right_w
    ry = top
    ry = section_head(c, rx, ry, rw, "Company Data")
    ry = field(c, rx, ry, rw, "Legal Name", build.LEGAL_NAME)
    ry = field(c, rx, ry, rw, "DBA", build.DBA_NAME)
    ry = field(c, rx, ry, rw, "UEI (SAM.gov)", build.UEI_CODE)
    ry = field(c, rx, ry, rw, "CAGE Code", build.CAGE_CODE)
    ry = field(c, rx, ry, rw, "USDOT Number", build.USDOT_NUMBER)
    ry = field(c, rx, ry, rw, "AK Entity Number", f"{build.AK_ENTITY} ({build.ENTITY_STATUS})")
    ry = field(c, rx, ry, rw, "AK Business License", build.AK_LICENSE)
    ry = field(c, rx, ry, rw, "Established", "2011")

    ry -= 4
    ry = section_head(c, rx, ry, rw, "NAICS Codes")
    for code, desc in build.NAICS_CODES:
        c.setFillColorRGB(*BLUE)
        c.setFont("Helvetica-Bold", 9)
        tag = code + ("  (primary)" if code == build.NAICS_PRIMARY else "")
        c.drawString(rx, ry, tag)
        ry -= 10
        c.setFillColorRGB(*GRAY)
        c.setFont("Helvetica", 7.6)
        for ln in simpleSplit(desc, "Helvetica", 7.6, rw):
            c.drawString(rx, ry, ln)
            ry -= 9
        ry -= 3

    ry -= 2
    ry = section_head(c, rx, ry, rw, "Point of Contact")
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 9.3)
    c.drawString(rx, ry, build.POC_NAME)
    ry -= 11
    c.setFillColorRGB(*GRAY)
    c.setFont("Helvetica", 8.4)
    for ln in (build.POC_TITLE, build.POC_EMAIL, build.PHONE_DISPLAY):
        c.drawString(rx, ry, ln)
        ry -= 10.5

    ry -= 4
    ry = section_head(c, rx, ry, rw, "Locations")
    c.setFillColorRGB(*GRAY)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(rx, ry, "PHYSICAL")
    ry -= 10
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica", 8.4)
    for ln in simpleSplit(f"{build.ADDR_STREET}, {build.ADDR_CITY}, {build.ADDR_STATE} {build.ADDR_ZIP}",
                          "Helvetica", 8.4, rw):
        c.drawString(rx, ry, ln)
        ry -= 10
    ry -= 3
    c.setFillColorRGB(*GRAY)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(rx, ry, "MAILING")
    ry -= 10
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica", 8.4)
    c.drawString(rx, ry, build.MAILING_ADDR)

    # ---------- footer band
    rect(c, 0, 0, W, foot_h, NAVY)
    rect(c, 0, foot_h, W, 3, ORANGE)
    c.setFillColorRGB(*WHITE)
    c.setFont("Helvetica-Bold", 9)
    site = build.SITE.replace("https://", "")
    c.drawString(M, 24, site)
    c.setFont("Helvetica", 8.6)
    c.setFillColorRGB(0.8, 0.86, 0.93)
    c.drawString(M, 12, f"{build.PHONE_DISPLAY}   ·   {build.EMAIL}")
    c.setFont("Helvetica-Bold", 7.6)
    c.setFillColorRGB(*ORANGE)
    c.drawRightString(W - M, 17, "LICENSED · BONDED · INSURED · OSHA COMPLIANT · DOT REGISTERED")

    c.showPage()
    c.save()
    print("wrote", OUT)


if __name__ == "__main__":
    build_pdf()
