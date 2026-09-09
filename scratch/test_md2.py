import re

def simple_markdown_to_html(markdown):
    if not markdown: return ""
    html = markdown

    # Code syntax blocks first to protect code
    html = re.sub(r'```python([\s\S]*?)```', r'<pre><code class="python-syntax">\1</code></pre>', html)
    html = re.sub(r'```lua([\s\S]*?)```', r'<pre><code class="lua-syntax">\1</code></pre>', html)
    html = re.sub(r'```([\s\S]*?)```', r'<pre><code>\1</code></pre>', html)

    # Math formulas
    html = re.sub(r'\$\$(.*?)\$\$', r'<code style="display:block; padding:8px; margin:5px 0;">\1</code>', html)
    html = re.sub(r'\$(.*?)\$', r'<code>\1</code>', html)

    # Inline code ticks
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    # Bold & Italic
    html = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'__(.*?)__', r'<strong>\1</strong>', html)

    # Bullet points
    html = re.sub(r'^\*\s(.*)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'^-\s(.*)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*<\/li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)

    # Headings
    html = re.sub(r'^####\s(.*)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^###\s(.*)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^##\s(.*)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^#\s(.*)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # Linebreaks
    html = html.replace('\n', '<br>')

    return html

test_cases = [
    "1. **Pre-order (Root -> Left -> Right)**: Used to clone trees.",
    "* **Important**: Check `null` pointer",
    "This is **bold** text and __another bold__ text."
]

for tc in test_cases:
    print("IN: ", tc)
    print("OUT:", simple_markdown_to_html(tc))
    print()
