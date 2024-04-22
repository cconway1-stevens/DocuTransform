import markdown2
from weasyprint import HTML

def convert_markdown_to_pdf(input_filename, output_filename):
    # Read the Markdown content from the file
    with open(input_filename, 'r', encoding='utf-8') as file:
        markdown_text = file.read()

    # Convert Markdown to HTML
    html_text = markdown2.markdown(markdown_text)

    # Convert HTML to PDF using WeasyPrint
    HTML(string=html_text).write_pdf(output_filename)

# Usage
convert_markdown_to_pdf('text.txt', 'project_report.pdf')
