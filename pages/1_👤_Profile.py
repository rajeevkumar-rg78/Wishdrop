import streamlit as st
import pandas as pd
from utils.storage import list_profiles, get_profile, save_profile, delete_profile

# Fix selectbox scrolling issue (global CSS)
st.markdown("""
<style>

/* Fix for selectbox dropdown scroll */
div[data-baseweb="select"] > div {
    max-height: 250px !important;
    overflow-y: auto !important;
}

/* Fix for multiselect dropdown scroll (brands, categories) */
div[role="listbox"] {
    max-height: 250px !important;
    overflow-y: auto !important;
}

/* Fix for popover containers used by multiselect */
div[data-baseweb="popover"] {
    max-height: 250px !important;
    overflow-y: auto !important;
}

</style>
""", unsafe_allow_html=True)


st.header("👤 Profile")

products = pd.read_csv("data/sample_products.csv")

# --------------------------
# SELECT PROFILE
# --------------------------

profiles = ["Create New"] + list_profiles()
chosen = st.selectbox("Choose a profile", profiles)

# Load existing or empty defaults
if chosen != "Create New":
    prof = get_profile(chosen)
    default_name = chosen
    default_height = prof.get("height_in", 64)
    default_weight = prof.get("weight_lb", 140)
    default_top = prof.get("sizes", {}).get("top", "")
    default_bottom = prof.get("sizes", {}).get("bottom", "")
    default_shoe = prof.get("sizes", {}).get("shoe", "")
    default_style = prof.get("style", [])
    default_price = prof.get("price_pref", "Mid-range")
    default_brands = prof.get("brands", [])
    default_stores = prof.get("stores", [])
    default_cats = prof.get("categories", [])
    default_notes = prof.get("notes", "")
else:
    default_name = ""
    default_height = 64
    default_weight = 140
    default_top = ""
    default_bottom = ""
    default_shoe = ""
    default_style = []
    default_price = "Mid-range"
    default_brands = []
    default_stores = []
    default_cats = []
    default_notes = ""

# --------------------------
# PROFILE FORM
# --------------------------

st.subheader("Edit Profile" if chosen != "Create New" else "Create Profile")

with st.form("profile_form"):
    name = st.text_input("Name", value=default_name)
    height_in = st.number_input("Height (inches)", min_value=50, max_value=80, value=default_height)
    weight_lb = st.number_input("Weight (lbs)", min_value=80, max_value=300, value=default_weight)
    top_size = st.text_input("Top Size (e.g., S, M, L, 8)", value=default_top)
    bottom_size = st.text_input("Bottom Size (e.g., 6, 8, 10)", value=default_bottom)
    shoe_size = st.text_input("Shoe Size", value=default_shoe)

    style = st.multiselect(
        "Style Preferences",
        ["Casual","Formal","Party","Business","Athleisure","Luxury"],
        default=default_style,
    )

    prefer_luxury = st.selectbox(
        "Price Level",
        ["Budget", "Mid-range", "Luxury Only"],
        index=["Budget","Mid-range","Luxury Only"].index(default_price),
    )

    st.markdown("**Favorite Brands**")
    all_brands = sorted(products["brand"].unique().tolist())
    fav_brands = st.multiselect("Choose brands", all_brands, default=default_brands)

    st.markdown("**Preferred Stores**")
    all_stores = sorted(products["store"].unique().tolist())
    fav_stores = st.multiselect("Choose stores", all_stores, default=default_stores)

    st.markdown("**Favorite Categories**")
    cats = sorted(products["category"].unique().tolist())
    fav_cats = st.multiselect("Categories", cats, default=default_cats)

    notes = st.text_area("Notes", value=default_notes)

    submitted = st.form_submit_button("💾 Save Changes")

    if submitted:
        if not name.strip():
            st.warning("Name cannot be empty.")
        else:
            updated_profile = {
                "height_in": height_in,
                "weight_lb": weight_lb,
                "sizes": {"top": top_size, "bottom": bottom_size, "shoe": shoe_size},
                "style": style,
                "price_pref": prefer_luxury,
                "brands": fav_brands,
                "stores": fav_stores,
                "categories": fav_cats,
                "notes": notes,
            }
            save_profile(name, updated_profile)
            st.success("Profile saved successfully!")

# --------------------------
# DELETE PROFILE
# --------------------------

if chosen != "Create New":
    if st.button("🗑️ Delete Profile"):
        delete_profile(chosen)
        st.success("Profile deleted. Please refresh the page.")
