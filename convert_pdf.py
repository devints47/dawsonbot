import PyPDF2
import pymupdf
import os
from glob import glob



def convert_pdf_to_png(pdf_paths):
    for i, pdf in enumerate(pdf_paths):
        print("--- Converting %s ---" % pdf)

        read_pdf = PyPDF2.PdfReader(f"original_pdfs/{pdf}")
        page0 = read_pdf.pages[0]
        page0.scale_by(2)  # float representing scale factor - this happens in-place
        writer = PyPDF2.PdfWriter()  # create a writer to save the updated results
        writer.add_page(page0)
        with open(f"temp_pdfs/temp_{pdf}", "wb+") as f:
            writer.write(f)

        doc = pymupdf.open(f"temp_pdfs/temp_{pdf}")
        page = doc.load_page(0)
        page.set_cropbox(pymupdf.Rect(100, 375, 1100, 850))  # set a cropbox for the page
        pixmap = page.get_pixmap(dpi=300)
        img = pixmap.tobytes()

        pixmap.save(f"fixed_pngs/img{i}.png")

        print("--- Finished converting %s ---" % pdf)
pdfs = []
for file in os.listdir("original_pdfs"):
    if file.endswith(".pdf"):
        pdfs.append(file)
print(pdfs)

convert_pdf_to_png(pdfs)
