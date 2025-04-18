#!/bin/usr/python

import os
import re
import argparse

markdown_titles = {
    "Organizing_Hyperparameter_Sweeps_in_PyTorch_with_W&B": "Tune Hyperparameters",
    "Intro_to_Weights_&_Biases":"Track experiments",
    "W&B_Tables_Quickstart": "View and analyze model predictions during training",
    "Pipeline_Versioning_with_W&B_Artifacts": "Track models and datasets"

}


def add_title(filename, page_titles):
    base_name = os.path.basename(filename).split('.')[0]

    if base_name in markdown_titles:
        return f"# {page_titles[base_name]}\n\n"
    else:
        print("Missing markdown title...setting title to 'W&B Tutorial' " )
        return f"# W&B Tutorial\n\n"



def add_import_statement():
    # Add CTA import statement
    return "import { CTAButtons } from '@site/src/components/CTAButtons/CTAButtons.tsx'\n\n"

def extract_href_links_from_markdown(markdown_text):
    # Define the regex pattern to match href attribute value in anchor tags
    href_pattern = r'<a\s+href="([^"]+)"'

    # Use re.findall() to find all href attribute values in the Markdown text
    href_links = re.findall(href_pattern, markdown_text)
    return href_links

def format_CTA_button(href_links):
    # Find index where colab URL link is
    indices = [index for (index, item) in enumerate(href_links) if "colab" in item]
    # Only get the first URL link
    if len(indices) == 1:
        cta_button = "<CTAButtons colabLink='"+ href_links[0] + "'/>"
        return cta_button
    else:
        return ''

def remove_patterns_from_markdown(markdown_text):
    # Define the regex patterns to match <img> tags and the specified comment
    img_pattern = r'<img[^>]+>'
    div_pattern = r'<div\b[^>]*>.*?</div>'
    comment_pattern = r'<!---\s*@wandbcode\{.*?\}\s*-->'
    empty_a_tag_pattern=r'<a\s+[^>]*\s*href\s*=\s*"[^"]*"\s*[^>]*>.*?</a>'

    # Use re.sub() to replace all occurrences of the patterns with an empty string
    cleaned_text = re.sub(img_pattern, '', markdown_text)
    cleaned_text = re.sub(div_pattern, '', cleaned_text)
    cleaned_text = re.sub(comment_pattern, '', cleaned_text)
    cleaned_text = re.sub(empty_a_tag_pattern, '', cleaned_text)

    return cleaned_text


def main(args):

    # Read the content of the input Markdown file
    with open(args.file, 'r') as file:
        markdown_text = file.read()

    # Extract href links from the Markdown content
    href_links = extract_href_links_from_markdown(markdown_text)

    # Create title of markdown file
    page_title = add_title(args.file, markdown_titles)

    # Create CTA button format
    colab_button_markdown = format_CTA_button(href_links)

    # Modify the Markdown content (e.g., remove <img> tags and specified comment)
    cleaned_markdown = remove_patterns_from_markdown(markdown_text)

    # Write the modified Markdown content to the output file
    with open(args.file, 'w') as file:
        file.write(add_import_statement())
        file.write(page_title)  # To do
        file.write(colab_button_markdown)
        file.write(cleaned_markdown)

    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("file", nargs="*", help="markdown file to process")
    parser.add_argument("file", help="markdown file to process")
    args = parser.parse_args()
    main(args)