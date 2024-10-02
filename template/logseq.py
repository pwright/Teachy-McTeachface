#!/usr/bin/env python3

# UID: replace with a unique identifier each time

import os
import re
import shutil
import argparse
import yaml
from datetime import datetime

# Function to clean the destination directory
def clean_destination(destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)  # Remove everything inside the destination directory
    os.makedirs(destination)  # Recreate the directory (empty)

# Function to populate destination with the template
def populate_with_template(template, destination):
    if os.path.exists(template):
        # Copy the template contents to the destination directory
        shutil.copytree(template, destination, dirs_exist_ok=True)

# Function to process and fix markdown headers
def process_markdown_headers(content):
    """
    Replace escaped front matter delimiters (\---) with standard delimiters (---).
    """
    # Replace \--- with ---
    content = re.sub(r'\\---', '---', content)
    return content

# Function to clean markdown content, using the logic to remove top-level bullet points
def clean_markdown_content(content, uid=None, strip_leading_dash=True):
    # First, process markdown headers
    content = process_markdown_headers(content)

    lines = content.splitlines()

    processed_lines = []
    for line in lines:
        # Check if it's a top-level item (starting with '- ' and no preceding tabs or spaces)
        if strip_leading_dash and line.startswith('- ') and not line.startswith('\t'):
            # Remove the '- ' from the start of the line and left-strip spaces
            processed_lines.append(line[2:].lstrip())
        elif line.startswith('\t'):
            # Remove the '\t' from the start of the line and left-strip spaces
            processed_lines.append(line[1:].lstrip())
        else:
            # Keep other lines (including subtasks) unchanged
            processed_lines.append(line)

    # Join the processed lines back into the cleaned markdown
    cleaned_markdown = '\n'.join(processed_lines)

    # Add the UID as a comment at the end of the markdown content
    if uid:
        cleaned_markdown += f"\n\n<!-- UID: {uid} -->"

    return cleaned_markdown.strip()

# Function to process course.md and move to destination
def process_course_file(source, destination, uid, strip_leading_dash):
    course_md_path = os.path.join(source, 'pages', 'course.md')
    if not os.path.exists(course_md_path):
        print(f"File {course_md_path} not found.")
        return

    # Read and clean content
    with open(course_md_path, 'r') as f:
        content = f.read()

    # Clean the markdown content and include the UID in the markdown output
    cleaned_content = clean_markdown_content(content, uid=uid, strip_leading_dash=strip_leading_dash)

    # Write to the destination directory directly as 'course.md'
    new_course_md_path = os.path.join(destination, 'course.md')
    with open(new_course_md_path, 'w') as f:
        f.write(cleaned_content)

    print(f'Processed {course_md_path} -> {new_course_md_path} (cleaned content, UID added)')

# Function to process and move unit files with cleaning (topic.md handling)
def process_and_move_unit_file(unit_file, destination_dir, uid, strip_leading_dash):
    new_file_path = os.path.join(destination_dir, 'topic.md')

    # Read and clean content
    with open(unit_file, 'r') as f:
        content = f.read()

    # Clean markdown content using the top-level bullet removal logic
    cleaned_content = clean_markdown_content(content, uid=uid, strip_leading_dash=strip_leading_dash)

    # Write to the destination as 'topic.md'
    with open(new_file_path, 'w') as f:
        f.write(cleaned_content)

    print(f'Processed {unit_file} -> {new_file_path} (cleaned top-level bullets, UID added)')

