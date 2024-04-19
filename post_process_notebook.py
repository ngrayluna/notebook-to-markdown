#!/bin/usr/python

import os
import re
import argparse

# broken_tmp ={
#     "Credit_Scorecards_with_XGBoost_and_W&B" : "xgboost",
#     "Simple_LightGBM_Integration": "lightgbm",
# }

# no_longer = {
#         "RayTune_with_wandb": "",
#         "Weights_&_Biases_with_fastai": "",
#         "WandB_Prompts_Quickstart":"",    
# }

title_mapping = {
    "Intro_to_Weights_&_Biases": "experiments",
    "Pipeline_Versioning_with_W&B_Artifacts": "artifacts",
    "Model_Registry_E2E": "models",
    "W&B_Tables_Quickstart": "tables",
    "Organizing_Hyperparameter_Sweeps_in_PyTorch_with_W&B": "sweeps",
    "Using_W&B_Sweeps_with_XGBoost": "xgboost_sweeps",
    "Simple_PyTorch_Integration": "pytorch",
    "Huggingface_wandb": "huggingface",
    "Hyperparameter_Optimization_in_TensorFlow_using_W&B_Sweeps": "tensorflow_sweeps",
    "Image_Classification_using_PyTorch_Lightning": "lightning",
    "Simple_TensorFlow_Integration": "tensorflow",
    "Use_WandbMetricLogger_in_your_Keras_workflow": "keras",
    "Use_WandbEvalCallback_in_your_Keras_workflow": "keras_table",
    "Use_WandbModelCheckpoint_in_your_Keras_workflow": "keras_models",
}

def rename_markdown_file(filename, title_names):
    "Rename notebook file."
    # Check if .ipynb name exists in our mapping

    base_name = os.path.basename(filename).split('.')[0]
    if base_name in title_names:
        new_filename = title_names[base_name]

        # Rename file
        print(f"Renaming notebook from {filename} to {new_filename}.md")
        os.rename(filename, new_filename+".md")


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
        cta_button = "<CTAButtons colab_button='"+ href_links[0] + "'/>"
    
    return cta_button

def remove_patterns_from_markdown(markdown_text):
    # Define the regex patterns to match <img> tags and the specified comment
    img_pattern = r'<img[^>]+>'    
    comment_pattern = r'<!--- @wandbcode{intro-colab} -->'
    empty_a_tag_pattern=r'<a\s+[^>]*\s*href\s*=\s*"[^"]*"\s*[^>]*>.*?</a>'

    # Use re.sub() to replace all occurrences of the patterns with an empty string
    cleaned_text = re.sub(img_pattern, '', markdown_text)
    cleaned_text = re.sub(comment_pattern, '', cleaned_text)
    cleaned_text = re.sub(empty_a_tag_pattern, '', cleaned_text)

    return cleaned_text


def main(args):

    # Read the content of the input Markdown file
    with open(args.file, 'r') as file:
        markdown_text = file.read()

    # Extract href links from the Markdown content
    href_links = extract_href_links_from_markdown(markdown_text)

    # Create CTA button format
    colab_button_markdown = format_CTA_button(href_links)

    # Modify the Markdown content (e.g., remove <img> tags and specified comment)
    cleaned_markdown = remove_patterns_from_markdown(markdown_text)

    # Write the modified Markdown content to the output file
    with open(args.file, 'w') as file:
        file.write(add_import_statement())
        file.write(colab_button_markdown)
        #file.write(add_title(title))  # To do
        file.write(cleaned_markdown)

    print("Checking if we need to rename notebook")
    # Rename notebook
    rename_markdown_file(args.file, title_mapping)

    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="markdown file to process")
    args = parser.parse_args()

    print("Formatting markdown...")
    main(args)
    print("Formatting done!")