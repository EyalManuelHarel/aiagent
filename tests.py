#!/home/eyal/aiagent/.venv/bin/python python

from functions.get_files_info import get_files_info, get_file_content, write_file, run_python_file

def test():
    result = run_python_file("calculator", "main.py")
    print(result + "\n")

    # Test with a directory outside the working directory
    result = run_python_file("calculator", "tests.py")
    print(result + "\n")

    result = run_python_file("calculator", "../main.py")
    print(result + "\n")

    result = run_python_file("calculator", "nonexistent.py")
    print(result)

if __name__ == "__main__":
    test()