# Function to parse the filename and create a new directory structure
def parse_filename_and_move(source, destination, uid, separator, strip_leading_dash):
    pages_dir = os.path.join(source, 'pages')
    assets_dir = os.path.join(source, 'assets')

    for root, dirs, files in os.walk(pages_dir):
        for file in files:
            # Skip files named 'contents.md' or 'template.md'
            if file in ['contents.md', 'template.md']:
                print(f"Skipping file: {file}")
                continue

            if file.endswith('.md'):
                if file == 'course.md':
                    # Skip course.md, handled separately
                    continue

                if separator in file:
                    # Handle files with separator in the name by creating nested directories
                    original_md_path = os.path.join(root, file)
                    file_stem = file.replace('.md', '')
                    parts = file_stem.split(separator)

                    # Create the new directory structure in the destination
                    new_md_dir = os.path.join(destination, *parts[:-1])
                    os.makedirs(new_md_dir, exist_ok=True)

                    # Move the markdown file to the new location
                    new_md_path = os.path.join(new_md_dir, parts[-1] + '.md')

                    # Read and clean the content
                    with open(original_md_path, 'r') as f:
                        content = f.read()

                    cleaned_content = clean_markdown_content(content, uid=uid, strip_leading_dash=strip_leading_dash)

                    # Write the cleaned content
                    with open(new_md_path, 'w') as f:
                        f.write(cleaned_content)

                    print(f'Processed {original_md_path} -> {new_md_path} (cleaned top-level bullets, UID added)')

                    # Move referenced assets from the markdown file
                    move_assets(new_md_path, assets_dir, new_md_dir)

                else:
                    # Handle unit-*.md files by copying them as topic.md in their respective directories
                    file_path = os.path.join(root, file)
                    unit_name = file.replace('.md', '')
                    new_unit_dir = os.path.join(destination, unit_name)
                    os.makedirs(new_unit_dir, exist_ok=True)
                    process_and_move_unit_file(file_path, new_unit_dir, uid, strip_leading_dash)

# Function to move assets referenced in markdown files
def move_assets(md_file, assets_dir, new_md_dir):
    asset_folder_name = "img"
    asset_folder_path = os.path.join(new_md_dir, asset_folder_name)
    os.makedirs(asset_folder_path, exist_ok=True)

    # Read the markdown file and search for asset references
    with open(md_file, 'r') as f:
        content = f.read()

    # Regex to find image references with relative paths from '../assets/'
    asset_references = re.findall(r'!\[.*?\]\((\.\./assets/.*?)\)', content)

    for ref in asset_references:
        # Resolve the asset's original location
        asset_source_path = os.path.normpath(os.path.join(assets_dir, os.path.basename(ref)))

        # If the asset exists, move it
        if os.path.exists(asset_source_path):
            new_asset_path = os.path.join(asset_folder_path, os.path.basename(asset_source_path))
            shutil.copy2(asset_source_path, new_asset_path)

            # Update the markdown file with the new asset path
            updated_ref = os.path.join(asset_folder_name, os.path.basename(asset_source_path))
            content = content.replace(ref, updated_ref)

    # Write the updated markdown file
    with open(md_file, 'w') as f:
        f.write(content)

# Function to generate a unique UID based on the current date and time
def generate_uid():
    return datetime.now().strftime("%Y-%m-%d-%H%M%S-uid")

# Main function for the command-line tool
def main():
    parser = argparse.ArgumentParser(description='Reorganize markdown files and assets.')
    parser.add_argument('source', type=str, help='Source directory containing the pages and assets.')
    parser.add_argument('destination', type=str, help='Destination directory for reorganized files.')
    parser.add_argument('template', type=str, help='Template directory to populate destination before processing.')
    parser.add_argument('-c', '--config', type=str, default='config.yaml', help='Path to the configuration file (default: config.yaml)')

    args = parser.parse_args()

    # Load configuration
    if os.path.exists(args.config):
        with open(args.config, 'r') as config_file:
            try:
                config = yaml.safe_load(config_file)
                separator = config.get('separator', '___')
                strip_leading_dash = config.get('strip_leading_dash', True)
            except yaml.YAMLError as e:
                print(f"Error parsing the config file: {e}")
                return
    else:
        print(f"Config file {args.config} not found. Using default settings.")
        separator = '___'
        strip_leading_dash = True

    # Generate a unique identifier for this version of the script
    uid = "2024-10-01-uid789"  # Replace with actual UID generation logic if desired

    # Clean destination directory
    clean_destination(args.destination)

    # Populate destination with the template
    populate_with_template(args.template, args.destination)

    # Process course.md specifically
    process_course_file(args.source, args.destination, uid, strip_leading_dash)

    # Run the file parsing and asset moving
    parse_filename_and_move(args.source, args.destination, uid, separator, strip_leading_dash)

if __name__ == '__main__':
    main()

