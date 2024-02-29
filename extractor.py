import easyocr
import fitz  # PyMuPDF for handling PDFs
import sys, os


def pdf2txt(pdf_name: str, reader: easyocr.Reader):
  dir_name, txt = pdf_name[:pdf_name.find('.')], ""
  print(f"{pdf_name}: ")

  # pdf -> png
  print("  generating imgs...")
  os.makedirs(dir_name)
  for i, page in enumerate(fitz.open(pdf_name)):
    pix = page.get_pixmap(matrix=fitz.Matrix(2,2))  # mat for hi-res
    pix.save(f"{dir_name}/page_{i+1:03}.png")

  # sort img names
  imgs = [f"{dir_name}/{img}" for img in os.listdir(dir_name)]
  imgs.sort()

  # png -> txt
  print("  running ocr...")
  num_img = len(imgs)
  for i, img in enumerate(imgs):
    print(f"    pp {i+1: 3}/{num_img}")
    for item in reader.readtext(img, paragraph=True):
      if len(item[1]) > 40: # filter out trivial paragraphs
        txt += item[1] + '\n\n'

  print("  writing to txt...")
  with open(f"{dir_name}.txt", 'w+') as f:
    f.write(txt)

  # remove pngs
  print("  removing imgs...")
  for img in imgs:
    os.remove(img)
  os.rmdir(dir_name)
  print("\n\n")

reader = easyocr.Reader(['en'])
pdfs = [file for file in os.listdir('.') if file.endswith('.pdf')]

for pdf in pdfs:
  pdf2txt(pdf, reader)

