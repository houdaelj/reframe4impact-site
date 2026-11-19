import re,sys
OUT=sys.argv[1]; DEFS=sys.argv[2]; DOMAIN="https://reframe4impact.com"
d=open(DEFS).read()
mark=re.search(r'<symbol id="r4i-mark" viewBox="([^"]*)">(.*?)</symbol>',d,re.S)
fav=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{mark.group(1)}"><style>.p-frame,.p-four{{fill:none;stroke:#123A31}}.p-ring{{fill:#C9B79A}}.p-leaf{{fill:#2E7D5B}}@media (prefers-color-scheme:dark){{.p-frame,.p-four{{stroke:#fff}}.p-ring{{fill:#C9B79A}}.p-leaf{{fill:#D7EDE0}}}}</style>{mark.group(2)}</svg>'''
open(OUT+'/assets/favicon.svg','w').write(fav)
open(OUT+'/index.html','w').write('''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>ReFrame 4Impact</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="https://reframe4impact.com/fr/">
<script>location.replace(/^en\\b/i.test(navigator.language||'')?'/en/':'/fr/');</script>
<meta http-equiv="refresh" content="0; url=/fr/"></head><body><a href="/fr/">Français</a> · <a href="/en/">English</a></body></html>''')
open(OUT+'/netlify.toml','w').write('''[build]
  publish = "."

# Visiteurs anglophones vers /en/, les autres vers /fr/
[[redirects]]
  from = "/"
  to = "/en/"
  status = 302
  conditions = {Language = ["en"]}

[[redirects]]
  from = "/"
  to = "/fr/"
  status = 302

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
''')
open(OUT+'/robots.txt','w').write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
paths=['', 'expertises/','methode/','academie/','contact/','mentions-legales/','confidentialite/']
en=['', 'services/','approach/','academy/','contact/','legal-notice/','privacy/']
urls=''.join(f'<url><loc>{DOMAIN}/fr/{a}</loc><xhtml:link rel="alternate" hreflang="fr" href="{DOMAIN}/fr/{a}"/><xhtml:link rel="alternate" hreflang="en" href="{DOMAIN}/en/{b}"/></url><url><loc>{DOMAIN}/en/{b}</loc><xhtml:link rel="alternate" hreflang="fr" href="{DOMAIN}/fr/{a}"/><xhtml:link rel="alternate" hreflang="en" href="{DOMAIN}/en/{b}"/></url>' for a,b in zip(paths,en))
open(OUT+'/sitemap.xml','w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">{urls}</urlset>\n')
css=open(OUT+'/assets/style.css').read()
css+='''.lang a{text-decoration:none;font:500 12px/1 var(--mono);padding:7px 9px;border-radius:999px;color:var(--muted)}
.lang a[aria-current="true"]{background:var(--ink);color:var(--paper)}
.lang a:hover{color:var(--ink)}
.legal{display:grid;gap:12px;max-width:68ch;margin-top:32px}
.legal h2{font-size:22px;margin-top:16px}
.legal p{color:var(--muted)}
.subhero .legal + p{display:none}
'''
open(OUT+'/assets/style.css','w').write(css)
