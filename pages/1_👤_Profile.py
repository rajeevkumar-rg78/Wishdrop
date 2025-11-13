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

        # Basic Info
        height_in = st.number_input("Height (inches)", min_value=50, max_value=80, value=64)
        weight_lb = st.number_input("Weight (lbs)", min_value=80, max_value=300, value=140)

        top_size = st.text_input("Top Size (e.g., S, M, L, 8)")
        bottom_size = st.text_input("Bottom Size (e.g., 6, 8, 10)")
        shoe_size = st.text_input("Shoe Size (e.g., 7.5)")

        style = st.multiselect(
            "Style Preferences",
            ["Casual","Formal","Party","Business","Athleisure","Luxury","Designer"]
        )

        prefer_luxury = st.selectbox(
            "Price Level",
            ["Budget", "Mid-range", "Luxury Only"],
            index=1
        )

        # -------------------- Luxury Brands --------------------
        st.markdown("### 🌟 Favorite Brands (Luxury + Modern)")
        brands = [
            # Luxury Designers
            "Chanel", "Prada", "Gucci", "Dior", "Louis Vuitton",
            "Saint Laurent", "Burberry", "Fendi", "Versace",
            "Valentino", "Celine", "Bottega Veneta",

            # Contemporary
            "Coach", "Kate Spade", "Michael Kors", "Tory Burch",
            "Ralph Lauren",

            # Beauty / Fragrance
            "Chanel Beauty", "Dior Beauty", "Estee Lauder",
            "Lancome", "Tom Ford Beauty", "Charlotte Tilbury",

            # Active / Sports
            "Lululemon", "Nike", "Adidas",

            # Electronics
            "Apple", "Samsung", "Sony", "Dyson"
        ]

        fav_brands = st.multiselect("Choose brands you like", brands)

        # -------------------- Luxury & Retail Stores --------------------
        st.markdown("### 🛍️ Preferred Stores (Luxury + Retail + Electronics)")

        stores = [
            # Luxury Retailers
            "Nordstrom",
            "Bloomingdale's",
            "Saks Fifth Avenue",
            "Neiman Marcus",
            "Bergdorf Goodman",

            # Luxury Brand Boutiques
            "Chanel",
            "Prada",
            "Gucci",
            "Louis Vuitton",
            "Burberry",
            "Saint Laurent",
            "Versace",

            # Beauty Stores
            "Sephora",
            "Ulta Beauty",

            # General / Online Retail
            "Macy's",
            "Amazon",
            "Target",

            # Electronics
            "Best Buy",
            "Apple Store",
            "Sony Store",

            # Sportswear
            "Nike",
            "Adidas",

            # Wholesale / Costco
            "Costco",
            "Home Depot"
        ]

        fav_stores = st.multiselect("Choose stores you like", stores)

        # -------------------- Categories --------------------
        st.markdown("### 🗂️ Favorite Categories (All Departments)")

        cats = [
            # Women
            "Women > Dresses",
            "Women > Tops",
            "Women > Bottoms",
            "Women > Shoes",
            "Women > Handbags",
            "Women > Accessories",
            "Women > Jewelry",

            # Men
            "Men > Shirts",
            "Men > Pants",
            "Men > Jackets",
            "Men > Shoes",
            "Men > Watches",
            "Men > Accessories",

            # Beauty
            "Beauty > Skincare",
            "Beauty > Makeup",
            "Beauty > Fragrance",

            # Electronics
            "Electronics > Laptops",
            "Electronics > Phones",
            "Electronics > Wearables",
            "Electronics > TVs",
            "Electronics > Headphones",

            # Home & Costco-style
            "Home > Kitchen",
            "Home > Appliances",
            "Home > Furniture",
            "Costco > Essentials",
            "Costco > Snacks",
            "Costco > Household",

            # Sports / Fitness
            "Sports > Fitness",
            "Sports > Equipment"
        ]

        fav_cats = st.multiselect("Choose categories", cats)

        # -------------------- Notes --------------------
        notes = st.text_area(
            "Notes (fit, materials, colors, must-avoid, etc.)",
            placeholder="e.g., Prefer silk, avoid wool; love pink, cream, navy"
        )

        # -------------------- Save --------------------
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
                st.success(f"Profile '{name}' saved!")
                st.balloons()

# Existing Profile View
else:
    st.subheader(f"Profile: {chosen}")
    prof = get_profile(chosen)
    st.json(prof)

    colA, colB = st.columns([1, 1])

    with colA:
        if st.button("Delete Profile", type="secondary"):
            delete_profile(chosen)
            st.success("Profile deleted. Reload to update.")

    with colB:
        st.info("Profile data stored locally in `data/profiles.json`.")
