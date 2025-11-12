
import streamlit as st

st.set_page_config(page_title="WishDrop — Smart Shopping (Pinterest + Hopper)", layout="wide")

st.title("🛍️ WishDrop v2")
st.caption("Pinterest-style discovery + Hopper-style price tracking, personalized to your profile.")

st.markdown("""
**How to use**
1. Go to **👤 Profile** and create your profile (height, weight, sizes, favorite brands/stores — e.g., *Nordstrom*, luxury brands).
2. Visit **🖼️ Discover** to see a personalized feed of items on sale.
3. Use **❤️ Boards & Alerts** to save favorites and track price drops.
""")

st.info("Use the left sidebar or the **Pages** menu to navigate.")
