from chise import settings
from django.utils.translation import ugettext_lazy as _
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.units import inch, mm

class ExecutionReport:
    object = None
    buffer = None
    r = None

    def __init__(self, object, *args, **kwargs):
        self.object = object

        self.buffer = BytesIO()
        self.r = SimpleDocTemplate(self.buffer, 
                                pagesize=landscape(A4), 
                                rightMargin=30,
                                leftMargin=30, 
                                topMargin=30,
                                bottomMargin=30)
        self.draw()

    def pdf(self):
        pdf = self.buffer.getvalue()
        self.buffer.close()

        return pdf
        
    def draw(self):
        elements = []

        # checkpoints
        data = [(
            _('Status'),
            _('Reference'),
            _('Object'),
            _('Name'),
            _('Description'),
            _('Date Checkpoint')
        ),]

        for object in self.object.checkpoints.all():
            data.append((
                object.get_status_display(),
                object.get_reference_display(),
                object.get_object_display(),
                object.name,
                object.description,
                object.date_checkpoint,
            ))
 
        table = Table(data, colWidths=45*mm)
        table.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray)
        ]))
    

        elements.append(table)

        self.r.build(elements)