import pandas as pd
import random

brands = [
    "Louis Vuitton","Gucci","Prada","Chanel","Burberry","Fendi",
    "Versace","Dior","Balenciaga","Givenchy","Valentino",
    "YSL","Bottega Veneta","Ferragamo","Moncler"
]

stores = [
    "Nordstrom","Bloomingdale's","Saks Fifth Avenue","Neiman Marcus",
    "Bergdorf Goodman","Chanel","Prada","Gucci","Louis Vuitton",
    "Burberry","Sephora","Ulta Beauty","Macy's","Amazon","Target",
    "Best Buy","Apple Store","Costco","Home Depot"
]

categories = [
    "Women > Shoes","Women > Handbags","Women > Dresses",
    "Women > Jewelry","Men > Shoes","Men > Shirts",
    "Men > Jackets","Beauty > Makeup","Beauty > Fragrance",
    "Electronics > Wearables","Electronics > Headphones",
    "Home > Decor","Sports > Fitness"
]

def create_item(i):
    brand = random.choice(brands)
    store = random.choice(stores)
    category = random.choice(categories)

    msrp = random.randint(150, 2500)
    discount_pct = random.choice([10, 15, 20, 25, 30, 35, 40, 50, 60])
    price = round(msrp * (1 - discount_pct/100), 2)

    return {
        "id": f"P-{1000+i}",
        "name": f"{brand} {random.choice(['Signature','Classic','Limited','Ultra','Icon'])} {random.choice(['Bag','Shoes','Watch','Jacket','Dress','Sneakers','Wallet','Backpack','Perfume','Laptop','Mixer'])}",
        "brand": brand,
        "category": category,
        "store": store,
        "msrp": msrp,
        "price": price,
        "discount_pct": discount_pct,
        "image_url": "https://source.unsplash.com/800x1000/?luxury,fashion,product",
        "product_url": "https://example.com/product"
    }

items = [create_item(i) for i in range(100)]
df = pd.DataFrame(items)

df.to_csv("data/sample_products.csv", index=False)

print("Wrote 100 luxury products → data/sample_products.csv")
