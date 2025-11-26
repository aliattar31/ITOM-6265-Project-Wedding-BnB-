"""
Wedding Destination Hotel Finder - Demo Dashboard
Streamlit Application (Single File)
Version 2.1 - Fixed and Enhanced
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import mysql.connector
from mysql.connector import Error

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Wedding Hotel Amazing Finder",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

st.sidebar.title("💍 Navigation")
st.sidebar.write("---")

pages = ["User Info", "Hotel Search", "Comparison", "Booking Confirmation"]
selected_page = st.sidebar.radio("Select a Page:", pages)
st.session_state.page = selected_page

# Show user info in sidebar if available
if st.session_state.user_name:
    st.sidebar.write("---")
    st.sidebar.subheader("👤 Current User")
    st.sidebar.write(f"**Name:** {st.session_state.user_name}")
    st.sidebar.write(f"**Email:** {st.session_state.user_email}")
    st.sidebar.write(f"**Role:** {st.session_state.user_role}")

# ============================================================
# PAGE 1: USER INFORMATION
# ============================================================

if st.session_state.page == "User Info":
    st.title("👤 User Information")
    st.write("Please enter your basic information to get started.")
    st.write("---")

    col1, col2 = st.columns(2)

    with col1:
        user_name = st.text_input(
            "Full Name",
            value=st.session_state.user_name,
            placeholder="John Doe"
        )

    with col2:
        user_email = st.text_input(
            "Email Address",
            value=st.session_state.user_email,
            placeholder="john@example.com"
        )

    col1, col2 = st.columns(2)

    with col1:
        user_phone = st.text_input(
            "Phone Number",
            value=st.session_state.user_phone,
            placeholder="+1 (555) 123-4567"
        )

    with col2:
        user_role = st.selectbox(
            "Role",
            ["Customer", "Wedding Planner"],
            index=0 if st.session_state.user_role == "Customer" else 1
        )

    st.write("---")

    if st.button("✓ Submit & Continue to Search", use_container_width=True, key="submit_user"):
        if user_name and user_email and user_phone:
            st.session_state.user_name = user_name
            st.session_state.user_email = user_email
            st.session_state.user_phone = user_phone
            st.session_state.user_role = user_role
            st.session_state.page = "Hotel Search"
            st.success("✓ Information saved successfully!")
            st.balloons()
            st.rerun()
        else:
            st.error("⚠️ Please fill in all fields.")

# ============================================================
# PAGE 2: HOTEL SEARCH
# ============================================================

elif st.session_state.page == "Hotel Search":
    st.title("🔍 Hotel Search Engine")

    if not st.session_state.user_name:
        st.warning("⚠️ Please complete your User Information first!")
        if st.button("Go to User Info"):
            st.session_state.page = "User Info"
            st.rerun()
    else:
        st.write("Find your perfect destination wedding hotel across the USA.")
        st.write("---")

        col1, col2 = st.columns(2)

        with col1:
            search_location = st.text_input(
                "Location (City, State or State Abbreviation)",
                value=st.session_state.search_location,
                placeholder="e.g., Hawaii, Miami, Maui, CA, TX"
            )

        with col2:
            search_budget = st.number_input(
                "Budget (per night in USD)",
                min_value=100,
                max_value=10000,
                value=st.session_state.search_budget,
                step=50
            )

        col1, col2 = st.columns(2)

        with col1:
            search_start_date = st.date_input(
                "Check-in Date",
                value=st.session_state.search_start_date
            )

        with col2:
            search_end_date = st.date_input(
                "Check-out Date",
                value=st.session_state.search_end_date
            )

        st.write("---")

        if st.button("🔍 Search Hotels", use_container_width=True, key="search_button"):
            st.session_state.search_location = search_location
            st.session_state.search_budget = search_budget
            st.session_state.search_start_date = search_start_date
            st.session_state.search_end_date = search_end_date

            # Validation
            if search_start_date >= search_end_date:
                st.error("⚠️ Check-out date must be after check-in date.")
            else:
                # Fetch hotels from MySQL database
                with st.spinner("🔍 Searching database for matching hotels..."):
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
                    st.success(f"✓ Found {len(results)} hotels matching your criteria! (Source: {data_source})")
                    st.write("---")
                    st.subheader("Search Results")

                    for i, hotel in enumerate(results, 1):
                        col1, col2, col3 = st.columns([2.5, 0.5, 1])
                        with col1:
                            st.write(f"**{i}. {hotel['name']}**")
                            st.write(f"📍 {hotel['location']} | **${hotel['price_per_night']:.2f}/night**")
                            st.write(f"⭐ Rating: {hotel['rating']}/5 | 🏨 {hotel['rooms']} rooms")
                            if hotel.get('amenities'):
                                amenities_display = hotel['amenities'][:100]
                                if len(hotel['amenities']) > 100:
                                    amenities_display += "..."
                                st.write(f"✨ {amenities_display}")
                        with col3:
                            if st.button(f"Select →", key=f"select_{i}", use_container_width=True):
                                st.session_state.selected_hotel = hotel
                                st.session_state.page = "Comparison"
                                st.rerun()
                else:
                    st.warning("❌ No hotels found matching your criteria. Try adjusting your budget or location!")

# ============================================================
# PAGE 3: HOTEL COMPARISON
# ============================================================

elif st.session_state.page == "Comparison":
    st.title("🏨 Hotel Comparison & Selection")

    if not st.session_state.user_name:
        st.warning("⚠️ Please complete your User Information first!")
    elif not st.session_state.search_results:
        st.warning("⚠️ Please perform a hotel search first!")
    else:
        st.write("Compare hotels and select your preferred venue.")
        st.write("---")

        # Create comparison dataframe
        comparison_data = []
        for hotel in st.session_state.search_results[:10]:  # Show top 10
            comparison_data.append({
                "Hotel Name": hotel["name"],
                "Location": hotel["location"],
                "Rating": f"{hotel['rating']}/5",
                "Price/Night": f"${hotel['price_per_night']}",
                "Rooms": hotel["rooms"],
                "Category": hotel["category"]
            })

        if comparison_data:
            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True)

            st.write("---")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Price Comparison")
                price_df = pd.DataFrame({
                    "Hotel": [h["name"][:20] for h in st.session_state.search_results[:10]],
                    "Price": [h["price_per_night"] for h in st.session_state.search_results[:10]]
                })
                st.bar_chart(price_df.set_index("Hotel"))

            with col2:
                st.subheader("Rating Comparison")
                rating_df = pd.DataFrame({
                    "Hotel": [h["name"][:20] for h in st.session_state.search_results[:10]],
                    "Rating": [h["rating"] for h in st.session_state.search_results[:10]]
                })
                st.bar_chart(rating_df.set_index("Hotel"))

            st.write("---")

            # Selection
            st.subheader("Select Your Hotel")
            hotel_names = [f"{h['name']} - ${h['price_per_night']}/night" for h in st.session_state.search_results[:10]]
            selected_idx = st.selectbox("Choose a hotel:", range(len(hotel_names)), format_func=lambda x: hotel_names[x])

            if st.button("✓ Confirm Selection & Proceed to Booking", use_container_width=True, key="confirm_hotel"):
                st.session_state.selected_hotel = st.session_state.search_results[selected_idx]
                st.session_state.page = "Booking Confirmation"
                st.rerun()

# ============================================================
# PAGE 4: BOOKING CONFIRMATION
# ============================================================

elif st.session_state.page == "Booking Confirmation":
    st.title("✓ Booking Confirmation")

    if not st.session_state.user_name or not st.session_state.selected_hotel:
        st.warning("⚠️ Please complete the previous steps first!")
    else:
        st.write("Review and confirm your booking details.")
        st.write("---")

        # User & Hotel Summary
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("👤 Guest Information")
            st.write(f"**Name:** {st.session_state.user_name}")
            st.write(f"**Email:** {st.session_state.user_email}")
            st.write(f"**Phone:** {st.session_state.user_phone}")
            st.write(f"**Role:** {st.session_state.user_role}")

        with col2:
            st.subheader("🏨 Hotel Details")
            hotel = st.session_state.selected_hotel
            st.write(f"**Hotel:** {hotel['name']}")
            st.write(f"**Location:** {hotel['location']}")
            st.write(f"**Category:** {hotel['category']}")
            st.write(f"**Rating:** ⭐ {hotel['rating']}/5")

        st.write("---")

        # Booking Dates & Pricing
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📅 Booking Dates")
            check_in = st.session_state.search_start_date
            check_out = st.session_state.search_end_date
            nights = (check_out - check_in).days
            st.write(f"**Check-in:** {check_in.strftime('%b %d, %Y')}")
            st.write(f"**Check-out:** {check_out.strftime('%b %d, %Y')}")
            st.write(f"**Total Nights:** {nights}")

        with col2:
            st.subheader("💰 Pricing Breakdown")
            price_per_night = hotel["price_per_night"]
            subtotal = price_per_night * nights
            tax = subtotal * 0.10
            total = subtotal + tax
            st.write(f"**Rate/Night:** ${price_per_night}")
            st.write(f"**Subtotal:** ${subtotal:,.2f}")
            st.write(f"**Tax (10%):** ${tax:,.2f}")
            st.write(f"**Total:** ${total:,.2f}")

        st.write("---")

        # Booking confirmation
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("✓ Confirm Booking", use_container_width=True, key="confirm_booking"):
                confirmation_number = f"WED-{st.session_state.user_name[:3].upper()}-{hash(st.session_state.selected_hotel['name']) % 10000:04d}"
                st.success(f"🎉 **Booking Confirmed!** Confirmation #: {confirmation_number}")
                st.balloons()
                st.session_state.booking_confirmed = True
                
        with col2:
            if st.button("↻ New Search", use_container_width=True, key="new_search"):
                st.session_state.page = "Hotel Search"
                st.session_state.selected_hotel = None
                st.session_state.search_results = []
                st.rerun()