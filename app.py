import streamlit as st
from calculations import calculate_apportionments
from pdf_generator import generate_pdf
from word_generator import generate_docx
from datetime import datetime

st.set_page_config(page_title="NZ Property Settlement Tool", layout="centered")
st.title("🏡 Settlement Rates Calculator")

st.markdown("Enter the details below to calculate the settlement rates for your property.")

# Sample councils list (can be expanded later)
local_councils = [
    "Tauranga City Council",
    "Auckland Council",
    "Christchurch City Council",
    "Dunedin City Council",
    "Far North District Council",
    "Hamilton City Council",
    "Kawerau District Council",
    "Opotiki District Council",
    "Taupo District Council",
    "Wellington City Council",
    "Western Bay of Plenty District Council",
    "Whakatane District Council",
    "Whangarei District Council"
]

regional_councils = [
    "Bay of Plenty Regional Council", "Canterbury Regional Council",
     "Otago Regional Council", "Waikato Regional Council"
]

with st.form("settlement_form"):
    #council info
    st.header("👋 Hi Ben, let's go!")
    
    settlement_date = st.date_input("Settlement Date", value=datetime.now().date())

    local_council = st.selectbox("Council", options=local_councils)
    local_yearly_rates = st.number_input("Yearly Rates", min_value=0.0)
    local_installment_paid = st.checkbox("Vendor will pay current instalment?")

    regional_council = st.selectbox("Regional Council", options=regional_councils)
    regional_yearly_rates = st.number_input("Regional Council Rates", min_value=0.0)
    regional_installment_paid = st.checkbox("Vendor will pay current instalment? ")

    # #client info
    # st.header("Client Information")
    # client_name = st.text_input("Client Name", value="Mike Ross")
    # client_address = st.text_input("Client Address", value="147 Pioneer Street, Bethlehem, Tauranga")
    # client_phone_number = st.text_input("Client Phone Number", value="021 123 4567")
    # client_email = st.text_input("Client Email", value="mike@ross.com")
    
    # #deal info
    # st.header("Transaction")
    # property_address = st.text_input("Property Address", value="130 Maunganui Road, Mount Maunganui")
    # purchase_price = st.number_input("Purchase Price", value=float(1500000))
    # deposit = st.number_input("Deposit", value=float(150000))
    

    #gst_applicable = st.checkbox("Is GST Applicable?")
    #adjustments = st.text_area("Any Adjustments (optional)", placeholder="e.g. Water charges, Rubbish collection")

    #submitted_word = st.form_submit_button("Generate Word")
    #submitted_pdf = st.form_submit_button("Generate PDF")
    submitted = st.form_submit_button("Go")

if submitted:

    # Get local and regional apportionments
    apportionments = calculate_apportionments(local_council, local_yearly_rates, regional_council, regional_yearly_rates, settlement_date, local_installment_paid, regional_installment_paid)
    
    # Extract local and regional apportionments
    local_vendor_days = apportionments["local"]["vendor_days"]
    local_vendor_amount = apportionments["local"]["vendor_amount"]
    local_purchaser_days = apportionments["local"]["purchaser_days"]
    local_purchaser_amount = apportionments["local"]["purchaser_amount"]
    local_installment_paid = apportionments["local"]["installment_paid"]
    regional_vendor_days = apportionments["regional"]["vendor_days"]
    regional_vendor_amount = apportionments["regional"]["vendor_amount"]
    regional_purchaser_days = apportionments["regional"]["purchaser_days"]
    regional_purchaser_amount = apportionments["regional"]["purchaser_amount"]
    regional_installment_paid = apportionments["regional"]["installment_paid"]


# if submitted_word:

#     # Get local and regional apportionments
#     apportionments = calculate_apportionments(local_council, local_yearly_rates, regional_council, regional_yearly_rates, settlement_date, local_installment_paid, regional_installment_paid)
    
#     # Extract local and regional apportionments
#     local_vendor_days = apportionments["local"]["vendor_days"]
#     local_vendor_amount = apportionments["local"]["vendor_amount"]
#     local_purchaser_days = apportionments["local"]["purchaser_days"]
#     local_purchaser_amount = apportionments["local"]["purchaser_amount"]
#     local_installment_paid = apportionments["local"]["installment_paid"]
#     regional_vendor_days = apportionments["regional"]["vendor_days"]
#     regional_vendor_amount = apportionments["regional"]["vendor_amount"]
#     regional_purchaser_days = apportionments["regional"]["purchaser_days"]
#     regional_purchaser_amount = apportionments["regional"]["purchaser_amount"]
#     regional_installment_paid = apportionments["regional"]["installment_paid"]

