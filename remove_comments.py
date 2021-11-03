import pyparsing
import re
import os
import sys

data = ''
filename = sys.argv[1]

try:
    with open(filename, 'a+', encoding="utf-8") as first:
        first.write("\n")
        
    with open(filename, 'r', encoding="utf-8") as file:
        data = file.read()

        multiline_comment = pyparsing.nestedExpr("#|", "|#").suppress()
        data = multiline_comment.transformString(data)

        data = re.sub(r'#.*\n', '\n', data)
        data = re.sub(r'include image\n', "include tables\n", data)
        data = re.sub(r'->\s*Image\s*:', ":", data)
        table_pattern = r'include shared-gdrive\(\"dcic-2021\", \"1wyQZj_L0qqV9Ekgr9au6RX2iqt2Ga8Ep\"\)'
        num_occur = len(re.findall(table_pattern, data))
        if num_occur > 1: data = re.sub(table_pattern, "", data, count=num_occur-1)
        data = re.sub(r'use context essentials2021', 'include essentials2021', data)

    os.remove(filename)
    output = open(filename, "w", encoding="utf-8")

    if 'provide *' not in data:
        output.write('provide *\n')
    if 'provide-types *' not in data:
        output.write('provide-types *\n')

    output.write(data)
    output.close()
except FileNotFoundError:
    print(f"ERROR: File {sys.argv[1]} not found.")
