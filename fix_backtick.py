#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix unescaped backticks inside JS template strings in sampleData.js.
Strategy: replace Markdown inline code backticks `code` with [code] inside template strings.
"""
import re

INPUT = 'src/data/sampleData.js'

with open(INPUT, 'r', encoding='utf-8') as fh:
    content = fh.read()

print('File loaded, length:', len(content))

# Strategy: parse template string segments and replace inline ` ` with [ ]
# Split by unescaped backtick pairs
# Index 0: before first template, 1: first template content, 2: between templates, 3: second template content, etc.

# Count backticks first
total_backticks = content.count('`')
print('Total backticks:', total_backticks)
# Should be even: (open + close) * N

# Simple substitution: inside template strings (odd-indexed segments after split),
# replace inline code `something` with [something]
# But we need to avoid replacing the template string boundaries themselves.

# Split on unescaped backtick (not preceded by backslash)
# Use re.split with lookahead/lookbehind won't work cleanly
# Instead: iterate character by character

segments = []
current = []
in_template = False

i = 0
while i < len(content):
    c = content[i]
    # Check if backtick is escaped
    bs_count = 0
    j = i - 1
    while j >= 0 and content[j] == '\\':
        bs_count += 1
        j -= 1
    is_escaped = (bs_count % 2 == 1)
    
    if c == '`' and not is_escaped:
        segments.append(''.join(current))
        current = []
        in_template = not in_template
        # Keep the backtick as segment separator marker
        segments.append('`')  # This is just a marker
        # Actually let's just build differently
    else:
        current.append(c)
    i += 1
segments.append(''.join(current))

# segments is: [before_bt1, '`', content1, '`', between, '`', content2, '`', ...]
# Odd positions (0-indexed after filtering markers): '`' are separators
# Let's rebuild: non-backtick segments alternate with backtick markers

# Simpler: rebuild the file, replacing inline code in template strings
# The segments list has structure:
# [text, '`', text, '`', text, '`', text, '`', ...]
#   0     1    2    3    4     5    6     7    ...
# Segments at even indices (0, 2, 4...) are normal code
# Odd-index segments are just '`' markers
# Template string CONTENTS are at indices 2, 6, 10... (every 4th starting at 2)
# Between-template text is at indices 4, 8, 12...

# Wait, let me redo this more clearly.
# After split-by-backtick (not the markers but actual content):
# parts[0] = before first `
# parts[1] = content of first template string  <- needs inline backtick fix
# parts[2] = code between first and second template strings
# parts[3] = content of second template string <- needs inline backtick fix
# etc.

# But our segments list has '`' as actual items mixed in.
# Let's filter to get just the text parts:
text_parts = [s for s in segments if s != '`']
print('Number of text segments:', len(text_parts))
# Even indices (0, 2, 4...): normal code (between templates)
# Odd indices (1, 3, 5...): template string contents

# But wait: template string contents themselves cannot contain backticks
# (that's the whole problem!). If they do, it means our split was wrong.
# Actually our split IS correct: when we encounter a ` inside a template string,
# it ENDS the template string (from JS parser's perspective, same as Python's perspective here).
# So text_parts[1] is the "first template string content up to the first unescaped backtick inside it"

# The fix is: in odd-indexed text_parts, inline backtick pairs SHOULD be escaped.
# But since we already split them out, what we see in odd segments is already "broken up".

# Let me try a completely different approach:
# Just find all lines that contain backtick pairs (even count) that are NOT
# template string boundary lines, and replace the backtick pairs with [...]

print()
print('Using line-by-line approach:')

lines = content.split('\n')
fixed_lines = []
fix_count = 0

for lineno, line in enumerate(lines, 1):
    # Detect lines that contain backtick pairs for Markdown inline code
    # These are lines inside template string content that have `code` patterns
    # Characteristics:
    #   - The line does NOT end with `), or `):  (template string end)
    #   - The line does NOT start with f( or just `  (template string start at end of f() args)
    #   - The line contains backticks in pairs (even count)
    
    stripped = line.strip()
    backtick_count = line.count('`')
    
    if backtick_count == 0:
        fixed_lines.append(line)
        continue
    
    # Check if this line is a template string boundary
    # Template start: line ends with: `\n (a line that has the opening backtick at end)
    #   e.g.: "      `## title\n" - actually content starts on same line
    #   or just: the last char before newline is `
    # Template end: line ends with `), or `)
    
    is_template_end = (stripped.endswith('`),') or stripped.endswith('`)') or stripped == '`')
    # Template start usually: contains `## or starts content with `
    # Actually the opening backtick of a template string in f() args ends a line like:
    # "      `## Title\n..."  - first line of content
    
    if backtick_count % 2 == 0 and not is_template_end:
        # Even number of backticks on this line, not a boundary - likely Markdown inline code
        # Replace `...` pairs with [...] 
        new_line = re.sub(r'`([^`\n]+)`', r'[\1]', line)
        if new_line != line:
            fix_count += 1
            fixed_lines.append(new_line)
            continue
    
    fixed_lines.append(line)

print(f'Fixed {fix_count} lines with inline backtick pairs')

fixed_content = '\n'.join(fixed_lines)

# Verify the fix reduced the problem
# Count lines with inline backtick pairs (should be 0 or close to 0)
remaining_bad = 0
for line in fixed_content.split('\n'):
    stripped = line.strip()
    if stripped.count('`') >= 2 and not stripped.endswith('`),') and not stripped.endswith('`)'):
        remaining_bad += 1

print(f'Remaining potentially bad lines: {remaining_bad}')

with open(INPUT, 'w', encoding='utf-8') as fh:
    fh.write(fixed_content)

print('File written.')
print(f'Size: {len(fixed_content)} bytes')
