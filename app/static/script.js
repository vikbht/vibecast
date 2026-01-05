const cityInput = document.getElementById('cityInput');
const searchBtn = document.getElementById('searchBtn');
const weatherCard = document.getElementById('weatherCard');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('errorMessage');

// Unit Toggle elements
const metricBtn = document.getElementById('metricBtn');
const imperialBtn = document.getElementById('imperialBtn');
let currentUnit = 'imperial';
let lastCity = ''; // Store last searched city to refresh on toggle

// Elements to update
const cityDisplay = document.getElementById('cityDisplay');
const temperature = document.getElementById('temperature');
const tempUnit = document.getElementById('tempUnit');
const description = document.getElementById('description');
const windSpeed = document.getElementById('windSpeed');
const windUnit = document.getElementById('windUnit');
const localTime = document.getElementById('localTime');

// Music elements
const musicContainer = document.getElementById('musicContainer');
const musicFrame = document.getElementById('musicFrame');
const musicMood = document.getElementById('musicMood');
const songTitle = document.getElementById('songTitle');

// Shopping elements
const shoppingContainer = document.getElementById('shoppingContainer');
const shoppingMood = document.getElementById('shoppingMood');
const shoppingCarousel = document.getElementById('shoppingCarousel');

// Dining elements
const diningContainer = document.getElementById('diningContainer');
const diningList = document.getElementById('diningList');

const suggestionsBox = document.getElementById('suggestions');

