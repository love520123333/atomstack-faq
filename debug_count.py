import re
c = open('src/data/sampleData.js', 'r', encoding='utf-8').read()
print('File size:', len(c))

# Count f() calls (the standard format)
ms = re.findall(r"f\('m-([^']+)'", c)
d = {}
for m in ms:
    d[m] = d.get(m, 0) + 1
print(f'Total f(m-xxx) calls: {len(ms)}')
for k, v in sorted(d.items(), key=lambda x: -x[1]):
    print(f'  {k}: {v}')

# Also search for supplement section
sup_idx = c.find('supplement')
if sup_idx > 0:
    print(f'\nSupplement section found at: {sup_idx}')
    # Count f() calls in supplement
    sup = c[sup_idx:]
    sup_ms = re.findall(r"f\('m-([^']+)'", sup)
    print(f'FAQs in supplement: {len(sup_ms)}')
    
# Check for syntax issues around supplement
lines_after_sup = c[sup_idx:sup_idx+2000].split('\n')
print(f'\nFirst 20 lines after supplement marker:')
for i, line in enumerate(lines_after_sup[:20]):
    print(f'  {i}: {line[:100]}')
