def generate_code(blocks, output_filename):
    code = [
        "import threading",
        "shared_vars = [0]*100",
        "lock = threading.Lock()",
        "input_values = []",
        "output_values = []"
    ]

    def generate_block_code(block):
        content = block["content"].split(',')
        if block["type"] == "assignment":
            if len(content) == 2:
                return f"shared_vars[{content[0]}] = shared_vars[{content[1]}]"
            else:
                return f"shared_vars[{content[0]}] = {content[1]}"
        elif block["type"] == "input":
            return f"shared_vars[{content[0]}] = input_values.pop(0)"
        elif block["type"] == "output":
            return f"output_values.append(shared_vars[{content[0]}])"
        elif block["type"] == "condition":
            if '==' in content[1]:
                return f"if shared_vars[{content[0]}] == {content[2]}:"
            elif '<' in content[1]:
                return f"if shared_vars[{content[0]}] < {content[2]}:"
            else:
                return ""

    for block in blocks:
        block_code = generate_block_code(block)
        if block["type"] == "condition":
            code.append(block_code)
            code.append(" " * 4 + "pass  # Add true condition logic here")
        else:
            code.append(block_code)

    code = "\n".join(code)
    with open(output_filename, 'w') as file:
        file.write(code)