// Debounce helper
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Autocomplete Logic
async function fetchSuggestions(query) {
    if (query.length < 2) {
        suggestionsBox.classList.add('hidden');
        return;
    }

    try {
        const response = await fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(query)}&count=5&language=en&format=json`);
        const data = await response.json();

        if (data.results && data.results.length > 0) {
            showSuggestions(data.results);
        } else {
            suggestionsBox.classList.add('hidden');
        }
    } catch (error) {
        console.error('Error fetching suggestions:', error);
    }
}

function showSuggestions(locations) {
    suggestionsBox.innerHTML = '';
    suggestionsBox.classList.remove('hidden');

    locations.forEach(location => {
        const div = document.createElement('div');
        div.className = "px-6 py-3 hover:bg-white/20 cursor-pointer transition-colors border-b border-white/5 last:border-0 text-white text-base";

        let locationText = `${location.name}`;
        if (location.admin1) locationText += `, ${location.admin1}`;
        locationText += `, ${location.country}`;

        div.textContent = locationText;

        div.addEventListener('click', () => {
            selectCity(location, locationText);
        });

        suggestionsBox.appendChild(div);
    });
}

function selectCity(location, displayText) {
    cityInput.value = location.name; // Keep input simple for search, or use full text
    suggestionsBox.classList.add('hidden');
    // Trigger search immediately
    fetchWeather(location.name);
}

// Event Listeners
const debouncedFetch = debounce((e) => fetchSuggestions(e.target.value), 300);

cityInput.addEventListener('input', debouncedFetch);

// Click outside to close
document.addEventListener('click', (e) => {
    if (!cityInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
        suggestionsBox.classList.add('hidden');
    }
});

searchBtn.addEventListener('click', () => fetchWeather(cityInput.value.trim()));
cityInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        suggestionsBox.classList.add('hidden');
        fetchWeather(cityInput.value.trim());
    }
});

// Toggle Event Listeners
metricBtn.addEventListener('click', () => setUnit('metric'));
imperialBtn.addEventListener('click', () => setUnit('imperial'));

function setUnit(unit) {
    if (currentUnit === unit) return;
    currentUnit = unit;

    // Update active class
    if (unit === 'metric') {
        metricBtn.className = "px-3 py-1 rounded-md text-sm font-semibold transition-all duration-300 bg-white text-blue-600 shadow-sm";
        imperialBtn.className = "px-3 py-1 rounded-md text-sm font-semibold transition-all duration-300 text-white/70 hover:text-white";
    } else {
        imperialBtn.className = "px-3 py-1 rounded-md text-sm font-semibold transition-all duration-300 bg-white text-blue-600 shadow-sm";
        metricBtn.className = "px-3 py-1 rounded-md text-sm font-semibold transition-all duration-300 text-white/70 hover:text-white";
    }

    // Refresh data if we have a city
    if (lastCity) {
        // We need to re-fetch. Since we don't store lat/lon globally, let's just re-trigger fetchWeather.
        // Optimization: We could store lat/lon to skip geocoding, but re-fetching by name is simpler for now.
        fetchWeather(lastCity);
    }
}

async function fetchWeather(city) {
    if (!city) return;
    lastCity = city;

    // Reset UI
    loading.classList.remove('hidden');
    weatherCard.classList.add('hidden');
    errorMessage.classList.add('hidden');
    musicContainer.classList.add('hidden');
    shoppingContainer.classList.add('hidden');
    diningContainer.classList.add('hidden');

    try {
        // 1. Get coordinates from OpenMeteo Geocoding API
        const geoResponse = await fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(city)}&count=1&language=en&format=json`);
        const geoData = await geoResponse.json();

        if (!geoData.results || geoData.results.length === 0) {
            throw new Error('City not found');
        }

        const { latitude, longitude, name, country } = geoData.results[0];

        // 2. Fetch weather from our backend with UNIT
        const response = await fetch(`/api/v1/weather?lat=${latitude}&lon=${longitude}&unit=${currentUnit}`);

        if (!response.ok) {
            throw new Error('Weather data fetch failed');
        }

        const data = await response.json();

        // 3. Fetch Music Recommendation
        // Convert to Celsius for music logic if needed, or simply force API to interpret. 
        // Our backend logic assumes Celsius for thresholds (<10, 10-20, etc). 
        // If currentUnit is metric, we have Celsius. If imperial, we have Fahrenheit.
        let tempCelsius = data.current.temperature;
        if (currentUnit === 'imperial') {
            tempCelsius = (tempCelsius - 32) * 5 / 9;
        }

        const musicResponse = await fetch(`/api/v1/music/recommend?temperature=${tempCelsius}&weather_code=${data.current.weather_code}`);
        const musicData = await musicResponse.json();

        // 4. Fetch Shopping Recommendation
        // Extract hour from current time (ISO format: YYYY-MM-DDTHH:mm)
        const hour = new Date(data.current.time).getHours();
        const shoppingResponse = await fetch(`/api/v1/shopping/recommend?temperature=${tempCelsius}&weather_code=${data.current.weather_code}&hour=${hour}`);
        const shoppingData = await shoppingResponse.json();

        // 5. Fetch Dining Recommendation
        const diningResponse = await fetch(`/api/v1/dining/recommend?city=${encodeURIComponent(name)}`);
        const diningData = await diningResponse.json();

        updateUI(data, name, country, musicData, shoppingData, diningData);
    } catch (error) {
        console.error(error);
        errorMessage.classList.remove('hidden');
    } finally {
        loading.classList.add('hidden');
    }
}

