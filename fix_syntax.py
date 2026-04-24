#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 sampleData.js 中所有 f() 调用之间缺逗号的问题
旧格式的 f() 以 `) 结束（反引号+右括号），然后空行后跟下一个 f(
需要在 `) 后面加上逗号变为 `),
"""
import re

INPUT = 'src/data/sampleData.js'

with open(INPUT, 'r', encoding='utf-8') as fh:
    content = fh.read()

# 统计修复前的问题数
# 模式：反引号 + 右括号 + 换行 + （可选空行） + 空格 + f(
# 需要在 `) 后加逗号
# 注意：这种 `) 结尾然后下一行是 f( 的情况说明缺逗号
pattern = r'(`\))\n(\n    f\()'
matches = list(re.finditer(pattern, content))
print(f'找到 {len(matches)} 处缺逗号的位置')

# 修复：在 `) 后面加逗号
fixed = re.sub(pattern, r'`),\n\2', content)

# 也处理 `) 后面有多个空行的情况
pattern2 = r'(`\))\n\n\n(\s+f\()'
matches2 = list(re.finditer(pattern2, fixed))
if matches2:
    print(f'另外找到 {len(matches2)} 处三空行缺逗号')
    fixed = re.sub(pattern2, r'`),\n\n\2', fixed)

if fixed == content:
    print('文件无需修改（可能已经正确）')
else:
    with open(INPUT, 'w', encoding='utf-8') as fh:
        fh.write(fixed)
    print('文件修复完成！')

# 重新验证 - 检查是否还有问题
with open(INPUT, 'r', encoding='utf-8') as fh:
    check = fh.read()

remaining = list(re.finditer(r'`\)\n\n    f\(', check))
print(f'修复后剩余问题: {len(remaining)} 处')
