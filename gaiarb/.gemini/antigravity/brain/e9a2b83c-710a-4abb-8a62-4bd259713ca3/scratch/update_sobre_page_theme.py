import re

filepath = "c:/Users/cauam/Desktop/gaiarb/sobre.css"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

new_content = content

# Update about-section background
new_content = re.sub(
    r'\.about-section \{\s*padding: 100px 0;\s*background: var\(--white\);',
    '.about-section {\n    padding: 100px 0;\n    background: #eff6ff; /* Soft pastel sky blue */',
    new_content
)

# Update alternate about-section background
new_content = re.sub(
    r'\.about-section\.alternate-bg \{\s*background: rgba\(248, 250, 252, 0\.5\);',
    '.about-section.alternate-bg {\n    background: #fdf2f8; /* Soft pastel pink */',
    new_content
)

# Update mvv-section background
new_content = re.sub(
    r'\.mvv-section \{\s*padding: 100px 0;\s*background: var\(--white\);',
    '.mvv-section {\n    padding: 100px 0;\n    background: #faf5ff; /* Soft pastel lavender */',
    new_content
)

# Update mvv-card
new_content = re.sub(
    r'\.mvv-card \{\s*background: var\(--white\);\s*border-radius: 24px;\s*padding: 40px 30px;\s*text-align: center;\s*transition: transform 0\.4s cubic-bezier\(0\.16, 1, 0\.3, 1\), box-shadow 0\.4s ease;\s*border: 1px solid rgba\(226, 232, 240, 0\.8\);\s*display: flex;\s*flex-direction: column;\s*align-items: center;\s*\}',
    '.mvv-card {\n    border-radius: 24px;\n    padding: 40px 30px;\n    text-align: center;\n    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s ease;\n    display: flex;\n    flex-direction: column;\n    align-items: center;\n}\n.mvv-card:nth-child(3n+1) { background: #fff1f2; border: 1.5px solid #fecdd3; }\n.mvv-card:nth-child(3n+2) { background: #f0fdfa; border: 1.5px solid #ccfbf1; }\n.mvv-card:nth-child(3n+3) { background: #fff7ed; border: 1.5px solid #ffedd5; }',
    new_content
)

# Update mvv-card hover shadow
new_content = re.sub(
    r'\.mvv-card:hover \{\s*transform: translateY\(-8px\);\s*box-shadow: 0 20px 40px rgba\(79, 70, 229, 0\.08\);\s*\}',
    '.mvv-card:hover {\n    transform: translateY(-8px);\n    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.04);\n}',
    new_content
)

# Update valores-section background
new_content = re.sub(
    r'\.valores-section \{\s*padding: 100px 0;\s*background: rgba\(248, 250, 252, 0\.7\);',
    '.valores-section {\n    padding: 100px 0;\n    background: #ecfdf5; /* Soft pastel green */',
    new_content
)

# Update valor-tag
new_content = re.sub(
    r'\.valor-tag \{\s*background: var\(--white\);\s*border: 1px solid rgba\(226, 232, 240, 0\.8\);\s*color: var\(--text-light\);\s*border-radius: 50px;\s*padding: 12px 24px;\s*font-family: \'Outfit\', sans-serif;\s*font-size: 15px;',
    '.valor-tag {\n    border-radius: 50px;\n    padding: 12px 24px;\n    font-family: \'Outfit\', sans-serif;\n    font-size: 15px;\n    font-weight: 700;\n    color: var(--text);\n    transition: transform 0.2s ease, border-color 0.2s ease;\n}\n.valor-tag:nth-child(6n+1) { background: #fff1f2; border: 1.5px solid #fecdd3; }\n.valor-tag:nth-child(6n+2) { background: #eef2ff; border: 1.5px solid #c7d2fe; }\n.valor-tag:nth-child(6n+3) { background: #ecfdf5; border: 1.5px solid #a7f3d0; }\n.valor-tag:nth-child(6n+4) { background: #fff7ed; border: 1.5px solid #ffedd5; }\n.valor-tag:nth-child(6n+5) { background: #eff6ff; border: 1.5px solid #dbeafe; }\n.valor-tag:nth-child(6n+6) { background: #faf5ff; border: 1.5px solid #e9d5ff; }',
    new_content
)

if new_content != content:
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated sobre.css successfully.")
else:
    print("No matches in sobre.css.")
