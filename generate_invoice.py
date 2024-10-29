import json
import datetime
from fpdf import FPDF

class InvoicePDF(FPDF):
    def header(self):
        self.set_font("Times", "B", 16)
        self.cell(0, 10, "INVOICE", 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-30)
        self.set_font("Times", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def add_info(self, data, invoice_ref, issue_date):
        # My Info
        self.set_font("Times", "", 10)
        self.cell(100, 10, f"{data['my_info']['name']}", 0, 0)
        self.set_x(120)
        self.cell(100, 10, f"{data['client_info']['name']}", 0, 1)

        self.cell(100, 5, f"{data['my_info']['address']}, {data['my_info']['city']}", 0, 0)
        self.set_x(120)
        self.cell(100, 5, f"{data['client_info']['address']}, {data['client_info']['city']}", 0, 1)

        self.cell(100, 5, f"Phone: {data['my_info']['phone']}", 0, 0)
        self.set_x(120)
        self.cell(100, 5, f"Phone: {data['client_info']['phone']}", 0, 1)

        self.cell(100, 5, f"SIRET: {data['my_info']['SIRET']}", 0, 0)
        self.set_x(120)
        self.cell(100, 5, f"SIRET: {data['client_info']['SIRET']}", 0, 1)

        self.cell(100, 5, f"Email: {data['my_info']['email']}", 0, 0)
        self.set_x(120)
        self.cell(100, 5, f"Email: {data['client_info']['email']}", 0, 1)

        self.cell(100, 5, f"VAT: {data['my_info']['VAT_number']}", 0, 0)
        self.set_x(120)
        self.cell(100, 5, f"VAT: {data['client_info']['VAT_number']}", 0, 1)

        # Invoice Details
        self.ln(10)
        self.cell(0, 10, f"Invoice Ref: {invoice_ref}", 0, 1)
        self.cell(0, 5, f"Issue Date: {issue_date}", 0, 1)
        self.cell(0, 5, "Payment Due Date: 30 days from receipt", 0, 1)
        self.ln(10)

    def add_table(self, prestations):
        # Table Header
        self.set_fill_color(200, 220, 255)
        self.cell(15, 10, "ID", 1, 0, "C", True)
        self.cell(60, 10, "Description", 1, 0, "C", True)
        self.cell(20, 10, "Unit", 1, 0, "C", True)
        self.cell(20, 10, "Quantity", 1, 0, "C", True)
        self.cell(20, 10, "Price", 1, 0, "C", True)
        self.cell(20, 10, "VAT %", 1, 0, "C", True)
        self.cell(20, 10, "Excl. VAT", 1, 0, "C", True)
        self.cell(20, 10, "Incl. VAT", 1, 1, "C", True)

        # Table Rows (Body)
        total_ht = total_ttc = total_tva = 0
        for prestation in prestations:
            amount_ht = prestation["quantity"] * prestation["price"]
            amount_vat = amount_ht * prestation["VAT_PCT"] / 100
            amount_ttc = amount_ht + amount_vat
            total_ht += amount_ht
            total_ttc += amount_ttc
            total_tva += amount_vat

            self.cell(15, 10, prestation["id"], 1, 0, "C")
            self.cell(60, 10, prestation["description"], 1, 0, "C")
            self.cell(20, 10, prestation["unit"], 1, 0, "C")
            self.cell(20, 10, str(prestation["quantity"]), 1, 0, "C")
            self.cell(20, 10, f"{prestation['price']:.2f}EUR", 1, 0, "C")
            self.cell(20, 10, f"{prestation['VAT_PCT']}%", 1, 0, "C")
            self.cell(20, 10, f"{amount_ht:.2f}EUR", 1, 0, "R")
            self.cell(20, 10, f"{amount_ttc:.2f}EUR", 1, 1, "R")

        # Align Payment Terms and Summary side by side
        self.ln(10)
        
        summary_x = 135 # X-position for Summary
        payment_x = 10 # X-position for Payment Terms
        top_y = self.get_y() # Starting Y position for both sections

        # Payment Terms
        self.set_xy(payment_x, top_y)
        self.cell(80, 8, "Payment terms: 30 days", 0, 1)
        self.set_x(payment_x)
        self.cell(80, 8, "Late fee: 3 times the legal rate", 0, 1)
        self.set_x(payment_x)
        self.cell(80, 8, "Fixed compensation for recovery costs: 40 EUR", 0, 1)
        self.set_x(payment_x)
        self.cell(80, 8, "Discount: None", 0, 1)

        # Summary
        self.set_xy(summary_x, top_y)
        self.cell(50, 10, "Total Excl. VAT", 1, 0)
        self.cell(20, 10, f"{total_ht:.2f}EUR", 1, 1, "R")
        self.set_x(summary_x)
        self.cell(50, 10, "Total VAT", 1, 0)
        self.cell(20, 10, f"{total_tva:.2f}EUR", 1, 1, "R")
        self.set_x(summary_x)
        self.cell(50, 10, "Total Incl. VAT", 1, 0)
        self.cell(20, 10, f"{total_ttc:.2f}EUR", 1, 1, "R")

def generate_invoice(days_worked, json_path="invoice_data.json"):
    # Load data from JSON
    with open(json_path, "r") as file:
        data = json.load(file)

    # Update prestations based on days worked
    for prestation in data["prestations"]:
        if prestation["description"] == "Fullstack Engineering":
            prestation["quantity"] = days_worked

    # Generate PDF
    pdf = InvoicePDF()
    pdf.add_page()

    # Set invoice details
    invoice_ref = f"INV-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    issue_date = datetime.datetime.now().strftime('%d/%m/%Y')

    # Add sections
    pdf.add_info(data, invoice_ref, issue_date)
    pdf.add_table(data["prestations"])

    # Save PDF
    pdf.output("freelance_invoice.pdf")
    print("Invoice generated: freelance_invoice.pdf")

generate_invoice(days_worked=5)
