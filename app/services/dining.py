from app.models.schemas import DiningResponse, DiningItem
import random

def get_dining_recommendations(cuisine_preference: str = None, city_name: str = "Unknown") -> DiningResponse:
    """
    Recommend top 5 dining locations based on city and preference (mock data).
    """
    
    # Heuristic for cuisines based on city name (simple approach)
    city_lower = city_name.lower()
    
    # Default cuisines
    cuisines = ["Italian", "Japanese", "Mexican", "Indian", "American"]
    
    # Customize based on city hints
    if "mumbai" in city_lower or "delhi" in city_lower:
        cuisines = ["North Indian", "Street Food", "Mughlai", "South Indian", "Continental"]
    elif "london" in city_lower:
        cuisines = ["British Pub", "Indian Curry", "Italian", "Modern European", "Asian Fusion"]
    elif "rome" in city_lower or "milan" in city_lower:
        cuisines = ["Authentic Italian", "Roman", "Pizza", "Seafood", "Gelato"]
    elif "tokyo" in city_lower:
        cuisines = ["Sushi", "Ramen", "Izakaya", "Tempura", "Yakitori"]
    elif "new york" in city_lower:
        cuisines = ["Pizza Slice", "Bagels", "Steakhouse", "Chinese", "Fine Dining"]

    items = []
    
    prefixes = ["The", "Golden", "Royal", "Urban", "Rustic", "Little", "Grand"]
    suffixes = ["Bistro", "Kitchen", "Place", "House", "Garden", "Lounge", "Eatery"]
    
    for i in range(5):
        cuisine = cuisines[i % len(cuisines)]
        name = f"{random.choice(prefixes)} {cuisine.split(' ')[-1]} {random.choice(suffixes)}"
        
        # Consistent random images
        # Using loremflickr with 'food' or specific cuisine keyword
        keyword = cuisine.split(' ')[0].lower()
        image_url = f"https://loremflickr.com/300/200/{keyword},food?lock={len(city_name)+i}"
        
        rating = round(random.uniform(4.0, 5.0), 1)
        price_level = "$" * random.randint(1, 4)
        
        items.append(DiningItem(
            name=name,
            cuisine=cuisine,
            rating=rating,
            price_level=price_level,
            image_url=image_url,
            location=f"Downtown {city_name}"
        ))

    return DiningResponse(items=items, city=city_name)
