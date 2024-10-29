def generate_invoice():
    with open('invoice_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    doc.build(elements)

    # Add reference automatically
    print("The invoice was successfully generated under the name 'invoice.pdf'.")

if __name__ == "__main__":
    generate_invoice()