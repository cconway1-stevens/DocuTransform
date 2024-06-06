import re
import os
import base64
import pypandoc
import streamlit as st
import tempfile
from pathlib import Path

def format_equations(text):
    """
    Process LaTeX-like syntax by wrapping equations with double dollar signs for LaTeX compatibility.
    """
    pattern = re.compile(r'\$\$(.*?)\$\$')
    return pattern.sub(lambda x: f'$$\\({x.group(1)}\\)$$', text)

def convert_to_md(input_text, output_dir, filename="text.txt"):
    """
    Apply Markdown formatting to the input text and write the output to a specified directory.
    """
    try:
        text = format_equations(input_text)
        text = text.replace('$$', '')  # Remove extra dollar signs
        markdown_content = text
        
        output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".md")
        with open(output_path, 'w') as f:
            f.write(markdown_content)

        return output_path
    except Exception as e:
        st.error(f"An error occurred: {e}")

def convert_to_word(input_md_file, output_dir):
    """
    Convert the given Markdown file to Word format using pypandoc.
    """
    try:
        word_file = os.path.splitext(os.path.basename(input_md_file))[0] + ".docx"
        pypandoc.convert_file(input_md_file, 'docx', outputfile=os.path.join(output_dir, word_file))
        return os.path.join(output_dir, word_file)
    except Exception as e:
        st.error(f"An error occurred during Word conversion: {e}")

def convert_to_pdf(input_md_file, output_dir):
    """
    Convert the given Markdown file to PDF using pypandoc.
    """
    try:
        pdf_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_md_file))[0] + ".pdf")
        pypandoc.convert_file(input_md_file, 'pdf', outputfile=pdf_file, extra_args=['--pdf-engine=pdflatex'])
        return pdf_file
    except Exception as e:
        st.error(f"An error occurred during PDF conversion: {e}")

def convert_to_rtf(input_md_file, output_dir):
    """
    Convert the given Markdown file to RTF format using pypandoc.
    """
    try:
        rtf_file = os.path.splitext(os.path.basename(input_md_file))[0] + ".rtf"
        pypandoc.convert_file(input_md_file, 'rtf', outputfile=os.path.join(output_dir, rtf_file))
        return os.path.join(output_dir, rtf_file)
    except Exception as e:
        st.error(f"An error occurred during RTF conversion: {e}")

def embed_images_in_md(input_text, images):
    """
    Embed images directly in the Markdown content as base64.
    """
    for image in images:
        with open(image, 'rb') as img_file:
            img_data = img_file.read()
            img_base64 = base64.b64encode(img_data).decode('utf-8')
            img_tag = f'![{os.path.basename(image)}](data:image/png;base64,{img_base64})'
            input_text = input_text.replace(f'![{os.path.basename(image)}]', img_tag)
    return input_text

def main():
    st.title("File Converter")

    st.sidebar.title("Directions")
    st.sidebar.write("""
        1. **Upload a text file** or **paste text** into the provided text area.
        2. Optionally, upload images to be included in the Markdown.
        3. Click the **Convert** button to generate Markdown, Word, PDF, and RTF files.
        4. Preview the Markdown content below.
        5. Download the generated files using the buttons in the sidebar.
    """)

    st.sidebar.title("Download Files")

    uploaded_file = st.file_uploader("Upload a text file", type="txt")
    input_text = st.text_area("Or, paste your text here")

    uploaded_images = st.file_uploader("Upload images for Markdown", type=["png", "jpg", "jpeg", "gif"], accept_multiple_files=True)

    if st.button("Convert"):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            
            if uploaded_file is not None:
                temp_file_path = temp_dir / uploaded_file.name
                with open(temp_file_path, 'wb') as temp_file:
                    temp_file.write(uploaded_file.getvalue())
                
                with open(temp_file_path, 'r') as f:
                    input_text = f.read()

                filename = uploaded_file.name
            elif input_text:
                filename = "pasted_text.txt"
            else:
                st.error("Please upload a file or paste text to convert.")
                return

            if uploaded_images:
                image_paths = []
                for image in uploaded_images:
                    image_path = temp_dir / image.name
                    with open(image_path, 'wb') as img_file:
                        img_file.write(image.getvalue())
                    image_paths.append(image_path)
                
                input_text = embed_images_in_md(input_text, image_paths)
            
            md_file = convert_to_md(input_text, temp_dir, filename=filename)
            if md_file:
                word_file = convert_to_word(md_file, temp_dir)
                pdf_file = convert_to_pdf(md_file, temp_dir)
                rtf_file = convert_to_rtf(md_file, temp_dir)

                with open(md_file, 'r') as f:
                    st.markdown("### Markdown Preview")
                    st.markdown(f.read(), unsafe_allow_html=True)
                
                st.sidebar.download_button("Download Markdown", data=open(md_file, 'rb'), file_name=os.path.basename(md_file))
                if word_file:
                    st.sidebar.download_button("Download Word", data=open(word_file, 'rb'), file_name=os.path.basename(word_file))
                if pdf_file:
                    st.sidebar.download_button("Download PDF", data=open(pdf_file, 'rb'), file_name=os.path.basename(pdf_file))
                if rtf_file:
                    st.sidebar.download_button("Download RTF", data=open(rtf_file, 'rb'), file_name=os.path.basename(rtf_file))

if __name__ == "__main__":
    main()
