#!/usr/bin/python
import glob
import fitz
import os

class CompressPdf:

	def __init__(self, path):
		self.path    = path
		self.picpath = path + "/pdfpic/"
		self.npdf    = path + "/newpdf.pdf"

		CompressPdf.operatefile(self, self.path)
		CompressPdf.operatefile(self, self.picpath)
		CompressPdf.operatefile(self, self.npdf, 2)

	def pdftopic(self, pdffile, rate=50):
		doc  = fitz.open(pdffile)
		width, height = fitz.PaperSize("a4")

		for pg in range(doc.pageCount):
			page   = doc[pg]
			zoom   = int(rate)
			rotate = int(0)
			trans  = fitz.Matrix(zoom / 100.0, zoom / 100.0).preRotate(rotate)
			pm     = page.getPixmap(matrix=trans, alpha=False)
			pic    = self.picpath + str(pg + 1) + ".jpg"
			pm.writePNG(pic)

		doc.close()

	def pictopdf(self):
		doc  = fitz.open()
		file = self.picpath + "*"

		for img in glob.glob(file):
			imgdoc   = fitz.open(img)
			pdfbytes = imgdoc.convertToPDF()
			imgpdf   = fitz.open("pdf", pdfbytes)
			doc.insertPDF(imgpdf)
			os.remove(img)

		doc.save(self.npdf)
		doc.close()
	
	def operatefile(self, file, otype=1):
		if not os.path.exists(file) and otype==1:
			os.makedirs(file)
		elif os.path.exists(file) and otype==2:
			os.remove(file)

c = CompressPdf("压缩后pdf的存放目录路径")
c.pdftopic("需要压缩的pdf路径", "压缩比率")
c.pictopdf()