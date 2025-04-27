from datetime import datetime
from pdf_generator import generate_pdf  # <- CHANGE THIS to the actual name of your module

# Generate a PDF using dummy data
pdf_bytes = generate_pdf(
    property_address="36 Carysfort Street, Mount Maunganui",
    yearly_rates=3801.05,
    local_council="Tauranga Council",
    regional_council="Bay of Plenty Regional Council",
    settlement_date=datetime(2025, 7, 31),
    purchase_price=1250000,
    gst_applicable=False,
    adjustments="None",
    local_vendor_days=31,
    local_vendor_amount=320.20,
    local_purchaser_days=61,
    local_purchaser_amount=630.07,
    regional_vendor_days=31,
    regional_vendor_amount=50.92,
    regional_purchaser_days=334,
    regional_purchaser_amount=548.67,
    deposit_amount=125000,
    matter_reference="REF: 987654-ZY"
)

# Save the PDF to a file
with open("settlement_statement_preview.pdf", "wb") as f:
    f.write(pdf_bytes)

print("✅ PDF preview generated: settlement_statement_preview.pdf")
