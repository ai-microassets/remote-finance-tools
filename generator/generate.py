"""
Remote Finance Tools — Page Generator
Reads data/keywords.json and creates new calculator pages in pages/
Only creates pages that don't already exist (protects manual edits).
Also updates sitemap.xml automatically.
"""

import json, os, re
from datetime import datetime, date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = os.path.join(BASE, "pages")
DATA  = os.path.join(BASE, "data", "keywords.json")
SITEMAP = os.path.join(BASE, "sitemap.xml")
DOMAIN = "https://remote-finance-tools.vercel.app"

SHARED_HEAD = """  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet" />
  <style>
    :root{--bg:#060912;--bg2:#0c1120;--surface:#0f1728;--s2:#162035;--border:#1e2d47;--b2:#243450;--accent:#10e8b8;--blue:#0ea5e9;--text:#eef2ff;--t2:#94a3c0;--t3:#4f6280;}
    *,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
    body{font-family:'Plus Jakarta Sans',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;}
    .glow{position:fixed;inset:0;z-index:0;pointer-events:none;background:radial-gradient(ellipse 50% 30% at 15% 10%,rgba(16,232,184,0.06),transparent 65%);}
    .grid-bg{position:fixed;inset:0;z-index:0;pointer-events:none;background-image:linear-gradient(rgba(16,232,184,0.02) 1px,transparent 1px),linear-gradient(90deg,rgba(16,232,184,0.02) 1px,transparent 1px);background-size:48px 48px;mask-image:radial-gradient(ellipse 100% 60% at 50% 0%,black 20%,transparent 75%);}
    .z{position:relative;z-index:1;}
    header{position:sticky;top:0;z-index:100;display:flex;align-items:center;justify-content:space-between;padding:0 2rem;height:60px;border-bottom:1px solid var(--border);backdrop-filter:blur(20px);background:rgba(6,9,18,0.82);}
    .logo{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:0.9rem;color:var(--accent);text-decoration:none;}
    .logo span{color:var(--t3);}
    nav a{color:var(--t2);text-decoration:none;font-size:0.8rem;font-weight:500;padding:0.35rem 0.7rem;border-radius:7px;transition:all 0.14s;}
    nav a:hover{color:var(--text);background:var(--s2);}
    main{max-width:760px;margin:0 auto;padding:3rem 1.5rem 5rem;}
    .breadcrumb{font-size:0.73rem;color:var(--t3);margin-bottom:2rem;}
    .breadcrumb a{color:var(--t3);text-decoration:none;}
    .page-tag{font-family:'JetBrains Mono',monospace;font-size:0.6rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--accent);background:rgba(16,232,184,0.07);border:1px solid rgba(16,232,184,0.15);padding:0.18rem 0.48rem;border-radius:4px;display:inline-block;margin-bottom:1rem;}
    h1{font-size:clamp(1.55rem,4vw,2.3rem);font-weight:800;line-height:1.12;letter-spacing:-0.03em;margin-bottom:0.7rem;}
    .subtitle{color:var(--t2);font-size:0.88rem;line-height:1.65;margin-bottom:2.2rem;}
    .card{background:var(--surface);border:1px solid var(--b2);border-radius:16px;padding:2rem;margin-bottom:1.5rem;}
    label{display:block;font-size:0.78rem;font-weight:600;color:var(--t2);margin-bottom:0.35rem;}
    input{width:100%;background:var(--bg2);border:1.5px solid var(--border);color:var(--text);font-family:'Plus Jakarta Sans',sans-serif;font-size:0.95rem;font-weight:600;padding:0.68rem 0.9rem;border-radius:9px;outline:none;transition:border-color 0.14s;margin-bottom:1.1rem;}
    input:focus{border-color:var(--accent);}
    .row{display:grid;grid-template-columns:1fr 1fr;gap:1rem;}
    @media(max-width:520px){.row{grid-template-columns:1fr;}}
    .btn{width:100%;background:var(--accent);color:var(--bg);font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;font-size:0.88rem;padding:0.78rem;border:none;border-radius:10px;cursor:pointer;box-shadow:0 0 20px rgba(16,232,184,0.2);transition:all 0.14s;}
    .btn:hover{transform:translateY(-1px);box-shadow:0 0 30px rgba(16,232,184,0.35);}
    .result{display:none;margin-top:1.5rem;background:var(--s2);border:1px solid var(--border);border-radius:12px;padding:1.5rem;position:relative;overflow:hidden;}
    .result::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--accent),var(--blue));}
    .result.show{display:block;}
    .r-main{font-family:'JetBrains Mono',monospace;font-size:2.4rem;font-weight:700;color:var(--accent);margin-bottom:0.2rem;}
    .r-lbl{font-size:0.7rem;color:var(--t3);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:1.2rem;}
    .bk{display:flex;flex-direction:column;gap:0;}
    .bk-row{display:flex;justify-content:space-between;font-size:0.8rem;padding:0.42rem 0;border-bottom:1px solid var(--border);}
    .bk-row:last-child{border:none;}
    .bk-row span:first-child{color:var(--t2);}
    .bk-row span:last-child{font-family:'JetBrains Mono',monospace;color:var(--text);}
    .aff{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.8rem;background:rgba(16,232,184,0.04);border:1px solid rgba(16,232,184,0.13);border-radius:11px;padding:1rem 1.4rem;margin:1.8rem 0;}
    .aff strong{font-size:0.84rem;}.aff p{font-size:0.73rem;color:var(--t2);margin-top:0.1rem;}
    .aff a{background:var(--accent);color:var(--bg);font-weight:700;font-size:0.73rem;padding:0.42rem 0.9rem;border-radius:7px;text-decoration:none;white-space:nowrap;flex-shrink:0;transition:opacity 0.14s;}
    .aff a:hover{opacity:0.85;}
    .content{margin-top:2.5rem;}
    .content h2{font-size:1.1rem;font-weight:700;margin-bottom:0.65rem;margin-top:2rem;}
    .content p{color:var(--t2);font-size:0.83rem;line-height:1.75;margin-bottom:0.85rem;}
    .faq-item{border-bottom:1px solid var(--border);padding:0.9rem 0;}
    .faq-item strong{font-size:0.86rem;display:block;margin-bottom:0.32rem;}
    .faq-item p{color:var(--t2);font-size:0.8rem;line-height:1.6;margin:0;}
    footer{border-top:1px solid var(--border);padding:1.5rem;text-align:center;color:var(--t3);font-size:0.72rem;}
    footer a{color:var(--t3);text-decoration:none;}footer a:hover{color:var(--accent);}
  </style>"""


