# Fix smart quotes in comprehensive.html
with open('comprehensive.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace smart quotes with regular quotes
original_content = content
content = content.replace(''', "'")  # Left smart quote
content = content.replace(''', "'")  # Right smart quote
content = content.replace('"', '"')   # Left smart double quote  
content = content.replace('"', '"')   # Right smart double quote

if content != original_content:
    with open('comprehensive.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('✅ Fixed smart quotes in file')
    print('Smart quotes replaced with regular ASCII quotes')
else:
    print('❌ No smart quotes found to replace')