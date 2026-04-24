import re
c = open('src/data/sampleData.js', 'r', encoding='utf-8').read()
ms = re.findall(r"f\('m-([^']+)'", c)
d = {}
for m in ms:
    d[m] = d.get(m, 0) + 1
for k, v in sorted(d.items(), key=lambda x: -x[1]):
    print(f'{k}: {v}')
print('---')
print('Total FAQs:', len(ms))
print('Total machines:', len(d))
