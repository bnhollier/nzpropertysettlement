import streamlit as st
import requests

ADDY_ADDRESS_DETAIL_URL = "https://api-nz.addysolutions.com/address-detail"
ADDY_API_KEY = "f53833b421d6464c96799ac374ee2e7d"  # For local testing

COUNCIL_MAPPING = {
    "Auckland": "Auckland Council",
    # Add more mappings as needed
}

if 'council1_mapped' not in st.session_state:
    st.session_state['council1_mapped'] = None
if 'council2_mapped' not in st.session_state:
    st.session_state['council2_mapped'] = None

def map_council(council_name):
    """Maps a council name to a display-friendly value."""
    return COUNCIL_MAPPING.get(council_name, council_name)

def fetch_councils_by_id(address_id):
    headers = {'Accept': 'application/json'}
    params = {'key': ADDY_API_KEY, 'id': address_id}
    try:
        response = requests.get(ADDY_ADDRESS_DETAIL_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if 'address' in data:
            territory = data['address'].get('territory')
            region = data['address'].get('region')
            return territory, region
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching address details: {e}")
        return None, None

st.subheader("Fetch Councils by Address ID")
address_id_input = st.text_input("Enter Address ID to Find Councils:")
fetch_button = st.button("Find Councils by ID")

if fetch_button and address_id_input:
    try:
        address_id = int(address_id_input)
        with st.spinner("Fetching council details..."):
            territory, region = fetch_councils_by_id(address_id)
            st.session_state['council1_mapped'] = map_council(territory) if territory else None
            st.session_state['council2_mapped'] = map_council(region) if region else None
    except ValueError:
        st.error("Please enter a valid integer for the Address ID.")

st.subheader("Form with Councils")
council1_options = ["", st.session_state.get('council1_mapped')] if st.session_state.get('council1_mapped') else [""]
council2_options = ["", st.session_state.get('council2_mapped')] if st.session_state.get('council2_mapped') else [""]

council1 = st.selectbox("Council 1", options=council1_options, index=1 if st.session_state.get('council1_mapped') else 0)
council2 = st.selectbox("Council 2 (Optional)", options=council2_options, index=1 if st.session_state.get('council2_mapped') else 0)