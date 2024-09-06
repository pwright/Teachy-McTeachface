#!/usr/bin/env python3

import os
import re
import shutil
import argparse

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

# Function to clean the markdown content (removes first two chars from each line)
def clean_markdown_content(content, is_topic_md=False):
    # Split into YAML header and markdown if applicable
    parts = content.split('---', 2)
    
    if len(parts) < 3:
        # If there isn't a valid YAML + markdown separation, treat it as plain markdown
        markdown_content = content
        yaml_header = ""
    else:
        yaml_header = '---' + parts[1] + '---'  # Keep the YAML header intact
        markdown_content = parts[2]

    # For topic.md, replace '- ' with '# '
    if is_topic_md:
        cleaned_markdown = markdown_content.replace('- ', '# ')
    else:
        # Remove the first two characters from each line for all non-topic.md files
        cleaned_markdown = re.sub(r'^..', '', markdown_content, flags=re.MULTILINE)

    # Recombine YAML header (if present) with cleaned markdown content
    return (yaml_header + '\n' + cleaned_markdown).strip()

# Function to process course.md and move to destination
def process_course_file(source, destination):
    course_md_path = os.path.join(source, 'pages', 'course.md')
    if not os.path.exists(course_md_path):
        print(f"File {course_md_path} not found.")
        return

    # Read and clean content
    with open(course_md_path, 'r') as f:
        content = f.read()

    # Clean the markdown content
    cleaned_content = clean_markdown_content(content)

    # Write to the destination directory directly as 'course.md'
    new_course_md_path = os.path.join(destination, 'course.md')
    with open(new_course_md_path, 'w') as f:
        f.write(cleaned_content)

    print(f'Processed {course_md_path} -> {new_course_md_path} (cleaned content)')

# Function to process and move unit files with cleaning (excluding course.md)
def process_and_move_unit_file(unit_file, destination_dir):
    new_file_path = os.path.join(destination_dir, 'topic.md')

    # Read and clean content
    with open(unit_file, 'r') as f:
        content = f.read()

    # Clean markdown section and replace '- ' with '# ' for topic.md
    cleaned_content = clean_markdown_content(content, is_topic_md=True)

    # Write to the destination as 'topic.md'
    with open(new_file_path, 'w') as f:
        f.write(cleaned_content)

    print(f'Processed {unit_file} -> {new_file_path} (replaced - with # in topic.md)')

# Function to parse the filename and create a new directory structure
def parse_filename_and_move(source, destination):
    pages_dir = os.path.join(source, 'pages')
    assets_dir = os.path.join(source, 'assets')

    for root, dirs, files in os.walk(pages_dir):
        for file in files:
            if file.endswith('.md'):
                if file == 'course.md':
                    # Skip course.md, handled separately
                    continue

                if '___' in file:
                    # Handle files with '___' in the name by creating nested directories
                    original_md_path = os.path.join(root, file)
                    file_stem = file.replace('.md', '')
                    parts = file_stem.split('___')

                    # Create the new directory structure in the destination
                    new_md_dir = os.path.join(destination, *parts[:-1])
                    os.makedirs(new_md_dir, exist_ok=True)

                    # Move the markdown file to the new location
                    new_md_path = os.path.join(new_md_dir, parts[-1] + '.md')

                    # Read and clean the content (remove first 2 characters from each line)
                    with open(original_md_path, 'r') as f:
                        content = f.read()

                    cleaned_content = clean_markdown_content(content)

                    # Write the cleaned content
                    with open(new_md_path, 'w') as f:
                        f.write(cleaned_content)

                    print(f'Processed {original_md_path} -> {new_md_path} (removed first two characters)')

                    # Move referenced assets from the markdown file
                    move_assets(new_md_path, assets_dir, new_md_dir)

                else:
                    # Handle unit-*.md files by copying them as topic.md in their respective directories
                    file_path = os.path.join(root, file)
                    unit_name = file.replace('.md', '')
                    new_unit_dir = os.path.join(destination, unit_name)
                    os.makedirs(new_unit_dir, exist_ok=True)
                    process_and_move_unit_file(file_path, new_unit_dir)

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

# Main function for the command-line tool
def main():
    parser = argparse.ArgumentParser(description='Reorganize markdown files and assets.')
    parser.add_argument('source', type=str, help='Source directory containing the pages and assets.')
    parser.add_argument('destination', type=str, help='Destination directory for reorganized files.')
    parser.add_argument('template', type=str, help='Template directory to populate destination before processing.')

    args = parser.parse_args()

    # Clean destination directory
    clean_destination(args.destination)

    # Populate destination with the template
    populate_with_template(args.template, args.destination)

    # Process course.md specifically
    process_course_file(args.source, args.destination)

    # Run the file parsing and asset moving
    parse_filename_and_move(args.source, args.destination)

if __name__ == '__main__':
    main()
