
import streamlit as st
import pandas as pd
from utils.storage import list_profiles, get_profile, save_profile, delete_profile

st.header("👤 Profile")

products = pd.read_csv("data/sample_products.csv")

st.subheader("Select or Create Profile")
existing = ["Create New"] + list_profiles()
chosen = st.selectbox("Choose profile", existing, index=0)

if chosen == "Create New":
    st.subheader("Create Your Shopping Profile")
    with st.form("profile_form", clear_on_submit=False):
        name = st.text_input("Name", placeholder="e.g., Shalini")
        height_in = st.number_input("Height (inches)", min_value=50, max_value=80, value=64)
        weight_lb = st.number_input("Weight (lbs)", min_value=80, max_value=300, value=140)
        top_size = st.text_input("Top Size (e.g., S, M, L, 8)")
        bottom_size = st.text_input("Bottom Size (e.g., 6, 8, 10)")
        shoe_size = st.text_input("Shoe Size (e.g., 7.5)")
        style = st.multiselect("Style Preferences", ["Casual","Formal","Party","Business","Athleisure","Luxury"])
        prefer_luxury = st.selectbox("Price Level", ["Budget", "Mid-range", "Luxury Only"], index=1)

        st.markdown("**Favorite Brands**")
        brands = sorted(products["brand"].unique().tolist())
        fav_brands = st.multiselect("Choose brands you like", brands, default=[b for b in brands if b in ["Gucci","Chanel","Prada","Lululemon","Nike","Coach","Calvin Klein","Estee Lauder"]])

        st.markdown("**Preferred Stores**")
        stores = sorted(products["store"].unique().tolist())
        fav_stores = st.multiselect("Choose stores you like", stores, default=[s for s in stores if s in ["Nordstrom","Sephora","Amazon"]])

        st.markdown("**Favorite Categories**")
        cats = sorted(products["category"].unique().tolist())
        fav_cats = st.multiselect("Choose categories", cats, default=[c for c in cats if "Women" in c or "Beauty" in c])

        notes = st.text_area("Notes (fit, materials, colors, must-avoid, etc.)", placeholder="e.g., Prefer silk, avoid wool; colors: blush, cream, black")

        submitted = st.form_submit_button("Save Profile")
        if submitted:
            if not name.strip():
                st.warning("Please enter a name before saving.")
            else:
                profile = {
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
                save_profile(name, profile)
                st.success(f"Profile '{name}' saved.")
                st.balloons()
else:
    st.subheader(f"Profile: {chosen}")
    prof = get_profile(chosen)
    st.json(prof)

    colA, colB = st.columns([1,1])
    with colA:
        if st.button("Delete Profile", type="secondary"):
            delete_profile(chosen)
            st.success("Profile deleted. Reload the page to see changes.")
    with colB:
        st.info("Profile data is stored locally in `data/profiles.json`.")
