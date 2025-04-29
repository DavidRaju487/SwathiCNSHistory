import PyPDF2
import os

def extract_pages(pdf_path, start_page, end_page, output_path):
    """
    Extract specific pages from a PDF file and save them to a new PDF.
    
    Args:
        pdf_path (str): Path to the input PDF file
        start_page (int): Starting page number (1-based index)
        end_page (int): Ending page number (1-based index)
        output_path (str): Path to save the extracted pages
    """
    try:
        # Open the PDF file
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Create a PDF writer object
            pdf_writer = PyPDF2.PdfWriter()
            
            # Adjust page numbers to 0-based index
            start_page = start_page - 1
            end_page = end_page - 1
            
            # Validate page numbers
            if start_page < 0 or end_page >= len(pdf_reader.pages):
                raise ValueError("Invalid page range")
            
            # Add the specified pages to the writer
            for page_num in range(start_page, end_page + 1):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)
            
            # Save the extracted pages to a new PDF
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            print(f"Successfully extracted pages {start_page + 1} to {end_page + 1} to {output_path}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Example usage
    pdf_path = "PediatricGastroRiyaz.pdf"
    start_page = 114  # Example: starting from page 150
    end_page = 121    # Example: ending at page 175
    output_path = "PediatricGastroRiyaz_extracted_pages.pdf"
    
    extract_pages(pdf_path, start_page, end_page, output_path)
