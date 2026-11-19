"""Génère le site statique ReFrame 4Impact (FR/EN) à partir de la maquette validée.
Usage : python3 build.py <maquette.html> <dossier_sortie>"""
import sys, os, re, copy, shutil
from bs4 import BeautifulSoup

SRC, OUT = sys.argv[1], sys.argv[2]
DOMAIN = "https://reframe4impact.com"
CAL = "https://calendly.com/houda-eljoundi-reframe4impact/30min"
PAGES = [  # id dans la maquette, slug FR, slug EN, titres
  ("accueil",   "",           "",          "ReFrame 4Impact · Conseil ESG et durabilité", "ReFrame 4Impact · ESG & sustainability consulting"),
  ("expertises","expertises", "services",  "Expertises · ReFrame 4Impact", "Services · ReFrame 4Impact"),
  ("methode",   "methode",    "approach",  "Méthode · ReFrame 4Impact", "Approach · ReFrame 4Impact"),
  ("academie",  "academie",   "academy",   "L'Académie 4Impact · ReFrame 4Impact", "4Impact Academy · ReFrame 4Impact"),
  ("contact",   "contact",    "contact",   "Contact · ReFrame 4Impact", "Contact · ReFrame 4Impact"),
]
DESC = {
 "fr": "ReFrame 4Impact accompagne les entreprises et les organisations au Maroc et en France : reporting ESG, bilan carbone, économie circulaire, formation. Changer de regard, accélérer l'impact.",
 "en": "ReFrame 4Impact supports companies and organizations in Morocco and France: ESG reporting, carbon footprint, circular economy, training. Shifting perspectives, driving impact.",
}
EXTRA = {"mentions-legales": ("mentions-legales", "legal-notice"), "confidentialite": ("confidentialite", "privacy")}
def url(lang, pid):
    if pid in EXTRA:
        return f"/{lang}/" + EXTRA[pid][0 if lang == "fr" else 1] + "/"
    for p in PAGES:
        if p[0] == pid:
            slug = p[1] if lang == "fr" else p[2]
            return f"/{lang}/" + (slug + "/" if slug else "")
    raise KeyError(pid)

raw = open(SRC, encoding="utf-8").read()
src = BeautifulSoup(raw, "lxml")
css = src.find("style").string
# Le site n'a plus besoin du routage par #ancre ni du bandeau « maquette »
css = css.replace("section.page{display:none}", "section.page{display:block}")
svgdefs = str(src.find("svg", attrs={"style": "position:absolute"}))

os.makedirs(f"{OUT}/assets", exist_ok=True)
open(f"{OUT}/assets/style.css", "w").write(css.strip() + "\n.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}\n.hp{display:none}\n")

def localise(node, lang):
    other = "en" if lang == "fr" else "fr"
    for el in node.find_all(class_=other):
        el.decompose()
    for el in node.find_all(class_=lang):
        if el.name == "span" and el.get("class") == [lang]:
            el.unwrap()
        else:
            el["class"] = [c for c in el["class"] if c != lang] or None
            if el.get("class") is None: del el["class"]

def fix_links(node, lang):
    for a in node.find_all("a", href=True):
        h = a["href"]
        if h.startswith("#"):
            a["href"] = url(lang, h[1:] or "accueil")

