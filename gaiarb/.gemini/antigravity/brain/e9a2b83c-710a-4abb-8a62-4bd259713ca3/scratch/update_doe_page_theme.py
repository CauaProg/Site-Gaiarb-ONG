import re

filepath = "c:/Users/cauam/Desktop/gaiarb/doe.css"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

new_content = content

# Update doe-hero background
new_content = re.sub(
    r'\.doe-hero \{\s*padding: 80px 0;\s*background: var\(--bg\);',
    '.doe-hero {\n    padding: 80px 0;\n    background: #eff6ff; /* Soft pastel sky-blue */',
    new_content
)

# Update doe-card-hero
new_content = re.sub(
    r'\.doe-card-hero \{\s*background: var\(--white\);\s*border-radius: 24px;\s*padding: 40px;\s*box-shadow: 0 20px 40px rgba\(15, 23, 42, 0\.06\);\s*border: 1px solid rgba\(226, 232, 240, 0\.8\);',
    '.doe-card-hero {\n    background: #fdf2f8;\n    border-radius: 24px;\n    padding: 40px;\n    box-shadow: 0 15px 35px rgba(15, 23, 42, 0.03);\n    border: 1.5px solid #fbcfe8;',
    new_content
)

# Update escolha-section background
new_content = re.sub(
    r'\.escolha-section \{\s*padding: 100px 0;\s*background: var\(--white\);',
    '.escolha-section {\n    padding: 100px 0;\n    background: #faf5ff; /* Soft pastel lavender */',
    new_content
)

# Update formas-section background
new_content = re.sub(
    r'\.formas-section \{\s*padding: 100px 0;\s*background: rgba\(248, 250, 252, 0\.7\);',
    '.formas-section {\n    padding: 100px 0;\n    background: #ecfdf5; /* Soft pastel green */',
    new_content
)

# Update forma-card
new_content = re.sub(
    r'\.forma-card \{\s*background: var\(--white\);\s*border: 1px solid rgba\(226, 232, 240, 0\.8\);\s*border-radius: 24px;\s*padding: 40px 30px;\s*text-align: center;\s*box-shadow: 0 10px 30px rgba\(15, 23, 42, 0\.02\);\s*display: flex;\s*flex-direction: column;\s*align-items: center;\s*transition: transform 0\.4s cubic-bezier\(0\.16, 1, 0\.3, 1\);\s*\}',
    '.forma-card {\n    border-radius: 24px;\n    padding: 40px 30px;\n    text-align: center;\n    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.02);\n    display: flex;\n    flex-direction: column;\n    align-items: center;\n    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);\n}\n.forma-card:nth-child(3n+1) { background: #fff1f2; border: 1.5px solid #fecdd3; }\n.forma-card:nth-child(3n+2) { background: #faf5ff; border: 1.5px solid #e9d5ff; }\n.forma-card:nth-child(3n+3) { background: #eff6ff; border: 1.5px solid #dbeafe; }',
    new_content
)

# Update impacto-section background
new_content = re.sub(
    r'\.impacto-section \{\s*padding: 100px 0;\s*background: var\(--white\);',
    '.impacto-section {\n    padding: 100px 0;\n    background: #fffbeb; /* Soft pastel yellow */',
    new_content
)

# Update impacto-item
new_content = re.sub(
    r'\.impacto-item \{\s*background: rgba\(248, 250, 252, 0\.7\);\s*border: 1px solid rgba\(226, 232, 240, 0\.6\);\s*border-radius: 20px;\s*padding: 30px 20px;\s*transition: background 0\.3s ease;\s*\}',
    '.impacto-item {\n    border-radius: 20px;\n    padding: 30px 20px;\n    transition: transform 0.3s ease, background-color 0.3s ease;\n}\n.impacto-item:nth-child(5n+1) { background: #fff1f2; border: 1.5px solid #fecdd3; }\n.impacto-item:nth-child(5n+2) { background: #eef2ff; border: 1.5px solid #c7d2fe; }\n.impacto-item:nth-child(5n+3) { background: #ecfdf5; border: 1.5px solid #a7f3d0; }\n.impacto-item:nth-child(5n+4) { background: #fff7ed; border: 1.5px solid #ffedd5; }\n.impacto-item:nth-child(5n+5) { background: #eff6ff; border: 1.5px solid #dbeafe; }',
    new_content
)

if new_content != content:
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated doe.css successfully.")
else:
    print("No matches in doe.css.")