function updateUI(data, cityName, countryName, musicData, shoppingData, diningData) {
    // Display city and country
    cityDisplay.textContent = `${cityName}, ${countryName}`;

    temperature.textContent = Math.round(data.current.temperature);
    tempUnit.textContent = currentUnit === 'metric' ? '°C' : '°F';

    windSpeed.textContent = data.current.wind_speed;
    windUnit.textContent = currentUnit === 'metric' ? 'km/h' : 'mph';

    // Weather code mapping (simplified for demo)
    const weatherCodes = {
        0: 'Clear sky',
        1: 'Mainly clear',
        2: 'Partly cloudy',
        3: 'Overcast',
        45: 'Fog',
        48: 'Depositing rime fog',
        51: 'Light drizzle',
        53: 'Moderate drizzle',
        55: 'Dense drizzle',
        61: 'Slight rain',
        63: 'Moderate rain',
        65: 'Heavy rain',
        71: 'Slight snow',
        73: 'Moderate snow',
        75: 'Heavy snow',
        95: 'Thunderstorm',
        96: 'Thunderstorm with slight hail',
        99: 'Thunderstorm with heavy hail'
    };
    description.textContent = weatherCodes[data.current.weather_code] || 'Unknown';

    // Format Data time
    const date = new Date(data.current.time);
    localTime.textContent = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    weatherCard.classList.remove('hidden');

    // Update Music
    if (musicData) {
        musicMood.textContent = `Mood: ${musicData.mood}`;
        songTitle.textContent = `${musicData.title} - ${musicData.artist}`;
        musicFrame.src = `https://www.youtube.com/embed/${musicData.video_id}?autoplay=1`;
        musicContainer.classList.remove('hidden');
    }

    // Update Shopping
    if (shoppingData && shoppingData.items && shoppingData.items.length > 0) {
        shoppingMood.textContent = `Vibe: ${shoppingData.mood}`;
        shoppingCarousel.innerHTML = '';

        shoppingData.items.forEach(item => {
            const card = document.createElement('div');
            card.className = "min-w-[200px] w-[200px] bg-white/10 rounded-xl overflow-hidden snap-center flex flex-col border border-white/10 hover:bg-white/20 transition-all duration-300";

            // Image
            const imgDiv = document.createElement('div');
            imgDiv.className = "h-48 w-full bg-white/5 relative overflow-hidden";
            const img = document.createElement('img');
            img.src = item.image_url;
            img.alt = item.title;
            img.className = "w-full h-full object-cover transition-transform duration-500 hover:scale-110";
            imgDiv.appendChild(img);

            // Content
            const contentDiv = document.createElement('div');
            contentDiv.className = "p-3 flex flex-col flex-1 justify-between";

            const title = document.createElement('h3');
            title.className = "text-sm font-medium leading-tight mb-1 line-clamp-2 min-h-[2.5em]";
            title.textContent = item.title;

            const price = document.createElement('p');
            price.className = "text-blue-200 font-bold text-sm mb-2";
            price.textContent = item.price;

            const link = document.createElement('a');
            link.href = item.product_url;
            link.target = "_blank";
            link.className = "block w-full text-center bg-white/20 hover:bg-white/30 text-white text-xs font-semibold py-2 rounded-lg transition-colors";
            link.textContent = "View on Amazon";

            contentDiv.appendChild(title);
            contentDiv.appendChild(price);
            contentDiv.appendChild(link);

            card.appendChild(imgDiv);
            card.appendChild(contentDiv);

            shoppingCarousel.appendChild(card);
        });

        shoppingContainer.classList.remove('hidden');
    }

    // Update Dining
    if (diningData && diningData.items && diningData.items.length > 0) {
        diningList.innerHTML = '';

        diningData.items.forEach(item => {
            const div = document.createElement('div');
            div.className = "flex gap-3 items-center p-2 rounded-xl bg-white/5 hover:bg-white/10 transition-colors border border-white/5";

            // Image
            const img = document.createElement('img');
            img.src = item.image_url;
            img.alt = item.name;
            img.className = "w-16 h-16 rounded-lg object-cover flex-none";

            // Content
            const content = document.createElement('div');
            content.className = "flex-1 min-w-0";

            const header = document.createElement('div');
            header.className = "flex justify-between items-start";

            const name = document.createElement('h3');
            name.className = "text-sm font-semibold truncate pr-2 leading-tight";
            name.textContent = item.name;

            const rating = document.createElement('span');
            rating.className = "text-xs font-bold bg-yellow-400 text-black px-1.5 py-0.5 rounded flex-none";
            rating.textContent = item.rating.toFixed(1);

            header.appendChild(name);
            header.appendChild(rating);

            const meta = document.createElement('p');
            meta.className = "text-xs text-blue-200 mt-1 truncate";
            meta.textContent = `${item.cuisine} • ${item.price_level}`;

            content.appendChild(header);
            content.appendChild(meta);

            div.appendChild(img);
            div.appendChild(content);

            diningList.appendChild(div);
        });

        diningContainer.classList.remove('hidden');
    }
}
