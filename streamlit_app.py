import streamlit as st
import PyPDF2
import os
from tempfile import NamedTemporaryFile

# Set page config
st.set_page_config(
    page_title="PDF Page Extractor",
    page_icon="📄",
    layout="centered"
)

st.title("📄 PDF Page Extractor")
st.markdown("""
This application allows you to extract specific pages from a PDF file.
You can either select a range of pages or specify individual page numbers.
""")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Get the number of pages in the PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    total_pages = len(pdf_reader.pages)
    
    st.write(f"Total pages in the PDF: {total_pages}")
    
    # Create tabs for different extraction methods
    tab1, tab2 = st.tabs(["Page Range", "Specific Pages"])
    
    with tab1:
        st.subheader("Extract by Page Range")
        # Create two columns for page range input
        col1, col2 = st.columns(2)
        
        with col1:
            start_page = st.number_input(
                "Start Page",
                min_value=1,
                max_value=total_pages,
                value=1,
                help="Enter the starting page number",
                key="start_page"
            )
            start_page = start_page + 3 if start_page > 1500 else start_page + 25
        
        with col2:
            end_page = st.number_input(
                "End Page",
                min_value=1,
                max_value=total_pages,
                value=total_pages,
                help="Enter the ending page number",
                key="end_page"
            )
            end_page = end_page + 3 if end_page > 1500 else end_page + 25
        
        st.write(start_page, end_page)
        # Validate page range
        if start_page > end_page:
            st.error("Start page cannot be greater than end page!")
        else:
            if st.button("Extract Page Range"):
                try:
                    # Create a temporary file for the output
                    with NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        # Reset the file pointer to the beginning
                        uploaded_file.seek(0)
                        
                        # Create PDF reader and writer objects
                        pdf_reader = PyPDF2.PdfReader(uploaded_file)
                        pdf_writer = PyPDF2.PdfWriter()
                        
                        # Calculate actual page numbers to extract
                        actual_start = start_page - 25 if start_page <= 1500 + 25 else start_page - 3
                        actual_end = end_page - 25 if end_page <= 1500 + 25 else end_page - 3
                        
                        # Validate actual page numbers
                        if actual_start < 0 or actual_end >= len(pdf_reader.pages):
                            st.error("Invalid page range! Please check the page numbers.")
                        else:
                            # Add the specified pages to the writer
                            for page_num in range(actual_start, actual_end + 1):
                                page = pdf_reader.pages[page_num]
                                pdf_writer.add_page(page)
                        
                        # Write to the temporary file
                        pdf_writer.write(tmp_file)
                        tmp_file_path = tmp_file.name
                    
                    # Create a download button
                    with open(tmp_file_path, "rb") as file:
                        st.download_button(
                            label="Download Extracted PDF",
                            data=file,
                            file_name=f"extracted_pages_{start_page}_to_{end_page}.pdf",
                            mime="application/pdf"
                        )
                        
                    # Clean up the temporary file
                    os.unlink(tmp_file_path)
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    
    with tab2:
        st.subheader("Extract Specific Pages")
        st.info("Enter page numbers separated by commas (e.g., 1,3,5-7,9)")
        
        # Input for specific pages
        page_input = st.text_input(
            "Enter Page Numbers",
            help="Example: 1,3,5-7,9 will extract pages 1, 3, 5, 6, 7, and 9"
        )
        
        if st.button("Extract Specific Pages"):
            try:
                # Parse the page numbers
                page_numbers = set()
                for part in page_input.split(','):
                    part = part.strip()
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        if start > 1500:
                            page_numbers.update(range(start + 3, end + 4))  # Add 3 to both start and end
                        else:
                            page_numbers.update(range(start + 25, end + 26))  # Add 25 to both start and end
                    else:
                        page_num = int(part)
                        if page_num > 1500:
                            page_numbers.add(page_num + 3)  # Add 3 to page number
                        else:
                            page_numbers.add(page_num + 25)  # Add 25 to page number
                
                # Calculate actual page numbers to extract
                actual_page_numbers = set()
                for page in page_numbers:
                    actual_page = page - 25 if page <= 1500 + 25 else page - 3
                    if 0 <= actual_page < len(pdf_reader.pages):
                        actual_page_numbers.add(actual_page)
                    else:
                        st.error(f"Invalid page number: {page}")
                
                if not actual_page_numbers:
                    st.error("No valid pages to extract!")
                else:
                    # Create a temporary file for the output
                    with NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        # Reset the file pointer to the beginning
                        uploaded_file.seek(0)
                        
                        # Create PDF reader and writer objects
                        pdf_reader = PyPDF2.PdfReader(uploaded_file)
                        pdf_writer = PyPDF2.PdfWriter()
                        
                        # Add the specified pages to the writer
                        for page_num in sorted(actual_page_numbers):
                            page = pdf_reader.pages[page_num]
                            pdf_writer.add_page(page)
                        
                        # Write to the temporary file
                        pdf_writer.write(tmp_file)
                        tmp_file_path = tmp_file.name
                    
                    # Create a download button
                    with open(tmp_file_path, "rb") as file:
                        st.download_button(
                            label="Download Extracted PDF",
                            data=file,
                            file_name=f"extracted_specific_pages.pdf",
                            mime="application/pdf"
                        )
                        
                    # Clean up the temporary file
                    os.unlink(tmp_file_path)
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
else:
    st.info("Please upload a PDF file to begin.")
