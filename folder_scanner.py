#!/usr/bin/env python3
"""
Folder Scanner - A command-line tool to analyze folder contents
Usage: python3 folder_scanner.py <folder_path> [OPTIONS]

Options:
  --ext EXTENSION    Filter by file extension (e.g., --ext .txt or --ext txt)
  --min-size SIZE    Filter by minimum file size in bytes (e.g., --min-size 1024)
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def format_size(size_bytes):
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def scan_folder(folder_path, filter_extension=None, min_size=None):
    """Scan folder and collect statistics

    Args:
        folder_path: Path to the folder to scan
        filter_extension: Optional file extension to filter by (e.g., '.txt' or 'txt')
        min_size: Optional minimum file size in bytes
    """
    folder = Path(folder_path)

    # Normalize filter extension
    if filter_extension:
        if not filter_extension.startswith('.'):
            filter_extension = '.' + filter_extension
        filter_extension = filter_extension.lower()

    if not folder.exists():
        print(f"Error: Folder '{folder_path}' does not exist.")
        sys.exit(1)

    if not folder.is_dir():
        print(f"Error: '{folder_path}' is not a folder.")
        sys.exit(1)

    # Statistics
    total_files = 0
    total_size = 0
    largest_file = None
    largest_size = 0
    file_types = defaultdict(int)
    file_type_sizes = defaultdict(int)

    print(f"Scanning folder: {folder.absolute()}")
    if filter_extension:
        print(f"Filtering by extension: {filter_extension}")
    if min_size:
        print(f"Filtering by minimum size: {format_size(min_size)}")
    print("Please wait...\n")

    # Walk through all files
    for item in folder.rglob('*'):
        if item.is_file():
            try:
                # Get file extension
                extension = item.suffix.lower() if item.suffix else '.no-extension'

                file_size = item.stat().st_size

                # Apply extension filter if specified
                if filter_extension and extension != filter_extension:
                    continue

                # Apply size filter if specified
                if min_size and file_size < min_size:
                    continue
                total_files += 1
                total_size += file_size

                # Track largest file
                if file_size > largest_size:
                    largest_size = file_size
                    largest_file = item

                # Track file types
                file_types[extension] += 1
                file_type_sizes[extension] += file_size

            except (PermissionError, OSError) as e:
                print(f"Warning: Could not access {item}: {e}")

    return {
        'folder_path': folder.absolute(),
        'total_files': total_files,
        'total_size': total_size,
        'largest_file': largest_file,
        'largest_size': largest_size,
        'file_types': dict(file_types),
        'file_type_sizes': dict(file_type_sizes),
        'scan_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'filter_extension': filter_extension,
        'min_size': min_size
    }


def generate_report(stats):
    """Generate a formatted report"""
    report = []
    report.append("=" * 60)
    report.append("FOLDER SCAN REPORT")
    report.append("=" * 60)
    report.append(f"Scan Time: {stats['scan_time']}")
    report.append(f"Folder: {stats['folder_path']}")
    if stats.get('filter_extension'):
        report.append(f"Filter: {stats['filter_extension']} files only")
    if stats.get('min_size'):
        report.append(f"Minimum size: {format_size(stats['min_size'])}")
    report.append("")

    report.append("SUMMARY")
    report.append("-" * 60)
    report.append(f"Total Files: {stats['total_files']}")
    report.append(f"Total Size: {format_size(stats['total_size'])}")
    report.append("")

    if stats['largest_file']:
        report.append(f"Largest File: {stats['largest_file'].name}")
        report.append(f"Largest File Path: {stats['largest_file']}")
        report.append(f"Largest File Size: {format_size(stats['largest_size'])}")
    else:
        report.append("No files found")
    report.append("")

    if stats['file_types']:
        report.append("FILE TYPES BREAKDOWN")
        report.append("-" * 60)
        report.append(f"{'Extension':<20} {'Count':<10} {'Total Size'}")
        report.append("-" * 60)

        # Sort by count (descending)
        sorted_types = sorted(stats['file_types'].items(),
                            key=lambda x: x[1],
                            reverse=True)

        for ext, count in sorted_types:
            size = format_size(stats['file_type_sizes'][ext])
            report.append(f"{ext:<20} {count:<10} {size}")

    report.append("=" * 60)

    return "\n".join(report)


def save_report(report_text, folder_path):
    """Save report to a text file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = Path(folder_path).name
    report_filename = f"scan_report_{folder_name}_{timestamp}.txt"

    with open(report_filename, 'w') as f:
        f.write(report_text)

    return report_filename


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python3 folder_scanner.py <folder_path> [OPTIONS]")
        print("Example: python3 folder_scanner.py ~/Documents")
        print("Example: python3 folder_scanner.py ~/Documents --ext .txt")
        print("Example: python3 folder_scanner.py ~/Documents --min-size 1024")
        sys.exit(1)

    folder_path = sys.argv[1]
    filter_extension = None
    min_size = None

    # Parse optional arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--ext' and i + 1 < len(sys.argv):
            filter_extension = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--min-size' and i + 1 < len(sys.argv):
            try:
                min_size = int(sys.argv[i + 1])
            except ValueError:
                print(f"Error: Invalid size value '{sys.argv[i + 1]}'")
                sys.exit(1)
            i += 2
        else:
            i += 1

    # Expand user path (e.g., ~/ -> /Users/username/)
    folder_path = os.path.expanduser(folder_path)

    # Scan the folder
    stats = scan_folder(folder_path, filter_extension, min_size)

    # Generate report
    report_text = generate_report(stats)

    # Display report
    print(report_text)

    # Save report
    report_file = save_report(report_text, folder_path)
    print(f"\nReport saved to: {report_file}")


if __name__ == "__main__":
    main()
