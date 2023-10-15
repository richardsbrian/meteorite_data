from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def make_pdf():
    # Create a PDF document
    doc = SimpleDocTemplate("All_Data.pdf", pagesize=letter)

    # Create a list to store elements
    elements = []

    # Add text
    styles = getSampleStyleSheet()
    title = Paragraph("All Data", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 0.2 * inch))

    # Images
    image_paths = [
        "png_files\\world_impacts.png",
        "png_files\\continent_counts.png",
        "png_files\\americas_impacts.png",
        "png_files\\top_20_meteorite_types_north_america.png",
    ]
    for path in image_paths:
        image = Image(path, width=6 * inch, height=4 * inch)
        elements.append(image)

    # Build the PDF
    doc.build(elements)


if __name__ == "__main__":
    make_pdf()