def build_page(pid, lang, slug_fr, slug_en, title):
    soup = BeautifulSoup(raw, "lxml")
    header = soup.find("header", class_="top")
    footer = soup.find("footer")
    section = soup.find("section", attrs={"data-page": pid})
    section["class"] = ["page", "on"]
    # sélecteur de langue -> liens
    langbox = header.find(class_="lang")
    new = soup.new_tag("nav", attrs={"class": "lang", "aria-label": "Langue / Language"})
    for l in ("fr", "en"):
        a = soup.new_tag("a", href=url(l, pid), hreflang=l, lang=l)
        a.string = l.upper()
        if l == lang: a["aria-current"] = "true"
        new.append(a)
    langbox.replace_with(new)
    # formulaire de contact réel (Netlify Forms)
    form = section.find("form")
    if form:
        form.attrs = {"class": ["ccard"], "id": "form", "name": "contact", "method": "POST",
                      "action": url(lang, "contact") + "merci/", "data-netlify": "true",
                      "netlify-honeypot": "bot-field"}
        hidden = soup.new_tag("input", type="hidden", attrs={"name": "form-name", "value": "contact"})
        hp = BeautifulSoup('<p class="hp"><label>Ne pas remplir <input name="bot-field"></label></p>', "html.parser")
        form.insert(0, hidden); form.insert(1, hp)
        org = form.find("label", attrs={"for": "f-org"})
        email = BeautifulSoup(f'<label for="f-email"><span class="fr">Email professionnel</span><span class="en">Work email</span><input id="f-email" name="email" type="email" autocomplete="email" required></label>', "html.parser")
        org.insert_after(email)
        form.find(id="f-name")["required"] = ""
        form.find(id="f-msg")["required"] = ""
        ok = form.find(id="ok")
        if ok: ok.decompose()
        note = BeautifulSoup('<p class="note"><span class="fr">Vos informations servent uniquement à vous répondre.</span><span class="en">Your details are only used to reply to you.</span></p>', "html.parser")
        form.append(note)
    for el in (header, footer, section):
        localise(el, lang); fix_links(el, lang)
    for a in header.select("nav.main a"):
        if a["href"] == url(lang, pid): a["aria-current"] = "page"
    alt = {l: DOMAIN + url(l, pid) for l in ("fr", "en")}
    page = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{DESC[lang]}">
