from app.models.schemas import ShoppingResponse, ShoppingItem
from app.core.config import settings
from amazon_paapi import AmazonApi
import random

def get_shopping_recommendation(temperature: float, weather_code: int, hour: int) -> ShoppingResponse:
    """
    Recommend apparel based on weather and time using Amazon PA-API with fallback.
    """
    
    # 1. Determine Search Keywords & Mood
    keywords = "fashion"
    mood = "Style"
    
    rain_codes = [51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99]
    snow_codes = [71, 73, 75, 77, 85, 86]
    
    is_night = hour < 6 or hour >= 18
    
    if weather_code in rain_codes:
        keywords = "raincoat umbrella waterproof boots"
        mood = "Rainy Day Essentials"
    elif weather_code in snow_codes:
        keywords = "snow boots winter jacket gloves scarf"
        mood = "Winter Warmth"
    elif temperature < 10:
        keywords = "heavy winter coat wool sweater thermal wear"
        mood = "Cozy & Warm"
    elif 10 <= temperature < 20:
        keywords = "light jacket hoodie denim jeans sneakers"
        mood = "Crisp & Cool"
    elif 20 <= temperature < 30:
        if is_night:
             keywords = "party dress casual shirt evening wear"
             mood = "Evening Vibes"
        else:
             keywords = "t-shirt shorts sunglasses cap cotton dress"
             mood = "Sunny Comfort"
    else: # Hot >= 30
        if is_night:
            keywords = "linen shirt breezy dress light cotton"
            mood = "Tropical Nights"
        else:
            keywords = "swimwear tank top shorts sun hat sandals"
            mood = "Beat the Heat"

    # 2. Try fetching from Amazon
    items = []
    
    if settings.AMAZON_ACCESS_KEY and settings.AMAZON_SECRET_KEY and settings.AMAZON_TAG:
        try:
            amazon = AmazonApi(
                settings.AMAZON_ACCESS_KEY, 
                settings.AMAZON_SECRET_KEY, 
                settings.AMAZON_TAG, 
                settings.AMAZON_REGION
            )
            # Search for products
            # Note: simplistic search; real usage might need specific search index like 'Apparel'
            search_result = amazon.search_items(keywords=keywords, search_index="Apparel", item_count=10)
            
            for item in search_result.items:
                 # Extract standard price or lowest price
                 price = "N/A"
                 if item.offers and item.offers.listings:
                     price = item.offers.listings[0].price.display_amount
                 
                 # Extract image (large)
                 image_url = ""
                 if item.images and item.images.primary and item.images.primary.large:
                     image_url = item.images.primary.large.url
                 
                 items.append(ShoppingItem(
                     title=item.item_info.title.display_value,
                     price=price,
                     image_url=image_url,
                     product_url=item.detail_page_url
                 ))
                 
        except Exception as e:
            print(f"Amazon API failed: {e}")
            # Fallback will trigger below
            
    # 3. Fallback Mock Data (if no keys or API failed/empty)
    if not items:
        # Generate 10 mock items
        base_titles = ["Stylish Jacket", "Comfortable Jeans", "Classic T-Shirt", "Cool Sneakers", "Warm Scarf", "Trendy Hat", "Cozy Sweater", "Elegant Dress", "Casual Shirt", "Modern Boots"]
        
        for i in range(10):
            mock_price = f"${random.randint(15, 150)}.99"
            mock_image = f"https://loremflickr.com/300/400/fashion?lock={i+random.randint(1,100)}"
            mock_title = f"{base_titles[i]} - {mood} Edition"
            
            items.append(ShoppingItem(
                title=mock_title,
                price=mock_price,
                image_url=mock_image,
                product_url="#" # No real link for mock
            ))

    return ShoppingResponse(items=items, mood=mood)
