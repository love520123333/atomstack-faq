"""
将 batch1-4.js 中的 FAQ 数据合并到 sampleData.js 的 generateFaqs() 函数中。
batch 文件只包含 f() 调用片段，需要插入到 return [...] 数组的末尾。
"""
import re, os

base = r'c:\Users\amyxu\WorkBuddy\20260422134443\machine-faq\src\data'
sample_path = os.path.join(base, 'sampleData.js')

with open(sample_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 找到 generateFaqs 函数中 return [ ... ] 的结束位置
# 寻找最后的 `]` + `}` (return 数组关闭 + 函数关闭)
# generateFaqs 函数在 line 256 开始

# 找到 `  ]\n}\n\nfunction generateFaqs` 之前的 `]` 和 `\n}` 
# 实际结构是:
#   return [
#     f(...),
#     f(...),
#     ...
#   ]
# }
# 
# 我们需要在最后的 `]` 之前（也就是最后一个 f() 调用之后）插入 batch 数据

# 读取所有 batch 文件内容
batch_content = ""
for i in range(1, 5):
    batch_path = os.path.join(base, f'batch{i}.js')
    with open(batch_path, 'r', encoding='utf-8') as f:
        batch_content += f.read() + "\n"

# 找到最后一个 `)` 后面跟着 `]\n}` 的位置
# 也就是 return 数组的关闭括号
# 搜索 pattern: `)`, 可能后跟逗号，然后是 `\n  ]`

# 简单方法：找到 "]\n}" 的位置，这就是 return 数组结束的地方
# 然后在 `]` 之前插入 batch 内容（加逗号分隔）

# 找到 generateFaqs 函数的结束位置
# 函数结构是:
# function generateFaqs() {
#   let id = 1
#   const f = ...
#   return [
#     ...
#   ]
# }

# 在 sampleData.js 中找到最后一个 `]` 后面紧跟 `\n}` 的位置
# 但要确保这是 generateFaqs 的结束，不是别的数组

# 更精确的方法：找到 "  ]\n}\n\nfunction generateFaqs" 或者文件末尾的 "]\n}"
# 根据之前看到的，generateFaqs 是文件中最后一个函数，结束在文件末尾

# 找到文件末尾附近的结构
# 文件最后是:
#   ...`)
#   ]
# }

# 找到匹配的 return 数组的结束 ]
lines = content.split('\n')
# 从后往前找第一个只有 "]" 的行
insert_line_idx = None
for i in range(len(lines) - 1, -1, -1):
    stripped = lines[i].strip()
    if stripped == ']' and i + 1 < len(lines) and lines[i+1].strip() == '}':
        insert_line_idx = i
        break

if insert_line_idx is None:
    print("ERROR: Could not find insertion point")
    exit(1)

print(f"Found insertion point at line {insert_line_idx + 1}")
print(f"Line content: '{lines[insert_line_idx]}'")
print(f"Next line: '{lines[insert_line_idx + 1]}'")

# 检查前一行是否以逗号结尾或反引号结尾
prev_line = lines[insert_line_idx - 1].strip()
print(f"Previous line ends with: '{prev_line[-5:]}'")

# batch 内容需要缩进处理 - 保持和现有数据一样的缩进
# 去掉 batch 文件中已有的缩进，重新用 8 空格缩进（和现有 f() 调用一致）
batch_lines = batch_content.strip().split('\n')
indented_batch = []
for line in batch_lines:
    stripped = line.strip()
    if not stripped:
        indented_batch.append('')
    else:
        indented_batch.append('        ' + stripped)  # 8 spaces indent

batch_text = '\n'.join(indented_batch)

# 在 ] 之前插入 batch 数据（前一行加逗号，如果还没有的话）
if not prev_line.endswith(','):
    lines[insert_line_idx - 1] = lines[insert_line_idx - 1] + ','

# 在 ] 行之前插入 batch 数据
new_lines = lines[:insert_line_idx] + [batch_text] + lines[insert_line_idx:]
new_content = '\n'.join(new_lines)

# 写回文件
with open(sample_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Successfully merged batch data into sampleData.js")
print(f"New file size: {os.path.getsize(sample_path)} bytes")

# 验证
with open(sample_path, 'r', encoding='utf-8') as f:
    new_content_check = f.read()
new_count = new_content_check.count("f('m-")
print(f"Total FAQ entries after merge: {new_count}")
