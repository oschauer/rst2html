import sys
from docutils.core import publish_string
from pathlib import Path

# === CONFIGURATION ===
css_subdir = "css"  # subdirectory where your CSS files are
css_files = ["basic.css", "default.css", "rst.css"]  # list of CSS files

# === INPUT ===
if len(sys.argv) < 2:
    print("Usage: python rst_to_html_with_css.py <yourfile.rst>")
    sys.exit(1)

input_rst = Path(sys.argv[1])
output_html = input_rst.with_suffix(".html")

# === 1. Read the .rst file content ===
with open(input_rst, "r", encoding="utf-8") as f:
    rst_content = f.read()

# === 2. Convert RST content to HTML string ===
html_bytes = publish_string(source=rst_content, writer_name='html')
html = html_bytes.decode('utf-8')

# === 3. Build CSS <link> tags with subdir paths ===
link_tags = "\n".join([
    f'<link rel="stylesheet" type="text/css" href="{css_subdir}/{css}">'
    for css in css_files
])

# === 4. Insert CSS into the <head> section ===
insert_point = html.find("<head>") + len("<head>")
html_with_css = html[:insert_point] + "\n" + link_tags + html[insert_point:]

# === 5. Write the styled HTML to output file ===
with open(output_html, "w", encoding="utf-8") as f:
    f.write(html_with_css)

print(f"✅ HTML with CSS written to {output_html}")