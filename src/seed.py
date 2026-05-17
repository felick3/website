from models import get_db

def seed():
    db = get_db()

    db.execute("DELETE FROM products")

    products = [
        ("Асимметричная куртка","zip","Верхняя одежда",68000,
         "Асимметричная куртка...",
         "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=800"),

        ("Классическая рубашка","tshirt","Рубашки",24000,
         "Рубашка строгого кроя...",
         "https://images.unsplash.com/photo-1620012253295-c15cc3e65df4?w=800"),

        ("Oversized худи","longsleeve","Верхняя одежда",52000,
         "Оверсайз худи...",
         "https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=800"),

        ("Карго штаны","jeans","Брюки",48000,
         "Карго-брюки...",
         "https://images.unsplash.com/photo-1542272604-787c3835535d?w=800"),

        ("Pullover Essential","hoodie","Худи",32000,
         "Базовое худи...",
         "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800"),
    ]

    db.executemany("""
    INSERT INTO products (name, category, category_label, price, description, image)
    VALUES (?, ?, ?, ?, ?, ?)
    """, products)

    db.commit()
    db.close()

if __name__ == "__main__":
    seed()
    print("Seed done")