import json
import os

def slugify(text):
    return text.lower().replace(" ", "-")

def get_tool_logic(keyword):
    # Simulação de lógica inteligente: se a keyword tiver "tax", usa cálculo de taxa
    if "tax" in keyword.lower():
        return "result = input * 0.25; // Simple 25% estimate"
    elif "hourly" in keyword.lower() or "rate" in keyword.lower():
        return "result = input / 160; // Based on 160h month"
    else:
        return "result = input * 1.10; // General margin"

def generate_html(keyword):
    logic = get_tool_logic(keyword)
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{keyword} | RemoteFinanceTools</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-50 text-slate-900 p-8">
        <div class="max-w-2xl mx-auto">
            <a href="../index.html" class="text-blue-600 mb-4 inline-block">← Back to Dashboard</a>
            <h1 class="text-4xl font-black mb-6">{keyword}</h1>
            
            <div class="bg-white p-8 rounded-3xl shadow-xl border border-slate-100 mb-8">
                <label class="block text-sm font-bold mb-2">Enter Amount (€)</label>
                <input id="val" type="number" class="w-full p-4 bg-slate-100 rounded-xl mb-4 outline-none focus:ring-2 focus:ring-blue-500">
                <button onclick="runCalc()" class="w-full bg-blue-600 text-white font-bold py-4 rounded-xl shadow-lg">Calculate Now</button>
                <h2 id="res" class="text-2xl font-bold mt-6 text-center text-blue-700"></h2>
            </div>

            <article class="prose lg:prose-xl text-slate-600">
                <h3 class="text-xl font-bold text-slate-900">Why use a {keyword}?</h3>
                <p>Managing finances as a digital nomad or freelancer requires precision. This <strong>{keyword}</strong> was designed to help you navigate the complexities of remote work compensation and global tax standards in 2026.</p>
                <p>By using professional tools, you ensure your business remains profitable and compliant with international standards.</p>
            </article>
        </div>
        <script>
            function runCalc() {{
                let input = document.getElementById('val').value;
                let result = 0;
                {logic}
                document.getElementById('res').innerText = "Estimated: €" + result.toFixed(2);
            }}
        </script>
    </body>
    </html>
    """

def main():
    if not os.path.exists('pages'): os.makedirs('pages')
    with open("data/keywords.json") as f:
        keywords = json.load(f)
    
    for kw in keywords:
        path = f"pages/{slugify(kw)}.html"
        # Forçamos a sobrescrita para atualizar os esqueletos antigos com a nova lógica
        with open(path, "w", encoding="utf-8") as f:
            f.write(generate_html(kw))
    print("✅ All pages updated with functional logic and SEO text.")

if __name__ == "__main__":
    main()
