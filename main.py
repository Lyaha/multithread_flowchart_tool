import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
import json
from code_generator import generate_code
from test_runner import run_tests


class BlockSchemeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Block Scheme Editor")
        self.blocks = []
        self.create_ui()

    def create_ui(self):
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(fill=tk.X)

        self.add_block_button = tk.Button(self.toolbar, text="Add Block", command=self.add_block)
        self.add_block_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.toolbar, text="Save", command=self.save)
        self.save_button.pack(side=tk.LEFT)

        self.load_button = tk.Button(self.toolbar, text="Load", command=self.load)
        self.load_button.pack(side=tk.LEFT)

        self.generate_code_button = tk.Button(self.toolbar, text="Generate Code", command=self.generate_code)
        self.generate_code_button.pack(side=tk.LEFT)

        self.run_tests_button = tk.Button(self.toolbar, text="Run Tests", command=self.run_tests)
        self.run_tests_button.pack(side=tk.LEFT)

    def add_block(self):
        block_type = simpledialog.askstring("Input", "Enter block type (assignment, input, output, condition):")
        if block_type:
            content = simpledialog.askstring("Input",
                                             "Enter block content (for assignment: V1,V2 or V,C; for input/output: V; for condition: V op C):")
            block = {"type": block_type, "content": content}
            self.blocks.append(block)
            self.draw_blocks()

    def draw_blocks(self):
        self.canvas.delete("all")
        y = 20
        for i, block in enumerate(self.blocks):
            self.canvas.create_rectangle(50, y, 750, y + 50, fill="lightgrey")
            self.canvas.create_text(400, y + 25, text=f"{i + 1}. {block['type']}: {block['content']}")
            y += 60

    def save(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'w') as file:
                json.dump(self.blocks, file)

    def load(self):
        filename = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'r') as file:
                self.blocks = json.load(file)
            self.draw_blocks()

    def generate_code(self):
        filename = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py")])
        if filename:
            generate_code(self.blocks, filename)
            messagebox.showinfo("Info", "Code generated successfully")

    def run_tests(self):
        test_cases_file = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if test_cases_file:
            with open(test_cases_file, 'r') as file:
                test_cases = json.load(file)
            run_tests(self.blocks, test_cases)


if __name__ == "__main__":
    root = tk.Tk()
    app = BlockSchemeEditor(root)
    root.mainloop()