def slugify(text):
    return re.sub(r"[^a-z0-9-]", "", text.lower().replace(" ", "-"))


def title_case(slug):
    return slug.replace("-", " ").replace(".html", "").title()


def detect_tax_rate(keyword):
    kw = keyword.lower()
    if "portugal" in kw or "pt " in kw:  return 0.25
    if "uk" in kw or "britain" in kw:    return 0.28
    if "germany" in kw or "german" in kw: return 0.35
    if "france" in kw or "french" in kw:  return 0.30
    if "spain" in kw or "spanish" in kw:  return 0.28
    if "brazil" in kw or "brasil" in kw:  return 0.27
    return 0.25


def generate_page(keyword):
    tax = detect_tax_rate(keyword)
    title_str = title_case(keyword)
    slug = slugify(keyword) + ".html"
    is_rate = any(w in keyword.lower() for w in ["rate","hourly","daily","pricing"])
    is_tax  = any(w in keyword.lower() for w in ["tax","irs","vat","nI"])
    is_income = any(w in keyword.lower() for w in ["income","net","salary","earn"])

    if is_rate or is_income:
        calc_type = "income"
    elif is_tax:
        calc_type = "tax"
    else:
        calc_type = "general"

    if calc_type == "income":
        form_html = f"""    <div class="row">
      <div>
        <label>Monthly Amount (€/$)</label>
        <input type="number" id="v1" placeholder="3000" value="3000" oninput="run()" />
      </div>
      <div>
        <label>Hours per Week</label>
        <input type="number" id="v2" placeholder="25" value="25" oninput="run()" />
      </div>
    </div>
    <label>Tax Rate (%)</label>
    <input type="number" id="v3" placeholder="{int(tax*100)}" value="{int(tax*100)}" oninput="run()" />
    <button class="btn" onclick="run()">Calculate</button>
    <div class="result" id="result">
      <div class="r-main" id="rMain">—</div>
      <div class="r-lbl" id="rLbl">Result</div>
      <div class="bk">
        <div class="bk-row"><span>Monthly amount</span><span id="b1">—</span></div>
        <div class="bk-row"><span>Annual gross</span><span id="b2">—</span></div>
        <div class="bk-row"><span>Tax ({int(tax*100)}%)</span><span id="b3">—</span></div>
        <div class="bk-row"><span>Hourly rate</span><span id="b4">—</span></div>
      </div>
    </div>"""
        script = f"""function fmt(n){{return'€'+n.toFixed(2).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g,',');}}
function run(){{
  var v1=parseFloat(document.getElementById('v1').value)||0;
  var v2=parseFloat(document.getElementById('v2').value)||1;
  var tax=parseFloat(document.getElementById('v3').value)/100||{tax};
  var annGross=(v1*12)/(1-tax);
  var taxAmt=annGross*tax;
  var hrs=v2*46;
  var rate=annGross/hrs;
  document.getElementById('rMain').textContent=fmt(rate)+'/hr';
  document.getElementById('rLbl').textContent='Estimated hourly rate';
  document.getElementById('b1').textContent=fmt(v1)+'/mo';
  document.getElementById('b2').textContent=fmt(annGross);
  document.getElementById('b3').textContent=fmt(taxAmt);
  document.getElementById('b4').textContent=fmt(rate)+'/hr';
  document.getElementById('result').classList.add('show');
}}
run();"""
    else:
        form_html = f"""    <label>Annual Income (€/$)</label>
    <input type="number" id="v1" placeholder="40000" value="40000" oninput="run()" />
    <label>Expenses (€/$)</label>
    <input type="number" id="v2" placeholder="3000" value="3000" oninput="run()" />
    <button class="btn" onclick="run()">Calculate</button>
    <div class="result" id="result">
      <div class="r-main" id="rMain">—</div>
      <div class="r-lbl" id="rLbl">Estimated net</div>
      <div class="bk">
        <div class="bk-row"><span>Gross</span><span id="b1">—</span></div>
        <div class="bk-row"><span>Expenses</span><span id="b2">—</span></div>
        <div class="bk-row"><span>Tax ({int(tax*100)}%)</span><span id="b3">—</span></div>
        <div class="bk-row"><span>Net</span><span id="b4">—</span></div>
      </div>
    </div>"""
        script = f"""function fmt(n){{return'€'+n.toFixed(0).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g,',');}}
function run(){{
  var gross=parseFloat(document.getElementById('v1').value)||0;
  var exp=parseFloat(document.getElementById('v2').value)||0;
  var tax={tax};
  var taxable=gross-exp;
  var taxAmt=taxable*tax;
  var net=taxable-taxAmt;
  document.getElementById('rMain').textContent=fmt(net);
  document.getElementById('rLbl').textContent='Estimated annual net income';
  document.getElementById('b1').textContent=fmt(gross);
  document.getElementById('b2').textContent=fmt(exp);
  document.getElementById('b3').textContent=fmt(taxAmt);
  document.getElementById('b4').textContent=fmt(net);
  document.getElementById('result').classList.add('show');
}}
run();"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title_str} — Remote Finance Tools</title>
  <meta name="description" content="Free {title_str.lower()} for freelancers and remote workers. Instant results, no signup required." />
  <link rel="canonical" href="{DOMAIN}/pages/{slug}" />
{SHARED_HEAD}
</head>
<body>
<div class="glow"></div><div class="grid-bg"></div>
<header class="z">
  <a class="logo" href="../index.html">rft<span>_tools</span></a>
  <nav><a href="../index.html">← All Tools</a></nav>
</header>
<main class="z">
  <div class="breadcrumb"><a href="../index.html">Home</a> / {title_str}</div>
  <span class="page-tag">CALCULATOR · 2025</span>
  <h1>{title_str}</h1>
  <p class="subtitle">Free tool for freelancers and remote workers. Enter your numbers to get instant, accurate results.</p>
  <div class="card">
{form_html}
  </div>
  <div class="aff">
    <div>
      <strong>Working with international clients?</strong>
      <p>Wise saves you money on every transfer — open free in 2 minutes.</p>
    </div>
    <a href="https://wise.com/?utm_source=remotefinancetools" target="_blank" rel="nofollow sponsored">Open Wise →</a>
  </div>
  <div class="content">
    <h2>About this calculator</h2>
    <p>This {title_str.lower()} helps freelancers and remote workers get accurate financial estimates without needing a spreadsheet or accountant for every decision. Whether you're pricing a new client, comparing contract options, or planning your year, having the right numbers makes a measurable difference to your income.</p>
    <p>All calculations are instant and run in your browser. No data is sent to any server. No signup, no tracking, no ads blocking your screen.</p>
    <h2>Frequently asked questions</h2>
    <div class="faq-item">
      <strong>How accurate are these estimates?</strong>
      <p>They're reliable as planning tools but not legal or tax advice. Tax rates and rules vary by country, year, and individual circumstances. For binding decisions, confirm with a local accountant.</p>
    </div>
    <div class="faq-item">
      <strong>Is my data stored?</strong>
      <p>No. All calculations happen in your browser and nothing is ever sent to a server. You can verify this by using the tool offline.</p>
    </div>
    <div class="faq-item">
      <strong>Which countries does this cover?</strong>
      <p>The general calculators work worldwide. For country-specific tools (Portugal, UK), see the dedicated calculators linked from the homepage.</p>
    </div>
  </div>
</main>
<footer class="z"><p>© 2025 <a href="../index.html">Remote Finance Tools</a> · <a href="../sitemap.xml">Sitemap</a></p></footer>
<script>
{script}
</script>
</body>
</html>"""


def update_sitemap(page_slugs):
    today = date.today().isoformat()
    urls = [f"""  <url>
    <loc>{DOMAIN}/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>"""]
    for slug in sorted(page_slugs):
        urls.append(f"""  <url>
    <loc>{DOMAIN}/pages/{slug}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>""")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "\n".join(urls) + "\n</urlset>\n"
    with open(SITEMAP, "w") as f:
        f.write(xml)


def main():
    os.makedirs(PAGES, exist_ok=True)

    with open(DATA) as f:
        keywords = json.load(f)

    created = 0
    for kw in keywords:
        slug = slugify(kw) + ".html"
        path = os.path.join(PAGES, slug)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(generate_page(kw))
            print(f"  ✓ Created: {slug}")
            created += 1

    all_slugs = [f for f in os.listdir(PAGES) if f.endswith(".html") and not f.startswith("_")]
    update_sitemap(all_slugs)

    print(f"\nDone. Created {created} new page(s). Total: {len(all_slugs)} pages.")


if __name__ == "__main__":
    main()
