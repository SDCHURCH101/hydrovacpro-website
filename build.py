#!/usr/bin/env python3
# Hydrovac Pro static site generator.
# Edit this file, then run:  python3 build.py
# Emits the 6 HTML pages + robots.txt + sitemap.xml + manifest + 404 into this dir.
import os, html, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
VER  = "12"  # bump to cache-bust styles.css / app.js

# ------------------------------------------------------------------ business facts
SITE   = "https://www.hydrovacpro.com"
NAME   = "Hydrovac Pro"
PHONE_DISPLAY = "(907) 759-8068"
PHONE_TEL     = "+19077598068"
EMAIL  = "office@hydrovacpro.com"
ADDR_STREET = "300 Barnette St, Ste 202B"
ADDR_CITY   = "Fairbanks"
ADDR_STATE  = "AK"
ADDR_ZIP    = "99701"
GEO_LAT = "64.8401"
GEO_LNG = "-147.7200"
FACEBOOK = "https://www.facebook.com/61559111513765"
GMAPS    = "https://www.google.com/maps/search/?api=1&query=Hydrovac+Pro+300+Barnette+St+Fairbanks+AK"
GREVIEWS = "https://www.google.com/maps/search/?api=1&query=Hydrovac+Pro+Fairbanks+AK+reviews"
SISTER = [
    ("Septic Pro Alaska", "https://www.septicproak.com", "Septic pumping, thawing & tank service", "sister-septic.png"),
    ("Husband for an Hour", "https://www.husbandforhour.com", "Flat-rate handyman & property services", "sister-husband.png"),
]

# ------------------------------------------------------------------ government / capability statement
# Verified from State of Alaska Business License #2158460 (SABE CAPITAL LLC dba Hydrovac Pro).
# Federal codes left as "Provided on request" until confirmed by the company (do NOT guess).
LEGAL_NAME   = "Sabe Capital, LLC"
DBA_NAME     = "Hydrovac Pro"
AK_LICENSE   = "2158460"
AK_ENTITY    = "10185264"
ENTITY_STATUS= "Good Standing"
UEI_CODE     = "Provided on request"
CAGE_CODE    = "13HP6"
USDOT_NUMBER = "4264044"
NAICS_PRIMARY = "238910"
NAICS_CODES  = [
    ("238910", "Site Preparation Contractors"),
    ("562998", "All Other Miscellaneous Waste Management Services"),
    ("237990", "Other Heavy & Civil Engineering Construction"),
    ("562910", "Remediation Services"),
    ("484220", "Specialized Freight Trucking, Local"),
]
POC_NAME     = "Fernando Escobar"
POC_TITLE    = "General Manager"
POC_EMAIL    = "gm@hydrovacpro.com"
MAILING_ADDR = "PO Box 70200, Fairbanks, AK 99707"

# ------------------------------------------------------------------ navigation
NAV = [
    ("index.html",      "Home"),
    ("services.html",   "Services"),
    ("equipment.html",  "Fleet"),
    ("industries.html", "Industries"),
    ("about.html",      "About"),
    ("contact.html",    "Contact"),
]

# ------------------------------------------------------------------ languages (Google Translate codes)
LANGS = [
    ("en","English"),("es","Espanol"),("zh-CN","Chinese (Simplified)"),("zh-TW","Chinese (Traditional)"),
    ("hi","Hindi"),("ar","Arabic"),("bn","Bengali"),("pt","Portugues"),("ru","Russian"),("ja","Japanese"),
    ("pa","Punjabi"),("de","Deutsch"),("jw","Javanese"),("ko","Korean"),("fr","Francais"),("te","Telugu"),
    ("mr","Marathi"),("tr","Turkce"),("ta","Tamil"),("vi","Tieng Viet"),("ur","Urdu"),("it","Italiano"),
    ("th","Thai"),("gu","Gujarati"),("fa","Persian"),("pl","Polski"),("uk","Ukrainian"),("ro","Romana"),
    ("nl","Nederlands"),("id","Indonesia"),("ms","Malay"),("tl","Filipino"),("my","Burmese"),("km","Khmer"),
    ("am","Amharic"),("ne","Nepali"),("si","Sinhala"),("el","Greek"),("hu","Magyar"),("cs","Cestina"),
    ("sv","Svenska"),("he","Hebrew"),("da","Dansk"),("fi","Suomi"),("no","Norsk"),("sk","Slovak"),
    ("hr","Croatian"),("bg","Bulgarian"),("sr","Serbian"),("lt","Lithuanian"),("sl","Slovenian"),
    ("lv","Latvian"),("et","Estonian"),("az","Azerbaijani"),("ka","Georgian"),("hy","Armenian"),
    ("kk","Kazakh"),("uz","Uzbek"),("mn","Mongolian"),("sw","Swahili"),("ha","Hausa"),("yo","Yoruba"),
    ("ig","Igbo"),("zu","Zulu"),("xh","Xhosa"),("af","Afrikaans"),("so","Somali"),("rw","Kinyarwanda"),
    ("mg","Malagasy"),("ny","Chichewa"),("st","Sesotho"),("sn","Shona"),("ga","Irish"),("cy","Welsh"),
    ("gl","Galician"),("ca","Catala"),("eu","Basque"),("is","Icelandic"),("mk","Macedonian"),("sq","Albanian"),
    ("bs","Bosnian"),("be","Belarusian"),("ky","Kyrgyz"),("tg","Tajik"),("tk","Turkmen"),("ps","Pashto"),
    ("sd","Sindhi"),("lo","Lao"),("ml","Malayalam"),("kn","Kannada"),("or","Odia"),("as","Assamese"),
    ("mt","Maltese"),("lb","Luxembourgish"),("la","Latin"),("ht","Haitian Creole"),("co","Corsican"),
    ("fy","Frisian"),("haw","Hawaiian"),("sm","Samoan"),("mi","Maori"),("ku","Kurdish"),("yi","Yiddish"),
]

