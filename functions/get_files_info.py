import os
import subprocess
import sys
# from aiagent.config import CHAR_READ_LIMIT

def get_files_info(working_directory, directory=None):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = abs_working_dir
    if directory:
        target_dir = os.path.abspath(os.path.join(working_directory, directory))
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    try:
        files_info = []
        for filename in os.listdir(target_dir):
            filepath = os.path.join(target_dir, filename)
            file_size = 0
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            files_info.append(
                f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"
    

def get_file_content(working_directory, file_path):
    if "Cannot list" in get_files_info(working_directory, file_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    try:
        with open(abs_file_path, 'r', encoding='utf-8') as f:
            content = f.read(10000)
            if f.read(1):  # Check if there is more content after 10000 chars
                content += f'\n[...File "{file_path}" truncated at 10000 characters]'
            return content
    except Exception as e:
        return f"Error: can't read file {e}"
    

def write_file(working_directory, file_path, content):
    if "Cannot list" in get_files_info(working_directory, file_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    try:
        with open(abs_file_path, 'w', encoding='utf-8') as f:
            result = f.write(content)
            if result > 0:
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            return "Error: can't write to file"
    except Exception as e:
        return f"Error: can't write to file {e}"


def run_python_file(working_directory, file_path):
    if "Cannot list" in get_files_info(working_directory, file_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if os.path.splitext(abs_file_path)[1] != ".py":
        return f'Error: "{file_path}" is not a Python file.'
    try:
        result = subprocess.run([sys.executable, abs_file_path], stdout=True, stderr=True, cwd=working_directory, timeout=30)
        return_str = f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}'
        if result.stdout == None:
            return_str += "\nNo output produced."
        if result.returncode != 0:
            return_str += f'\nProcess exited with code {result.returncode}'
        return return_str
    except Exception as e:
        return f"Error: executing Python file: {e}"
