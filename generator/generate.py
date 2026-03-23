import json, os

def slugify(text):
    return text.lower().replace(" ", "-")

def generate_html(keyword):
    return f"""
    <html>
    <head>
    <title>{keyword}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="p-6">
    <h1>{keyword}</h1>
    <p>Auto generated calculator page.</p>
    </body>
    </html>
    """

def main():
    with open("data/keywords.json") as f:
        keywords = json.load(f)

    for kw in keywords:
        filename = slugify(kw) + ".html"
        path = f"pages/{filename}"

        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write(generate_html(kw))

if __name__ == "__main__":
    main()
