import os

from PyPDF2 import PdfFileReader, PdfFileWriter, PdfWriter, PdfReader 
from typing import List

class PDFMaster:
    def __init__(self, directory_path):
        self.directory_path = directory_path

    def _is_valid_dir(self ,path):
        return os.path.isdir(path)

    # Traverse a directory and its sub-directories to find all PDF files.    
    def find_pdf_files(self) -> List[str]:

        pdf_files = []
        for dirpath, dirnames, filenames in os.walk(self.directory_path):
            for file in filenames:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(dirpath, file))
                    
        return pdf_files

    def merge_pdfs(self, output_filename: str):

        input_filename_paths = self.find_pdf_files()

        if (len(input_filename_paths) != 0) & (self._is_valid_dir(self.directory_path)):
          
            # Initializing a PDF writer object
            pdf_writer = PdfWriter()

            for filename in input_filename_paths:

                # Open the input PDF file
                with open(filename, 'rb') as f:

                    # Create a new PDF reader object
                    pdf_reader = PdfReader(f)

                    # Loop through each page in the input PDF file
                    for page_num in range(len(pdf_reader.pages)):

                        # Get the current page
                        page = pdf_reader.pages[page_num]

                        # Ensure that the content of each file begins on a new page
                        if page_num != 0:
                            page.merge_page(pdf_writer.add_blank_page())

                        # Add the page to the PDF writer object
                        pdf_writer.add_page(page)

            with open(output_filename, 'wb') as f:

                # Write the PDF data to the output file
                pdf_writer.write(f)

        elif not self._is_valid_dir(self.directory_path):
            print('Fix your path')
        else:
            print(f'No PDFs present in path: {self.directory_path}')

if __name__ == '__main__':

    directory_path = os.getcwd()
    output_filename = 'output.pdf'
    
    tool = PDFMaster(directory_path)

    # Merge the PDF files
    tool.merge_pdfs(output_filename = output_filename)
