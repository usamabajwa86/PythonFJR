import streamlit as st
import pdf2docx
from io import BytesIO
import tempfile
from pdf2docx import Converter

def convert_pdf_to_word(pdf_file_path, docx_file_path):
    # Create a PDF converter
    cv = Converter(pdf_file_path)

    # Convert PDF to Word
    cv.convert(docx_file_path, start=0, end=None)

    # Close the converter
    cv.close()

# Set page title
st.set_page_config(page_title="PDF to Word Converter")

st.markdown("""
# PDF to Word Converter

This application is a simple tool that allows you to convert your PDF files into Word documents.
Just upload your PDF file and download the converted Word file.

Created by Salahudin Bajwa
""")

# Define function to convert PDF to Word
def convert_pdf_to_word(file_stream):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        # Write contents of the uploaded file into the temporary file
        temp_pdf.write(file_stream.read())
        temp_pdf_path = temp_pdf.name

    # Convert the PDF file to a Word document
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_docx:
        temp_docx_path = temp_docx.name

    try:
        pdf2docx.parse(temp_pdf_path, temp_docx_path)
        with open(temp_docx_path, 'rb') as docx_file:
            docx_file_content = docx_file.read()
    except Exception as e:
        return None, str(e)
    
    docx_file = BytesIO(docx_file_content)
    return docx_file, None

# Define main function
import PyPDF2

def main():
    # Add file uploader to sidebar
    uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type="pdf")

    # Check if file has been uploaded
    if uploaded_file is not None:
        # Convert PDF to Word
        docx_file, error = convert_pdf_to_word(uploaded_file)

        if error:
            st.write("Error: ", error)  # Show error
        elif docx_file:
            docx_file.seek(0)  # Make sure we're at the start of the file stream
            # Add download link to sidebar
            st.sidebar.download_button("Download Word file", data=docx_file.getvalue(), file_name="output_file.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

            # Display file info in main window
            st.write("File name:", uploaded_file.name)
            st.write("File size:", uploaded_file.size, "bytes")
            # Get number of pages in PDF file
            num_pages = len(PyPDF2.PdfReader(uploaded_file).pages)
            st.write("Number of pages:", num_pages)

# Run main function
if __name__ == "__main__":
    main()
