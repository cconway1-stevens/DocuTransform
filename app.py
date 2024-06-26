import re
import os
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

def find_image_paths(text):
    """
    Find all image paths in the text using Markdown syntax.
    """
    pattern = re.compile(r'!\[.*?\]\((.*?)\)')
    return pattern.findall(text)

def replace_image_paths(text, image_replacements):
    """
    Replace image paths in the text with the provided replacements.
    """
    pattern = re.compile(r'!\[.*?\]\((.*?)\)')
    for image_path, new_path in image_replacements.items():
        text = text.replace(image_path, new_path)
    return text

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

def main():
    st.title("File Converter")

    st.sidebar.title("Directions")
    st.sidebar.write("""
        1. **Upload a text file** or **paste text** into the provided text area.
        2. Optionally, upload images to replace any placeholders found in the text.
        3. Click the **Convert** button to generate Markdown, Word, PDF, and RTF files.
        4. Preview the Markdown content below.
        5. Download the generated files using the buttons in the sidebar.
    """)

    st.sidebar.title("Download Files")

    if 'input_text' not in st.session_state:
        st.session_state.input_text = ""
    if 'uploaded_images' not in st.session_state:
        st.session_state.uploaded_images = {}
    if 'filename' not in st.session_state:
        st.session_state.filename = "pasted_text.txt"

    uploaded_file = st.file_uploader("Upload a text file", type="txt")
    input_text = st.text_area("Or, paste your text here", value=st.session_state.input_text)

    if input_text != st.session_state.input_text:
        st.session_state.input_text = input_text

    if uploaded_file is not None:
        temp_file_path = f"temp_{uploaded_file.name}"
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(uploaded_file.getvalue())
        
        with open(temp_file_path, 'r') as f:
            st.session_state.input_text = f.read()
        st.session_state.filename = uploaded_file.name

    # Find and count image paths
    image_paths = find_image_paths(st.session_state.input_text)
    st.info(f"Found {len(image_paths)} image paths.")

    for i, image_path in enumerate(image_paths):
        st.markdown(f"Placeholder for image {i+1}: {image_path}")
        if image_path not in st.session_state.uploaded_images:
            uploaded_image = st.file_uploader(f"Upload image to replace {image_path}", type=["png", "jpg", "jpeg", "gif"], key=f"image_{i}")
            if uploaded_image:
                image_file_path = f"temp_image_{uploaded_image.name}"
                with open(image_file_path, 'wb') as img_file:
                    img_file.write(uploaded_image.getvalue())
                st.session_state.uploaded_images[image_path] = image_file_path

    if st.button("Convert"):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            input_text = replace_image_paths(st.session_state.input_text, st.session_state.uploaded_images)

            md_file = convert_to_md(input_text, temp_dir, filename=st.session_state.filename)
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
