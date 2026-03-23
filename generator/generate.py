import json
import os
from datetime import datetime

def slugify(text):
    return text.lower().replace(" ", "-")

def generate_html(keyword):
    # Template profissional para as novas páginas
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{keyword} | RemoteFinanceTools</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-50 p-6 text-slate-900">
        <div class="max-w-2xl mx-auto">
            <a href="../index.html" class="text-blue-600">← Back to Tools</a>
            <h1 class="text-3xl font-bold mt-6 mb-4">{keyword}</h1>
            <div class="bg-white p-8 rounded-2xl shadow-sm border border-slate-200">
                <p class="text-slate-600 italic">Financial logic for {keyword} is being optimized by our AI. Check back soon for the full interactive calculator.</p>
            </div>
        </div>
    </body>
    </html>
    """

def main():
    # 1. Carregar Keywords
    with open("data/keywords.json") as f:
        keywords = json.load(f)

    new_pages_count = 0
    
    # 2. Criar páginas que ainda não existem
    for kw in keywords:
        filename = slugify(kw) + ".html"
        path = f"pages/{filename}"

        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(generate_html(kw))
            new_pages_count += 1

    # 3. Atualizar o Log de Crescimento (Stats)
    total_pages = len(os.listdir('pages'))
    with open("stats.txt", "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"[{timestamp}] Total: {total_pages} pages. Added {new_pages_count} today.\n")

if __name__ == "__main__":
    if not os.path.exists('pages'):
        os.makedirs('pages')
    main()
