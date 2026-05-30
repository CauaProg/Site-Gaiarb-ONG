import re

filepath = "c:/Users/cauam/Desktop/gaiarb/voluntario.css"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

new_content = content

# Update banner background
new_content = re.sub(
    r'\.banner \{\s*padding: 80px 0;\s*background: var\(--bg\);',
    '.banner {\n    padding: 80px 0;\n    background: #eff6ff; /* Soft pastel sky-blue */',
    new_content
)

# Update voluntario-section background
new_content = re.sub(
    r'\.voluntario-section \{\s*padding: 100px 0;\s*background: var\(--white\);',
    '.voluntario-section {\n    padding: 100px 0;\n    background: #faf5ff; /* Soft pastel lavender */',
    new_content
)

# Update voluntario-form-wrap
new_content = re.sub(
    r'\.voluntario-form-wrap \{\s*background: var\(--white\);\s*border: 1px solid rgba\(226, 232, 240, 0\.8\);\s*border-radius: 28px;\s*padding: 40px;\s*box-shadow: 0 15px 40px rgba\(15, 23, 42, 0\.04\);\s*\}',
    '.voluntario-form-wrap {\n    background: #fdf2f8;\n    border: 1.5px solid #fbcfe8;\n    border-radius: 28px;\n    padding: 40px;\n    box-shadow: 0 15px 40px rgba(15, 23, 42, 0.03);\n}',
    new_content
)

# Update areas-lista li
new_content = re.sub(
    r'\.areas-lista li \{\s*font-size: 14px;\s*font-weight: 700;\s*color: var\(--text\);\s*padding: 14px 20px;\s*border-radius: 16px;\s*background: rgba\(248, 250, 252, 0\.8\);\s*border: 1px solid rgba\(226, 232, 240, 0\.8\);\s*transition: transform 0\.25s ease, border-color 0\.25s ease;\s*display: flex;\s*align-items: center;\s*gap: 12px;\s*\}',
    '.areas-lista li {\n    font-size: 14px;\n    font-weight: 700;\n    color: var(--text);\n    padding: 14px 20px;\n    border-radius: 16px;\n    transition: transform 0.25s ease, border-color 0.25s ease;\n    display: flex;\n    align-items: center;\n    gap: 12px;\n}\n.areas-lista li:nth-child(6n+1) { background: #fff1f2; border: 1.5px solid #fecdd3; }\n.areas-lista li:nth-child(6n+2) { background: #eef2ff; border: 1.5px solid #c7d2fe; }\n.areas-lista li:nth-child(6n+3) { background: #ecfdf5; border: 1.5px solid #a7f3d0; }\n.areas-lista li:nth-child(6n+4) { background: #fff7ed; border: 1.5px solid #ffedd5; }\n.areas-lista li:nth-child(6n+5) { background: #eff6ff; border: 1.5px solid #dbeafe; }\n.areas-lista li:nth-child(6n+6) { background: #faf5ff; border: 1.5px solid #e9d5ff; }',
    new_content
)

if new_content != content:
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated voluntario.css successfully.")
else:
    print("No matches in voluntario.css.")
