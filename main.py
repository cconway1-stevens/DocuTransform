import re
import os
import pypandoc

def format_equations(text):
    """
    Process LaTeX-like syntax by wrapping equations with double dollar signs for LaTeX compatibility.
    """
    pattern = re.compile(r'\$\$(.*?)\$\$')
    return pattern.sub(lambda x: f'$$\\({x.group(1)}\\)$$', text)

def convert_to_md(input_file, output_dir="outputs"):
    """
    Read from an input file, apply Markdown formatting, and write the output to a specified directory.
    """
    try:
        with open(input_file, 'r') as f:
            text = f.read()

        text = format_equations(text)
        text = text.replace('$$', '')  # Remove extra dollar signs
        markdown_content = "" + text
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        else:
            # Clear all contents of the directory if it already exists
            for file in os.listdir(output_dir):
                file_path = os.path.join(output_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        
        output_path = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + ".md")
        with open(output_path, 'w') as f:
            f.write(markdown_content)

        print(f"Conversion to Markdown successful! Output saved to {output_path}")
        return output_path
    except FileNotFoundError:
        print(f"Error: The file {input_file} does not exist.")
    except PermissionError:
        print(f"Error: Permission denied to access the file {input_file}.")
    except Exception as e:
        print(f"An error occurred: {e}")

def convert_to_word(input_md_file, output_dir="outputs"):
    """
    Convert the given Markdown file to Word format using pypandoc.
    """
    try:
        word_file = os.path.splitext(os.path.basename(input_md_file))[0] + ".docx"
        pypandoc.convert_file(input_md_file, 'docx', outputfile=os.path.join(output_dir, word_file))
        print(f"Conversion to Word successful! Output saved to {word_file}")
    except Exception as e:
        print(f"An error occurred during Word conversion: {e}")

def convert_to_pdf(input_md_file):
    """
    Convert the given Markdown file to PDF using pypandoc.
    """
    try:
        pdf_file = input_md_file.replace('.md', '.pdf')
        pypandoc.convert_file(input_md_file, 'pdf', outputfile=pdf_file, extra_args=['--pdf-engine=xelatex'])
        print(f"Conversion to PDF successful! Output saved to {pdf_file}")
    except Exception as e:
        print(f"An error occurred during PDF conversion: {e}")

def convert_to_rtf(input_md_file, output_dir="outputs"):
    """
    Convert the given Markdown file to RTF format using pypandoc.
    """
    try:
        rtf_file = os.path.splitext(os.path.basename(input_md_file))[0] + ".rtf"
        pypandoc.convert_file(input_md_file, 'rtf', outputfile=os.path.join(output_dir, rtf_file))
        print(f"Conversion to RTF successful! Output saved to {rtf_file}")
    except Exception as e:
        print(f"An error occurred during RTF conversion: {e}")

def main():
    input_file = "text.txt"  # Assuming input file is always "text.txt"
    output_dir = "outputs"

    md_file = convert_to_md(input_file, output_dir)
    if md_file:
        convert_to_word(md_file, output_dir)
        convert_to_pdf(md_file)
        convert_to_rtf(md_file, output_dir)

if __name__ == "__main__":
    main()
