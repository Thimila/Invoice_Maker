from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import locale

# Set locale for proper comma placement
locale.setlocale(locale.LC_ALL, '')

def format_currency(value):
    """Format the value to two decimal places with comma separators."""
    return locale.format_string("%.2f", value, grouping=True)

def generate_invoice(invoice_data, filename, logo_path=None):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Draw the logo if provided
    if logo_path:
        logo_width, logo_height = 1.5 * inch, 1.5 * inch
        c.drawImage(logo_path, width - logo_width - 30, height - logo_height - 30, width=logo_width, height=logo_height, mask='auto')

    # Invoice Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(30, height - 50, "INVOICE")

    # Company Details
    c.setFont("Helvetica", 12)
    c.drawString(30, height - 100, "ATC Sports")
    c.drawString(30, height - 120, "Kahagolla, Diyathalawa")
    c.drawString(30, height - 140, "072 8839233 / 072 7969510")

    # Invoice Details
    c.drawString(400, height - 100, f"Date: {invoice_data['date']}")
    c.drawString(400, height - 120, f"Invoice No: {invoice_data['invoice_number']}")

    # Customer Details
    c.drawString(30, height - 180, "Invoice To:")
    c.drawString(30, height - 200, invoice_data['customer_name'])

    # Table Data
    data = [["DESCRIPTION", "QTY", "UNIT PRICE", "TOTAL"]]
    for item in invoice_data['items']:
        formatted_unit_price = format_currency(item['unit_price'])
        formatted_total = format_currency(item['total'])
        data.append([item['description'], str(item['quantity']), formatted_unit_price, formatted_total])

    total_amount = sum(item['total'] for item in invoice_data['items'])
    data.append(["", "", "TOTAL", format_currency(total_amount)])

    # Create Table
    table = Table(data, colWidths=[250, 50, 100, 100])
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)

    # Draw the Table
    table.wrapOn(c, width, height)
    table.drawOn(c, 30, height - 350)

    # Save the PDF
    c.save()

def get_invoice_data():
    invoice_data = {}
    invoice_data['invoice_number'] = input("Enter Invoice Number: ")
    invoice_data['date'] = input("Enter Date: ")
    invoice_data['customer_name'] = input("Enter Customer Name: ")

    items = []
    while True:
        description = input("Enter item description (or 'done' to finish): ")
        if description.lower() == 'done':
            break
        quantity = int(input("Enter quantity: "))
        unit_price = float(input("Enter unit price: "))
        total = quantity * unit_price
        items.append({"description": description, "quantity": quantity, "unit_price": unit_price, "total": total})

    invoice_data['items'] = items
    return invoice_data

def choose_logo():
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = askopenfilename(title="Select Logo Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    root.destroy()  # Destroy the root window after file selection
    return file_path

def main():
    invoice_data = get_invoice_data()
    filename = input("Enter the filename for the invoice PDF (e.g., invoice.pdf): ")

    add_logo = input("Would you like to add a logo? (yes/no): ").lower()
    logo_path = None
    if add_logo == 'yes':
        logo_path = choose_logo()

    generate_invoice(invoice_data, filename, logo_path)
    print(f"Invoice {filename} has been generated.")

if __name__ == "__main__":
    main()
