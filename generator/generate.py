import json
import os

def slugify(text):
    return text.lower().replace(" ", "-").replace(".html", "")

def generate_pro_html(keyword):
    # Lógica customizada baseada na keyword
    tax_rate = 0.25 if "portugal" in keyword.lower() else 0.20
    
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><title>{keyword} | RemoteFinanceTools</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Inter', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-900 p-4 md:p-12">
    <div class="max-w-3xl mx-auto">
        <a href="../index.html" class="text-sm font-bold text-blue-600 hover:text-blue-800 transition-colors">← DASHBOARD</a>
        
        <header class="mt-8 mb-12">
            <h1 class="text-4xl font-black tracking-tight text-slate-900 mb-4">{keyword}</h1>
            <p class="text-lg text-slate-500">Professional grade financial modeling for remote experts.</p>
        </header>

        <div class="grid md:grid-cols-2 gap-8">
            <div class="bg-white p-8 rounded-3xl shadow-sm border border-slate-200">
                <h3 class="text-sm font-black uppercase tracking-widest text-slate-400 mb-6">Configuration</h3>
                <div class="space-y-6">
                    <div>
                        <label class="block text-sm font-bold mb-2">Base Monthly Amount (€)</label>
                        <input type="number" id="baseInput" oninput="calculate()" placeholder="5000" 
                               class="w-full p-4 bg-slate-50 border-2 border-transparent focus:border-blue-500 rounded-2xl outline-none transition-all text-xl font-bold">
                    </div>
                    <div>
                        <label class="block text-sm font-bold mb-2">Operational Costs (%)</label>
                        <input type="range" id="costsRange" min="0" max="50" value="10" oninput="calculate()" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer">
                        <span id="costsVal" class="text-sm text-slate-500 font-medium">10%</span>
                    </div>
                </div>
            </div>

            <div class="bg-blue-600 p-8 rounded-3xl shadow-xl text-white flex flex-col justify-between">
                <div>
                    <h3 class="text-sm font-black uppercase tracking-widest opacity-60 mb-8">Estimated Net Profit</h3>
                    <div id="resultDisplay" class="text-5xl font-black leading-none mt-2">€0.00</div>
                </div>
                <div class="mt-8 pt-8 border-t border-blue-500/30 space-y-3">
                    <div class="flex justify-between text-sm"><span class="opacity-70">Tax Estimate ({int(tax_rate*100)}%):</span> <span id="taxDisplay" class="font-bold">€0.00</span></div>
                    <div class="flex justify-between text-sm"><span class="opacity-70">Business Expenses:</span> <span id="expDisplay" class="font-bold">€0.00</span></div>
                </div>
            </div>
        </div>

        <article class="mt-16 prose prose-slate max-w-none border-t pt-12">
            <h2 class="text-2xl font-black text-slate-900">Understanding {keyword}</h2>
            <p class="text-slate-600 leading-relaxed">This tool calculates your real take-home pay by factoring in the average {int(tax_rate*100)}% tax burden and your custom operational overhead. In 2026, remote workers must account for global inflation and shifting fiscal residency rules.</p>
        </article>
    </div>

    <script>
        function calculate() {{
            const base = parseFloat(document.getElementById('baseInput').value) || 0;
            const costPerc = parseFloat(document.getElementById('costsRange').value) || 0;
            document.getElementById('costsVal').innerText = costPerc + "%";

            const expenses = base * (costPerc / 100);
            const taxable = base - expenses;
            const tax = taxable * {tax_rate};
            const net = taxable - tax;

            document.getElementById('resultDisplay').innerText = "€" + net.toLocaleString('en-US', {{minimumFractionDigits: 2, maximumFractionDigits: 2}});
            document.getElementById('taxDisplay').innerText = "€" + tax.toLocaleString('en-US', {{minimumFractionDigits: 2}});
            document.getElementById('expDisplay').innerText = "€" + expenses.toLocaleString('en-US', {{minimumFractionDigits: 2}});
        }}
    </script>
</body>
</html>
    """

def main():
    base_dir = os.getcwd()
    pages_dir = os.path.join(base_dir, 'pages')
    if not os.path.exists(pages_dir): os.makedirs(pages_dir)
    
    with open(os.path.join(base_dir, 'data', 'keywords.json'), 'r') as f:
        keywords = json.load(f)

    for kw in keywords:
        path = os.path.join(pages_dir, slugify(kw) + ".html")
        # Mantemos a proteção: não sobrescreve se já editaste manualmente a lógica
        if not os.path.exists(path):
            with open(path, 'w', encoding="utf-8") as f:
                f.write(generate_pro_html(kw))

if __name__ == "__main__":
    main()
