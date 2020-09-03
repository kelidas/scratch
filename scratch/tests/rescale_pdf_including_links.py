from PyPDF3 import PdfFileReader, PdfFileWriter
from PyPDF3.pdf import PageObject
from PyPDF3.generic import RectangleObject, NameObject
import decimal
 
pdf_input = PdfFileReader(open("original.pdf","rb"))
output = PdfFileWriter()

y_scale = decimal.Decimal(0.5)
x_offset = 0
y_offset = 0
 
for i in range(pdf_input.getNumPages()):
    input_page = pdf_input.getPage(i)
    output_page = PageObject.createBlankPage(None,
                                             input_page.mediaBox.getWidth(),
                                             input_page.mediaBox.getHeight())
    output_page.mergeTransformedPage(input_page, (1, 0, 0, y_scale, x_offset, y_offset))
    annots = output_page["/Annots"]
    
    for annot in annots:
        annot = annot.getObject()
        rect = RectangleObject(annot['/Rect'])
        rect_x0 = rect.getUpperLeft_x()
        rect_y0 = rect.getUpperLeft_y()
        rect_x1 = rect.getLowerRight_x()
        rect_y1 = rect.getLowerRight_y()
        annot.update({
            #NameObject('/Open'): BooleanObject(False),
            NameObject('/Rect'): RectangleObject([rect_x0, rect_y0 * y_scale, rect_x1, rect_y1 * y_scale])
        })
    
    output.addPage(output_page)
 
outputStream = open("output.pdf", "wb")
output.write(outputStream)
