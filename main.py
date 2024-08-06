from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_invoice(invoice_data, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Invoice Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(30, height - 50, "Invoice")

    # Invoice Details
    c.setFont("Helvetica", 12)
    c.drawString(30, height - 100, f"Invoice Number: {invoice_data['invoice_number']}")
    c.drawString(30, height - 120, f"Date: {invoice_data['date']}")
    c.drawString(30, height - 140, f"Customer Name: {invoice_data['customer_name']}")
    c.drawString(30, height - 160, f"Customer Address: {invoice_data['customer_address']}")

    # Table Headers
    c.drawString(30, height - 200, "Description")
    c.drawString(300, height - 200, "Quantity")
    c.drawString(400, height - 200, "Unit Price")
    c.drawString(500, height - 200, "Total")

    y = height - 220
    for item in invoice_data['items']:
        c.drawString(30, y, item['description'])
        c.drawString(300, y, str(item['quantity']))
        c.drawString(400, y, f"${item['unit_price']:.2f}")
        c.drawString(500, y, f"${item['total']:.2f}")
        y -= 20

    # Calculate and draw total amount
    total_amount = sum(item['total'] for item in invoice_data['items'])
    c.drawString(400, y - 20, "Total Amount:")
    c.drawString(500, y - 20, f"${total_amount:.2f}")

    c.save()

def get_invoice_data():
    invoice_data = {}
    invoice_data['invoice_number'] = input("Enter Invoice Number: ")
    invoice_data['date'] = input("Enter Date: ")
    invoice_data['customer_name'] = input("Enter Customer Name: ")
    invoice_data['customer_address'] = input("Enter Customer Address: ")

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

def main():
    invoice_data = get_invoice_data()
    filename = input("Enter the filename for the invoice PDF (e.g., invoice.pdf): ")
    generate_invoice(invoice_data, filename)
    print(f"Invoice {filename} has been generated.")

if __name__ == "__main__":
    main()
