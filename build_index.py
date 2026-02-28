#!/usr/bin/env python3
"""
Build script to generate a self-contained index.html by merging:
- index-backup.html (V1 content: all HTML body sections)
- css/shared.css (shared styles)
- css/home.css (home page styles)
- js/shared.js (shared JavaScript)
- js/home.js (home page JavaScript)

Plus additional CSS from the sugerencia layout (fade-in, scrollbar, etc.)
All CSS and JS are inlined into a single index.html file.
"""

import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def read_file(relative_path):
    full_path = os.path.join(SCRIPT_DIR, relative_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_body_content(html):
    """Extract everything between <body> and </body> tags."""
    match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    if match:
        return match.group(1)
    return html

def remove_script_tags(html):
    """Remove external script references (we'll inline them)."""
    html = re.sub(r'<script\s+src="js/shared\.js"\s*>\s*</script>', '', html)
    html = re.sub(r'<script\s+src="js/home\.js"\s*>\s*</script>', '', html)
    return html

def fix_nav_map(js_content):
    """Fix navMap to use 'index.html' instead of 'index.backup.html'."""
    js_content = js_content.replace("'index.backup.html'", "'index.html'")
    return js_content

def build():
    # Read all source files
    backup_html = read_file('index-backup.html')
    shared_css = read_file('css/shared.css')
    home_css = read_file('css/home.css')
    shared_js = read_file('js/shared.js')
    home_js = read_file('js/home.js')

    # Fix the navMap in shared.js
    shared_js = fix_nav_map(shared_js)

    # Extract body content from index-backup.html
    body_content = extract_body_content(backup_html)

    # Remove external script tags from body
    body_content = remove_script_tags(body_content)

    # Additional CSS for sugerencia-style fade-in animations, scrollbar, etc.
    additional_css = """
/* ========== FADE-IN ANIMATION (from sugerencia layout) ========== */
.fade-in {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.8s ease, transform 0.8s ease;
}

.fade-in.visible {
    opacity: 1;
    transform: translateY(0);
}

/* ========== CUSTOM SCROLLBAR ========== */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-darker, #070D17);
}

::-webkit-scrollbar-thumb {
    background: var(--accent-cyan, #1DA1F2);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--accent-cyan-light, #4DC9F6);
}

/* Firefox scrollbar */
html {
    scrollbar-width: thin;
    scrollbar-color: var(--accent-cyan, #1DA1F2) var(--bg-darker, #070D17);
}
"""

    # Additional JS for fade-in observer
    additional_js = """
// ========== FADE-IN OBSERVER (sugerencia layout) ==========
const fadeElements = document.querySelectorAll('.fade-in');
const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
});

fadeElements.forEach(el => {
    fadeObserver.observe(el);
});
"""

    # Build the final HTML
    output = f'''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description"
        content="N-Expert.ai - Enterprise AI consulting specializing in Multi-Agent Systems. Transform your business with coordinated AI solutions.">
    <title>N-Expert.ai - Multi-Agent AI Systems for Enterprise</title>

    <!-- Preconnect to CDNs -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preconnect" href="https://images.unsplash.com">
    <link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>

    <!-- Google Fonts (non-blocking) -->
    <link rel="preload" as="style"
        href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap"
        onload="this.onload=null;this.rel='stylesheet'">
    <noscript>
        <link
            href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap"
            rel="stylesheet">
    </noscript>

    <!-- Font Awesome (non-blocking) -->
    <link rel="preload" as="style" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"
        onload="this.onload=null;this.rel='stylesheet'">
    <noscript>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    </noscript>

    <!-- ALL CSS INLINED -->
    <style>
{shared_css}

{home_css}

{additional_css}
    </style>
</head>

<body>
{body_content}

    <!-- ALL JS INLINED -->
    <script>
{shared_js}

{home_js}

{additional_js}
    </script>
</body>

</html>'''

    # Write the output file
    output_path = os.path.join(SCRIPT_DIR, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    # Report stats
    line_count = output.count('\n') + 1
    size_kb = len(output.encode('utf-8')) / 1024
    print(f"SUCCESS: index.html generated")
    print(f"  Lines: {line_count}")
    print(f"  Size: {size_kb:.1f} KB")
    print(f"  Output: {output_path}")

if __name__ == '__main__':
    build()
