import streamlit as st
from calculations import calculate_apportionments # Assuming this exists and works as before
from datetime import datetime
import pandas as pd # Import pandas for DataFrame

st.set_page_config(page_title="NZ Property Settlement Tool", layout="centered")
st.title("🏡 Settlement Rates Calculator")

st.markdown("Use this tool to calculate the rates adjustments for a property settlement.")

# Sample councils list (can be expanded later)
local_councils = [
    "Tauranga City Council",
    "Kawerau District Council",
    "Opotiki District Council",
    "Taupo District Council",
    "Western Bay of Plenty District Council",
    "Whakatane District Council",
]

regional_councils = [
    "Bay of Plenty Regional Council"
]

# --- Input Form (Keep As Is) ---
with st.form("settlement_form"):
    st.header("👋 Hi Simon, let's go!")

    # Use current date as default
    today = datetime.now().date()
    settlement_date = st.date_input("Settlement Date", value=today)

    local_council = st.selectbox("Local Council", local_councils)
    local_yearly_rates = st.number_input("Yearly Rates", min_value=0.0, format="%.2f")
    local_installment_paid_by_vendor = st.checkbox("Vendor pays current instalment?", key="local_paid") # Clarified label

    regional_council = st.selectbox("Regional Council", options=regional_councils)
    regional_yearly_rates = st.number_input("Regional Council Rates", min_value=0.0, format="%.2f")
    regional_installment_paid_by_vendor = st.checkbox("Vendor pays current instalment?", key="regional_paid") # Clarified label

    submitted = st.form_submit_button("🚀  Go!") # Changed button label

# --- Output Section (Revised for Two Tables, Index Hidden) ---
if submitted:
    st.subheader("📈 Settlement Adjustments")

    # Get apportionments (same as before)
    # NOTE: Ensure the calculation logic correctly handles the installment_paid flag
    # to determine the final credit/debit between parties.
    try:
        apportionments = calculate_apportionments(
            local_council,
            local_yearly_rates,
            regional_council,
            regional_yearly_rates,
            settlement_date,
            local_installment_paid_by_vendor,
            regional_installment_paid_by_vendor
        )
    except Exception as e:
        st.error(f"An error occurred during calculation: {e}")
        # Stop execution for this block if calculation fails
        st.stop()


    # --- Local Council Table ---
    st.markdown(f"**{local_council}:**") # Header for local table
    local_data_for_table = [
        {
            "Party": "Vendor",
            "Days": apportionments["local"]["vendor_days"],
            "Amount (NZD)": apportionments["local"]["vendor_amount"]
        },
        {
            "Party": "Purchaser",
            "Days": apportionments["local"]["purchaser_days"],
            "Amount (NZD)": apportionments["local"]["purchaser_amount"]
        },
    ]
    local_df = pd.DataFrame(local_data_for_table)

    # Display local table, formatting the currency column AND hiding the index
    st.table(local_df.style
             .format({"Amount (NZD)": "NZD {:,.2f}"})
             .hide(axis="index") # <--- Added this method call
            )

    # Display local installment status right after its table
    st.info(f"Current installment {'**paid** by Vendor' if local_installment_paid_by_vendor else '**not paid** by Vendor. Allow a Vendor credit to the Purchaser'}.")
    st.divider() # Add a visual separator

    # --- Regional Council Table ---
    # Check if regional rates were entered to avoid showing an empty table if not applicable
    # Also check if the apportionment calculation actually produced regional results
    regional_rates_applicable = (regional_yearly_rates > 0 or
                                (apportionments.get("regional") and
                                 apportionments["regional"]["vendor_days"] + apportionments["regional"]["purchaser_days"] > 0))

    if regional_rates_applicable:
        st.markdown(f"**{regional_council}:**") # Header for regional table
        regional_data_for_table = [
            {
                "Party": "Vendor",
                "Days": apportionments["regional"]["vendor_days"],
                "Amount (NZD)": apportionments["regional"]["vendor_amount"]
            },
            {
                "Party": "Purchaser",
                "Days": apportionments["regional"]["purchaser_days"],
                "Amount (NZD)": apportionments["regional"]["purchaser_amount"]
            },
        ]
        regional_df = pd.DataFrame(regional_data_for_table)

        # Display regional table, formatting the currency column AND hiding the index
        st.table(regional_df.style
                 .format({"Amount (NZD)": "NZD {:,.2f}"})
                 .hide(axis="index") # <--- Added this method call
                )

        # Display regional installment status right after its table
        st.info(f"Current installment {'**paid** by Vendor' if regional_installment_paid_by_vendor else '**not paid** by Vendor. Allow a Vendor credit to the Purchaser'}.")
        st.divider() # Add a visual separator
    else:
         # Only show this if regional rates > 0 but calculation resulted in zero days/amount?
         # Or maybe just skip if regional_yearly_rates is 0 initially? Let's simplify:
         if regional_yearly_rates > 0:
             st.info(f"No adjustment calculation needed for {regional_council} based on the dates.")
             st.divider()
         # If regional_yearly_rates was 0, we don't need to say anything