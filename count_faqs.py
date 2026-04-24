import re, os
base = r'c:\Users\amyxu\WorkBuddy\20260422134443\machine-faq\src\data'
for fname in ['sampleData.js', 'batch1.js', 'batch2.js', 'batch3.js', 'batch4.js']:
    path = os.path.join(base, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    count = content.count("f('m-")
    print(f"{fname}: {count} FAQ entries")
