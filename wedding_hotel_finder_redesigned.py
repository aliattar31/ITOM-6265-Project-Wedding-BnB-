"""
Wedding Destination Hotel Finder - Premium Edition
Streamlit Application with Modern UI Design
Version 3.0 - Complete Redesign
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import mysql.connector
from mysql.connector import Error
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Wedding Venue Finder",
    page_icon="💒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS FOR BEAUTIFUL STYLING
# ============================================================

st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #D4AF37;
        --secondary-color: #8B7355;
        --accent-color: #FFE4E1;
        --text-dark: #2C3E50;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #FFF5F5 0%, #FFE4E1 100%);
    }
    
    /* Custom header styling */
    .custom-header {
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    
    .custom-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .custom-header p {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        opacity: 0.95;
    }
    
    /* Hotel card styling */
    .hotel-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 5px solid #D4AF37;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .hotel-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(212,175,55,0.3);
    }
    
    .hotel-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2C3E50;
        margin-bottom: 0.5rem;
    }
    
    .hotel-location {
        color: #7F8C8D;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .hotel-price {
        font-size: 1.8rem;
        font-weight: 700;
        color: #D4AF37;
        margin: 0.5rem 0;
    }
    
    .hotel-rating {
        display: inline-block;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    /* Info box styling */
    .info-box {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 15px rgba(0,0,0,0.06);
        border-top: 4px solid #D4AF37;
    }
    
    .info-box h3 {
        color: #2C3E50;
        margin-top: 0;
        font-size: 1.3rem;
    }
    
    /* Stats card */
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .stats-label {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(212,175,55,0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(212,175,55,0.4);
    }
    
    /* Progress step indicator */
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
        padding: 0;
    }
    
    .step {
        flex: 1;
        text-align: center;
        padding: 1rem;
        background: white;
        margin: 0 0.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .step.active {
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%);
        color: white;
        font-weight: 700;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2C3E50 0%, #34495E 100%);
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    .badge-luxury {
        background: linear-gradient(135deg, #8B7355 0%, #6B5745 100%);
        color: white;
    }
    
    .badge-popular {
        background: linear-gradient(135deg, #FF6B6B 0%, #EE5A6F 100%);
        color: white;
    }
    
    .badge-featured {
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATABASE CONNECTION
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
        st.error(f"❌ Database connection error: {e}")
        return None

@st.cache_data(ttl=3600)
def fetch_hotels_from_db(location_filter=None, budget_filter=None, min_rating=None):
    """Fetch hotels from MySQL database with enhanced filtering"""
    connection = get_db_connection()
    if connection is None:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        
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
            h.Description,
            COALESCE(AVG(r.BasePrice), 300) as price_per_night,
            COALESCE(COUNT(DISTINCT r.RoomID), 0) as rooms,
            GROUP_CONCAT(DISTINCT a.AmenityName SEPARATOR ', ') as amenities,
            h.StarRating,
            h.TotalRooms
        FROM HOTEL h
        LEFT JOIN ROOM r ON h.HotelID = r.HotelID AND r.RoomStatus = 'Available'
        LEFT JOIN HOTELAMENITIES ha ON h.HotelID = ha.HotelID
        LEFT JOIN AMENITIES a ON ha.AmenityID = a.AmenityID
        WHERE 1=1
        """
        
        params = []
        
        if location_filter and location_filter.strip():
            location_filter_lower = location_filter.lower().strip()
            query += " AND (LOWER(h.City) LIKE %s OR LOWER(h.State) = %s)"
            params.extend([f"%{location_filter_lower}%", location_filter_lower])
        
        query += """ GROUP BY h.HotelID, h.HotelName, h.City, h.State, 
                     h.PhoneNumber, h.Email, h.Website, h.StreetAddress, 
                     h.AverageRating, h.StarRating, h.Description, h.TotalRooms"""
        
        if budget_filter:
            query += " HAVING COALESCE(AVG(r.BasePrice), 300) <= %s"
            params.append(budget_filter)
        
        if min_rating:
            query += " AND h.AverageRating >= %s" if not budget_filter else " AND h.AverageRating >= %s"
            params.append(min_rating)
        
        query += " ORDER BY h.AverageRating DESC, h.StarRating DESC LIMIT 100"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        hotels = []
        for row in results:
            hotels.append({
                "hotel_id": row.get("HotelID"),
                "name": row.get("name", ""),
                "location": row.get("location", ""),
                "city": row.get("City", ""),
                "state": row.get("State", ""),
                "rating": float(row.get("rating", 4.5)) if row.get("rating") else 4.5,
                "price_per_night": float(row.get("price_per_night", 300)) if row.get("price_per_night") else 300,
                "rooms": int(row.get("rooms", 0)) if row.get("rooms") else 0,
                "total_rooms": int(row.get("TotalRooms", 0)) if row.get("TotalRooms") else 0,
                "amenities": row.get("amenities", "Amenities available"),
                "category": f"{row.get('StarRating', 4)}-Star Hotel" if row.get("StarRating") else "Luxury Hotel",
                "star_rating": row.get('StarRating', 4),
                "phone": row.get("phone", ""),
                "email": row.get("email", ""),
                "website": row.get("website", ""),
                "address": row.get("address", ""),
                "description": row.get("Description", "Beautiful venue for your special day")
            })
        
        cursor.close()
        return hotels
        
    except Error as e:
        st.error(f"❌ Error fetching hotels: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            connection.close()

@st.cache_data(ttl=3600)
def get_location_stats():
    """Get statistics about available locations"""
    connection = get_db_connection()
    if connection is None:
        return {}
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                State,
                COUNT(*) as hotel_count,
                AVG(AverageRating) as avg_rating,
                MIN(AverageRating) as min_rating,
                MAX(AverageRating) as max_rating
            FROM HOTEL
            GROUP BY State
            ORDER BY hotel_count DESC
        """)
        results = cursor.fetchall()
        cursor.close()
        return {row['State']: row for row in results}
    except Error as e:
        return {}
    finally:
        if connection and connection.is_connected():
            connection.close()

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "user_phone" not in st.session_state:
    st.session_state.user_phone = ""

if "user_role" not in st.session_state:
    st.session_state.user_role = "Couple"

if "search_location" not in st.session_state:
    st.session_state.search_location = ""

if "search_budget" not in st.session_state:
    st.session_state.search_budget = 500

if "min_rating" not in st.session_state:
    st.session_state.min_rating = 4.0

if "search_start_date" not in st.session_state:
    st.session_state.search_start_date = datetime.now().date() + timedelta(days=180)

if "search_end_date" not in st.session_state:
    st.session_state.search_end_date = datetime.now().date() + timedelta(days=183)

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "selected_hotel" not in st.session_state:
    st.session_state.selected_hotel = None

if "booking_confirmed" not in st.session_state:
    st.session_state.booking_confirmed = False

if "guest_count" not in st.session_state:
    st.session_state.guest_count = 50

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    st.markdown("### 💒 Wedding Venue Finder")
    st.markdown("---")
    
    # Progress indicator
    pages = ["Home", "Search", "Results", "Details", "Booking"]
    current_page_idx = pages.index(st.session_state.page) if st.session_state.page in pages else 0
    
    st.markdown("#### 📍 Your Journey")
    for idx, page in enumerate(pages):
        if idx < current_page_idx:
            st.markdown(f"✅ {page}")
        elif idx == current_page_idx:
            st.markdown(f"**➡️ {page}**")
        else:
            st.markdown(f"⚪ {page}")
    
    st.markdown("---")
    
    # Navigation buttons
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"
        st.rerun()
    
    if st.button("🔍 Search Hotels", use_container_width=True):
        st.session_state.page = "Search"
        st.rerun()
    
    if st.session_state.search_results and st.button("📋 View Results", use_container_width=True):
        st.session_state.page = "Results"
        st.rerun()
    
    if st.session_state.selected_hotel and st.button("🏨 Hotel Details", use_container_width=True):
        st.session_state.page = "Details"
        st.rerun()
    
    if st.session_state.selected_hotel and st.button("✓ Book Now", use_container_width=True):
        st.session_state.page = "Booking"
        st.rerun()
    
    st.markdown("---")
    st.markdown("#### 👤 User Info")
    if st.session_state.user_name:
        st.success(f"**{st.session_state.user_name}**")
        st.caption(f"📧 {st.session_state.user_email}")
    else:
        st.info("Not logged in")

# ============================================================
# PAGE 1: HOME / LANDING
# ============================================================

if st.session_state.page == "Home":
    # Hero header
    st.markdown("""
    <div class="custom-header">
        <h1>💒 Find Your Perfect Wedding Venue</h1>
        <p>Discover stunning hotels for your dream destination wedding</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### ✨ Welcome to Your Wedding Journey")
        st.markdown("""
        Start planning your perfect day by finding the ideal venue that matches your vision. 
        Whether you're dreaming of a beachfront ceremony or an elegant ballroom celebration, 
        we'll help you find the perfect setting.
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Stats section
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stats-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div class="stats-number">46+</div>
            <div class="stats-label">Premium Hotels</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="stats-number">20+</div>
            <div class="stats-label">US Cities</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="stats-number">136+</div>
            <div class="stats-label">Luxury Rooms</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stats-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <div class="stats-number">4.8★</div>
            <div class="stats-label">Avg Rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # User information section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h3>👤 Tell Us About You</h3>
        </div>
        """, unsafe_allow_html=True)
        
        name = st.text_input("Full Name *", value=st.session_state.user_name, placeholder="Enter your full name")
        email = st.text_input("Email Address *", value=st.session_state.user_email, placeholder="your@email.com")
        phone = st.text_input("Phone Number", value=st.session_state.user_phone, placeholder="+1 (555) 123-4567")
        role = st.selectbox("I am a...", ["Couple", "Wedding Planner", "Hotel Admin", "Event Organizer"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("✓ Continue to Search", use_container_width=True, type="primary"):
            if name and email:
                st.session_state.user_name = name
                st.session_state.user_email = email
                st.session_state.user_phone = phone
                st.session_state.user_role = role
                st.session_state.page = "Search"
                st.success("✓ Profile saved! Redirecting to search...")
                st.rerun()
            else:
                st.error("❌ Please fill in your name and email to continue")
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h3>🎯 What Makes Us Special</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        #### ✨ Curated Selection
        Hand-picked venues perfect for weddings and special celebrations
        
        #### 💰 Transparent Pricing
        No hidden fees - see complete pricing breakdown upfront
        
        #### ⭐ Verified Reviews
        Real ratings from couples who celebrated their special day
        
        #### 🎪 Complete Amenities
        From catering to coordination, find venues with everything you need
        
        #### 📞 Direct Contact
        Connect directly with hotel coordinators for personalized service
        """)

# ============================================================
# PAGE 2: SEARCH
# ============================================================

elif st.session_state.page == "Search":
    st.markdown("""
    <div class="custom-header">
        <h1>🔍 Search Your Dream Venue</h1>
        <p>Filter by location, budget, and preferences</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.user_name:
        st.warning("⚠️ Please complete your profile on the Home page first")
        if st.button("← Back to Home"):
            st.session_state.page = "Home"
            st.rerun()
    else:
        st.markdown(f"### 👋 Welcome back, {st.session_state.user_name}!")
        st.markdown("---")
        
        # Search filters in elegant layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div class="info-box">
                <h3>📍 Location & Budget</h3>
            </div>
            """, unsafe_allow_html=True)
            
            location = st.text_input(
                "Destination City or State",
                value=st.session_state.search_location,
                placeholder="e.g., Hawaii, Miami, New York, CA",
                help="Search by city name or state abbreviation"
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                budget = st.slider(
                    "Maximum Price per Night",
                    min_value=100,
                    max_value=1000,
                    value=st.session_state.search_budget,
                    step=50,
                    format="$%d"
                )
            
            with col_b:
                min_rating = st.slider(
                    "Minimum Rating",
                    min_value=1.0,
                    max_value=5.0,
                    value=st.session_state.min_rating,
                    step=0.5,
                    format="%.1f ⭐"
                )
        
        with col2:
            st.markdown("""
            <div class="info-box">
                <h3>📅 Event Details</h3>
            </div>
            """, unsafe_allow_html=True)
            
            start_date = st.date_input(
                "Check-in Date",
                value=st.session_state.search_start_date,
                min_value=datetime.now().date()
            )
            
            end_date = st.date_input(
                "Check-out Date",
                value=st.session_state.search_end_date,
                min_value=start_date
            )
            
            guest_count = st.number_input(
                "Expected Guests",
                min_value=10,
                max_value=500,
                value=st.session_state.guest_count,
                step=10
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Search button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔍 Search Hotels", use_container_width=True, type="primary"):
                with st.spinner("🔎 Searching for your perfect venue..."):
                    st.session_state.search_location = location
                    st.session_state.search_budget = budget
                    st.session_state.min_rating = min_rating
                    st.session_state.search_start_date = start_date
                    st.session_state.search_end_date = end_date
                    st.session_state.guest_count = guest_count
                    
                    # Fetch from database
                    results = fetch_hotels_from_db(
                        location_filter=location if location else None,
                        budget_filter=budget,
                        min_rating=min_rating
                    )
                    
                    if results:
                        st.session_state.search_results = results
                        st.success(f"✓ Found {len(results)} amazing venues!")
                        st.session_state.page = "Results"
                        st.rerun()
                    else:
                        st.warning("❌ No venues found. Try adjusting your filters.")

# ============================================================
# PAGE 3: RESULTS
# ============================================================

elif st.session_state.page == "Results":
    st.markdown("""
    <div class="custom-header">
        <h1>🏨 Available Venues</h1>
        <p>Browse through our curated selection</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.search_results:
        st.warning("⚠️ No search results found. Please perform a search first.")
        if st.button("← Back to Search"):
            st.session_state.page = "Search"
            st.rerun()
    else:
        # Results summary
        st.markdown(f"### 📊 Found {len(st.session_state.search_results)} Venues")
        st.markdown(f"**Location:** {st.session_state.search_location or 'All Locations'} | **Budget:** ${st.session_state.search_budget}/night | **Rating:** {st.session_state.min_rating}+ ⭐")
        st.markdown("---")
        
        # Filter and sort options
        col1, col2, col3 = st.columns(3)
        with col1:
            sort_by = st.selectbox("Sort by", ["Highest Rated", "Lowest Price", "Highest Price", "Most Rooms"])
        with col2:
            view_mode = st.radio("View", ["Grid", "List"], horizontal=True)
        with col3:
            results_per_page = st.selectbox("Show", [10, 20, 50], index=0)
        
        # Sort results
        results = st.session_state.search_results.copy()
        if sort_by == "Highest Rated":
            results.sort(key=lambda x: x['rating'], reverse=True)
        elif sort_by == "Lowest Price":
            results.sort(key=lambda x: x['price_per_night'])
        elif sort_by == "Highest Price":
            results.sort(key=lambda x: x['price_per_night'], reverse=True)
        elif sort_by == "Most Rooms":
            results.sort(key=lambda x: x['total_rooms'], reverse=True)
        
        results = results[:results_per_page]
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display results
        if view_mode == "Grid":
            # Grid view - 2 columns
            for i in range(0, len(results), 2):
                cols = st.columns(2)
                for j, col in enumerate(cols):
                    if i + j < len(results):
                        hotel = results[i + j]
                        with col:
                            # Create hotel card
                            st.markdown(f"""
                            <div class="hotel-card">
                                <div class="hotel-name">{hotel['name']}</div>
                                <div class="hotel-location">📍 {hotel['location']}</div>
                                <div style="margin: 0.5rem 0;">
                                    <span class="hotel-rating">⭐ {hotel['rating']}/5.0</span>
                                    <span class="badge badge-luxury">{hotel['category']}</span>
                                </div>
                                <div class="hotel-price">${hotel['price_per_night']:.0f}<span style="font-size: 1rem; color: #7F8C8D;">/night</span></div>
                                <div style="color: #7F8C8D; margin-top: 0.5rem;">
                                    🏨 {hotel['total_rooms']} rooms | 🛏️ {hotel['rooms']} available
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button(f"View Details →", key=f"view_{hotel['hotel_id']}", use_container_width=True):
                                st.session_state.selected_hotel = hotel
                                st.session_state.page = "Details"
                                st.rerun()
        else:
            # List view
            for idx, hotel in enumerate(results, 1):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="hotel-card">
                        <div class="hotel-name">{idx}. {hotel['name']}</div>
                        <div class="hotel-location">📍 {hotel['location']}</div>
                        <div style="margin: 0.5rem 0;">
                            <span class="hotel-rating">⭐ {hotel['rating']}/5.0</span>
                            <span class="badge badge-luxury">{hotel['category']}</span>
                        </div>
                        <div style="color: #7F8C8D; font-size: 0.9rem; margin-top: 0.5rem;">
                            ✨ {hotel['amenities'][:150]}...
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.metric("Price/Night", f"${hotel['price_per_night']:.0f}")
                    st.caption(f"🏨 {hotel['total_rooms']} total rooms")
                
                with col3:
                    st.markdown("<br><br>", unsafe_allow_html=True)
                    if st.button("View Details", key=f"list_view_{hotel['hotel_id']}", use_container_width=True):
                        st.session_state.selected_hotel = hotel
                        st.session_state.page = "Details"
                        st.rerun()

# ============================================================
# PAGE 4: HOTEL DETAILS
# ============================================================

elif st.session_state.page == "Details":
    if not st.session_state.selected_hotel:
        st.warning("⚠️ Please select a hotel first")
        if st.button("← Back to Results"):
            st.session_state.page = "Results"
            st.rerun()
    else:
        hotel = st.session_state.selected_hotel
        
        # Hotel header
        st.markdown(f"""
        <div class="custom-header">
            <h1>{hotel['name']}</h1>
            <p>📍 {hotel['location']} | ⭐ {hotel['rating']}/5.0 Rating</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Back button
        if st.button("← Back to Results"):
            st.session_state.page = "Results"
            st.rerun()
        
        st.markdown("---")
        
        # Hotel details layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Image placeholder
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        height: 300px; border-radius: 15px; display: flex; 
                        align-items: center; justify-content: center; color: white; 
                        font-size: 4rem; box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
                🏨
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Description
            st.markdown("""
            <div class="info-box">
                <h3>📝 About This Venue</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(hotel.get('description', 'A stunning venue perfect for your wedding celebration. Our experienced team will ensure every detail of your special day is perfect.'))
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Amenities
            st.markdown("""
            <div class="info-box">
                <h3>✨ Amenities & Features</h3>
            </div>
            """, unsafe_allow_html=True)
            
            amenities_list = hotel['amenities'].split(', ')
            # Display in columns
            for i in range(0, len(amenities_list), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    if i + j < len(amenities_list):
                        col.markdown(f"✓ {amenities_list[i + j]}")
        
        with col2:
            # Quick info card
            st.markdown("""
            <div class="info-box" style="background: linear-gradient(135deg, #FFE4E1 0%, #FFF5F5 100%);">
                <h3>💰 Pricing & Availability</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.metric("Price per Night", f"${hotel['price_per_night']:.2f}", delta=None)
            st.metric("Available Rooms", hotel['rooms'])
            st.metric("Total Capacity", hotel['total_rooms'])
            st.metric("Star Rating", f"{hotel['star_rating']} ⭐")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Contact info
            st.markdown("""
            <div class="info-box">
                <h3>📞 Contact Information</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if hotel.get('phone'):
                st.markdown(f"**Phone:** {hotel['phone']}")
            if hotel.get('email'):
                st.markdown(f"**Email:** {hotel['email']}")
            if hotel.get('website'):
                st.markdown(f"**Website:** [{hotel['website']}]({hotel['website']})")
            if hotel.get('address'):
                st.markdown(f"**Address:** {hotel['address']}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Book button
            if st.button("✓ Book This Venue", use_container_width=True, type="primary"):
                st.session_state.page = "Booking"
                st.rerun()
        
        st.markdown("---")
        
        # Price comparison chart
        st.markdown("### 📊 Compare with Similar Venues")
        
        # Get comparison data
        comparison_hotels = [h for h in st.session_state.search_results if h['hotel_id'] != hotel['hotel_id']][:5]
        comparison_hotels.insert(0, hotel)
        
        chart_data = pd.DataFrame({
            'Hotel': [h['name'][:25] for h in comparison_hotels],
            'Price': [h['price_per_night'] for h in comparison_hotels],
            'Rating': [h['rating'] for h in comparison_hotels],
            'Selected': ['This Hotel' if h['hotel_id'] == hotel['hotel_id'] else 'Other' for h in comparison_hotels]
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Price comparison
            fig_price = px.bar(
                chart_data,
                x='Hotel',
                y='Price',
                color='Selected',
                title='Price Comparison',
                color_discrete_map={'This Hotel': '#D4AF37', 'Other': '#B8B8B8'}
            )
            fig_price.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig_price, use_container_width=True)
        
        with col2:
            # Rating comparison
            fig_rating = px.bar(
                chart_data,
                x='Hotel',
                y='Rating',
                color='Selected',
                title='Rating Comparison',
                color_discrete_map={'This Hotel': '#FFD700', 'Other': '#B8B8B8'}
            )
            fig_rating.update_layout(showlegend=False, height=300, yaxis_range=[0, 5])
            st.plotly_chart(fig_rating, use_container_width=True)

# ============================================================
# PAGE 5: BOOKING CONFIRMATION
# ============================================================

elif st.session_state.page == "Booking":
    if not st.session_state.selected_hotel:
        st.warning("⚠️ Please select a hotel first")
        if st.button("← Back to Results"):
            st.session_state.page = "Results"
            st.rerun()
    else:
        hotel = st.session_state.selected_hotel
        
        st.markdown("""
        <div class="custom-header">
            <h1>✓ Confirm Your Booking</h1>
            <p>Review all details before confirming</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Summary cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="info-box">
                <h3>👤 Guest Information</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"**Name:** {st.session_state.user_name}")
            st.markdown(f"**Email:** {st.session_state.user_email}")
            st.markdown(f"**Phone:** {st.session_state.user_phone or 'Not provided'}")
            st.markdown(f"**Role:** {st.session_state.user_role}")
            st.markdown(f"**Expected Guests:** {st.session_state.guest_count}")
        
        with col2:
            st.markdown("""
            <div class="info-box">
                <h3>🏨 Venue Details</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"**Venue:** {hotel['name']}")
            st.markdown(f"**Location:** {hotel['location']}")
            st.markdown(f"**Category:** {hotel['category']}")
            st.markdown(f"**Rating:** {hotel['rating']} ⭐")
            st.markdown(f"**Contact:** {hotel.get('phone', 'N/A')}")
        
        st.markdown("---")
        
        # Booking dates and pricing
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="info-box">
                <h3>📅 Event Dates</h3>
            </div>
            """, unsafe_allow_html=True)
            
            check_in = st.session_state.search_start_date
            check_out = st.session_state.search_end_date
            nights = (check_out - check_in).days
            
            st.markdown(f"**Check-in:** {check_in.strftime('%A, %B %d, %Y')}")
            st.markdown(f"**Check-out:** {check_out.strftime('%A, %B %d, %Y')}")
            st.markdown(f"**Total Nights:** {nights}")
            
            # Room selection
            st.markdown("<br>", unsafe_allow_html=True)
            num_rooms = st.number_input(
                "Number of Rooms",
                min_value=1,
                max_value=hotel['rooms'],
                value=min(5, hotel['rooms']),
                help=f"{hotel['rooms']} rooms available"
            )
        
        with col2:
            st.markdown("""
            <div class="info-box" style="background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);">
                <h3>💰 Pricing Breakdown</h3>
            </div>
            """, unsafe_allow_html=True)
            
            price_per_night = hotel["price_per_night"]
            subtotal = price_per_night * nights * num_rooms
            service_fee = subtotal * 0.05
            tax = (subtotal + service_fee) * 0.10
            total = subtotal + service_fee + tax
            
            st.markdown(f"**Room Rate:** ${price_per_night:.2f} × {nights} nights × {num_rooms} rooms")
            st.markdown(f"**Subtotal:** ${subtotal:,.2f}")
            st.markdown(f"**Service Fee (5%):** ${service_fee:,.2f}")
            st.markdown(f"**Tax (10%):** ${tax:,.2f}")
            st.markdown("---")
            st.markdown(f"### **Total Amount:** ${total:,.2f}")
        
        st.markdown("---")
        
        # Special requests
        st.markdown("""
        <div class="info-box">
            <h3>📝 Special Requests (Optional)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        special_requests = st.text_area(
            "Add any special requirements or requests",
            placeholder="e.g., Dietary restrictions, accessibility needs, preferred ceremony location, etc.",
            height=100
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Terms and conditions
        agree_terms = st.checkbox("I agree to the terms and conditions and cancellation policy")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Confirmation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("← Back to Details", use_container_width=True):
                st.session_state.page = "Details"
                st.rerun()
        
        with col2:
            pass  # Empty column for spacing
        
        with col3:
            if st.button("✓ Confirm Booking", use_container_width=True, type="primary", disabled=not agree_terms):
                if agree_terms:
                    # Generate confirmation number
                    confirmation_number = f"WED-{st.session_state.user_name[:3].upper()}-{hash(hotel['name']) % 10000:04d}"
                    
                    st.balloons()
                    
                    st.success(f"""
                    ### 🎉 Booking Confirmed!
                    
                    **Confirmation Number:** `{confirmation_number}`
                    
                    Thank you for booking with us! A confirmation email has been sent to **{st.session_state.user_email}**
                    
                    The venue coordinator will contact you within 24 hours to discuss your special requirements.
                    """)
                    
                    st.session_state.booking_confirmed = True
                    
                    # Summary box
                    st.markdown(f"""
                    <div class="info-box" style="background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%); color: white;">
                        <h3>📋 Booking Summary</h3>
                        <p><strong>Venue:</strong> {hotel['name']}</p>
                        <p><strong>Dates:</strong> {check_in.strftime('%b %d')} - {check_out.strftime('%b %d, %Y')}</p>
                        <p><strong>Rooms:</strong> {num_rooms}</p>
                        <p><strong>Total:</strong> ${total:,.2f}</p>
                        <p><strong>Confirmation:</strong> {confirmation_number}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    if st.button("🏠 Return to Home", use_container_width=True):
                        # Reset for new search
                        st.session_state.selected_hotel = None
                        st.session_state.search_results = []
                        st.session_state.page = "Home"
                        st.rerun()
                else:
                    st.error("Please agree to the terms and conditions to proceed")

# ============================================================
# FOOTER
# ============================================================

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7F8C8D; padding: 2rem;">
    <p>💒 <strong>Wedding Venue Finder</strong> - Making Your Dream Wedding a Reality</p>
    <p style="font-size: 0.9rem;">Questions? Contact us at support@weddingvenues.com | © 2025 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
