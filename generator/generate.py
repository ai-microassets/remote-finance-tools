import json
import os
from datetime import datetime

def slugify(text):
    return text.lower().replace(" ", "-")

def generate_html(keyword):
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>{keyword}</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-slate-50 p-10"><div class="max-w-xl mx-auto">
<a href="../index.html" class="text-blue-500">← Back</a>
<h1 class="text-3xl font-bold mt-4">{keyword}</h1>
<p class="mt-4 text-slate-600 italic">This AI-powered tool is being calibrated for your region.</p>
</div></body></html>"""

def update_index(pages):
    links_html = "".join([f'<li><a href="pages/{p}" class="text-blue-600 hover:underline">{p.replace("-", " ").replace(".html", "").title()}</a></li>' for p in pages])
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head><title>RemoteFinanceTools</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="p-10 bg-white"><div class="max-w-2xl mx-auto">
<h1 class="text-4xl font-black mb-8 text-slate-900 text-center">RemoteFinance<span class="text-blue-600">Tools</span></h1>
<div class="bg-slate-50 p-8 rounded-3xl border border-slate-100">
<h2 class="text-xl font-bold mb-4">Available Calculators:</h2>
<ul class="space-y-3 list-disc pl-5">{links_html}</ul>
</div></div></body></html>""")

def main():
    with open("data/keywords.json") as f:
        keywords = json.load(f)

    if not os.path.exists('pages'): os.makedirs('pages')

    for kw in keywords:
        filename = slugify(kw) + ".html"
        path = f"pages/{filename}"
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(generate_html(kw))

    # Atualiza o Index com todas as páginas encontradas
    all_pages = [f for f in os.listdir('pages') if f.endswith('.html')]
    update_index(all_pages)

if __name__ == "__main__":
    main()
