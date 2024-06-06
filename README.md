# File Converter README

This project is a Streamlit application that converts text files into Markdown, Word, PDF, and RTF formats. Users can upload a text file or paste text directly into the app, and optionally upload images to replace any image placeholders found in the text.

## Streamlit App URL

You can access the live Streamlit app here: [https://txt-md.streamlit.app/](https://txt-md.streamlit.app/)

## Features

- Convert text to Markdown, Word, PDF, and RTF formats.
- Supports LaTeX-like equation formatting.
- Replace image placeholders in the text with uploaded images.
- Preview Markdown content in the app.
- Download generated files from the sidebar.

## How to Use

1. **Upload a text file** or **paste text** into the provided text area.
2. Optionally, upload images to replace any placeholders found in the text.
3. Click the **Convert** button to generate Markdown, Word, PDF, and RTF files.
4. Preview the Markdown content below.
5. Download the generated files using the buttons in the sidebar.

## Requirements

- `re`: Regular expression operations.
- `os`: Miscellaneous operating system interfaces.
- `pypandoc`: A Python wrapper for Pandoc, a universal document converter.
- `streamlit`: An open-source app framework for Machine Learning and Data Science projects.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/cconway1-stevens/chat-helper.git
   cd yourrepository
