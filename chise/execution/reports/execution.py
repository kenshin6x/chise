from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch

class ExecutionReport:
    object = None
    buffer = None
    c = None

    def __init__(self, object, *args, **kwargs):
        self.object = object

        self.buffer = BytesIO()
        self.c = canvas.Canvas(self.buffer)
        self.draw()

    def pdf(self):
        pdf = self.buffer.getvalue()
        self.buffer.close()

        return pdf
        
    def draw(self):
        self.c.drawString(100,750, "Welcanvasome to Reportlab!")
        
        self.c.showPage()
        self.c.save()