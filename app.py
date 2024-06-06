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
    Find all image paths in the markdown text, stripping any directory structure.
    """
    pattern = re.compile(r'!\[.*?\]\((.*?)\)')
    paths = pattern.findall(text)
    return [Path(path).name for path in paths]

def convert_to_md(input_text, output_dir, filename="text.txt"):
    """
    Apply Markdown formatting to the input text and write the output to a specified directory.
    """
    try:
        text = format_equations(input_text)
        text = text.replace('$$', '')  # Remove extra dollar signs
        markdown_content = "" + text
        
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
        2. Click the **Convert** button to generate Markdown, Word, PDF, and RTF files.
        3. Preview the Markdown content below.
        4. Download the generated files using the buttons in the sidebar.
    """)

    st.sidebar.title("Download Files")

    uploaded_file = st.file_uploader("Upload a text file", type="txt")
    input_text = st.text_area("Or, paste your text here")

    image_paths = find_image_paths(input_text)
    image_files_needed = {}

    if image_paths:
        st.sidebar.markdown("### Image Paths Detected")
        st.sidebar.write("The following image paths were detected in your Markdown text. Please upload the corresponding images.")
        for image_path in image_paths:
            st.sidebar.write(f"- {image_path}")
            image_files_needed[image_path] = None

        uploaded_images = st.file_uploader("Upload images for Markdown", type=["png", "jpg", "jpeg", "gif"], accept_multiple_files=True)

        if uploaded_images:
            for image in uploaded_images:
                if image.name in image_files_needed:
                    image_files_needed[image.name] = image
    else:
        uploaded_images = None

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

            if image_files_needed:
                image_dir = temp_dir / "images"
                image_dir.mkdir()
                for image_name, image in image_files_needed.items():
                    if image is not None:
                        image_path = image_dir / image_name
                        with open(image_path, 'wb') as img_file:
                            img_file.write(image.getvalue())
                        # Update Markdown to use the new image path
                        input_text = input_text.replace(image_name, image_path.as_posix())
                    else:
                        st.error(f"Missing image file: {image_name}")
                        return
            
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

                # Provide links to open files in a new tab
                st.sidebar.markdown("### Open in New Tab")
                md_file_url = f"/files/{md_file.name}"
                word_file_url = f"/files/{word_file.name}" if word_file else None
                pdf_file_url = f"/files/{pdf_file.name}" if pdf_file else None
                rtf_file_url = f"/files/{rtf_file.name}" if rtf_file else None

                st.sidebar.markdown(f"[Open Markdown]({md_file_url})", unsafe_allow_html=True)
                if word_file_url:
                    st.sidebar.markdown(f"[Open Word]({word_file_url})", unsafe_allow_html=True)
                if pdf_file_url:
                    st.sidebar.markdown(f"[Open PDF]({pdf_file_url})", unsafe_allow_html=True)
                if rtf_file_url:
                    st.sidebar.markdown(f"[Open RTF]({rtf_file_url})", unsafe_allow_html=True)

                # Serve files using static files
                if md_file:
                    st.markdown(f"[Open Markdown](file://{md_file})", unsafe_allow_html=True)
                if word_file:
                    st.markdown(f"[Open Word](file://{word_file})", unsafe_allow_html=True)
                if pdf_file:
                    st.markdown(f"[Open PDF](file://{pdf_file})", unsafe_allow_html=True)
                if rtf_file:
                    st.markdown(f"[Open RTF](file://{rtf_file})", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
