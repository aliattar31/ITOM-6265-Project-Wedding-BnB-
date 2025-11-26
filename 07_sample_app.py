"""
Wedding Destination Hotel Finder - Demo Dashboard
Streamlit Application (Single File)
Version 2.0 - Enhanced with Auto-Navigation & 100+ US Hotels
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
            database=st.secrets.get("mysql_database", "wedding_bnb_db"),
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
        
        # Query using actual database structure:
        # HOTEL table - main hotel info
        # ROOM table - room pricing (BasePrice)
        # HOTELAMENITIES table - hotel amenities junction
        # AMENITIES table - amenity names
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
        query += """ GROUP BY h.HotelID, h.HotelName, h.City, h.State, h.PhoneNumber, h.Email, h.Website, h.StreetAddress, h.AverageRating, h.StarRating"""
        
        # Add budget filter to HAVING clause
        if budget_filter:
            query += " HAVING COALESCE(AVG(r.BasePrice), 300) <= %s"
            params.append(budget_filter)
        
        query += " ORDER BY h.AverageRating DESC LIMIT 100"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        # Convert results to list of dictionaries with expected format
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
        if connection.is_connected():
            connection.close()
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
        if connection.is_connected():
            connection.close()

# ============================================================
# FALLBACK SAMPLE DATA - 100+ US HOTELS
# ============================================================

SAMPLE_HOTELS = [
    # Hawaii - Maui (10)
    {"name": "Maui Grand Resort", "location": "Maui, HI", "state": "HI", "rating": 4.8, "price_per_night": 350, "rooms": 150, "amenities": "Ceremony Space, Catering, Coordination", "category": "Beachfront Resort"},
    {"name": "Wailea Beach Resort", "location": "Maui, HI", "state": "HI", "rating": 4.7, "price_per_night": 320, "rooms": 120, "amenities": "Beach Access, Pool, Spa", "category": "Beachfront Resort"},
    {"name": "Maui Sunset Villas", "location": "Maui, HI", "state": "HI", "rating": 4.6, "price_per_night": 280, "rooms": 95, "amenities": "Ocean View, WiFi, Restaurant", "category": "Boutique Hotel"},
    {"name": "Kapalua Bay Resort", "location": "Maui, HI", "state": "HI", "rating": 4.9, "price_per_night": 420, "rooms": 110, "amenities": "Private Beach, Golf, Concierge", "category": "Golf Resort"},
    {"name": "Lahaina Shores Hotel", "location": "Maui, HI", "state": "HI", "rating": 4.5, "price_per_night": 250, "rooms": 200, "amenities": "Beachfront, WiFi, Pool", "category": "Beachfront Resort"},
    {"name": "The Ritz-Carlton Maui", "location": "Maui, HI", "state": "HI", "rating": 4.9, "price_per_night": 580, "rooms": 80, "amenities": "Ultra-Luxury, Spa, Beach Ceremony", "category": "Luxury Resort"},
    {"name": "Hyatt Regency Maui", "location": "Maui, HI", "state": "HI", "rating": 4.7, "price_per_night": 380, "rooms": 160, "amenities": "Beach, Pool, Entertainment", "category": "Beachfront Resort"},
    {"name": "Fairmont Kea Lani", "location": "Maui, HI", "state": "HI", "rating": 4.8, "price_per_night": 500, "rooms": 140, "amenities": "All-Suite, Beach, Spa", "category": "Luxury Resort"},
    {"name": "Sheraton Maui Resort", "location": "Maui, HI", "state": "HI", "rating": 4.6, "price_per_night": 340, "rooms": 170, "amenities": "Beachfront, Pool, Volcano View", "category": "Beachfront Resort"},
    {"name": "Marriott Maui Ocean Club", "location": "Maui, HI", "state": "HI", "rating": 4.5, "price_per_night": 300, "rooms": 190, "amenities": "Beach Access, WiFi, Restaurant", "category": "Beachfront Resort"},
    
    # Hawaii - Honolulu/Oahu (10)
    {"name": "Royal Hawaiian Honolulu", "location": "Honolulu, HI", "state": "HI", "rating": 4.9, "price_per_night": 480, "rooms": 180, "amenities": "Waikiki Beach, Luxury, Fine Dining", "category": "Urban Luxury"},
    {"name": "Hilton Hawaiian Village", "location": "Honolulu, HI", "state": "HI", "rating": 4.7, "price_per_night": 350, "rooms": 300, "amenities": "Beach, Pool, Entertainment", "category": "Beachfront Resort"},
    {"name": "Moana Surfrider Hotel", "location": "Honolulu, HI", "state": "HI", "rating": 4.8, "price_per_night": 410, "rooms": 130, "amenities": "Historic, Beach, Restaurant", "category": "Historic Inn"},
    {"name": "Waikiki Beach Marriott", "location": "Honolulu, HI", "state": "HI", "rating": 4.6, "price_per_night": 380, "rooms": 170, "amenities": "Beach View, Pool, Gym", "category": "Beachfront Resort"},
    {"name": "Outrigger Waikiki Beach", "location": "Honolulu, HI", "state": "HI", "rating": 4.5, "price_per_night": 290, "rooms": 160, "amenities": "Beach, WiFi, Restaurant", "category": "Beachfront Resort"},
    {"name": "The Halekulani", "location": "Honolulu, HI", "state": "HI", "rating": 4.9, "price_per_night": 650, "rooms": 50, "amenities": "Ultra-Luxury, Private Beach", "category": "Luxury Resort"},
    {"name": "Sheraton Waikiki", "location": "Honolulu, HI", "state": "HI", "rating": 4.6, "price_per_night": 320, "rooms": 250, "amenities": "Beachfront, Pool, Entertainment", "category": "Beachfront Resort"},
    {"name": "Grand Wailea Maui", "location": "Wailea, HI", "state": "HI", "rating": 4.7, "price_per_night": 420, "rooms": 200, "amenities": "All-Inclusive, Pool, Spa", "category": "Beachfront Resort"},
    {"name": "Kahala Hotel & Resort", "location": "Honolulu, HI", "state": "HI", "rating": 4.8, "price_per_night": 550, "rooms": 100, "amenities": "Private Beach, Dolphins, Luxury", "category": "Luxury Resort"},
    {"name": "Waikiki Beachcomber by Outrigger", "location": "Honolulu, HI", "state": "HI", "rating": 4.4, "price_per_night": 250, "rooms": 180, "amenities": "Budget Beachfront, Pool", "category": "Beachfront Resort"},
    
    # Florida - Miami (8)
    {"name": "Miami Luxury Downtown", "location": "Miami, FL", "state": "FL", "rating": 4.3, "price_per_night": 400, "rooms": 180, "amenities": "Urban, Rooftop Events, Restaurant", "category": "Urban Luxury"},
    {"name": "Mandarin Oriental Miami", "location": "Miami, FL", "state": "FL", "rating": 4.8, "price_per_night": 550, "rooms": 130, "amenities": "Luxury, Spa, Fine Dining", "category": "Urban Luxury"},
    {"name": "Fontainebleau Miami Beach", "location": "Miami, FL", "state": "FL", "rating": 4.6, "price_per_night": 420, "rooms": 220, "amenities": "Beach, Pool, Entertainment", "category": "Beachfront Resort"},
    {"name": "The Setai Miami Beach", "location": "Miami, FL", "state": "FL", "rating": 4.9, "price_per_night": 680, "rooms": 105, "amenities": "Ultra-Luxury, Spa, Private Beach", "category": "Urban Luxury"},
    {"name": "Betsy Hotel Miami Beach", "location": "Miami, FL", "state": "FL", "rating": 4.7, "price_per_night": 380, "rooms": 50, "amenities": "Boutique, Art Gallery, Restaurant", "category": "Boutique Hotel"},
    {"name": "Four Seasons Miami", "location": "Miami, FL", "state": "FL", "rating": 4.9, "price_per_night": 620, "rooms": 150, "amenities": "Luxury, Bay View, Spa", "category": "Urban Luxury"},
    {"name": "Loews Miami Beach Hotel", "location": "Miami Beach, FL", "state": "FL", "rating": 4.5, "price_per_night": 320, "rooms": 200, "amenities": "Beach, Pool, Family Friendly", "category": "Beachfront Resort"},
    {"name": "Edition Miami Beach", "location": "Miami Beach, FL", "state": "FL", "rating": 4.8, "price_per_night": 580, "rooms": 120, "amenities": "Modern Luxury, Beach, Events", "category": "Urban Luxury"},
    
    # Florida - Key West (6)
    {"name": "Key West Ocean View", "location": "Key West, FL", "state": "FL", "rating": 4.4, "price_per_night": 450, "rooms": 85, "amenities": "Historic Charm, Sunset Venue, WiFi", "category": "Historic Inn"},
    {"name": "Marker Waterfront Resort", "location": "Key West, FL", "state": "FL", "rating": 4.6, "price_per_night": 520, "rooms": 95, "amenities": "Waterfront, Pool, Restaurant", "category": "Beachfront Resort"},
    {"name": "Tropic Cinema Resort", "location": "Key West, FL", "state": "FL", "rating": 4.5, "price_per_night": 380, "rooms": 70, "amenities": "Historic, WiFi, Entertainment", "category": "Historic Inn"},
    {"name": "Sunset Key Guest Cottages", "location": "Key West, FL", "state": "FL", "rating": 4.8, "price_per_night": 650, "rooms": 40, "amenities": "Private Island, Beach, Exclusive", "category": "Villa Resort"},
    {"name": "Hyatt Centric Key West", "location": "Key West, FL", "state": "FL", "rating": 4.6, "price_per_night": 420, "rooms": 80, "amenities": "Modern, Downtown, Beach", "category": "Boutique Hotel"},
    {"name": "The Marker Waterfront", "location": "Key West, FL", "state": "FL", "rating": 4.7, "price_per_night": 500, "rooms": 90, "amenities": "Luxury, Pool, Dining", "category": "Urban Luxury"},
    
    # Florida - Fort Lauderdale & Boca Raton (6)
    {"name": "The Atlantic Resort", "location": "Fort Lauderdale, FL", "state": "FL", "rating": 4.5, "price_per_night": 340, "rooms": 140, "amenities": "Beach, Pool, Spa", "category": "Beachfront Resort"},
    {"name": "Boca Beach Club", "location": "Boca Raton, FL", "state": "FL", "rating": 4.7, "price_per_night": 480, "rooms": 115, "amenities": "Luxury Beach, Golf, Spa", "category": "Golf Resort"},
    {"name": "Ocean Reef Club", "location": "Key Largo, FL", "state": "FL", "rating": 4.6, "price_per_night": 420, "rooms": 100, "amenities": "Private Marina, Golf, Beach", "category": "Golf Resort"},
    {"name": "Lago Mar Resort", "location": "Fort Lauderdale, FL", "state": "FL", "rating": 4.7, "price_per_night": 500, "rooms": 60, "amenities": "Private Beach, Intimate, Luxury", "category": "Luxury Resort"},
    {"name": "Riverside Hotel", "location": "Fort Lauderdale, FL", "state": "FL", "rating": 4.5, "price_per_night": 280, "rooms": 180, "amenities": "Waterfront, Historic, Events", "category": "Historic Inn"},
    {"name": "Pelican Grand Beach Resort", "location": "Fort Lauderdale, FL", "state": "FL", "rating": 4.6, "price_per_night": 380, "rooms": 140, "amenities": "Beach, Pool, Restaurant", "category": "Beachfront Resort"},
    
    # California - San Diego (8)
    {"name": "Park Hyatt Aviara", "location": "San Diego, CA", "state": "CA", "rating": 4.8, "price_per_night": 520, "rooms": 175, "amenities": "Golf, Spa, Beach Access", "category": "Golf Resort"},
    {"name": "Fairmont Grand Del Mar", "location": "San Diego, CA", "state": "CA", "rating": 4.9, "price_per_night": 650, "rooms": 150, "amenities": "Luxury, Golf, Spa", "category": "Golf Resort"},
    {"name": "Hotel del Coronado", "location": "San Diego, CA", "state": "CA", "rating": 4.7, "price_per_night": 480, "rooms": 200, "amenities": "Historic Beach, Luxury, Events", "category": "Historic Inn"},
    {"name": "Paradise Point Resort", "location": "San Diego, CA", "state": "CA", "rating": 4.5, "price_per_night": 380, "rooms": 160, "amenities": "Waterfront, Beach, Pool", "category": "Beachfront Resort"},
    {"name": "Scripps Coastal Lodge", "location": "San Diego, CA", "state": "CA", "rating": 4.6, "price_per_night": 420, "rooms": 90, "amenities": "Ocean View, Spa, Restaurant", "category": "Boutique Hotel"},
    {"name": "Four Seasons San Diego", "location": "San Diego, CA", "state": "CA", "rating": 4.9, "price_per_night": 680, "rooms": 120, "amenities": "Ultra-Luxury, Beach, Spa", "category": "Luxury Resort"},
    {"name": "Omni San Diego Hotel", "location": "San Diego, CA", "state": "CA", "rating": 4.6, "price_per_night": 400, "rooms": 200, "amenities": "Waterfront, Downtown, Pool", "category": "Urban Luxury"},
    {"name": "Beach Village Resort", "location": "San Diego, CA", "state": "CA", "rating": 4.5, "price_per_night": 320, "rooms": 180, "amenities": "Beach Access, Pool, Family", "category": "Beachfront Resort"},
    
    # California - Malibu/Ventura (4)
    {"name": "Malibu Beach Inn", "location": "Malibu, CA", "state": "CA", "rating": 4.8, "price_per_night": 580, "rooms": 50, "amenities": "Private Beach, Luxury, WiFi", "category": "Boutique Hotel"},
    {"name": "Surfrider Malibu Resort", "location": "Malibu, CA", "state": "CA", "rating": 4.6, "price_per_night": 450, "rooms": 60, "amenities": "Beach, Surf, Ocean View", "category": "Beachfront Resort"},
    {"name": "Santa Barbara Biltmore", "location": "Santa Barbara, CA", "state": "CA", "rating": 4.8, "price_per_night": 520, "rooms": 130, "amenities": "Historic, Spa, Beach", "category": "Historic Inn"},
    {"name": "Rosewood Malibu", "location": "Malibu, CA", "state": "CA", "rating": 4.9, "price_per_night": 750, "rooms": 30, "amenities": "Ultra-Luxury, Private Beach", "category": "Luxury Resort"},
    
    # Arizona - Scottsdale (6)
    {"name": "Scottsdale Desert Resort", "location": "Scottsdale, AZ", "state": "AZ", "rating": 4.2, "price_per_night": 320, "rooms": 120, "amenities": "Desert Ceremony, Golf, Spa", "category": "Golf Resort"},
    {"name": "Fairmont Scottsdale Princess", "location": "Scottsdale, AZ", "state": "AZ", "rating": 4.8, "price_per_night": 480, "rooms": 180, "amenities": "Championship Golf, Spa, Wedding", "category": "Golf Resort"},
    {"name": "The Phoenician", "location": "Scottsdale, AZ", "state": "AZ", "rating": 4.9, "price_per_night": 620, "rooms": 200, "amenities": "Luxury, Golf, Spa, Pool", "category": "Golf Resort"},
    {"name": "Hyatt Regency Scottsdale", "location": "Scottsdale, AZ", "state": "AZ", "rating": 4.5, "price_per_night": 380, "rooms": 160, "amenities": "Desert Resort, Golf, Pool", "category": "Golf Resort"},
    {"name": "JW Marriott Scottsdale", "location": "Scottsdale, AZ", "state": "AZ", "rating": 4.7, "price_per_night": 420, "rooms": 190, "amenities": "Championship Golf, Spa", "category": "Golf Resort"},
    {"name": "Four Seasons Scottsdale", "location": "Scottsdale, AZ", "state": "AZ", "rating": 4.9, "price_per_night": 680, "rooms": 100, "amenities": "Luxury, Golf, Spa", "category": "Luxury Resort"},
    
    # Colorado - Denver & Mountain (5)
    {"name": "The Brown Palace", "location": "Denver, CO", "state": "CO", "rating": 4.7, "price_per_night": 410, "rooms": 240, "amenities": "Historic, Downtown, Fine Dining", "category": "Historic Inn"},
    {"name": "Four Seasons Denver", "location": "Denver, CO", "state": "CO", "rating": 4.8, "price_per_night": 520, "rooms": 180, "amenities": "Luxury, Downtown, Spa", "category": "Urban Luxury"},
    {"name": "Beaver Creek Lodge", "location": "Beaver Creek, CO", "state": "CO", "rating": 4.8, "price_per_night": 480, "rooms": 150, "amenities": "Mountain, Ski, Wedding", "category": "Mountain Resort"},
    {"name": "St. Julien Hotel & Spa", "location": "Boulder, CO", "state": "CO", "rating": 4.6, "price_per_night": 380, "rooms": 80, "amenities": "Luxury, Spa, Flatirons View", "category": "Luxury Resort"},
    {"name": "Hotel Jerome", "location": "Aspen, CO", "state": "CO", "rating": 4.7, "price_per_night": 520, "rooms": 95, "amenities": "Historic Luxury, Mountain", "category": "Historic Inn"},
    
    # New York (5)
    {"name": "Plaza Hotel New York", "location": "New York, NY", "state": "NY", "rating": 4.8, "price_per_night": 800, "rooms": 300, "amenities": "Iconic, Luxury, Ballroom", "category": "Urban Luxury"},
    {"name": "The Peninsula New York", "location": "New York, NY", "state": "NY", "rating": 4.9, "price_per_night": 750, "rooms": 150, "amenities": "Luxury, Spa, Fine Dining", "category": "Urban Luxury"},
    {"name": "Mandarin Oriental New York", "location": "New York, NY", "state": "NY", "rating": 4.9, "price_per_night": 850, "rooms": 190, "amenities": "Luxury, Spa, Event Spaces", "category": "Urban Luxury"},
    {"name": "St. Regis New York", "location": "New York, NY", "state": "NY", "rating": 4.8, "price_per_night": 820, "rooms": 100, "amenities": "Iconic Luxury, Ballroom", "category": "Urban Luxury"},
    {"name": "The Pierre New York", "location": "New York, NY", "state": "NY", "rating": 4.7, "price_per_night": 680, "rooms": 190, "amenities": "Historic Luxury, Central Park View", "category": "Historic Inn"},
    
    # Massachusetts - Boston (4)
    {"name": "Boston Harbor Hotel", "location": "Boston, MA", "state": "MA", "rating": 4.8, "price_per_night": 480, "rooms": 230, "amenities": "Waterfront, Historic, Fine Dining", "category": "Urban Luxury"},
    {"name": "Fairmont Copley Plaza", "location": "Boston, MA", "state": "MA", "rating": 4.7, "price_per_night": 420, "rooms": 300, "amenities": "Historic, Downtown, Luxury", "category": "Historic Inn"},
    {"name": "The Liberty Hotel", "location": "Boston, MA", "state": "MA", "rating": 4.6, "price_per_night": 380, "rooms": 298, "amenities": "Modern Luxury, Historic Building", "category": "Urban Luxury"},
    {"name": "Mandarin Oriental Boston", "location": "Boston, MA", "state": "MA", "rating": 4.8, "price_per_night": 550, "rooms": 160, "amenities": "Luxury, Spa, Events", "category": "Urban Luxury"},
    
    # South Carolina - Charleston (5)
    {"name": "Charleston Historic Inn", "location": "Charleston, SC", "state": "SC", "rating": 4.1, "price_per_night": 320, "rooms": 85, "amenities": "Colonial Charm, Historic, Southern", "category": "Historic Inn"},
    {"name": "The Vendue", "location": "Charleston, SC", "state": "SC", "rating": 4.7, "price_per_night": 450, "rooms": 40, "amenities": "Art Gallery, Boutique, Modern", "category": "Boutique Hotel"},
    {"name": "Planters Inn", "location": "Charleston, SC", "state": "SC", "rating": 4.6, "price_per_night": 380, "rooms": 60, "amenities": "Historic, Downtown, Courtyard", "category": "Historic Inn"},
    {"name": "Belmond Charleston Place", "location": "Charleston, SC", "state": "SC", "rating": 4.8, "price_per_night": 520, "rooms": 150, "amenities": "Luxury, Historic, Spa", "category": "Urban Luxury"},
    {"name": "The Restoration Hotel", "location": "Charleston, SC", "state": "SC", "rating": 4.7, "price_per_night": 420, "rooms": 54, "amenities": "Boutique, Modern, Rooftop", "category": "Boutique Hotel"},
    
    # Georgia - Savannah (4)
    {"name": "Kehoe House", "location": "Savannah, GA", "state": "GA", "rating": 4.6, "price_per_night": 340, "rooms": 50, "amenities": "Historic B&B, Charming, WiFi", "category": "Historic Inn"},
    {"name": "Thunderbird Inn", "location": "Savannah, GA", "state": "GA", "rating": 4.5, "price_per_night": 290, "rooms": 70, "amenities": "Retro, Trendy, Pool", "category": "Boutique Hotel"},
    {"name": "Marshall House", "location": "Savannah, GA", "state": "GA", "rating": 4.4, "price_per_night": 280, "rooms": 68, "amenities": "Historic, Haunted, Character", "category": "Historic Inn"},
    {"name": "Sentient Bean Hotel", "location": "Savannah, GA", "state": "GA", "rating": 4.6, "price_per_night": 360, "rooms": 40, "amenities": "Boutique, Artsy, Downtown", "category": "Boutique Hotel"},
    
    # Louisiana - New Orleans (4)
    {"name": "The Roosevelt New Orleans", "location": "New Orleans, LA", "state": "LA", "rating": 4.7, "price_per_night": 420, "rooms": 210, "amenities": "Historic Luxury, Ballroom, French Quarter", "category": "Historic Inn"},
    {"name": "Windsor Court Hotel", "location": "New Orleans, LA", "state": "LA", "rating": 4.8, "price_per_night": 500, "rooms": 120, "amenities": "Luxury, Art Collection, Fine Dining", "category": "Urban Luxury"},
    {"name": "Hotel Monteleone", "location": "New Orleans, LA", "state": "LA", "rating": 4.6, "price_per_night": 380, "rooms": 600, "amenities": "Historic, French Quarter, Rooftop", "category": "Historic Inn"},
    {"name": "Ritz-Carlton New Orleans", "location": "New Orleans, LA", "state": "LA", "rating": 4.8, "price_per_night": 580, "rooms": 150, "amenities": "Luxury, French Quarter, Spa", "category": "Urban Luxury"},
    
    # Texas (6)
    {"name": "Lake Travis Resort", "location": "Austin, TX", "state": "TX", "rating": 4.5, "price_per_night": 280, "rooms": 150, "amenities": "Lake View, Pool, Restaurant", "category": "Beachfront Resort"},
    {"name": "Fairmont Austin", "location": "Austin, TX", "state": "TX", "rating": 4.8, "price_per_night": 480, "rooms": 200, "amenities": "Luxury, Spa, Downtown", "category": "Urban Luxury"},
    {"name": "The Westin Riverwalk", "location": "San Antonio, TX", "state": "TX", "rating": 4.6, "price_per_night": 380, "rooms": 140, "amenities": "River Walk, Luxury, Events", "category": "Urban Luxury"},
    {"name": "Omni Corpus Christi Hotel", "location": "Corpus Christi, TX", "state": "TX", "rating": 4.5, "price_per_night": 290, "rooms": 200, "amenities": "Waterfront, Beach, Events", "category": "Beachfront Resort"},
    {"name": "Hilton Dallas Market Center", "location": "Dallas, TX", "state": "TX", "rating": 4.6, "price_per_night": 320, "rooms": 180, "amenities": "Downtown, Modern, Events", "category": "Urban Luxury"},
    {"name": "Fort Worth Stockyards Hotel", "location": "Fort Worth, TX", "state": "TX", "rating": 4.4, "price_per_night": 240, "rooms": 100, "amenities": "Western Theme, Historic", "category": "Historic Inn"},
    
    # Pacific Northwest (5)
    {"name": "Fairmont Olympic Hotel", "location": "Seattle, WA", "state": "WA", "rating": 4.8, "price_per_night": 520, "rooms": 280, "amenities": "Historic, Luxury, Downtown", "category": "Historic Inn"},
    {"name": "Arctic Ocean Resort", "location": "Seattle, WA", "state": "WA", "rating": 4.5, "price_per_night": 380, "rooms": 100, "amenities": "Water View, Modern, WiFi", "category": "Boutique Hotel"},
    {"name": "The Benson Portland", "location": "Portland, OR", "state": "OR", "rating": 4.6, "price_per_night": 380, "rooms": 150, "amenities": "Historic, Luxury, Downtown", "category": "Historic Inn"},
    {"name": "Salishan Coastal Lodge", "location": "Lincoln City, OR", "state": "OR", "rating": 4.5, "price_per_night": 320, "rooms": 220, "amenities": "Beach, Golf, Nature", "category": "Golf Resort"},
    {"name": "The Edgewater Seattle", "location": "Seattle, WA", "state": "WA", "rating": 4.7, "price_per_night": 480, "rooms": 230, "amenities": "Waterfront, Modern Luxury", "category": "Urban Luxury"},
    
    # Nevada - Las Vegas (5)
    {"name": "Bellagio Las Vegas", "location": "Las Vegas, NV", "state": "NV", "rating": 4.7, "price_per_night": 320, "rooms": 1000, "amenities": "Strip View, Entertainment, Wedding", "category": "Urban Luxury"},
    {"name": "Caesars Palace", "location": "Las Vegas, NV", "state": "NV", "rating": 4.6, "price_per_night": 280, "rooms": 1100, "amenities": "Iconic, Ballroom, Entertainment", "category": "Urban Luxury"},
    {"name": "Wynn Las Vegas", "location": "Las Vegas, NV", "state": "NV", "rating": 4.8, "price_per_night": 420, "rooms": 2700, "amenities": "Luxury, Spa, Golf", "category": "Urban Luxury"},
    {"name": "Venetian Las Vegas", "location": "Las Vegas, NV", "state": "NV", "rating": 4.7, "price_per_night": 400, "rooms": 2000, "amenities": "All-Suite, Luxury, Spa", "category": "Urban Luxury"},
    {"name": "Mandalay Bay Resort", "location": "Las Vegas, NV", "state": "NV", "rating": 4.5, "price_per_night": 280, "rooms": 3200, "amenities": "Beach, Pool, Events", "category": "Beachfront Resort"},
    
    # Utah - Salt Lake City (3)
    {"name": "The Grand America", "location": "Salt Lake City, UT", "state": "UT", "rating": 4.8, "price_per_night": 480, "rooms": 330, "amenities": "Luxury, Ballroom, Events", "category": "Urban Luxury"},
    {"name": "Park City Marriott", "location": "Park City, UT", "state": "UT", "rating": 4.6, "price_per_night": 380, "rooms": 190, "amenities": "Mountain, Ski, Events", "category": "Mountain Resort"},
    {"name": "Snowbird Cliff Lodge", "location": "Snowbird, UT", "state": "UT", "rating": 4.7, "price_per_night": 420, "rooms": 130, "amenities": "Mountain, Ski, Spa", "category": "Mountain Resort"},
    
    # Wyoming (3)
    {"name": "Jackson Lake Lodge", "location": "Jackson, WY", "state": "WY", "rating": 4.6, "price_per_night": 380, "rooms": 130, "amenities": "Mountain View, Lake, Scenic", "category": "Mountain Resort"},
    {"name": "Amangani Resort", "location": "Jackson, WY", "state": "WY", "rating": 4.9, "price_per_night": 680, "rooms": 30, "amenities": "Ultra-Luxury, Private, Spa", "category": "Villa Resort"},
    {"name": "Snake River Sporting Club", "location": "Jackson, WY", "state": "WY", "rating": 4.7, "price_per_night": 500, "rooms": 70, "amenities": "Luxury, Fly-Fishing, Mountain", "category": "Luxury Resort"},
    
    # Montana (2)
    {"name": "Mountain Resort Bozeman", "location": "Bozeman, MT", "state": "MT", "rating": 4.5, "price_per_night": 320, "rooms": 90, "amenities": "Mountain, Ski Access, Restaurant", "category": "Mountain Resort"},
    {"name": "Chico Hot Springs Resort", "location": "Pray, MT", "state": "MT", "rating": 4.4, "price_per_night": 280, "rooms": 110, "amenities": "Hot Springs, Mountain, Historic", "category": "Mountain Resort"},
    
    # Midwest (8)
    {"name": "The St. Paul Hotel", "location": "Saint Paul, MN", "state": "MN", "rating": 4.7, "price_per_night": 380, "rooms": 150, "amenities": "Historic, Downtown, Luxury", "category": "Historic Inn"},
    {"name": "The Palmer House", "location": "Chicago, IL", "state": "IL", "rating": 4.8, "price_per_night": 480, "rooms": 300, "amenities": "Iconic, Luxury, Downtown", "category": "Historic Inn"},
    {"name": "The Peninsula Chicago", "location": "Chicago, IL", "state": "IL", "rating": 4.9, "price_per_night": 580, "rooms": 200, "amenities": "Luxury, Spa, Fine Dining", "category": "Urban Luxury"},
    {"name": "Guardian Building Hotel", "location": "Detroit, MI", "state": "MI", "rating": 4.6, "price_per_night": 340, "rooms": 100, "amenities": "Art Deco Historic, Luxury", "category": "Historic Inn"},
    {"name": "Renaissance Cleveland Hotel", "location": "Cleveland, OH", "state": "OH", "rating": 4.5, "price_per_night": 290, "rooms": 170, "amenities": "Downtown, Modern, Events", "category": "Urban Luxury"},
    {"name": "Hilton Milwaukee", "location": "Milwaukee, WI", "state": "WI", "rating": 4.5, "price_per_night": 300, "rooms": 190, "amenities": "Waterfront, Downtown, Events", "category": "Urban Luxury"},
    {"name": "Hotel Fort Des Moines", "location": "Des Moines, IA", "state": "IA", "rating": 4.4, "price_per_night": 240, "rooms": 160, "amenities": "Downtown, Historic, Modern", "category": "Historic Inn"},
    {"name": "The Ritz-Carlton St. Louis", "location": "Saint Louis, MO", "state": "MO", "rating": 4.8, "price_per_night": 520, "rooms": 200, "amenities": "Luxury, Fine Dining, Arch View", "category": "Urban Luxury"},
    
    # Northeast (6)
    {"name": "Four Seasons Philadelphia", "location": "Philadelphia, PA", "state": "PA", "rating": 4.9, "price_per_night": 620, "rooms": 200, "amenities": "Luxury, Spa, Fine Dining", "category": "Urban Luxury"},
    {"name": "The Rittenhouse Hotel", "location": "Philadelphia, PA", "state": "PA", "rating": 4.8, "price_per_night": 580, "rooms": 98, "amenities": "Luxury, Historic Square, Events", "category": "Urban Luxury"},
    {"name": "The Harbor Court", "location": "Baltimore, MD", "state": "MD", "rating": 4.6, "price_per_night": 380, "rooms": 195, "amenities": "Waterfront, Luxury, Events", "category": "Urban Luxury"},
    {"name": "The Hay-Adams", "location": "Washington, DC", "state": "DC", "rating": 4.8, "price_per_night": 620, "rooms": 145, "amenities": "Luxury, Historic, Iconic", "category": "Historic Inn"},
    {"name": "The Jefferson Hotel", "location": "Richmond, VA", "state": "VA", "rating": 4.7, "price_per_night": 420, "rooms": 55, "amenities": "Historic Luxury, Downtown", "category": "Historic Inn"},
    {"name": "The Greenbriar", "location": "White Sulphur Springs, WV", "state": "WV", "rating": 4.7, "price_per_night": 450, "rooms": 700, "amenities": "Historic, Golf, Spa", "category": "Golf Resort"},
    
    # South Atlantic (5)
    {"name": "First Colony Inn", "location": "Nags Head, NC", "state": "NC", "rating": 4.4, "price_per_night": 280, "rooms": 100, "amenities": "Beach, WiFi, Restaurant", "category": "Beachfront Resort"},
    {"name": "The Outer Banks Resort", "location": "Kill Devil Hills, NC", "state": "NC", "rating": 4.5, "price_per_night": 320, "rooms": 120, "amenities": "Beach Access, Pool, Events", "category": "Beachfront Resort"},
    {"name": "The Caribe Resort", "location": "Gulf Shores, AL", "state": "AL", "rating": 4.5, "price_per_night": 280, "rooms": 180, "amenities": "Beach, Pool, Waterpark", "category": "Beachfront Resort"},
    {"name": "Gulf State Park Resort", "location": "Gulf Shores, AL", "state": "AL", "rating": 4.4, "price_per_night": 240, "rooms": 140, "amenities": "Beach, Nature, Restaurant", "category": "Beachfront Resort"},
    {"name": "Beau Rivage Resort", "location": "Biloxi, MS", "state": "MS", "rating": 4.5, "price_per_night": 250, "rooms": 370, "amenities": "Beachfront, Casino, Events", "category": "Beachfront Resort"},
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
                results = db_results if db_results else [
                    h for h in SAMPLE_HOTELS 
                    if h["price_per_night"] <= search_budget and 
                    (search_location.lower() in h["location"].lower() or 
                     search_location.lower() in h["state"].lower() or
                     h["state"].lower() == search_location.lower())
                ] if search_location else []

                if results:
                    st.session_state.search_results = results
                    data_source = "database" if db_results else "sample"
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
                                st.write(f"✨ {hotel['amenities'][:100]}...")
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
                prices = [h["price_per_night"] for h in st.session_state.search_results[:10]]
                names = [h["name"][:15] for h in st.session_state.search_results[:10]]
                st.bar_chart({"Hotel": names, "Price": prices})

            with col2:
                ratings = [h["rating"] for h in st.session_state.search_results[:10]]
                names = [h["name"][:15] for h in st.session_state.search_results[:10]]
                st.bar_chart({"Hotel": names, "Rating": ratings})

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
