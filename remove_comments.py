import pyparsing
import re
import os
import sys

data = ''
if len(sys.argv) - 1 == 1:
    filename = sys.argv[1]

    try:
        with open(filename, 'r', encoding="utf-8") as file:
            data = file.read()

            multiline_comment = pyparsing.nestedExpr("#|", "|#").suppress()
            data = multiline_comment.transformString(data)

            data = re.sub(r'#.*\n', '\n', data)

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
else:
    print("ERROR: python3 remove_comments.py <pyret-file.arr>")
