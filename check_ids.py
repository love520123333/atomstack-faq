import re
with open(r'c:\Users\amyxu\WorkBuddy\20260422134443\machine-faq\src\data\sampleData.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Simulate the id counter
ids = []
current_id = 1
pattern = r"f\('m-"
for match in re.finditer(pattern, content):
    ids.append(current_id)
    current_id += 1

print(f"Total FAQs: {len(ids)}")
print(f"ID range: faq-{ids[0]} .. faq-{ids[-1]}")
# Check for duplicates
unique_ids = set(ids)
print(f"Unique IDs: {len(unique_ids)}")
if len(unique_ids) != len(ids):
    print(f"WARNING: {len(ids) - len(unique_ids)} duplicate IDs!")
