import json
import os

def slugify(text):
    return text.lower().replace(" ", "-").replace(".html", "")

def main():
    base_dir = os.getcwd()
    pages_dir = os.path.join(base_dir, 'pages')
    index_file = os.path.join(base_dir, 'index.html')

    # 1. GERAR PÁGINAS NOVAS (Sem apagar as antigas)
    with open(os.path.join(base_dir, 'data', 'keywords.json'), 'r') as f:
        keywords = json.load(f)

    for kw in keywords:
        filename = slugify(kw) + ".html"
        path = os.path.join(pages_dir, filename)
        
        # SÓ CRIA SE NÃO EXISTIR - Protege o teu trabalho manual
        if not os.path.exists(path):
            with open(path, 'w', encoding="utf-8") as f:
                f.write(f"<html><body><h1>{kw}</h1><p>AI Tool in progress...</p></body></html>")

    # 2. RECONSTRUIR O MENU (Mantendo o teu design profissional)
    all_pages = sorted([f for f in os.listdir(pages_dir) if f.endswith('.html')])
    
    # Criamos os blocos de links com o estilo do teu site
    links_html = "".join([
        f'<a href="pages/{p}" class="block p-4 bg-white rounded-xl border border-slate-200 hover:border-blue-500 shadow-sm transition-all">'
        f'<h3 class="font-bold text-slate-900">{p.replace("-", " ").replace(".html", "").title()}</h3>'
        f'<span class="text-xs text-blue-600 font-medium font-semibold uppercase">Open Tool →</span>'
        f'</a>' 
        for p in all_pages
    ])

    # O Novo Index com o teu design HERO e os novos links
    with open(index_file, 'w', encoding="utf-8") as f:
        f.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><title>RemoteFinanceTools | Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900">
    <nav class="bg-white border-b p-4 mb-8">
        <div class="max-w-5xl mx-auto font-bold text-blue-600 text-xl italic">RemoteFinanceTools</div>
    </nav>
    <header class="max-w-5xl mx-auto px-6 mb-12">
        <h1 class="text-4xl font-black text-slate-900 mb-2">Your AI Financial Hub</h1>
        <p class="text-slate-500 italic">Total assets active: {len(all_pages)}</p>
    </header>
    <main class="max-w-5xl mx-auto px-6 grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {links_html}
    </main>
</body>
</html>
        """)

if __name__ == "__main__":
    main()