# ------------------------------------------------------------------ inline SVG icons (stroke = currentColor)
def icon(name):
    p = {
      "dig":'<path d="M3 21h18M5 21V11l5-3 5 3v10M9 21v-5h2v5"/><path d="M14 8l4-4 3 3-4 4"/>',
      "pothole":'<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>',
      "trench":'<path d="M3 7h18M3 7l3 12h12l3-12M8 11v4M12 11v4M16 11v4"/>',
      "jet":'<path d="M2 12h7M2 9h5M2 15h5"/><path d="M9 7h7a4 4 0 0 1 4 4v2a4 4 0 0 1-4 4H9z"/><path d="M14 11h2"/>',
      "tank":'<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18M8 6v12"/>',
      "snow":'<path d="M12 2v20M2 12h20M5 5l14 14M19 5L5 19M9 4l3 3 3-3M9 20l3-3 3 3M4 9l3 3-3 3M20 9l-3 3 3 3"/>',
      "alert":'<path d="M12 3l9 16H3z"/><path d="M12 10v4M12 17v.5"/>',
      "shield":'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
      "truck":'<path d="M3 7h11v8H3zM14 10h4l3 3v2h-7z"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/>',
      "utility":'<path d="M12 2v6M8 8h8M6 8v12M18 8v12M9 12h6M9 16h6"/>',
      "gov":'<path d="M3 21h18M5 21V9M19 21V9M3 9l9-6 9 6zM9 21v-7h6v7"/>',
      "mine":'<path d="M14 3l7 7-4 4-7-7zM10 7l-7 7v4h4l7-7"/>',
      "oil":'<path d="M6 21V8l4-5 4 5v13M4 21h12M16 13h3a2 2 0 0 1 2 2v6"/>',
      "build":'<path d="M3 21h18M6 21V8h6v13M12 12h6v9M8 11h2M8 14h2M8 17h2"/>',
      "leaf":'<path d="M11 21C5 19 3 13 5 5c8 0 14 2 14 10 0 0-1 6-8 6z"/><path d="M9 17c2-4 5-6 8-7"/>',
      "phone":'<path d="M5 4h4l2 5-3 2a12 12 0 0 0 5 5l2-3 5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
      "mail":'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
      "pin":'<path d="M12 22s7-6 7-12a7 7 0 0 0-14 0c0 6 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
      "clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
      "check":'<path d="M20 6L9 17l-5-5"/>',
      "star":'<path d="M12 3l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5L12 18.8 6.2 21l1.1-6.5L2.6 9.8l6.5-.9z"/>',
      "loc":'<path d="M12 21s7-6 7-12a7 7 0 0 0-14 0c0 6 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
      "arrow":'<path d="M5 12h14M13 6l6 6-6 6"/>',
      "globe":'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
      "fb":'<path d="M14 9h3V5h-3a4 4 0 0 0-4 4v2H7v4h3v6h4v-6h3l1-4h-4V9a1 1 0 0 1 1-1z"/>',
      "doc":'<path d="M6 2h8l4 4v16H6z"/><path d="M14 2v4h4M9 12h6M9 16h6"/>',
      "gauge":'<path d="M4 13a8 8 0 0 1 16 0"/><path d="M12 13l4-3"/><circle cx="12" cy="13" r="1"/>',
      "drop":'<path d="M12 3c4 5 7 8 7 12a7 7 0 0 1-14 0c0-4 3-7 7-12z"/>',
    }.get(name, '')
    return ('<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+p+'</svg>')

def e(s): return html.escape(s, quote=True)

# ------------------------------------------------------------------ SEO head
def head(page, title, desc, extra_ld=None, og_img="assets/img/og-image.jpg"):
    canonical = SITE + "/" + ("" if page == "index.html" else page)
    if page == "index.html":
        canonical = SITE + "/"
    ld = [local_business_ld()]
    ld.append(breadcrumb_ld(page, title))
    if extra_ld:
        ld.extend(extra_ld)
    ld_tags = "\n".join(
        '<script type="application/ld+json">%s</script>' % j for j in ld)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(canonical)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="author" content="{NAME}">
<meta name="theme-color" content="#0b182b">
<meta name="geo.region" content="US-AK">
<meta name="geo.placename" content="Fairbanks, Alaska">
<meta name="geo.position" content="{GEO_LAT};{GEO_LNG}">
<meta name="ICBM" content="{GEO_LAT}, {GEO_LNG}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(canonical)}">
<meta property="og:image" content="{SITE}/{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}/{og_img}">
<link rel="icon" href="assets/img/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="assets/img/favicon-180.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Barlow:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css?v={VER}">
{ld_tags}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{topbar()}
{nav(page)}
<main id="main">"""

# ------------------------------------------------------------------ JSON-LD blocks
import json as _json
def local_business_ld():
    data = {
      "@context":"https://schema.org",
      "@type":["LocalBusiness","HomeAndConstructionBusiness"],
      "@id": SITE + "/#business",
      "name": NAME,
      "legalName": LEGAL_NAME,
      "naics": NAICS_PRIMARY,
      "url": SITE + "/",
      "image": SITE + "/assets/img/hydrovac.jpg",
      "logo": SITE + "/assets/img/favicon-512.png",
      "telephone": PHONE_TEL,
      "email": EMAIL,
      "description": "Non-destructive hydro excavation, vacuum truck, and Vactor 2100 jetter services for utilities, government, mining, oil and gas, and construction across Interior Alaska.",
      "slogan": "Dig Safe.",
      "foundingDate": "2011",
      "priceRange": "$$",
      "address": {
        "@type":"PostalAddress",
        "streetAddress": ADDR_STREET,
        "addressLocality": ADDR_CITY,
        "addressRegion": ADDR_STATE,
        "postalCode": ADDR_ZIP,
        "addressCountry":"US"
      },
      "geo": {"@type":"GeoCoordinates","latitude":GEO_LAT,"longitude":GEO_LNG},
      "areaServed":[
        {"@type":"State","name":"Alaska"},
        {"@type":"City","name":"Fairbanks"},
        {"@type":"City","name":"North Pole"},
        {"@type":"AdministrativeArea","name":"Fairbanks North Star Borough"},
        {"@type":"AdministrativeArea","name":"Interior Alaska"}
      ],
      "openingHoursSpecification":[{
        "@type":"OpeningHoursSpecification",
        "dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],
        "opens":"08:00","closes":"17:00"
      }],
      "sameAs":[FACEBOOK],
      "knowsLanguage":["en"],
      "aggregateRating":{"@type":"AggregateRating","ratingValue":"5.0","reviewCount":"3","bestRating":"5"},
      "hasOfferCatalog":{
        "@type":"OfferCatalog","name":"Hydro Excavation & Vacuum Services",
        "itemListElement":[
          {"@type":"Offer","itemOffered":{"@type":"Service","name":"Hydro Excavation (Daylighting & Potholing)"}},
          {"@type":"Offer","itemOffered":{"@type":"Service","name":"Slot Trenching & Precision Excavation"}},
          {"@type":"Offer","itemOffered":{"@type":"Service","name":"Vactor 2100 Jetter & Culvert Cleaning"}},
          {"@type":"Offer","itemOffered":{"@type":"Service","name":"Service Pit & Tank Cleanouts"}},
          {"@type":"Offer","itemOffered":{"@type":"Service","name":"Cold-Weather & Frozen Ground Excavation"}},
          {"@type":"Offer","itemOffered":{"@type":"Service","name":"Emergency & Spill Response"}}
        ]
      }
    }
    return _json.dumps(data, ensure_ascii=False)

def breadcrumb_ld(page, title):
    items = [{"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"}]
    if page != "index.html":
        clean = title.split("|")[0].split("-")[0].strip()
        items.append({"@type":"ListItem","position":2,"name":clean,"item":SITE+"/"+page})
    return _json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items}, ensure_ascii=False)

def faq_ld(qa):
    return _json.dumps({
      "@context":"https://schema.org","@type":"FAQPage",
      "mainEntity":[{"@type":"Question","name":q,
        "acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qa]
    }, ensure_ascii=False)

def service_ld(name, desc):
    return _json.dumps({
      "@context":"https://schema.org","@type":"Service","name":name,"description":desc,
      "serviceType":name,"provider":{"@id":SITE+"/#business"},
      "areaServed":{"@type":"AdministrativeArea","name":"Interior Alaska"}
    }, ensure_ascii=False)

# ------------------------------------------------------------------ utility bar + language switcher
def topbar():
    opts = "".join(
        f'<li role="option" data-code="{c}" tabindex="-1">{e(n)}</li>' for c,n in LANGS)
    return f"""
<div class="topbar">
  <div class="wrap topbar-in">
    <div class="topbar-left">
      <span class="tb-item">{icon('shield')}<span translate="no">Licensed · Bonded · Insured</span></span>
      <span class="tb-item tb-hide">{icon('check')}OSHA Compliant · Perfect Safety Record</span>
    </div>
    <div class="topbar-right">
      <a class="tb-item" href="tel:{PHONE_TEL}">{icon('phone')}<span translate="no">{PHONE_DISPLAY}</span></a>
      <a class="tb-item tb-hide" href="mailto:{EMAIL}">{icon('mail')}<span translate="no">{EMAIL}</span></a>
      <div class="lang" id="lang">
        <button class="lang-btn" id="langBtn" aria-haspopup="listbox" aria-expanded="false">
          {icon('globe')}<span id="langCur" translate="no">English</span>
          <svg viewBox="0 0 24 24" class="caret" aria-hidden="true"><path d="M6 9l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2"/></svg>
        </button>
        <div class="lang-pop" id="langPop" role="dialog" aria-label="Choose language">
          <input type="text" id="langSearch" placeholder="Search 100+ languages" autocomplete="off">
          <ul id="langList" role="listbox" aria-label="Languages">{opts}</ul>
        </div>
      </div>
    </div>
  </div>
</div>
<div id="google_translate_element" aria-hidden="true"></div>"""

# ------------------------------------------------------------------ header / nav
def nav(page):
    links = "".join(
        f'<a href="{href}" class="{"active" if href==page else ""}">{e(label)}</a>'
        for href,label in NAV)
    return f"""
<header class="site-head" id="head">
  <div class="wrap head-in">
    <a class="brand" href="index.html" aria-label="Hydrovac Pro, Dig Safe, Fairbanks Alaska home" translate="no">
      <img src="assets/img/logo-wordmark.png" alt="Hydrovac Pro — Dig Safe" class="brand-logo" width="200" height="50">
    </a>
    <nav class="nav-links" id="navLinks" aria-label="Primary">{links}</nav>
    <div class="head-cta">
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">{icon('phone')}<span translate="no">{PHONE_DISPLAY}</span></a>
      <a class="btn btn-orange" href="contact.html">Request a Bid</a>
    </div>
    <button class="burger" id="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>"""

# ------------------------------------------------------------------ footer
def footer():
    nav_links = "".join(f'<li><a href="{h}">{e(l)}</a></li>' for h,l in NAV)
    nav_links += '<li><a href="contact.html#capability-statement">Capability Statement</a></li>'
    svc = ["Hydro Excavation","Daylighting & Potholing","Slot Trenching",
           "Jetter & Culvert Cleaning","Tank & Pit Cleanouts","Emergency Response"]
    svc_links = "".join(f'<li><a href="services.html">{e(s)}</a></li>' for s in svc)
    sister = "".join(
        f'<li><a href="{u}" rel="noopener" target="_blank">'
        f'<span class="sister-logo"><img src="assets/img/{logo}" alt="{e(n)} logo" width="54" height="54" loading="lazy"></span>'
        f'<span class="sister-txt"><b>{e(n)}</b><span>{e(d)}</span></span>'
        f'</a></li>'
        for n,u,d,logo in SISTER)
    yr = datetime.date.today().year
    return f"""
{cta_band()}
<footer class="foot">
  <div class="wrap foot-grid">
    <div class="foot-brand">
      <a class="brand foot-logo" href="index.html" translate="no">
        <img src="assets/img/logo-wordmark-white.png" alt="Hydrovac Pro — Dig Safe" class="foot-wordmark" width="230" height="58">
      </a>
      <p>Non-destructive hydro excavation, vacuum truck, and jetter services built for Alaska's utilities, government agencies, mines, and industrial operators. Customer and contractor becoming one.</p>
      <div class="foot-social">
        <a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook">{icon('fb')}</a>
        <a href="{GREVIEWS}" target="_blank" rel="noopener" aria-label="Google reviews">{icon('star')}</a>
      </div>
    </div>
    <div class="foot-col">
      <h4>Company</h4><ul>{nav_links}</ul>
    </div>
    <div class="foot-col">
      <h4>Services</h4><ul>{svc_links}</ul>
    </div>
    <div class="foot-col foot-contact">
      <h4>Contact</h4>
      <ul>
        <li><a href="tel:{PHONE_TEL}">{icon('phone')}<span translate="no">{PHONE_DISPLAY}</span></a></li>
        <li><a href="mailto:{EMAIL}">{icon('mail')}<span translate="no">{EMAIL}</span></a></li>
        <li><a href="{GMAPS}" target="_blank" rel="noopener">{icon('pin')}<span translate="no">{ADDR_STREET}, {ADDR_CITY}, {ADDR_STATE} {ADDR_ZIP}</span></a></li>
        <li>{icon('clock')}Mon to Fri, 8a to 5p · Emergency response available</li>
      </ul>
    </div>
  </div>
  <div class="wrap foot-sister">
    <span class="sister-label">More from our family of companies</span>
    <ul>{sister}</ul>
  </div>
  <div class="wrap foot-legal">
    <span translate="no">© {yr} {NAME}. A Sabe Capital company. All rights reserved.</span>
    <span>Fairbanks, Alaska · Serving the Interior &amp; the North Slope</span>
  </div>
</footer>
<a class="callbar" href="tel:{PHONE_TEL}">{icon('phone')} Call {PHONE_DISPLAY}</a>
<button class="totop" id="totop" aria-label="Back to top">{icon('arrow')}</button>
<script src="assets/app.js?v={VER}" defer></script>
</body></html>"""

def tail():
    return footer()

# ------------------------------------------------------------------ reusable blocks
def cta_band():
    return f"""
<section class="cta-band">
  <div class="hazard"></div>
  <div class="wrap cta-in">
    <div>
      <span class="eyebrow eyebrow-light">Ready when you are</span>
      <h2>Have a project with utilities in the ground?</h2>
      <p>Send the scope and we will return a competitive, no-obligation bid. Emergency and after-hours calls answered.</p>
    </div>
    <div class="cta-actions">
      <a class="btn btn-orange btn-lg" href="contact.html">Request a Bid {icon('arrow')}</a>
      <a class="btn btn-outline-light btn-lg" href="tel:{PHONE_TEL}">{icon('phone')}<span translate="no">{PHONE_DISPLAY}</span></a>
    </div>
  </div>
</section>"""

def eyebrow(t, light=False):
    cls = "eyebrow eyebrow-light" if light else "eyebrow"
    return f'<span class="{cls}">{e(t)}</span>'

def stat(num, label, sub=""):
    return f'<div class="stat"><span class="stat-num" translate="no">{e(num)}</span><span class="stat-label">{e(label)}</span>{f"<span class=stat-sub>{e(sub)}</span>" if sub else ""}</div>'

def svc_card(ic, title, body, page="services.html"):
    return f"""<a class="svc-card reveal" href="{page}">
      <span class="svc-ic">{icon(ic)}</span>
      <h3>{e(title)}</h3>
      <p>{e(body)}</p>
      <span class="svc-more">Learn more {icon('arrow')}</span>
    </a>"""

REVIEWS = [
    ("Love these guys. They came right out and helped all night to get the job done. Professional, fast, and they did not stop until it was finished.", "Google review · Fairbanks"),
    ("Sent a request on a Saturday evening and got a call back the same day. Hard to find that kind of responsiveness from a contractor up here.", "Google review · Verified customer"),
    ("An absolute game-changer for hydro excavation. One crew, one truck, and the work of several pieces of equipment done safely.", "Google review · Industrial client"),
]

def reviews_section():
    cards = ""
    for txt, who in REVIEWS:
        stars = "".join(icon('star') for _ in range(5))
        cards += f"""<figure class="rev-card reveal">
          <div class="stars">{stars}</div>
          <blockquote>{e(txt)}</blockquote>
          <figcaption>{e(who)}</figcaption>
        </figure>"""
    return f"""
<section class="reviews">
  <div class="wrap">
    <div class="sec-head center">
      {eyebrow('What clients say', light=True)}
      <h2>Trusted on the job site and after hours</h2>
      <p class="lead">Real reviews from the people who call us when the work has to be done right the first time.</p>
    </div>
    <div class="rev-grid">{cards}</div>
    <div class="rev-cta">
      <a class="btn btn-outline-light" href="{GREVIEWS}" target="_blank" rel="noopener">{icon('star')} Read our Google reviews</a>
      <a class="btn btn-outline-light" href="{FACEBOOK}" target="_blank" rel="noopener">{icon('fb')} Follow us on Facebook</a>
    </div>
  </div>
</section>"""

VIDEO_ID = "aQEVApFhXK0"
VIDEO_TITLE = "The Alaska Hydrovac Song — Hydrovac Pro AK"
def video_section():
    return f"""
<section class="video-band">
  <div class="wrap video-in">
    <div class="video-head">
      {eyebrow('All across Alaska', light=True)}
      <h2>From the Slope to the Interior, we've been everywhere</h2>
      <p class="lead">A little Hydrovac Pro personality. Our own spin on a classic, made for the crews and clients we work with all over the state. Turn the sound on.</p>
      <a class="btn btn-orange" href="contact.html">Put us on your next job {icon('arrow')}</a>
    </div>
    <div class="video-frame">
      <div class="video-ratio">
        <iframe src="https://www.youtube-nocookie.com/embed/{VIDEO_ID}?start=2&amp;rel=0"
          title="{e(VIDEO_TITLE)}" loading="lazy"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
      </div>
    </div>
  </div>
</section>"""

def video_ld():
    return _json.dumps({
      "@context":"https://schema.org","@type":"VideoObject",
      "name":VIDEO_TITLE,
      "description":"Hydrovac Pro's Alaska hydrovac parody of \"I've Been Everywhere,\" featuring hydro excavation and vacuum truck work across Alaska.",
      "thumbnailUrl":["https://i.ytimg.com/vi/"+VIDEO_ID+"/maxresdefault.jpg"],
      "embedUrl":"https://www.youtube.com/embed/"+VIDEO_ID,
      "contentUrl":"https://www.youtube.com/watch?v="+VIDEO_ID,
      "publisher":{"@type":"Organization","name":NAME,"logo":{"@type":"ImageObject","url":SITE+"/assets/img/favicon-512.png"}}
    }, ensure_ascii=False)

def process_section():
    steps = [
        ("01","Locate &amp; plan","We confirm utility locates and a dig-safe plan before a single drop of water hits the ground."),
        ("02","Cut with water","High-pressure water breaks up soil and frozen ground without blades, augers, or strike risk."),
        ("03","Vacuum &amp; haul","An 8-inch boom vacuums spoil straight into the 13-cubic-yard debris tank for clean off-site disposal."),
        ("04","Expose &amp; restore","Utilities are daylighted intact, the work is documented, and the site is left clean and safe."),
    ]
    cards = "".join(
        f'<div class="step reveal"><span class="step-n" translate="no">{n}</span><h3>{t}</h3><p>{d}</p></div>'
        for n,t,d in steps)
    return f"""
<section class="process">
  <div class="wrap">
    <div class="sec-head">
      {eyebrow('How a dig works')}
      <h2>Precision excavation, start to finish</h2>
      <p class="lead">A repeatable, documented process that protects buried infrastructure and keeps crews safe.</p>
    </div>
    <div class="step-grid">{cards}</div>
  </div>
</section>"""

# ------------------------------------------------------------------ HOME
def page_index():
    services = "".join([
      svc_card("pothole","Daylighting & Potholing","Expose buried utilities intact before you bore, dig, or design. Zero strikes, every time."),
      svc_card("trench","Slot Trenching","Clean, narrow trenches for conduit, pipe, and cable with minimal surface restoration."),
      svc_card("jet","Jetter & Culvert Cleaning","Vactor 2100 hydro-jetting clears culverts, storm lines, and sewers fast."),
      svc_card("tank","Service Pit & Tank Cleanouts","Vacuum sludge, residue, and debris from pits and tanks of any size."),
      svc_card("snow","Frozen Ground Excavation","Hot water and steam cut through Alaska permafrost and frost when machines stall."),
      svc_card("alert","Emergency & Spill Response","After-hours vacuum, water, and cleanup crews ready when the call comes in."),
    ])
    inds = "".join([
      f'<a href="industries.html" class="ind-pill">{icon("utility")}Utilities</a>',
      f'<a href="industries.html" class="ind-pill">{icon("gov")}Government</a>',
      f'<a href="industries.html" class="ind-pill">{icon("mine")}Mining</a>',
      f'<a href="industries.html" class="ind-pill">{icon("oil")}Oil &amp; Gas</a>',
      f'<a href="industries.html" class="ind-pill">{icon("build")}Construction</a>',
      f'<a href="industries.html" class="ind-pill">{icon("leaf")}Environmental</a>',
    ])
    faqs = [
      ("What is hydro excavation?","Hydro excavation, also called hydrovac, daylighting, or potholing, uses pressurized water to break up soil and a powerful vacuum to remove it. Nothing mechanical touches the ground, so buried utilities are exposed without damage. It is the safest way to dig near power, gas, water, fiber, and pipelines."),
      ("Do you work in winter and frozen ground?","Yes. We use hot water and steam to cut through frost and permafrost year round across Interior Alaska, including jobs that conventional equipment cannot touch."),
      ("What areas do you serve?","We are based in Fairbanks and serve the Fairbanks North Star Borough, North Pole, and projects across Interior Alaska and the North Slope. We have also worked the North Dakota oil fields."),
      ("Are you licensed and insured?","Yes. Hydrovac Pro is licensed, bonded, and fully insured, OSHA compliant, and DOT registered. Certificates of insurance and W-9 are available on request."),
      ("How do I get a bid?","Call %s or send your scope through our contact page. For public bids and RFPs we turn around competitive pricing quickly." % PHONE_DISPLAY),
    ]
    faq_html = "".join(
      f'<details class="faq"><summary>{q}{icon("arrow")}</summary><p>{a}</p></details>'
      for q,a in faqs)

    extra = [
      faq_ld([(q, a) for q,a in faqs]),
      service_ld("Hydro Excavation","Non-destructive hydrovac daylighting, potholing, and trenching in Interior Alaska."),
      video_ld(),
    ]
    h = head("index.html",
        "Hydrovac Pro | Hydro Excavation & Vacuum Truck Services in Fairbanks, Alaska",
        "Non-destructive hydro excavation, daylighting, potholing, jetter, and vacuum truck services for utilities, government, mining, and industry across Interior Alaska. 13 years, perfect safety record. Call (907) 759-8068.",
        extra_ld=extra)
    return h + f"""
<section class="hero">
  <div class="hero-bg"><img src="assets/img/hero.jpg" alt="Hydrovac Pro crew operating the vacuum boom beside the Dig Safe truck on an Alaska job site" fetchpriority="high" width="1700" height="1275"></div>
  <div class="hero-shade"></div>
  <div class="wrap hero-in">
    <div class="hero-copy">
      {eyebrow('Hydro Excavation · Vacuum Trucks · Fairbanks, Alaska', light=True)}
      <h1>Dig safe.<br>Dig precise.<br><span class="hl">Dig anywhere.</span></h1>
      <p class="hero-lead">Hydrovac Pro delivers non-destructive hydro excavation, jetter, and vacuum truck services for the utilities, agencies, mines, and industrial operators that keep Alaska running. Thirteen years in the Arctic. A perfect safety record. Zero utility strikes.</p>
      <div class="hero-cta">
        <a class="btn btn-orange btn-lg" href="contact.html">Request a Bid {icon('arrow')}</a>
        <a class="btn btn-outline-light btn-lg" href="tel:{PHONE_TEL}">{icon('phone')} Call {PHONE_DISPLAY}</a>
      </div>
      <ul class="hero-trust">
        <li>{icon('check')}OSHA Compliant</li>
        <li>{icon('check')}Licensed · Bonded · Insured</li>
        <li>{icon('check')}DOT Registered</li>
      </ul>
    </div>
  </div>
</section>

<section class="stats">
  <div class="wrap stat-row">
    {stat('13', 'Years in the Arctic', 'AK & ND oil fields')}
    {stat('0', 'Utility strikes', 'Perfect safety record')}
    {stat('13 yd³', 'Debris capacity', 'Per vacuum load')}
    {stat('24/7', 'Emergency response', 'After-hours crews')}
  </div>
</section>

<section class="intro">
  <div class="wrap intro-in">
    <div class="intro-copy reveal">
      {eyebrow('Who we are')}
      <h2>The contractor utilities and agencies call when a strike is not an option</h2>
      <p>Based in Fairbanks, Hydrovac Pro brings precision, safety, and efficiency to excavation across Interior Alaska and the oil fields beyond. Our hydrovac and Vactor 2100 jetter trucks do the work of several machines, exposing and clearing buried infrastructure without the risk that comes with a backhoe or auger.</p>
      <p>From a single pothole to a full pipeline corridor, public bid to emergency callout, we show up prepared, document the work, and leave the site clean. That is what "customer and contractor becoming one" means to us.</p>
      <a class="link-arrow" href="about.html">Read our story {icon('arrow')}</a>
    </div>
    <div class="intro-media reveal">
      <img src="assets/img/intro.jpg" alt="Hydrovac Pro truck working with boom deployed while a crew member operates the dig" loading="lazy" width="1500" height="1125">
      <div class="intro-badge"><img src="assets/img/logo.png" alt="" width="78" height="78"><span translate="no">Dig Safe</span></div>
    </div>
  </div>
</section>

{video_section()}

<section class="services-sec">
  <div class="wrap">
    <div class="sec-head">
      {eyebrow('Capabilities')}
      <h2>One crew. Two specialized trucks. Every excavation challenge.</h2>
      <p class="lead">Hydro excavation and vacuum services engineered for the hardest ground in the country.</p>
    </div>
    <div class="svc-grid">{services}</div>
  </div>
</section>

<section class="fleet-teaser">
  <div class="wrap fleet-in">
    <div class="fleet-media reveal">
      <img src="assets/img/jetter.jpg" alt="Vactor 2100 jetter truck operated by Hydrovac Pro" loading="lazy" width="1700" height="1096">
    </div>
    <div class="fleet-copy reveal">
      {eyebrow('The fleet', light=True)}
      <h2>Built for the work, maintained for the strike-free record</h2>
      <div class="fleet-spec">
        <div><span class="fs-name">{icon('truck')} Tornado F4 Hydrovac</span><p>13-cubic-yard debris tank, 8-inch boom-mounted suction, high-pressure water, and hot-water capability for frozen ground.</p></div>
        <div><span class="fs-name">{icon('jet')} Vactor 2100 Jetter</span><p>Combination jetter and vacuum for culverts, storm lines, sewers, and catch-basin cleaning.</p></div>
      </div>
      <a class="btn btn-outline-light" href="equipment.html">See the full fleet {icon('arrow')}</a>
    </div>
  </div>
</section>

{process_section()}

<section class="ind-strip">
  <div class="wrap">
    <div class="sec-head center">
      {eyebrow('Industries we serve')}
      <h2>Trusted across the sectors that build and power Alaska</h2>
    </div>
    <div class="ind-pills">{inds}</div>
  </div>
</section>

{reviews_section()}

<section class="faq-sec">
  <div class="wrap faq-in">
    <div class="faq-head">
      {eyebrow('Answers')}
      <h2>Hydro excavation, explained</h2>
      <p class="lead">Common questions from owners, agencies, and general contractors.</p>
      <a class="btn btn-orange" href="contact.html">Talk to our team {icon('arrow')}</a>
    </div>
    <div class="faq-list">{faq_html}</div>
  </div>
</section>
""" + tail()

# ------------------------------------------------------------------ page hero (inner)
def page_hero(eyebrow_txt, title, lead, img, alt):
    return f"""
<section class="phero">
  <div class="phero-bg"><img src="{img}" alt="{e(alt)}" width="1700" height="1275"></div>
  <div class="phero-shade"></div>
  <div class="wrap phero-in">
    {eyebrow(eyebrow_txt, light=True)}
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>"""

# ------------------------------------------------------------------ SERVICES
def page_services():
    SVCS = [
      ("pothole","Daylighting &amp; Potholing","daylighting.jpg",
       "Expose buried utilities without touching them",
       "Before you bore, trench, or set a foundation, you need to know exactly what is underground. Our hydrovac uses pressurized water and high-volume suction to daylight gas, power, water, sewer, fiber, and pipelines intact. The result is verified locations, zero strikes, and a documented dig your engineers and locators can trust.",
       ["Vertical and angled potholes to verify depth and alignment","Pre-bore and pre-design utility verification","Safe digging around live, energized, and pressurized lines","Clean, compact excavations with minimal restoration"]),
      ("trench","Slot Trenching &amp; Precision Excavation","trenching.jpg",
       "Narrow, exact trenches with less surface damage",
       "When conduit, pipe, or cable has to go in around existing infrastructure, hydro excavation cuts clean slot trenches to grade without the over-dig and collateral damage of mechanical digging. Less spoil, less restoration, and no surprise strikes.",
       ["Conduit and duct-bank trenching","Excavation in congested utility corridors","Tight access and indoor or under-structure digs","Reduced backfill, compaction, and restoration cost"]),
      ("jet","Vactor 2100 Jetter &amp; Culvert Cleaning","culvert.jpg",
       "Clear culverts, storm lines, and sewers fast",
       "Our Vactor 2100 combination truck pairs high-pressure water jetting with powerful vacuum recovery to clear blockages, silt, ice, and debris from culverts, storm drains, and sewer mains. Routine maintenance or emergency blockage, municipal or private, we keep flow moving.",
       ["Culvert thawing, flushing, and debris removal","Storm and sanitary sewer jetting","Catch-basin and manhole cleanout","Scheduled municipal maintenance programs"]),
      ("tank","Service Pit &amp; Tank Cleanouts","pit.jpg",
       "Vacuum sludge and residue from pits and tanks",
       "We remove sludge, residue, and build-up from service pits, sumps, vaults, and tanks of nearly any size, then haul the material for proper disposal. Confined-space-aware crews and the right vacuum power for thick, heavy material.",
       ["Industrial sump and service-pit cleanout","Tank, vault, and interceptor pump-out","Sludge, slurry, and heavy-debris recovery","Off-site transport and disposal coordination"]),
      ("snow","Cold-Weather &amp; Frozen Ground Excavation","arctic.jpg",
       "Hot water and steam that cut Alaska frost",
       "Frost and permafrost stop conventional equipment cold. Our hot-water hydrovac thaws and excavates frozen ground year round, including vault toilet and septic thawing for agencies and remote sites across the Interior.",
       ["Frozen ground and permafrost excavation","Frozen culvert and line thawing","Vault toilet and tank thawing and pumping","Winter utility repairs and emergency digs"]),
      ("alert","Emergency &amp; Spill Response","emergency.jpg",
       "After-hours vacuum and cleanup, ready to roll",
       "Line breaks, floods, and spills do not wait for business hours. Our crews mobilize for emergency vacuum, water recovery, and cleanup, with the documentation environmental and safety teams require. When clients say we helped all night to get the job done, this is the work they mean.",
       ["Emergency vacuum and liquid recovery","Spill containment and cleanup support","Flood and water removal","Rapid after-hours and weekend mobilization"]),
    ]
    blocks = ""
    for i,(ic,title,img,sub,desc,bullets) in enumerate(SVCS):
        bl = "".join(f'<li>{icon("check")}{b}</li>' for b in bullets)
        alt_cls = " flip" if i % 2 else ""
        anchor = title.lower().replace(" &amp; "," ").replace(" ","-").replace("&amp;","and")
        blocks += f"""
        <article class="svc-block{alt_cls} reveal" id="{anchor}">
          <div class="svc-block-media"><img src="assets/img/{img}" alt="{e(title.replace('&amp;','and'))} by Hydrovac Pro" loading="lazy" width="1600" height="1200"></div>
          <div class="svc-block-copy">
            <span class="svc-ic">{icon(ic)}</span>
            <h2>{title}</h2>
            <p class="svc-sub">{e(sub)}</p>
            <p>{e(desc)}</p>
            <ul class="ticklist">{bl}</ul>
            <a class="btn btn-orange" href="contact.html">Request a Bid {icon('arrow')}</a>
          </div>
        </article>"""
    extra = [service_ld(t.replace('&amp;','and'), d) for _,t,_,_,d,_ in SVCS]
    h = head("services.html",
        "Services | Hydro Excavation, Jetter & Vacuum Truck Services | Hydrovac Pro",
        "Daylighting, potholing, slot trenching, Vactor 2100 jetter and culvert cleaning, tank and pit cleanouts, frozen ground excavation, and emergency response across Interior Alaska.",
        extra_ld=extra)
    return h + page_hero("What we do",
        "Hydro excavation and vacuum services for every challenge",
        "Two specialized trucks and an experienced crew, ready for the daylighting, trenching, cleaning, and emergency work that keeps Alaska's infrastructure safe.",
        "assets/img/boom.jpg","Hydrovac Pro boom excavating on an Alaska job site") + f"""
<section class="svc-blocks"><div class="wrap">{blocks}</div></section>
""" + tail()

# ------------------------------------------------------------------ EQUIPMENT / FLEET
def page_equipment():
    def spec_table(rows):
        return '<table class="spec"><tbody>' + "".join(
            f'<tr><th>{e(k)}</th><td translate="no">{e(v)}</td></tr>' for k,v in rows) + '</tbody></table>'
    tornado = spec_table([
        ("Unit","Tornado F4 Hydrovac"),
        ("Chassis","Heavy-duty tandem / tri-axle truck"),
        ("Debris tank","13 cubic yards"),
        ("Suction","8 inch boom-mounted hose"),
        ("Boom","Hydraulic, extending and rotating reach"),
        ("Water system","High-pressure, hot-water capable"),
        ("Best for","Daylighting, potholing, trenching, frozen ground"),
    ])
    vactor = spec_table([
        ("Unit","Vactor 2100 Combination"),
        ("Type","Jetter + vacuum combination truck"),
        ("Water","High-pressure hose-reel jetting"),
        ("Recovery","Vacuum debris and liquid recovery"),
        ("Hose","Continuous-rod / culvert nozzle capable"),
        ("Best for","Culverts, storm and sewer lines, catch basins"),
    ])
    h = head("equipment.html",
        "Fleet & Capabilities | Tornado F4 Hydrovac & Vactor 2100 Jetter | Hydrovac Pro",
        "Inside the Hydrovac Pro fleet: a Tornado F4 hydrovac with a 13-cubic-yard debris tank and 8-inch boom suction, and a Vactor 2100 jetter for culvert and sewer cleaning.",
        extra_ld=[service_ld("Vacuum Excavation Equipment","Tornado F4 hydrovac and Vactor 2100 jetter trucks serving Interior Alaska.")])
    return h + page_hero("The fleet",
        "Purpose-built trucks. A perfect safety record.",
        "Every job runs on well-maintained, properly crewed equipment. Here is what shows up to your site.",
        "assets/img/hydrovac-4.jpg","Hydrovac Pro fleet of vacuum and jetter trucks") + f"""
<section class="fleet-detail">
  <div class="wrap">
    <article class="unit reveal" id="tornado-f4">
      <div class="unit-media"><img src="assets/img/hydrovac.jpg" alt="Tornado F4 hydrovac truck with Hydrovac Pro Dig Safe branding" loading="lazy" width="1700" height="1275"><span class="unit-tag">Hydrovac</span></div>
      <div class="unit-copy">
        {eyebrow('Vacuum excavation')}
        <h2>Tornado F4 Hydrovac</h2>
        <p>Our primary excavation truck cuts soil with pressurized water and vacuums it straight into a 13-cubic-yard debris tank through an 8-inch boom-mounted hose. It transports itself, performs the dig, and hauls the spoil, so one unit replaces a backhoe, a crew, and a dump truck while removing strike risk entirely. Hot-water capability lets it work frozen ground that stops mechanical equipment.</p>
        {tornado}
      </div>
    </article>
    <article class="unit flip reveal" id="vactor-2100">
      <div class="unit-media"><img src="assets/img/jetter.jpg" alt="Vactor 2100 combination jetter truck" loading="lazy" width="1700" height="1096"><span class="unit-tag">Jetter</span></div>
      <div class="unit-copy">
        {eyebrow('Jetting & cleaning')}
        <h2>Vactor 2100 Jetter</h2>
        <p>The Vactor 2100 is a combination jetter and vacuum truck built for culverts, storm drains, and sewer mains. High-pressure water scours lines clean while the vacuum recovers silt, debris, and ice. It is the workhorse behind our culvert maintenance, catch-basin cleanout, and municipal service programs.</p>
        {vactor}
      </div>
    </article>
  </div>
</section>

<section class="capabilities">
  <div class="wrap">
    <div class="sec-head center">
      {eyebrow('Why it matters')}
      <h2>What this fleet means for your project</h2>
    </div>
    <div class="cap-grid">
      <div class="cap reveal"><span class="svc-ic">{icon('shield')}</span><h3>No strike risk</h3><p>Water and vacuum cannot cut, crush, or nick a buried line the way a blade or auger can.</p></div>
      <div class="cap reveal"><span class="svc-ic">{icon('gauge')}</span><h3>One unit, many machines</h3><p>Dig, load, and haul in a single pass. Fewer machines and less labor on your site.</p></div>
      <div class="cap reveal"><span class="svc-ic">{icon('snow')}</span><h3>Works the Alaska winter</h3><p>Hot water cuts frost and permafrost so projects keep moving year round.</p></div>
      <div class="cap reveal"><span class="svc-ic">{icon('leaf')}</span><h3>Cleaner sites</h3><p>Contained spoil, less over-dig, and proper off-site disposal of recovered material.</p></div>
    </div>
  </div>
</section>
""" + tail()

# ------------------------------------------------------------------ INDUSTRIES
def page_industries():
    INDS = [
      ("utility","Utilities &amp; Telecom","Power, gas, water, sewer, and fiber operators rely on us to daylight and verify lines before any disturbance. We pothole around energized and pressurized infrastructure so your crews and your network stay safe."),
      ("gov","Government &amp; Municipal","DOT, FAA, boroughs, and agencies trust Hydrovac Pro for culvert maintenance, vault toilet and tank thawing, utility verification, and public-bid projects with the documentation procurement requires."),
      ("mine","Mining &amp; Resource","Exposing buried infrastructure, cleaning sumps and service pits, and supporting exploration and site work, all without putting a blade near a critical line."),
      ("oil","Oil, Gas &amp; Pipeline","From North Dakota oil fields to Alaska pads and corridors, we daylight pipelines, support tie-ins, clean tanks, and respond to spills with experienced, compliant crews."),
      ("build","Construction &amp; GC","General contractors use us to verify utilities before excavation, slot trench for conduit, and keep projects on schedule by avoiding the delays and fines a strike brings."),
      ("leaf","Environmental &amp; Industrial","Spill response, liquid recovery, tank and pit cleanouts, and cleanup support for industrial facilities and environmental contractors across the Interior."),
    ]
    cards = ""
    for ic,title,desc in INDS:
        cards += f"""<article class="ind-card reveal">
          <span class="svc-ic">{icon(ic)}</span>
          <h3>{title}</h3>
          <p>{e(desc)}</p>
        </article>"""
    h = head("industries.html",
        "Industries | Utilities, Government, Mining, Oil & Gas | Hydrovac Pro",
        "Hydrovac Pro serves utilities, government and municipal agencies, mining, oil and gas, construction, and environmental clients with safe hydro excavation and vacuum services across Alaska.")
    return h + page_hero("Who we serve",
        "Built for the work that cannot afford a mistake",
        "Utilities, agencies, mines, and industrial operators choose Hydrovac Pro because a strike-free record is not a marketing line. It is how we run every job.",
        "assets/img/daylighting.jpg","Hydrovac Pro daylighting utilities for an Alaska client") + f"""
<section class="ind-cards"><div class="wrap"><div class="ind-grid">{cards}</div>
  <div class="gov-cta">
    <div>
      <h3>Government buyer or prime contractor?</h3>
      <p>Our capability statement has the legal entity, codes, point of contact, and registrations your team needs to put us on a solicitation.</p>
    </div>
    <a class="btn btn-orange" href="contact.html#capability-statement">View capability statement {icon('arrow')}</a>
  </div>
</div></section>

<section class="band-quote">
  <div class="wrap">
    <p class="bq">"Customer and contractor becoming one."</p>
    <span>The standard behind every bid we hand you and every site we leave.</span>
  </div>
</section>
""" + tail()

# ------------------------------------------------------------------ ABOUT
def page_about():
    certs = [
      ("shield","Licensed, Bonded &amp; Insured","Full coverage with certificates of insurance and W-9 available on request."),
      ("check","OSHA Compliant","Safety-first crews and procedures on every job site."),
      ("truck","DOT Registered","Federal and Alaska DOT registered for commercial operation."),
      ("doc","Public Bid Ready","Experienced with IFB, RFP, and subcontract documentation."),
    ]
    cert_html = "".join(
      f'<div class="cert reveal"><span class="svc-ic">{icon(ic)}</span><div><h3>{t}</h3><p>{e(d)}</p></div></div>'
      for ic,t,d in certs)
    h = head("about.html",
        "About | 13 Years of Safe Hydro Excavation in Alaska | Hydrovac Pro",
        "Hydrovac Pro is a Fairbanks-based hydro excavation and vacuum truck company with 13 years of experience in Alaska's Arctic and the North Dakota oil fields, and a perfect safety record.")
    return h + page_hero("Our story",
        "Thirteen years of digging the safe way",
        "A Fairbanks company built on precision, safety, and showing up when the work is hard.",
        "assets/img/hydrovac-2.jpg","Hydrovac Pro truck and crew in Fairbanks, Alaska") + f"""
<section class="about-story">
  <div class="wrap about-in">
    <div class="about-copy reveal">
      {eyebrow('Who we are')}
      <h2>Precision, safety, and efficiency on the hardest ground in the country</h2>
      <p>Hydrovac Pro is based in Fairbanks, Alaska, with 13 years of experience across Alaska's Arctic and the oil fields of North Dakota. We built the company around a single idea: there is a safer, cleaner, smarter way to dig near the utilities and infrastructure that everything else depends on.</p>
      <p>Hydro excavation lets us break up soil with water and vacuum it away, exposing buried lines without ever risking a strike. Our Vactor 2100 jetter keeps culverts and sewers flowing. Together, that fleet does the work of several machines while protecting your people, your network, and your budget.</p>
      <p>We answer the phone, we show up prepared, and we treat your project like our own. Clients tell us we will work all night to get the job done. That is the reputation we have earned, and the one we protect on every call.</p>
    </div>
    <div class="about-media reveal">
      <img src="assets/img/truck-worker.jpg" alt="Hydrovac Pro technician beside the Dig Safe vacuum truck" loading="lazy" width="1125" height="1500">
    </div>
  </div>
</section>

<section class="safety-band">
  <div class="hazard"></div>
  <div class="wrap safety-in">
    <div class="safety-copy">
      {eyebrow('Safety', light=True)}
      <h2>A perfect safety record is the whole point</h2>
      <p>Every dig starts with confirmed locates and a dig-safe plan. Our equipment cannot cut or crush a buried line the way mechanical excavation can, and our crews are trained to treat every line as live. The result is zero utility strikes and the eco-friendly, low-impact sites our clients expect.</p>
      <ul class="ticklist light">
        <li>{icon('check')}Confirmed utility locates before every dig</li>
        <li>{icon('check')}OSHA-compliant procedures and trained operators</li>
        <li>{icon('check')}Non-destructive method with no strike risk</li>
        <li>{icon('check')}Contained spoil and responsible disposal</li>
      </ul>
    </div>
    <div class="safety-stat">
      <div class="big-stat"><span translate="no">0</span><small>Utility strikes</small></div>
      <div class="big-stat"><span translate="no">13</span><small>Years of experience</small></div>
    </div>
  </div>
</section>

<section class="certs">
  <div class="wrap">
    <div class="sec-head center">
      {eyebrow('Credentials')}
      <h2>Ready to work, ready to bid</h2>
      <p class="lead">Everything procurement and safety teams need to bring us on.</p>
    </div>
    <div class="cert-grid">{cert_html}</div>
  </div>
</section>
""" + tail()

# ------------------------------------------------------------------ CONTACT
def capability_statement():
    def card(ic, title, rows):
        items = "".join(
            f'<div class="cap-row"><dt>{e(l)}</dt><dd>{v}</dd></div>' for l, v in rows)
        return (f'<div class="cap-card reveal"><h3><span class="svc-ic">{icon(ic)}</span>{title}</h3>'
                f'<dl class="cap-dl">{items}</dl></div>')

    naics = "".join(
        f'<li><b translate="no">{c}</b> {e(d)}'
        f'{" <span class=cap-primary>Primary</span>" if c==NAICS_PRIMARY else ""}</li>'
        for c, d in NAICS_CODES)
    comp = ["Hydro excavation, daylighting & potholing","Slot trenching & utility verification",
            "Vactor 2100 jetter, culvert & sewer cleaning","Tank, sump & service-pit cleanouts",
            "Frozen-ground & permafrost excavation","Emergency, spill & after-hours response"]
    comp_html = "".join(f'<li>{icon("check")}{e(c)}</li>' for c in comp)

    company = card("gov", "Company", [
        ("Legal entity", f'<span translate="no">{e(LEGAL_NAME)}</span>'),
        ("Doing business as", f'<span translate="no">{e(DBA_NAME)}</span>'),
        ("Structure", "Limited Liability Company (Alaska, est. 2022)"),
        ("AK business license", f'<span translate="no">#{e(AK_LICENSE)}</span>'),
        ("AK entity number", f'<span translate="no">{e(AK_ENTITY)}</span>'),
        ("State status", f'{e(ENTITY_STATUS)}'),
    ])
    codes = card("doc", "Federal registrations &amp; codes", [
        ("CAGE code", f'<span translate="no">{e(CAGE_CODE)}</span>'),
        ("UEI (SAM.gov)", f'<span translate="no">{e(UEI_CODE)}</span>'),
        ("USDOT number", f'<span translate="no">{e(USDOT_NUMBER)}</span>'),
        ("NAICS codes", f'<ul class="cap-naics">{naics}</ul>'),
    ])
    poc = card("phone", "Point of contact", [
        ("Name", f'<span translate="no">{e(POC_NAME)}</span>'),
        ("Title", e(POC_TITLE)),
        ("Email", f'<a href="mailto:{POC_EMAIL}" translate="no">{POC_EMAIL}</a>'),
        ("Phone", f'<a href="tel:{PHONE_TEL}" translate="no">{PHONE_DISPLAY}</a>'),
    ])
    addr = card("pin", "Addresses", [
        ("Physical", f'<span translate="no">{ADDR_STREET}<br>{ADDR_CITY}, {ADDR_STATE} {ADDR_ZIP}</span>'),
        ("Mailing", f'<span translate="no">{e(MAILING_ADDR)}</span>'),
        ("Service area", "Interior Alaska, the North Slope &amp; statewide on contract"),
    ])
    return f"""
<section class="capstmt" id="capability-statement">
  <div class="wrap">
    <div class="sec-head center">
      {eyebrow('For government & prime contractors')}
      <h2>Capability Statement</h2>
      <p class="lead">The back-office details agencies, primes, and procurement teams need to add Hydrovac Pro to a solicitation, purchase order, or subcontract.</p>
    </div>
    <div class="cap-grid">{company}{codes}{poc}{addr}</div>
    <div class="cap-foot">
      <div class="cap-comp">
        <h3>Core competencies</h3>
        <ul class="ticklist">{comp_html}</ul>
      </div>
      <div class="cap-note">
        <h3>On request</h3>
        <p>W-9, certificate of insurance, references and past performance, bonding capacity, and our full capability statement are available to qualified buyers.</p>
        <div class="cap-cta">
          <a class="btn btn-orange" href="mailto:{POC_EMAIL}?subject=Capability%20statement%20request">{icon('mail')} Email {POC_NAME.split()[0]}</a>
          <a class="btn btn-outline" href="tel:{PHONE_TEL}">{icon('phone')} {PHONE_DISPLAY}</a>
        </div>
      </div>
    </div>
    <p class="cap-cert">Licensed, bonded &amp; insured · OSHA compliant · DOT registered · Small business · Fairbanks, Alaska</p>
  </div>
</section>"""

def page_contact():
    map_q = "300 Barnette St, Fairbanks, AK 99701"
    h = head("contact.html",
        "Contact & Request a Bid | Hydrovac Pro | Fairbanks, Alaska",
        "Request a hydro excavation or vacuum truck bid from Hydrovac Pro in Fairbanks, Alaska. Call (907) 759-8068 or send your project scope. Emergency and after-hours response available.")
    return h + f"""
<section class="contact-hero">
  <div class="phero-shade"></div>
  <div class="wrap">
    {eyebrow('Get in touch', light=True)}
    <h1>Request a bid</h1>
    <p class="lead">Tell us about the project. We return competitive, no-obligation pricing fast, and we answer emergency calls around the clock.</p>
  </div>
</section>

<section class="contact-sec">
  <div class="wrap contact-grid">
    <div class="contact-info">
      <div class="ci reveal"><span class="svc-ic">{icon('phone')}</span><div><h3>Call or text</h3><a href="tel:{PHONE_TEL}" translate="no">{PHONE_DISPLAY}</a><p>Emergency &amp; after-hours response available</p></div></div>
      <div class="ci reveal"><span class="svc-ic">{icon('mail')}</span><div><h3>Email</h3><a href="mailto:{EMAIL}" translate="no">{EMAIL}</a><p>Scopes, plans, and bid documents welcome</p></div></div>
      <div class="ci reveal"><span class="svc-ic">{icon('pin')}</span><div><h3>Office</h3><a href="{GMAPS}" target="_blank" rel="noopener" translate="no">{ADDR_STREET}<br>{ADDR_CITY}, {ADDR_STATE} {ADDR_ZIP}</a><p>Serving Interior Alaska &amp; the North Slope</p></div></div>
      <div class="ci reveal"><span class="svc-ic">{icon('clock')}</span><div><h3>Hours</h3><p translate="no">Monday to Friday, 8a to 5p<br>Emergency response 24/7</p></div></div>
      <div class="ci-social">
        <a class="btn btn-outline" href="{GREVIEWS}" target="_blank" rel="noopener">{icon('star')} Google reviews</a>
        <a class="btn btn-outline" href="{FACEBOOK}" target="_blank" rel="noopener">{icon('fb')} Facebook</a>
      </div>
    </div>

    <div class="contact-form-wrap reveal">
      <form id="bidForm" class="bidform" action="https://formsubmit.co/{EMAIL}" method="POST" enctype="multipart/form-data" novalidate>
        <input type="hidden" name="_subject" value="New bid request from hydrovacpro.com">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
        <h2>Project details</h2>
        <div class="frow">
          <label>Name<span>*</span><input type="text" name="name" required></label>
          <label>Company<input type="text" name="company"></label>
        </div>
        <div class="frow">
          <label>Phone<span>*</span><input type="tel" name="phone" required></label>
          <label>Email<span>*</span><input type="email" name="email" required></label>
        </div>
        <label>Project type
          <select name="project_type">
            <option>Daylighting / Potholing</option>
            <option>Slot Trenching</option>
            <option>Jetter / Culvert Cleaning</option>
            <option>Tank / Pit Cleanout</option>
            <option>Frozen Ground / Thawing</option>
            <option>Emergency / Spill Response</option>
            <option>Other / Not sure</option>
          </select>
        </label>
        <label>Job site location<input type="text" name="location" placeholder="City or address"></label>
        <label>Tell us about the project<span>*</span>
          <textarea name="message" rows="5" required placeholder="Scope, timeline, depth, access, and anything else we should know."></textarea>
        </label>
        <label class="upload" id="drop">
          <input type="file" name="attachments" accept="image/*,application/pdf" multiple>
          <span class="upload-cta">{icon('doc')} Attach site photos or bid documents</span>
          <span class="upload-hint">Images or PDF, optional</span>
          <span class="upload-files" id="files"></span>
        </label>
        <button type="submit" class="btn btn-orange btn-lg btn-block">Send bid request {icon('arrow')}</button>
        <p class="form-note">By submitting you agree to be contacted about your request. We never share your information.</p>
        <p class="form-status" id="formStatus" role="status"></p>
      </form>
    </div>
  </div>
</section>

{capability_statement()}

<section class="map-sec">
  <iframe title="Hydrovac Pro location map" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
    src="https://www.google.com/maps?q={map_q.replace(' ','+').replace(',','%2C')}&output=embed"></iframe>
</section>
""" + tail()

# ------------------------------------------------------------------ static files
def robots():
    return f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n"

def sitemap():
    today = datetime.date.today().isoformat()
    urls = ""
    for href,_ in NAV:
        loc = SITE + "/" + ("" if href=="index.html" else href)
        pr = "1.0" if href=="index.html" else "0.8"
        urls += f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>{pr}</priority></url>\n"
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+urls+'</urlset>\n'

def manifest():
    return _json.dumps({
      "name":NAME,"short_name":"Hydrovac Pro","start_url":"/","display":"standalone",
      "background_color":"#0b182b","theme_color":"#0b182b",
      "icons":[
        {"src":"assets/img/favicon-192.png","sizes":"192x192","type":"image/png"},
        {"src":"assets/img/favicon-512.png","sizes":"512x512","type":"image/png"}
      ]
    }, indent=2)

def page_404():
    h = head("404.html","Page not found | Hydrovac Pro",
             "That page could not be found. Return to Hydrovac Pro for hydro excavation and vacuum services in Fairbanks, Alaska.")
    return h + f"""
<section class="notfound"><div class="wrap">
  <span class="big404" translate="no">404</span>
  <h1>That page went off the grid</h1>
  <p class="lead">The page you were looking for is not here. Let us point you back to solid ground.</p>
  <div class="hero-cta">
    <a class="btn btn-orange btn-lg" href="index.html">Back to home {icon('arrow')}</a>
    <a class="btn btn-outline btn-lg" href="contact.html">Request a Bid</a>
  </div>
</div></section>
""" + tail()

# ------------------------------------------------------------------ build
def write(path, content):
    with open(os.path.join(HERE, path), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)

def main():
    write("index.html",      page_index())
    write("services.html",   page_services())
    write("equipment.html",  page_equipment())
    write("industries.html", page_industries())
    write("about.html",      page_about())
    write("contact.html",    page_contact())
    write("404.html",        page_404())
    write("robots.txt",      robots())
    write("sitemap.xml",     sitemap())
    write("site.webmanifest",manifest())
    print("Build complete.")

if __name__ == "__main__":
    main()


