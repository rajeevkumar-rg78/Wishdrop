import csv, random
from pathlib import Path

# ----- Full Luxury + Retail Category List -----
categories = [
    # Women
    "Women > Dresses", "Women > Tops", "Women > Bottoms",
    "Women > Shoes", "Women > Handbags", "Women > Accessories",
    "Women > Jewelry",

    # Men
    "Men > Shirts", "Men > Pants", "Men > Jackets",
    "Men > Shoes", "Men > Watches", "Men > Accessories",

    # Beauty
    "Beauty > Skincare", "Beauty > Makeup", "Beauty > Fragrance",

    # Electronics
    "Electronics > Laptops", "Electronics > Phones",
    "Electronics > Wearables", "Electronics > TVs",
    "Electronics > Headphones",

    # Home + Costco
    "Home > Kitchen", "Home > Appliances", "Home > Furniture",
    "Costco > Essentials", "Costco > Snacks", "Costco > Household",

    # Sports
    "Sports > Fitness", "Sports > Equipment"
]

# ----- Stores -----
stores = [
    # Luxury Retailers
    "Nordstrom", "Bloomingdale's", "Saks Fifth Avenue",
    "Neiman Marcus", "Bergdorf Goodman",

    # Luxury Brands
    "Chanel", "Prada", "Gucci", "Louis Vuitton",
    "Burberry", "Saint Laurent", "Versace",

    # Beauty
    "Sephora", "Ulta Beauty",

    # Retail
    "Amazon", "Target", "Macy's",

    # Electronics
    "Best Buy", "Apple Store", "Sony Store",

    # Sportswear
    "Nike", "Adidas",

    # Wholesale
    "Costco", "Home Depot"
]

# ----- Luxury Brands -----
brands = [
    "Chanel", "Prada", "Gucci", "Dior", "Louis Vuitton",
    "Saint Laurent", "Versace", "Fendi", "Burberry", "Celine",
    "Bottega Veneta", "Valentino",

    "Coach", "Kate Spade", "Michael Kors", "Tory Burch",

    "Lululemon", "Nike", "Adidas",

    "Apple", "Samsung", "Sony", "Dyson",

    "Estee Lauder", "Lancome", "Tom Ford Beauty"
]

# ----- Build Items -----
def get_image(name, brand, category):
    query = f"{brand} {category.split('>')[-1]}".replace(" ", "+")
    return f"https://source.unsplash.com/600x750/?{query}"

def product_url(store, name):
    base = {
        "Amazon": "https://www.amazon.com/s?k=",
        "Nordstrom": "https://www.nordstrom.com/sr?keyword=",
        "Bloomingdale's": "https://www.bloomingdales.com/shop/featured/",
        "Saks Fifth Avenue": "https://www.saksfifthavenue.com/search?q=",
        "Neiman Marcus": "https://www.neimanmarcus.com/s/",
        "Costco": "https://www.costco.com/CatalogSearch?dept=All&keyword=",
        "Best Buy": "https://www.bestbuy.com/site/searchpage.jsp?st=",
        "Apple Store": "https://www.apple.com/us/search/",
    }.get(store, "https://www.google.com/search?q=")
    return f"{base}{name.replace(' ', '+')}"

rows = []
random.seed(42)

for i in range(200):  # 200 luxury products
    brand = random.choice(brands)
    cat = random.choice(categories)
    store = random.choice(stores)

    msrp = round(random.uniform(50, 2000), 2)
    price = round(msrp * random.uniform(0.5, 0.9), 2)
    discount = round((1 - price/msrp) * 100)

    name = (
        f"{brand} {random.choice(['Classic','Signature','Limited','Icon','Ultra'])} "
        f"{random.choice(['Dress','Handbag','Shoes','Jacket','Watch','Serum','Laptop','TV','Airfryer','Perfume'])}"
    )

    img = get_image(name, brand, cat)
    url = product_url(store, name)

    rows.append({
        "id": f"P-{1000+i}",
        "name": name,
        "brand": brand,
        "category": cat,
        "store": store,
        "msrp": msrp,
        "price": price,
        "discount_pct": discount,
        "image_url": img,
        "product_url": url
    })

# ----- Save File -----
output = Path("data/sample_products.csv")
output.parent.mkdir(exist_ok=True)

with open(output, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print("Luxury sample_products.csv generated successfully!")