#     document_data = {
#     "property_address": property_address,
#     "purchase_price": purchase_price,
#     "client_name": client_name,
#     "client_address": client_address,
#     "client_phone_number": client_phone_number,
#     "client_email": client_email,
#     "local_yearly_rates": local_yearly_rates,
#     "regional_yearly_rates": regional_yearly_rates,
#     "local_council": local_council,
#     "regional_council": regional_council,
#     "settlement_date": settlement_date,
#     "deposit": deposit,
#     "local_installment_paid": local_installment_paid,
#     "regional_installment_paid": regional_installment_paid,
#     "local_vendor_days": local_vendor_days,
#     "local_vendor_amount": local_vendor_amount,
#     "local_purchaser_days": local_purchaser_days,
#     "local_purchaser_amount": local_purchaser_amount,
#     "regional_vendor_days": regional_vendor_days,
#     "regional_vendor_amount": regional_vendor_amount,
#     "regional_purchaser_days": regional_purchaser_days,
#     "regional_purchaser_amount": regional_purchaser_amount,
#     "logo_path": "assets1/logo.png"
# }
#     docx_bytes = generate_docx(document_data)

#     st.success("Word document generated successfully!")

#     st.download_button(
#         label="📝 Download Word Document",
#         data=docx_bytes,
#         file_name="settlement_statement.docx",
#         mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#     )

# if submitted_pdf:

#     # Get local and regional apportionments
#     apportionments = calculate_apportionments(local_council, local_yearly_rates, regional_council, regional_yearly_rates, settlement_date, local_installment_paid, regional_installment_paid)
    
#     # Extract local and regional apportionments
#     local_vendor_days = apportionments["local"]["vendor_days"]
#     local_vendor_amount = apportionments["local"]["vendor_amount"]
#     local_purchaser_days = apportionments["local"]["purchaser_days"]
#     local_purchaser_amount = apportionments["local"]["purchaser_amount"]
#     local_installment_paid = apportionments["local"]["installment_paid"]
#     regional_vendor_days = apportionments["regional"]["vendor_days"]
#     regional_vendor_amount = apportionments["regional"]["vendor_amount"]
#     regional_purchaser_days = apportionments["regional"]["purchaser_days"]
#     regional_purchaser_amount = apportionments["regional"]["purchaser_amount"]
#     regional_installment_paid = apportionments["regional"]["installment_paid"]

#     # Generate the PDF with detailed results
#     pdf_bytes = generate_pdf(
#     property_address, 
#     purchase_price, 
#     client_name, 
#     client_address,
#     local_yearly_rates,
#     regional_yearly_rates,
#     local_council,
#     regional_council,
#     local_purchaser_days,
#     regional_purchaser_days,
#     local_purchaser_amount,
#     regional_purchaser_amount,
#     local_vendor_days,
#     regional_vendor_days,
#     local_vendor_amount,
#     regional_vendor_amount,
#     settlement_date,
#     deposit,
#     local_installment_paid,
#     regional_installment_paid
#     )

#    st.success("PDF generated successfully!")

    # Display results on the UI
    
    st.write(f"**Local Council Apportionment**")
    st.write(f"Vendor: NZD {local_vendor_amount:.2f} | Days: {local_vendor_days}")
    st.write(f"Purchaser: NZD {local_purchaser_amount:.2f} | Days: {local_purchaser_days}")
    st.write(f"Installment Paid? {local_installment_paid}")
    
    st.write(f"**Regional Council Apportionment**")
    st.write(f"Vendor: NZD {regional_vendor_amount:.2f} | Days: {regional_vendor_days}")
    st.write(f"Purchaser: NZD {regional_purchaser_amount:.2f} | Days: {regional_purchaser_days}")
    st.write(f"Installment Paid? {regional_installment_paid}")
    
    
    # # Download button for PDF
    # st.download_button(
    #     label="📄 Download PDF",
    #     data=pdf_bytes,
    #     file_name="settlement_statement.pdf",
    #     mime="application/pdf"
    # )

    # if submitted_word:
    #     st.write("Generating Word document...")
    #     # Common: collect form inputs into a structured dict
    #     document_data = {
    #         "property_address": property_address,
    #         "purchase_price": purchase_price,
    #         "client_name": client_name,
    #         "client_address": client_address,
    #         "local_yearly_rates": local_yearly_rates,
    #         "regional_yearly_rates": regional_yearly_rates,
    #         "local_council": local_council,
    #         "regional_council": regional_council,
    #         "settlement_date": settlement_date,
    #         "deposit": deposit,
    #         "local_installment_paid": local_installment_paid,
    #         "regional_installment_paid": regional_installment_paid,
    #     }

    #     docx_bytes = generate_docx(document_data)

    #     st.success("Word document generated successfully!")
    #     st.download_button(
    #         label="📝 Download Word Document",
    #         data=docx_bytes,
    #         file_name="settlement_statement.docx",
    #         mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    #     )

    #     # Share button (for simulating email)
    #     if st.button("📤 Share via Email"):
    #         st.info("Simulating email send... (In production, this would send an email)")
    #         st.success("Settlement statement shared successfully!")