<link rel="canonical" href="{alt[lang]}">
<link rel="alternate" hreflang="fr" href="{alt['fr']}">
<link rel="alternate" hreflang="en" href="{alt['en']}">
<link rel="alternate" hreflang="x-default" href="{alt['fr']}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{DESC[lang]}">
<meta property="og:url" content="{alt[lang]}">
<meta property="og:locale" content="{'fr_FR' if lang=='fr' else 'en_GB'}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=Manrope:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
{svgdefs}
{header}
<main>
{section}
</main>
{footer}
<script src="/assets/site.js" defer></script>
</body>
</html>
"""
    out = OUT + url(lang, pid)
    os.makedirs(out, exist_ok=True)
    open(out + "index.html", "w", encoding="utf-8").write(page)
    return page

for pid, sfr, sen, tfr, ten in PAGES:
    for lang, t in (("fr", tfr), ("en", ten)):
        build_page(pid, lang, sfr, sen, t)

# Page de remerciement après envoi du formulaire, et 404
def simple(lang, path, title, h1, p, cta_href, cta):
    base = open(OUT + url(lang, "contact") + "index.html", encoding="utf-8").read()
    s = BeautifulSoup(base, "lxml")
    s.title.string = title
    sec = s.find("section")
    sec.clear()
    body = f'<p style="margin-top:28px"><a class="btn btn-primary" href="{cta_href}">{cta}</a></p>' if cta else ""
    sec.append(BeautifulSoup(f'<div class="subhero"><div class="wrap"><h1>{h1}</h1>{p}{body}</div></div>', "html.parser"))
    s.find("meta", attrs={"name": "description"})
    for l in s.find_all("link", rel=["canonical", "alternate"]): l.decompose()
    rob = s.new_tag("meta", attrs={"name": "robots", "content": "noindex"}); s.head.append(rob)
    os.makedirs(os.path.dirname(OUT + path), exist_ok=True)
    open(OUT + path, "w", encoding="utf-8").write(str(s))
simple("fr", url("fr","contact")+"merci/index.html", "Message envoyé · ReFrame 4Impact", "Merci, votre message est bien parti.", "<p>Nous vous répondons au plus vite. Vous pouvez aussi réserver directement un échange de 30 minutes.</p>", CAL, "Réserver un échange")
simple("en", url("en","contact")+"merci/index.html", "Message sent · ReFrame 4Impact", "Thank you, your message has been sent.", "<p>We will get back to you shortly. You can also book a 30-minute call directly.</p>", CAL, "Book a call")
simple("fr", "/404.html", "Page introuvable · ReFrame 4Impact", "Cette page n'existe pas.", "<p>Le lien est peut-être ancien. Repartez de l'accueil.</p>", "/fr/", "Retour à l'accueil")

ICE = "003811145000080"
NETLIFY = "Netlify, Inc., 512 2nd Street, Suite 200, San Francisco, CA 94107, États-Unis"
legal_fr = f"""<div class="legal"><h2>Éditeur du site</h2><p>ReFrame 4Impact, société à responsabilité limitée à associé unique (SARL AU) au capital de 100 000 MAD<br>Siège social : 5 rue Daraa, Résidence Fatima Zahra, Appt n° 5, Agdal, Rabat, Maroc (société domiciliée chez Logic Accounting SARL)<br>RC Rabat n° 191093<br>ICE : {ICE}<br>Responsable de la publication : la gérance de ReFrame 4Impact<br>Contact : contact@reframe4impact.com</p>
<h2>Hébergement</h2><p>{NETLIFY}</p>
<h2>Propriété intellectuelle</h2><p>Les textes, le logo et les éléments graphiques de ce site appartiennent à ReFrame 4Impact. Toute reproduction sans autorisation écrite est interdite.</p></div>"""
legal_en = f"""<div class="legal"><h2>Publisher</h2><p>ReFrame 4Impact, single-member limited liability company (SARL AU) with a share capital of MAD 100,000<br>Registered office: 5 rue Daraa, Résidence Fatima Zahra, Appt 5, Agdal, Rabat, Morocco (domiciled with Logic Accounting SARL)<br>Rabat Trade Register (RC) no. 191093<br>ICE: {ICE}<br>Publication manager: the management of ReFrame 4Impact<br>Contact: contact@reframe4impact.com</p>
<h2>Hosting</h2><p>{NETLIFY.replace('États-Unis','USA')}</p>
<h2>Intellectual property</h2><p>The text, logo and graphics on this site belong to ReFrame 4Impact. Reproduction without written permission is prohibited.</p></div>"""
priv_fr = """<div class="legal"><h2>Données collectées</h2><p>Quand vous utilisez le formulaire de contact, nous recevons votre nom, votre organisation, votre email, le sujet choisi et votre message. Ce site n'utilise pas de cookies de mesure d'audience ni de publicité.</p>
<h2>Utilisation</h2><p>Ces informations servent uniquement à répondre à votre demande. Elles ne sont ni vendues ni partagées à des fins commerciales.</p>
<h2>Prestataires</h2><p>Les messages du formulaire sont reçus via Netlify, notre hébergeur. La prise de rendez-vous se fait sur Calendly, qui applique sa propre politique de confidentialité.</p>
<h2>Conservation</h2><p>Nous conservons vos messages le temps nécessaire pour traiter votre demande et assurer le suivi de notre échange.</p>
<h2>Vos droits</h2><p>Vous pouvez demander l'accès, la rectification ou la suppression de vos données en écrivant à contact@reframe4impact.com, conformément à la loi marocaine 09-08 et au RGPD.</p></div>"""
priv_en = """<div class="legal"><h2>Data we collect</h2><p>When you use the contact form, we receive your name, organization, email, chosen topic and message. This site uses no analytics or advertising cookies.</p>
<h2>How we use it</h2><p>This information is only used to reply to your request. It is never sold or shared for marketing purposes.</p>
<h2>Service providers</h2><p>Form messages are received through Netlify, our hosting provider. Call booking happens on Calendly, which applies its own privacy policy.</p>
<h2>Retention</h2><p>We keep your messages for as long as needed to handle your request and follow up on our conversation.</p>
<h2>Your rights</h2><p>You can ask to access, correct or delete your data by writing to contact@reframe4impact.com, in line with Moroccan law 09-08 and the GDPR.</p></div>"""
simple("fr", url("fr","mentions-legales")+"index.html", "Mentions légales · ReFrame 4Impact", "Mentions légales", legal_fr, "", "")
simple("en", url("en","mentions-legales")+"index.html", "Legal notice · ReFrame 4Impact", "Legal notice", legal_en, "", "")
simple("fr", url("fr","confidentialite")+"index.html", "Confidentialité · ReFrame 4Impact", "Politique de confidentialité", priv_fr, "", "")
simple("en", url("en","confidentialite")+"index.html", "Privacy · ReFrame 4Impact", "Privacy policy", priv_en, "", "")
