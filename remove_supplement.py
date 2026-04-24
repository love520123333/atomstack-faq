import re

c = open('src/data/sampleData.js', 'r', encoding='utf-8').read()

# Find the supplement section start
sup_idx = c.find('\n    // ================ ')
# Also check the pattern before it - we want to find the first supplement line
# that appears after the last original FAQ

# The supplement text starts with "\n\n    // ================ "
# Find all such patterns
all_markers = list(re.finditer(r'\n    // ================ ', c))
if not all_markers:
    print("No markers found")
    exit()

# The last marker before the supplement start is the last original machine section
# We need to find where supplement starts
sup_start = c.find('supplement)')
if sup_start < 0:
    print("No supplement found")
    exit()

# Go back to find the start of the comment line
line_start = c.rfind('\n', 0, sup_start - 20)
if line_start < 0:
    print("Cannot find line start")
    exit()

# Also go back past any blank lines before the supplement comment
while line_start > 0 and c[line_start-1:line_start+1] == '\n':
    line_start -= 1

# Truncate here and add the closing bracket
new_c = c[:line_start] + '\n  ]\n}'

with open('src/data/sampleData.js', 'w', encoding='utf-8') as f:
    f.write(new_c)

print(f'Removed supplement section. New size: {len(new_c)} (was {len(c)})')

# Verify
ms = re.findall(r"f\('m-([^']+)'", new_c)
print(f'Total FAQs after cleanup: {len(ms)}')
