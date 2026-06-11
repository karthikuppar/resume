import io
import PyPDF2

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Takes raw file bytes from an uploaded PDF and returns the extracted text.
    """
    try:
        # Convert the raw bytes into a file-like object that PyPDF2 can read
        pdf_file_obj = io.BytesIO(file_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
        
        extracted_text = ""
        # Loop through every page and extract the text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            extracted_text += page.extract_text() + "\n"
            
        if not extracted_text.strip():
            raise ValueError("Could not extract any text. The PDF might be an image.")
            
        return extracted_text

    except Exception as e:
        # If anything goes wrong, we throw an error that the API can catch
        raise Exception(f"Failed to read PDF: {str(e)}")