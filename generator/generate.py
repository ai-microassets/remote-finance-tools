import os

# Lista de próximas calculadoras a gerar (podes expandir esta lista)
calculators = [
    {"slug": "project-profit-margin-calculator", "title": "Project Profit Margin Calculator", "desc": "Calculate the net profit of your freelance projects."},
    {"slug": "usd-to-eur-salary-converter", "title": "USD to EUR Net Salary Converter", "desc": "Convert your US remote salary to EUR after taxes."},
    {"slug": "freelancer-emergency-fund-calculator", "title": "Freelancer Emergency Fund Calculator", "desc": "How much should you save for a rainy day?"}
]

def generate_page(calc):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{calc['title']} | RemoteFinanceTools</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-50 p-6">
        <div class="max-w-2xl mx-auto">
            <a href="../index.html" class="text-blue-600">← Back</a>
            <h1 class="text-3xl font-bold mt-4">{calc['title']}</h1>
            <p class="text-slate-600 mb-8">{calc['desc']}</p>
            <div class="bg-white p-8 rounded-2xl shadow-sm border border-slate-200">
                <p class="text-center text-slate-400 italic">Calculator logic for {calc['title']} coming in next update...</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    file_path = f"pages/{calc['slug']}.html"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Generated: {file_path}")

# Executar geração
if __name__ == "__main__":
    if not os.path.exists('pages'):
        os.makedirs('pages')
    for c in calculators:
        generate_page(c)
