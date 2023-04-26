import os

from fpdf import FPDF

from constants import TEMP_FILE_FOLDER


def create_pdf_from_txt(policy_number):
    path_file = os.path.join(TEMP_FILE_FOLDER, "test.txt")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "", 20)
    with open(path_file, "r") as f:
        contents = f.read()
    pdf.multi_cell(0, 5, contents)
    pdf.output(os.path.join(TEMP_FILE_FOLDER, f"{policy_number}.pdf"))
