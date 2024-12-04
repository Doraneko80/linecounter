import os
import re
from tabulate import tabulate

# Define comment patterns for various languages, including .jsp, .css, and .js files
COMMENT_PATTERNS = {
    '.py': r'^\s*#',            # Python
    '.js': r'^\s*//',           # JavaScript
    '.jsp': r'^\s*//',          # JSP (JavaServer Pages)
    '.css': r'/\*.*?\*/',       # CSS
    '.html': r'<!--.*?-->',     # HTML
    '.java': r'^\s*//',         # Java
    '.sql': r'^\s*--|/\*.*?\*/',
    # add more extensions and comment patterns as needed
}

def is_comment(line, ext):
    """Check if a line is a comment based on file extension."""
    pattern = COMMENT_PATTERNS.get(ext)
    return pattern is not None and re.match(pattern, line.strip())

def count_lines(file_path, ext):
    """Count non-blank, non-comment lines in a single file."""
    line_count = 0
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            if line.strip() == '' or is_comment(line, ext):
                continue
            line_count += 1
    return line_count

def count_lines_in_folder(folder_path):
    """Walk through folder, count lines by file extension, calculate sizes, and count files."""
    total_counts = {}
    total_sizes = {}  # Size of non-blank, non-comment lines in MB
    total_files = {}  # Count of files
    total_disk_sizes = {}  # Size on disk for each file type
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            ext = os.path.splitext(file_name)[1].lower()
            if ext not in COMMENT_PATTERNS:
                continue  # Skip files with unsupported extensions
            if ext not in total_counts:
                total_counts[ext] = 0
                total_sizes[ext] = 0.0  # Initialize size for this extension
                total_files[ext] = 0  # Initialize file count for this extension
                total_disk_sizes[ext] = 0.0  # Initialize disk size for this extension
            
            # Count lines and calculate size of non-blank, non-comment lines
            line_count = 0
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    if line.strip() == '' or is_comment(line, ext):
                        continue
                    line_count += 1
                    total_sizes[ext] += len(line.encode('utf-8'))  # Calculate size in bytes
            
            total_counts[ext] += line_count
            total_disk_sizes[ext] += os.path.getsize(file_path) / (1024 * 1024)  # Size on disk in MB
            total_files[ext] += 1  # Increment file count
            
    # Convert total_sizes from bytes to MB
    for ext in total_sizes:
        total_sizes[ext] /= (1024 * 1024)  # Convert bytes to MB

    return total_counts, total_sizes, total_files, total_disk_sizes  # Return counts, sizes, file counts, and disk sizes

# Example usage
folder_path = './'  # Update this path
result, sizes, file_counts, disk_sizes = count_lines_in_folder(folder_path)  # Update to capture sizes, file counts, and disk sizes

# Display the results in a table format
table = [(ext, count, sizes[ext], file_counts[ext], disk_sizes[ext]) for ext, count in result.items()]  # Include sizes, file counts, and disk sizes in the table
print(tabulate(table, headers=["File Extension", "Line Count", "Size of Code (MB)", "File Count", "Disk Size (MB)"], tablefmt="grid"))  # Updated headers
total_lines = sum(result.values())
total_size = sum(sizes.values())  # Calculate total size of non-blank, non-comment lines
total_files_count = sum(file_counts.values())  # Calculate total file count
total_disk_size = sum(disk_sizes.values())  # Calculate total disk size
print(f"Total lines: {total_lines}")
print(f"Total size of non-blank, non-comment lines: {total_size:.2f} MB")  # Display total size of code
print(f"Total files: {total_files_count}")  # Display total file count
print(f"Total disk size: {total_disk_size:.2f} MB")  # Display total disk size
