import streamlit as st
from calculations import calculate_apportionments
from pdf_generator import generate_pdf

st.set_page_config(page_title="NZ Property Settlement Tool", layout="centered")
st.title("🏡 NZ Property Settlement Statement Generator")

st.markdown("Enter the details below to generate a professional settlement statement PDF.")

# Sample councils list (can be expanded later)
local_councils = [
    "Auckland Council", "Far North District Council", "Wellington City Council", "Whangarei District Council", "Christchurch City Council",
    "Hamilton City Council", "Tauranga City Council", "Dunedin City Council"
]
regional_councils = [
    "Auckland Regional Council", "Wellington Regional Council", "Canterbury Regional Council",
    "Waikato Regional Council", "Bay of Plenty Regional Council", "Otago Regional Council"
]

with st.form("settlement_form"):
    property_address = st.text_input("Property Address")
    local_council = st.selectbox("Local Council", options=local_councils)
    regional_council = st.selectbox("Regional Council", options=regional_councils)
    
    # Separate inputs for local and regional council rates
    local_yearly_rates = st.number_input("Local Council Yearly Rates Amount (NZD)", min_value=0.0)
    regional_yearly_rates = st.number_input("Regional Council Yearly Rates Amount (NZD)", min_value=0.0)
    
    settlement_date = st.date_input("Settlement Date")
    purchase_price = st.number_input("Purchase Price (NZD)", min_value=0.0)
    gst_applicable = st.checkbox("Is GST Applicable?")
    adjustments = st.text_area("Any Adjustments (optional)", placeholder="e.g. Water charges, Rubbish collection")

    submitted = st.form_submit_button("Generate Statement")

if submitted:
    # Get local and regional apportionments
    apportionments = calculate_apportionments(local_council, local_yearly_rates, regional_council, regional_yearly_rates, settlement_date)
    
    # Extract local and regional apportionments
    local_vendor_days = apportionments["local"]["vendor_days"]
    local_vendor_amount = apportionments["local"]["vendor_amount"]
    local_purchaser_days = apportionments["local"]["purchaser_days"]
    local_purchaser_amount = apportionments["local"]["purchaser_amount"]
    regional_vendor_days = apportionments["regional"]["vendor_days"]
    regional_vendor_amount = apportionments["regional"]["vendor_amount"]
    regional_purchaser_days = apportionments["regional"]["purchaser_days"]
    regional_purchaser_amount = apportionments["regional"]["purchaser_amount"]

    # Generate the PDF with detailed results
    pdf_bytes = generate_pdf(
        property_address,
        local_yearly_rates,  # passing local rates
        local_council,
        regional_council,
        settlement_date,
        purchase_price,
        gst_applicable,
        adjustments,
        local_vendor_days, local_vendor_amount, local_purchaser_days, local_purchaser_amount,
        regional_vendor_days, regional_vendor_amount, regional_purchaser_days, regional_purchaser_amount
    )

    # Display results on the UI
    st.success("PDF generated successfully!")
    st.write(f"**Local Council Apportionment**")
    st.write(f"Vendor: NZD {local_vendor_amount:.2f} | Days: {local_vendor_days}")
    st.write(f"Purchaser: NZD {local_purchaser_amount:.2f} | Days: {local_purchaser_days}")
    
    st.write(f"**Regional Council Apportionment**")
    st.write(f"Vendor: NZD {regional_vendor_amount:.2f} | Days: {regional_vendor_days}")
    st.write(f"Purchaser: NZD {regional_purchaser_amount:.2f} | Days: {regional_purchaser_days}")
    
    # Download button for PDF
    st.download_button(
        label="📄 Download Settlement Statement",
        data=pdf_bytes,
        file_name="settlement_statement.pdf",
        mime="application/pdf"
    )

    # Share button (for simulating email)
    if st.button("📤 Share via Email"):
        st.info("Simulating email send... (In production, this would send an email)")
        st.success("Settlement statement shared successfully!")
