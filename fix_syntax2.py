#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Full syntax fix for sampleData.js:
1. Fix missing comma after `) when followed by // comment then f(
2. Fix any remaining f() calls missing trailing comma
"""
import re

INPUT = 'src/data/sampleData.js'

with open(INPUT, 'r', encoding='utf-8') as fh:
    content = fh.read()

original_len = len(content)

# Fix 1: `) \n\n    // comment \n    f(  -> `),\n\n    // comment\n    f(
# Pattern: backtick + ) + newline + (optional blank line) + // comment + newline + spaces + f(
pattern1 = r'(`\))\n(\n    // [^\n]+\n    f\()'
matches1 = re.findall(pattern1, content)
print(f'Pattern1 (`) before comment then f(): {len(matches1)} matches')
content = re.sub(pattern1, r'`),\n\2', content)

# Fix 2: `) \n\n    f(  (already fixed before but double-check)
pattern2 = r'(`\))\n(\n    f\()'
matches2 = re.findall(pattern2, content)
print(f'Pattern2 (`) directly before f(): {len(matches2)} matches')
content = re.sub(pattern2, r'`),\n\2', content)

# Fix 3: ')  (single-quote close) followed by comment then f( - missing comma
# e.g.   '...')  \n\n    // comment\n    f(
pattern3 = r"(')\)\n(\n    // [^\n]+\n    f\()"
matches3 = re.findall(pattern3, content)
print(f'Pattern3 (single-quote `) before comment then f(): {len(matches3)} matches')
content = re.sub(pattern3, r"'),\n\2", content)

# Fix 4: ')  (single-quote) directly before f(  
pattern4 = r"(')\)\n(\n    f\()"
matches4 = re.findall(pattern4, content)
print(f'Pattern4 (single-quote `) before f(): {len(matches4)} matches')
content = re.sub(pattern4, r"'),\n\2", content)

print(f'\nOriginal size: {original_len}, New size: {len(content)}')

if content != open(INPUT, encoding='utf-8').read():
    with open(INPUT, 'w', encoding='utf-8') as fh:
        fh.write(content)
    print('File updated.')
else:
    print('No changes needed.')

# Verify: check remaining issues
# Build will fail at f( lines that are not preceded by comma
# Find all places where f( is not preceded by a comma (at array element level)
lines = content.split('\n')
issues = 0
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith("f('m-") and i > 0:
        # Check previous non-empty line
        prev_line = ''
        for j in range(i-1, max(0, i-5), -1):
            if lines[j].strip():
                prev_line = lines[j].strip()
                break
        # Previous meaningful line should end with , or [ or be a comment
        if prev_line and not prev_line.endswith(',') and not prev_line.endswith('[') and not prev_line.startswith('//'):
            print(f'  Possible issue at line {i+1}: prev="{prev_line[:60]}"')
            issues += 1

print(f'\nTotal remaining possible issues: {issues}')
