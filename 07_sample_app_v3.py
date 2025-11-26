"""
Wedding Destination Hotel Finder - Premium Experience
Streamlit Application (Single File)
Version 3.0 - Stunning UI & Flow
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import mysql.connector
from mysql.connector import Error
import time

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Wedding Hotel Finder | Find Your Dream Venue",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS STYLING
# ============================================================

st.markdown("""
<style>
    /* Main Theme Colors */
    :root {
        --primary-color: #FF6B9D;
        --secondary-color: #C44569;
        --accent-color: #FFC1CC;
        --dark-bg: #1E1E2E;
        --card-bg: #2A2A3E;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        text-align: center;
        animation: fadeIn 1s ease-in;
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: #f0f0f0;
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    /* Card Styling */
    .hotel-card {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 5px solid #667eea;
    }
    
    .hotel-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    /* Progress Bar */
    .progress-container {
        width: 100%;
        background: #e0e0e0;
        border-radius: 10px;
        margin: 2rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 8px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    /* Step Indicator */
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
        position: relative;
    }
    
    .step {
        flex: 1;
        text-align: center;
        position: relative;
        padding: 1rem;
    }
    
    .step-circle {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: #e0e0e0;
        margin: 0 auto 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .step-circle.active {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        transform: scale(1.1);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .step-circle.completed {
        background: #4CAF50;
        color: white;
    }
    
    /* Stat Cards */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin: 0.5rem 0;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
    }
    
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Input Field Styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .animate-in {
        animation: slideIn 0.5s ease-out;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: white;
    }
    
    /* Success/Error Messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Dataframe Styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Price Tag */
    .price-tag {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    /* Rating Badge */
    .rating-badge {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def show_progress_bar(current_step):
    """Display animated progress bar"""
    steps = ["User Info", "Hotel Search", "Comparison", "Booking Confirmation"]
    progress = (steps.index(current_step) + 1) / len(steps) * 100
    
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {progress}%"></div>
    </div>
    """, unsafe_allow_html=True)

def show_step_indicator(current_step):
    """Display step indicator with icons"""
    steps = [
        ("👤", "User Info"),
        ("🔍", "Search"),
        ("📊", "Compare"),
        ("✓", "Confirm")
    ]
    
    current_index = ["User Info", "Hotel Search", "Comparison", "Booking Confirmation"].index(current_step)
    
    cols = st.columns(4)
    for idx, (icon, label) in enumerate(steps):
        with cols[idx]:
            status = "completed" if idx < current_index else ("active" if idx == current_index else "")
            st.markdown(f"""
            <div class="step">
                <div class="step-circle {status}">
                    {icon}
                </div>
                <div style="color: {'#667eea' if status else '#999'}; font-weight: {'bold' if status else 'normal'};">
                    {label}
                </div>
            </div>
            """, unsafe_allow_html=True)

def display_hotel_card(hotel, index):
    """Display beautiful hotel card"""
    amenities_list = hotel.get('amenities', 'N/A')[:80]
    if len(str(hotel.get('amenities', ''))) > 80:
        amenities_list += "..."
    
    return st.markdown(f"""
    <div class="hotel-card animate-in">
        <h3 style="color: #667eea; margin: 0 0 1rem 0;">🏨 {hotel['name']}</h3>
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
            <div>
                <p style="margin: 0.3rem 0;"><strong>📍 Location:</strong> {hotel['location']}</p>
                <p style="margin: 0.3rem 0;"><strong>🏷️ Category:</strong> {hotel['category']}</p>
                <p style="margin: 0.3rem 0;"><strong>✨ Amenities:</strong> {amenities_list}</p>
            </div>
            <div style="text-align: right;">
                <span class="price-tag">${hotel['price_per_night']:.0f}/night</span><br>
                <span class="rating-badge">⭐ {hotel['rating']}/5</span><br>
                <span style="color: #666; font-size: 0.9rem;">🏨 {hotel['rooms']} rooms</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# DATABASE CONNECTION CONFIGURATION
# ============================================================

@st.cache_resource
def get_db_connection():
    """Establish and cache MySQL database connection"""
    try:
        connection = mysql.connector.connect(
            host=st.secrets.get("mysql_host", "localhost"),
            user=st.secrets.get("mysql_user", "root"),
            password=st.secrets.get("mysql_password", ""),
            database=st.secrets.get("mysql_database", "5033_ali"),
            port=st.secrets.get("mysql_port", 3306)
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
        return None

@st.cache_data(ttl=3600)
def fetch_hotels_from_db(location_filter=None, budget_filter=None):
    """
    Fetch hotels from MySQL database with optional filtering
    
    Args:
        location_filter: Filter by city or state (partial match)
        budget_filter: Filter by max price per night
    
    Returns:
        List of hotel dictionaries or empty list if connection fails
    """
    connection = get_db_connection()
    if connection is None:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Query using actual database structure
        query = """
        SELECT 
            h.HotelID,
            h.HotelName as name,
            h.City,
            h.State,
            CONCAT(h.City, ', ', h.State) as location,
            h.AverageRating as rating,
            h.PhoneNumber as phone,
            h.Email as email,
            h.Website as website,
            h.StreetAddress as address,
            COALESCE(AVG(r.BasePrice), 300) as price_per_night,
            COALESCE(COUNT(DISTINCT r.RoomID), 0) as rooms,
            GROUP_CONCAT(DISTINCT a.AmenityName SEPARATOR ', ') as amenities,
            h.StarRating
        FROM HOTEL h
        LEFT JOIN ROOM r ON h.HotelID = r.HotelID AND r.RoomStatus = 'Available'
        LEFT JOIN HOTELAMENITIES ha ON h.HotelID = ha.HotelID
        LEFT JOIN AMENITIES a ON ha.AmenityID = a.AmenityID
        WHERE 1=1
        """
        
        params = []
        
        # Add location filter
        if location_filter and location_filter.strip():
            location_filter_lower = location_filter.lower().strip()
            query += " AND (LOWER(h.City) LIKE %s OR LOWER(h.State) = %s)"
            params.extend([f"%{location_filter_lower}%", location_filter_lower])
        
        # Group by hotel
        query += """ GROUP BY h.HotelID, h.HotelName, h.City, h.State, 
                     h.PhoneNumber, h.Email, h.Website, h.StreetAddress, 
                     h.AverageRating, h.StarRating"""
        
        # Add budget filter to HAVING clause
        if budget_filter:
            query += " HAVING COALESCE(AVG(r.BasePrice), 300) <= %s"
            params.append(budget_filter)
        
        query += " ORDER BY h.AverageRating DESC LIMIT 100"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        # Convert results to list of dictionaries
        hotels = []
        for row in results:
            hotels.append({
                "hotel_id": row.get("HotelID"),
                "name": row.get("name", ""),
                "location": row.get("location", ""),
                "state": row.get("State", ""),
                "rating": float(row.get("rating", 4.5)) if row.get("rating") else 4.5,
                "price_per_night": float(row.get("price_per_night", 300)) if row.get("price_per_night") else 300,
                "rooms": int(row.get("rooms", 0)) if row.get("rooms") else 0,
                "amenities": row.get("amenities", "Amenities not listed"),
                "category": f"{row.get('StarRating', 4)}-star Hotel" if row.get("StarRating") else "Hotel",
                "phone": row.get("phone", ""),
                "email": row.get("email", ""),
                "website": row.get("website", "")
            })
        
        cursor.close()
        return hotels
        
    except Error as e:
        st.error(f"Error fetching hotels from database: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            connection.close()

# ============================================================
# FALLBACK SAMPLE DATA
# ============================================================

SAMPLE_HOTELS = [
    # Hawaii - Maui (10)
    {"name": "Maui Grand Resort", "location": "Maui, HI", "state": "HI", "rating": 4.8, "price_per_night": 350, "rooms": 150, "amenities": "Ceremony Space, Catering, Coordination", "category": "Beachfront Resort"},
    {"name": "Wailea Beach Resort", "location": "Maui, HI", "state": "HI", "rating": 4.7, "price_per_night": 320, "rooms": 120, "amenities": "Beach Access, Pool, Spa", "category": "Beachfront Resort"},
    {"name": "The Ritz-Carlton Maui", "location": "Maui, HI", "state": "HI", "rating": 4.9, "price_per_night": 580, "rooms": 80, "amenities": "Ultra-Luxury, Spa, Beach Ceremony", "category": "Luxury Resort"},
    
    # Florida - Miami (5)
    {"name": "Miami Luxury Downtown", "location": "Miami, FL", "state": "FL", "rating": 4.3, "price_per_night": 400, "rooms": 180, "amenities": "Urban, Rooftop Events, Restaurant", "category": "Urban Luxury"},
    {"name": "Fontainebleau Miami Beach", "location": "Miami, FL", "state": "FL", "rating": 4.6, "price_per_night": 420, "rooms": 220, "amenities": "Beach, Pool, Entertainment", "category": "Beachfront Resort"},
    
    # New York (3)
    {"name": "Plaza Hotel New York", "location": "New York, NY", "state": "NY", "rating": 4.8, "price_per_night": 800, "rooms": 300, "amenities": "Iconic, Luxury, Ballroom", "category": "Urban Luxury"},
    {"name": "The Peninsula New York", "location": "New York, NY", "state": "NY", "rating": 4.9, "price_per_night": 750, "rooms": 150, "amenities": "Luxury, Spa, Fine Dining", "category": "Urban Luxury"},
]

# ============================================================
# INITIALIZE SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "User Info"

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "user_phone" not in st.session_state:
    st.session_state.user_phone = ""

if "user_role" not in st.session_state:
    st.session_state.user_role = "Customer"

if "search_location" not in st.session_state:
    st.session_state.search_location = ""

if "search_budget" not in st.session_state:
    st.session_state.search_budget = 500

if "search_start_date" not in st.session_state:
    st.session_state.search_start_date = datetime.now().date()

if "search_end_date" not in st.session_state:
    st.session_state.search_end_date = (datetime.now() + timedelta(days=3)).date()

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "selected_hotel" not in st.session_state:
    st.session_state.selected_hotel = None

if "booking_confirmed" not in st.session_state:
    st.session_state.booking_confirmed = False

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem 0; color: white;">
    <h1 style="font-size: 2.5rem; margin: 0;">💍</h1>
    <h2 style="color: white; margin: 0.5rem 0;">Wedding Venue</h2>
    <p style="opacity: 0.9; font-size: 0.9rem;">Find Your Dream Location</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

pages = ["User Info", "Hotel Search", "Comparison", "Booking Confirmation"]

# Custom radio buttons with better styling
st.sidebar.markdown("<h3 style='color: white;'>Navigation</h3>", unsafe_allow_html=True)
selected_page = st.sidebar.radio(
    "Select a Page:",
    pages,
    label_visibility="collapsed"
)
st.session_state.page = selected_page

# Show user info in sidebar if available
if st.session_state.user_name:
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; color: white;">
        <h3 style="color: white; margin-top: 0;">👤 Welcome!</h3>
        <p style="margin: 0.3rem 0;"><strong>Name:</strong> {}</p>
        <p style="margin: 0.3rem 0;"><strong>Email:</strong> {}</p>
        <p style="margin: 0.3rem 0;"><strong>Role:</strong> {}</p>
    </div>
    """.format(st.session_state.user_name, st.session_state.user_email, st.session_state.user_role), 
    unsafe_allow_html=True)

# Add some stats if search results exist
if st.session_state.search_results:
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h3 style='color: white;'>Quick Stats</h3>", unsafe_allow_html=True)
    st.sidebar.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{len(st.session_state.search_results)}</div>
        <div class="stat-label">Hotels Found</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.search_results:
        avg_price = sum(h['price_per_night'] for h in st.session_state.search_results) / len(st.session_state.search_results)
        st.sidebar.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="stat-number">${avg_price:.0f}</div>
            <div class="stat-label">Avg. Price/Night</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# PAGE 1: USER INFORMATION
# ============================================================

if st.session_state.page == "User Info":
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>👰🤵 Welcome to Your Wedding Journey</h1>
        <p>Let's start by getting to know you better</p>
    </div>
    """, unsafe_allow_html=True)
    
    show_step_indicator("User Info")
    show_progress_bar("User Info")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Form in a nice container
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1);">
        """, unsafe_allow_html=True)
        
        st.markdown("### 📝 Your Information")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            user_name = st.text_input(
                "Full Name",
                value=st.session_state.user_name,
                placeholder="e.g., John Doe",
                help="Enter your full name as it appears on official documents"
            )

        with col_b:
            user_email = st.text_input(
                "Email Address",
                value=st.session_state.user_email,
                placeholder="e.g., john@example.com",
                help="We'll send your booking confirmation here"
            )

        col_a, col_b = st.columns(2)

        with col_a:
            user_phone = st.text_input(
                "Phone Number",
                value=st.session_state.user_phone,
                placeholder="e.g., +1 (555) 123-4567",
                help="For urgent booking-related communications"
            )

        with col_b:
            user_role = st.selectbox(
                "I am a...",
                ["Customer", "Wedding Planner"],
                index=0 if st.session_state.user_role == "Customer" else 1,
                help="Select your role in this wedding planning process"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("✨ Continue to Hotel Search", use_container_width=True, key="submit_user", type="primary"):
            if user_name and user_email and user_phone:
                st.session_state.user_name = user_name
                st.session_state.user_email = user_email
                st.session_state.user_phone = user_phone
                st.session_state.user_role = user_role
                
                # Animated success
                with st.spinner("Saving your information..."):
                    time.sleep(0.5)
                st.success("✓ Perfect! Let's find your dream venue!")
                st.balloons()
                time.sleep(1)
                st.session_state.page = "Hotel Search"
                st.rerun()
            else:
                st.error("⚠️ Please fill in all fields to continue.")
        
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# PAGE 2: HOTEL SEARCH
# ============================================================

elif st.session_state.page == "Hotel Search":
    st.markdown("""
    <div class="main-header">
        <h1>🔍 Discover Your Perfect Wedding Venue</h1>
        <p>Search through our curated collection of premium hotels</p>
    </div>
    """, unsafe_allow_html=True)

    show_step_indicator("Hotel Search")
    show_progress_bar("Hotel Search")

    if not st.session_state.user_name:
        st.warning("⚠️ Please complete your User Information first!")
        if st.button("👤 Go to User Info", type="primary"):
            st.session_state.page = "User Info"
            st.rerun()
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Search Form
        with st.container():
            st.markdown("### 🎯 Search Criteria")
            
            col1, col2 = st.columns(2)

            with col1:
                search_location = st.text_input(
                    "🌍 Location",
                    value=st.session_state.search_location,
                    placeholder="e.g., Hawaii, Miami, New York, CA",
                    help="Enter a city, state name, or state abbreviation"
                )

            with col2:
                search_budget = st.number_input(
                    "💰 Maximum Budget (per night)",
                    min_value=100,
                    max_value=10000,
                    value=st.session_state.search_budget,
                    step=50,
                    help="Set your maximum price per night in USD"
                )

            col1, col2 = st.columns(2)

            with col1:
                search_start_date = st.date_input(
                    "📅 Check-in Date",
                    value=st.session_state.search_start_date,
                    min_value=datetime.now().date(),
                    help="Select your arrival date"
                )

            with col2:
                search_end_date = st.date_input(
                    "📅 Check-out Date",
                    value=st.session_state.search_end_date,
                    min_value=datetime.now().date() + timedelta(days=1),
                    help="Select your departure date"
                )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🔍 Search Hotels", use_container_width=True, key="search_button", type="primary"):
                st.session_state.search_location = search_location
                st.session_state.search_budget = search_budget
                st.session_state.search_start_date = search_start_date
                st.session_state.search_end_date = search_end_date

                # Validation
                if search_start_date >= search_end_date:
                    st.error("⚠️ Check-out date must be after check-in date.")
                else:
                    # Animated search
                    with st.spinner("🔍 Searching our database for the perfect venues..."):
                        time.sleep(1)  # Dramatic effect
                        db_results = fetch_hotels_from_db(
                            location_filter=search_location if search_location else None,
                            budget_filter=search_budget
                        )
                    
                    # Fallback to sample data if database fetch fails
                    if db_results:
                        results = db_results
                        data_source = "database"
                    else:
                        results = [
                            h for h in SAMPLE_HOTELS 
                            if h["price_per_night"] <= search_budget and 
                            (not search_location or 
                             search_location.lower() in h["location"].lower() or 
                             search_location.lower() in h["state"].lower() or
                             h["state"].lower() == search_location.lower())
                        ]
                        data_source = "sample"

                    if results:
                        st.session_state.search_results = results
                        st.success(f"🎉 Found {len(results)} amazing hotels for you!")
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("### 🏨 Available Hotels")
                        st.caption(f"Showing results from: {data_source}")

                        for i, hotel in enumerate(results, 1):
                            col1, col2 = st.columns([4, 1])
                            with col1:
                                display_hotel_card(hotel, i)
                            with col2:
                                st.markdown("<br><br>", unsafe_allow_html=True)
                                if st.button(f"Select →", key=f"select_{i}", use_container_width=True, type="primary"):
                                    st.session_state.selected_hotel = hotel
                                    st.session_state.page = "Comparison"
                                    st.rerun()
                    else:
                        st.warning("❌ No hotels found matching your criteria. Try adjusting your budget or location!")
                        st.info("💡 Tip: Try searching for states like 'CA', 'NY', 'FL', or cities like 'Miami', 'New York'.")

# ============================================================
# PAGE 3: HOTEL COMPARISON
# ============================================================

elif st.session_state.page == "Comparison":
    st.markdown("""
    <div class="main-header">
        <h1>📊 Compare & Choose Your Venue</h1>
        <p>Side-by-side comparison to help you make the perfect choice</p>
    </div>
    """, unsafe_allow_html=True)
    
    show_step_indicator("Comparison")
    show_progress_bar("Comparison")

    if not st.session_state.user_name:
        st.warning("⚠️ Please complete your User Information first!")
    elif not st.session_state.search_results:
        st.warning("⚠️ Please perform a hotel search first!")
    else:
        st.markdown("<br>", unsafe_allow_html=True)

        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(st.session_state.search_results)}</div>
                <div class="stat-label">Hotels Available</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_price = sum(h['price_per_night'] for h in st.session_state.search_results[:10]) / min(10, len(st.session_state.search_results))
            st.markdown(f"""
            <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <div class="stat-number">${avg_price:.0f}</div>
                <div class="stat-label">Avg. Price</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_rating = sum(h['rating'] for h in st.session_state.search_results[:10]) / min(10, len(st.session_state.search_results))
            st.markdown(f"""
            <div class="stat-card" style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);">
                <div class="stat-number">{avg_rating:.1f}</div>
                <div class="stat-label">Avg. Rating</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            total_rooms = sum(h['rooms'] for h in st.session_state.search_results[:10])
            st.markdown(f"""
            <div class="stat-card" style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);">
                <div class="stat-number">{total_rooms}</div>
                <div class="stat-label">Total Rooms</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Comparison table
        st.markdown("### 📋 Detailed Comparison")
        comparison_data = []
        for hotel in st.session_state.search_results[:10]:
            comparison_data.append({
                "Hotel Name": hotel["name"],
                "Location": hotel["location"],
                "Rating": f"⭐ {hotel['rating']}/5",
                "Price/Night": f"${hotel['price_per_night']:.0f}",
                "Rooms": hotel["rooms"],
                "Category": hotel["category"]
            })

        if comparison_data:
            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True, height=400)

            st.markdown("<br>", unsafe_allow_html=True)
            
            # Visual Charts
            st.markdown("### 📈 Visual Insights")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 💵 Price Distribution")
                price_df = pd.DataFrame({
                    "Hotel": [h["name"][:25] + "..." if len(h["name"]) > 25 else h["name"] for h in st.session_state.search_results[:10]],
                    "Price ($)": [h["price_per_night"] for h in st.session_state.search_results[:10]]
                })
                st.bar_chart(price_df.set_index("Hotel"), use_container_width=True, height=300)

            with col2:
                st.markdown("#### ⭐ Rating Comparison")
                rating_df = pd.DataFrame({
                    "Hotel": [h["name"][:25] + "..." if len(h["name"]) > 25 else h["name"] for h in st.session_state.search_results[:10]],
                    "Rating": [h["rating"] for h in st.session_state.search_results[:10]]
                })
                st.bar_chart(rating_df.set_index("Hotel"), use_container_width=True, height=300)

            st.markdown("<br>", unsafe_allow_html=True)

            # Hotel Selection
            st.markdown("### 🎯 Make Your Selection")
            hotel_options = [f"{h['name']} - ${h['price_per_night']:.0f}/night (⭐ {h['rating']}/5)" 
                           for h in st.session_state.search_results[:10]]
            
            selected_idx = st.selectbox(
                "Choose your preferred hotel:",
                range(len(hotel_options)),
                format_func=lambda x: hotel_options[x],
                help="Select the hotel you'd like to book"
            )
            
            # Show selected hotel details
            if selected_idx is not None:
                selected_hotel = st.session_state.search_results[selected_idx]
                st.markdown("<br>", unsafe_allow_html=True)
                display_hotel_card(selected_hotel, selected_idx + 1)
            
            st.markdown("<br>", unsafe_allow_html=True)

            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button("✓ Confirm Selection & Proceed to Booking", use_container_width=True, key="confirm_hotel", type="primary"):
                    st.session_state.selected_hotel = st.session_state.search_results[selected_idx]
                    with st.spinner("Preparing your booking..."):
                        time.sleep(0.5)
                    st.success("Perfect choice! Let's finalize your booking.")
                    time.sleep(1)
                    st.session_state.page = "Booking Confirmation"
                    st.rerun()
            
            with col2:
                if st.button("← Back to Search", use_container_width=True, key="back_to_search"):
                    st.session_state.page = "Hotel Search"
                    st.rerun()

# ============================================================
# PAGE 4: BOOKING CONFIRMATION
# ============================================================

elif st.session_state.page == "Booking Confirmation":
    st.markdown("""
    <div class="main-header">
        <h1>🎉 Finalize Your Dream Wedding Venue</h1>
        <p>You're just one step away from securing your perfect location!</p>
    </div>
    """, unsafe_allow_html=True)
    
    show_step_indicator("Booking Confirmation")
    show_progress_bar("Booking Confirmation")

    if not st.session_state.user_name or not st.session_state.selected_hotel:
        st.warning("⚠️ Please complete the previous steps first!")
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Booking Summary in Beautiful Cards
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 2rem; border-radius: 15px; color: white; box-shadow: 0 5px 20px rgba(0,0,0,0.2);">
                <h3 style="margin-top: 0; color: white;">👤 Guest Information</h3>
            """, unsafe_allow_html=True)
            st.markdown(f"""
                <p style="margin: 0.5rem 0;"><strong>Name:</strong> {st.session_state.user_name}</p>
                <p style="margin: 0.5rem 0;"><strong>Email:</strong> {st.session_state.user_email}</p>
                <p style="margin: 0.5rem 0;"><strong>Phone:</strong> {st.session_state.user_phone}</p>
                <p style="margin: 0.5rem 0;"><strong>Role:</strong> {st.session_state.user_role}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            hotel = st.session_state.selected_hotel
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 2rem; border-radius: 15px; color: white; box-shadow: 0 5px 20px rgba(0,0,0,0.2);">
                <h3 style="margin-top: 0; color: white;">🏨 Hotel Details</h3>
            """, unsafe_allow_html=True)
            st.markdown(f"""
                <p style="margin: 0.5rem 0;"><strong>Hotel:</strong> {hotel['name']}</p>
                <p style="margin: 0.5rem 0;"><strong>Location:</strong> {hotel['location']}</p>
                <p style="margin: 0.5rem 0;"><strong>Category:</strong> {hotel['category']}</p>
                <p style="margin: 0.5rem 0;"><strong>Rating:</strong> ⭐ {hotel['rating']}/5</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Dates and Pricing in Cards
        col1, col2 = st.columns(2)

        with col1:
            check_in = st.session_state.search_start_date
            check_out = st.session_state.search_end_date
            nights = (check_out - check_in).days
            
            st.markdown("""
            <div style="background: white; padding: 2rem; border-radius: 15px; 
                        box-shadow: 0 5px 20px rgba(0,0,0,0.1); border-left: 5px solid #667eea;">
                <h3 style="color: #667eea; margin-top: 0;">📅 Booking Dates</h3>
            """, unsafe_allow_html=True)
            st.markdown(f"""
                <p style="margin: 0.5rem 0;"><strong>Check-in:</strong> {check_in.strftime('%B %d, %Y')}</p>
                <p style="margin: 0.5rem 0;"><strong>Check-out:</strong> {check_out.strftime('%B %d, %Y')}</p>
                <p style="margin: 0.5rem 0;"><strong>Total Nights:</strong> {nights} night{'s' if nights != 1 else ''}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            price_per_night = hotel["price_per_night"]
            subtotal = price_per_night * nights
            tax = subtotal * 0.10
            total = subtotal + tax
            
            st.markdown("""
            <div style="background: white; padding: 2rem; border-radius: 15px; 
                        box-shadow: 0 5px 20px rgba(0,0,0,0.1); border-left: 5px solid #f5576c;">
                <h3 style="color: #f5576c; margin-top: 0;">💰 Pricing Breakdown</h3>
            """, unsafe_allow_html=True)
            st.markdown(f"""
                <p style="margin: 0.5rem 0;"><strong>Rate/Night:</strong> ${price_per_night:.2f}</p>
                <p style="margin: 0.5rem 0;"><strong>Subtotal ({nights} nights):</strong> ${subtotal:,.2f}</p>
                <p style="margin: 0.5rem 0;"><strong>Tax (10%):</strong> ${tax:,.2f}</p>
                <hr style="border: 1px solid #f5576c; margin: 1rem 0;">
                <p style="margin: 0.5rem 0; font-size: 1.3rem;"><strong>Total:</strong> 
                   <span style="color: #f5576c; font-weight: bold;">${total:,.2f}</span></p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

        # Action Buttons
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            if st.button("🎉 Confirm Booking", use_container_width=True, key="confirm_booking", type="primary"):
                with st.spinner("Processing your booking..."):
                    time.sleep(1.5)
                    confirmation_number = f"WED{st.session_state.user_name[:3].upper()}{hash(st.session_state.selected_hotel['name']) % 10000:04d}"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); 
                            padding: 2rem; border-radius: 15px; color: white; 
                            text-align: center; box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4);
                            animation: fadeIn 0.5s ease-in;">
                    <h2 style="color: white; margin: 0;">🎊 Booking Confirmed!</h2>
                    <p style="font-size: 1.2rem; margin: 1rem 0;">Your dream venue is secured!</p>
                    <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin-top: 1rem;">
                        <p style="margin: 0; font-size: 0.9rem;">Confirmation Number:</p>
                        <p style="font-size: 1.8rem; font-weight: bold; margin: 0.5rem 0; letter-spacing: 2px;">
                            {confirmation_number}
                        </p>
                    </div>
                    <p style="margin-top: 1rem; font-size: 0.9rem;">
                        📧 A confirmation email has been sent to {st.session_state.user_email}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                st.balloons()
                st.session_state.booking_confirmed = True
                
        with col2:
            if st.button("↻ Start New Search", use_container_width=True, key="new_search"):
                st.session_state.page = "Hotel Search"
                st.session_state.selected_hotel = None
                st.session_state.search_results = []
                st.rerun()
        
        with col3:
            if st.button("← Back", use_container_width=True, key="back_to_comparison"):
                st.session_state.page = "Comparison"
                st.rerun()