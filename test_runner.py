import threading
import json
import sys
from io import StringIO

def run_thread(blocks, shared_vars, input_values, output_values):
    i = 0
    while i < len(blocks):
        block = blocks[i]
        content = block["content"].split(',')
        print(f"Executing block: {block}")  # Diagnostic output
        if block["type"] == "assignment":
            if len(content) == 2:
                shared_vars[int(content[0])] = shared_vars[int(content[1])]
            else:
                shared_vars[int(content[0])] = int(content[1])
            i += 1
        elif block["type"] == "input":
            if input_values:
                shared_vars[int(content[0])] = int(input_values.pop(0))
            else:
                raise ValueError("Not enough input values provided.")
            i += 1
        elif block["type"] == "output":
            output_values.append(shared_vars[int(content[0])])
            print(f"Output: {shared_vars[int(content[0])]}")  # Diagnostic output
            i += 1
        elif block["type"] == "condition":
            print(f"Condition block: {block}")  # Diagnostic output
            if content[1] == '==':
                if shared_vars[int(content[0])] == int(content[2]):
                    print(f"Condition true: {block}")  # Diagnostic output
                    i += 1  # Proceed to the next block if the condition is true
                else:
                    print(f"Condition false: {block}")  # Diagnostic output
                    i += 2  # Skip the next block if the condition is false
            elif content[1] == '<':
                if shared_vars[int(content[0])] < int(content[2]):
                    print(f"Condition true: {block}")  # Diagnostic output
                    i += 1  # Proceed to the next block if the condition is true
                else:
                    print(f"Condition false: {block}")  # Diagnostic output
                    i += 2  # Skip the next block if the condition is false
        else:
            i += 1

def run_tests(blocks, test_cases):
    for test_case in test_cases:
        print(f"Running test case: {test_case}")  # Diagnostic output
        shared_vars = [0] * 100
        input_values = test_case["input"] * test_case["num_threads"]  # Duplicate inputs for each thread
        expected_output = test_case["expected_output"]
        output_values = []

        # Redirect stdin and stdout
        old_stdin = sys.stdin
        old_stdout = sys.stdout
        sys.stdin = StringIO("\n".join(map(str, input_values)) + "\n")
        sys.stdout = StringIO()

        threads = []
        for _ in range(test_case["num_threads"]):
            thread = threading.Thread(target=run_thread, args=(blocks, shared_vars, input_values, output_values))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        sys.stdout.seek(0)
        stdout_output = sys.stdout.read().strip()
        print(f"Raw stdout: {stdout_output}")  # Diagnostic output
        actual_output = output_values

        sys.stdin = old_stdin
        sys.stdout = old_stdout

        print(f"Actual output: {actual_output}")  # Diagnostic output

        if actual_output == expected_output:
            print("Test passed")
            print(f"Expected: {expected_output}")
            print(f"Got: {actual_output}")
        else:
            print("Test failed")
            print(f"Expected: {expected_output}")
            print(f"Got: {actual_output}")

if __name__ == "__main__":
    run_tests(blocks, test_cases)
