import urllib.request, json
from datetime import datetime
from pathlib import Path

# 1. Fetch top 4 posts
req = urllib.request.Request('https://dev.to/api/articles?username=benji377&page=1&per_page=4', headers={'User-Agent': 'GitHub Bot'})
posts = json.loads(urllib.request.urlopen(req).read())

# 2. Build Markdown using a list comprehension
md = "\n" + "\n".join(
    f"- **[{p['title']}]({p['url']})** <br> <sub> 📅 {datetime.strptime(p['published_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%b %d, %Y')} | ⏱️ {p['reading_time_minutes']} min read</sub>"
    for p in posts
) + "\n"

# 3. Read, update, and save README.md
readme = Path('README.md')
text = readme.read_text(encoding='utf-8')
start, end = '<!-- BLOG-POST-LIST:START -->', '<!-- BLOG-POST-LIST:END -->'

if start in text and end in text:
    readme.write_text(text[:text.find(start)+len(start)] + md + text[text.find(end):], encoding='utf-8')
    print("Successfully updated README.md!")
else:
    print("Error: Could not find the HTML comment tags.")
    exit(1)
