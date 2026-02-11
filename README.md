# Professional Folder Scanner

A command-line tool that analyzes folder contents and generates detailed reports.

## Features

- Scans all files in a given folder (including subfolders)
- Calculates total file count and total size
- Identifies the largest file
- Provides file type breakdown with counts and sizes
- Saves detailed report to a text file

## Usage

```bash
python3 folder_scanner.py <folder_path>
```

### Example

```bash
python3 folder_scanner.py ~/Desktop
```

## Requirements

- Python 3.x (no additional packages required)

## Output

The tool generates:
1. Console output with the scan results
2. A timestamped report file (e.g., `scan_report_folder-name_20260211_122906.txt`)

## Report Contents

- Scan timestamp
- Folder path
- Total number of files
- Total size (in human-readable format)
- Largest file details
- File types breakdown table

## Example Output

```
============================================================
FOLDER SCAN REPORT
============================================================
Scan Time: 2026-02-11 12:29:06
Folder: /Users/username/test-folder

SUMMARY
------------------------------------------------------------
Total Files: 7
Total Size: 50.33 KB

Largest File: image.jpg
Largest File Size: 50.00 KB

FILE TYPES BREAKDOWN
------------------------------------------------------------
Extension            Count      Total Size
------------------------------------------------------------
.txt                 2          108.00 B
.jpg                 1          50.00 KB
============================================================
```

## License

MIT
