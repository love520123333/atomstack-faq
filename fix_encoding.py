import sys

full_path = r"c:/Users/amyxu/WorkBuddy/20260422134443/machine-faq/src/data/sampleData.js"

with open(full_path, "rb") as f:
    raw = f.read()

print(f"文件大小: {len(raw)} 字节")
print(f"头4字节: {list(raw[:4])}")

# 处理 BOM
if raw[:3] == b'\xef\xbb\xbf':
    print("发现 UTF-8 BOM，去除...")
    raw = raw[3:]
elif raw[:2] == b'\xff\xfe':
    print("发现 UTF-16 LE BOM，重新解码...")
    content = raw.decode('utf-16-le')
    raw = content.encode('utf-8')
    print(f"  解码后: {len(content)} 字符")
elif raw[:2] == b'\xfe\xff':
    print("发现 UTF-16 BE BOM，重新解码...")
    content = raw[2:].decode('utf-16-be')
    raw = content.encode('utf-8')

# 统一换行符为 LF
content = raw.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')

with open(full_path, 'wb') as f:
    f.write(content.encode('utf-8'))

with open(full_path, "rb") as f:
    first4 = f.read(4)
print(f"修复后头4字节: {list(first4)}")
print(f"修复后文件大小: {len(content.encode('utf-8'))} 字节")
print("完成！")
