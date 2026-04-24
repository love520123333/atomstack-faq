#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive fix: ensure every f(...) call in the array ends with a comma.
The f() calls are array elements, so all but the last one must be followed by a comma.
Pattern: any line ending with `) (closing paren) that is NOT followed by a comma,
and where the next non-empty, non-comment line starts with f( or // 
should have a comma added.
"""
import re

INPUT = 'src/data/sampleData.js'

with open(INPUT, 'r', encoding='utf-8') as fh:
    content = fh.read()

print(f'File size: {len(content)}')

# Strategy: find all occurrences of f() closings without trailing comma
# A f() call ends when we see ) or `) at the end of a line
# and the NEXT non-empty non-comment line starts with f(
#
# Specifically: lines ending with `) or ') or ") where the closing is the f() call end
# These lines DON'T end with ),
#
# Simplest reliable fix: find all )\n followed (after optional blank lines and comments) by f(
# and ensure there's a comma after )

# More targeted: look for lines that:
# 1. End with `) - template string + close paren (no comma)  
# 2. End with ') - string + close paren (no comma)
# And are followed by f( in subsequent lines

# Let's do it line by line
lines = content.split('\n')
new_lines = []
fix_count = 0
i = 0

while i < len(lines):
    line = lines[i]
    stripped = line.rstrip()
    
    # Check if this line closes a f() call without a comma
    # Patterns: ends with `) or ends with ')  or ends with ")
    # But NOT ends with `), or '), or "),
    needs_fix = False
    if (stripped.endswith('`)') or stripped.endswith("')") or stripped.endswith('")')):
        if not stripped.endswith('`),') and not stripped.endswith("'),") and not stripped.endswith('"),'):
            # Check if the next f( requires a comma
            # Look ahead: skip blank lines and comments
            j = i + 1
            found_next_f = False
            found_array_end = False
            while j < len(lines):
                next_stripped = lines[j].strip()
                if not next_stripped:
                    j += 1
                    continue
                if next_stripped.startswith('//'):
                    j += 1
                    continue
                # Non-empty, non-comment line
                if next_stripped.startswith("f('m-") or next_stripped.startswith('f("m-'):
                    found_next_f = True
                elif next_stripped == ']' or next_stripped.startswith(']'):
                    found_array_end = True
                break
            
            if found_next_f:
                needs_fix = True
    
    if needs_fix:
        # Add comma
        new_lines.append(stripped + ',')
        fix_count += 1
    else:
        new_lines.append(lines[i])
    
    i += 1

print(f'Fixed {fix_count} missing commas')

fixed = '\n'.join(new_lines)

with open(INPUT, 'w', encoding='utf-8') as fh:
    fh.write(fixed)

print(f'File written, size: {len(fixed)}')

# Verify: count remaining issues
remaining = 0
lines2 = fixed.split('\n')
for i, line in enumerate(lines2):
    stripped = line.rstrip()
    if (stripped.endswith('`)') or stripped.endswith("')") or stripped.endswith('")')):
        # Check next non-empty non-comment line
        j = i + 1
        while j < len(lines2):
            ns = lines2[j].strip()
            if not ns or ns.startswith('//'):
                j += 1
                continue
            if ns.startswith("f('m-"):
                remaining += 1
                print(f'  Still missing comma at line {i+1}: ...{stripped[-30:]}')
            break

print(f'Remaining issues: {remaining}')
