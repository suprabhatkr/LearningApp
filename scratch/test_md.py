import sys
sys.path.insert(0, '.')
import re
from app.data.dsa_data import DSA_TOPICS
from app.data.sys_design_data import SYSTEM_DESIGN_CHAPTERS
from app.data.ai_data import AI_CHAPTERS

sample_text = DSA_TOPICS["trees"]["concept"]
print("Original snippet:")
print(sample_text[:300])

# JS logic equivalent in python
def js_simple_markdown_to_html(md):
    if not md: return ""
    html = md
    
    # Code blocks
    html = re.sub(r'```python([\s\S]*?)```', r'<pre><code class="python-syntax">\1</code></pre>', html)
    html = re.sub(r'```lua([\s\S]*?)```', r'<pre><code class="lua-syntax">\1</code></pre>', html)
    html = re.sub(r'```([\s\S]*?)```', r'<pre><code>\1</code></pre>', html)
    
    # Math
    html = re.sub(r'\$\$(.*?)\$\$', r'<code style="display:block; padding:8px; margin:5px 0;">\1</code>', html)
    html = re.sub(r'\$(.*?)\$', r'<code>\1</code>', html)
    
    # Inline code ticks
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Bold **text** and __text__
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'__(.*?)__', r'<strong>\1</strong>', html)
    
    # Italic *text* and _text_ (optional)
    html = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'<em>\1</em>', html)
    
    # Bullet points
    html = re.sub(r'^\*\s(.*)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'^-\s(.*)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # Headings
    html = re.sub(r'^####\s(.*)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^###\s(.*)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^##\s(.*)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^#\s(.*)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Linebreaks
    html = html.replace('\n', '<br>')
    
    return html

converted = js_simple_markdown_to_html(sample_text)
print("\nConverted snippet:")
print(converted[:400])
