-- Wedding Destination Hotel Finder - Database Schema
-- MySQL DDL (Data Definition Language) Script
-- MVP Database Schema v1.0
-- Generated from DBML ERD v1.0

-- ============================================================
-- MySQL CONFIGURATION
-- ============================================================

SET FOREIGN_KEY_CHECKS = 1;
SET SQL_MODE = 'STRICT_TRANS_TABLES';

-- ============================================================
-- USER MANAGEMENT TABLES
-- ============================================================

-- Table: UserRoles
-- Description: User role types and permissions
-- Purpose: Reference table for user role definitions
CREATE TABLE UserRoles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    
    CHECK (role_name IS NOT NULL AND role_name != '')
);

CREATE INDEX idx_user_roles_role_name ON UserRoles(role_name);

-- Table: Users
-- Description: Core user accounts for all user types
-- Purpose: Manage user authentication and core profile info
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(20),
    user_role_id INTEGER NOT NULL,
    account_status TEXT DEFAULT 'active' CHECK(account_status IN ('active', 'suspended', 'deleted')),
    profile_picture_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    
    CONSTRAINT fk_users_role FOREIGN KEY (user_role_id) REFERENCES UserRoles(role_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CHECK (email IS NOT NULL AND email != ''),
    CHECK (password_hash IS NOT NULL AND password_hash != '')
);

CREATE INDEX idx_users_email ON Users(email);
CREATE INDEX idx_users_role_id ON Users(user_role_id);
CREATE INDEX idx_users_account_status ON Users(account_status);

-- Table: UserProfiles
-- Description: Extended user profile information and preferences
-- Purpose: Store additional user details, preferences, and company info
CREATE TABLE UserProfiles (
    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    preferred_location VARCHAR(255),
    preferred_budget_min DECIMAL(10,2),
    preferred_budget_max DECIMAL(10,2),
    preferred_amenities TEXT,
    bio_company_description TEXT,
    company_name VARCHAR(255),
    years_in_business INTEGER,
    website VARCHAR(255),
    social_media_links TEXT,
    profile_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_user_profiles_user FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_user_profiles_user_id ON UserProfiles(user_id);

-- ============================================================
-- LOCATION & REFERENCE TABLES
-- ============================================================

-- Table: Locations
-- Description: Supported wedding destination cities and regions
-- Purpose: Geographic reference for hotel locations and searches
CREATE TABLE Locations (
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    city VARCHAR(100) NOT NULL,
    state CHAR(2) NOT NULL,
    country VARCHAR(100) DEFAULT 'USA',
    region VARCHAR(100),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    popularity_score INTEGER,
    total_hotels INTEGER,
    is_featured BOOLEAN DEFAULT FALSE,
    
    CHECK (city IS NOT NULL AND city != ''),
    CHECK (state IS NOT NULL AND state != '')
);

CREATE INDEX idx_locations_city ON Locations(city);
CREATE INDEX idx_locations_state ON Locations(state);
CREATE INDEX idx_locations_country ON Locations(country);

-- Table: HotelCategories
-- Description: Hotel classification types
-- Purpose: Categorize hotels (Beachfront, Mountain, Urban, etc.)
CREATE TABLE HotelCategories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    icon_url VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    
    CHECK (category_name IS NOT NULL AND category_name != '')
);

CREATE INDEX idx_hotel_categories_name ON HotelCategories(category_name);

-- Table: RoomTypes
-- Description: Room type classifications
-- Purpose: Define room type options (Suite, Deluxe, Oceanfront, etc.)
CREATE TABLE RoomTypes (
    room_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_type_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    typical_capacity INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    
    CHECK (room_type_name IS NOT NULL AND room_type_name != '')
);

CREATE INDEX idx_room_types_name ON RoomTypes(room_type_name);

-- Table: Amenities
-- Description: All possible hotel and room amenities
-- Purpose: Reference table for searchable amenities
CREATE TABLE Amenities (
    amenity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amenity_name VARCHAR(100) UNIQUE NOT NULL,
    category TEXT DEFAULT 'facility' CHECK(category IN ('room', 'facility', 'service', 'wedding-specific')),
    description TEXT,
    icon_url VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    
    CHECK (amenity_name IS NOT NULL AND amenity_name != '')
);

CREATE INDEX idx_amenities_name ON Amenities(amenity_name);
CREATE INDEX idx_amenities_category ON Amenities(category);

-- Table: PricingTiers
-- Description: Dynamic pricing season definitions
-- Purpose: Define pricing tiers (Low Season, High Season, Peak, etc.)
CREATE TABLE PricingTiers (
    pricing_tier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tier_name VARCHAR(100) UNIQUE NOT NULL,
    tier_description TEXT,
    season_start_date DATE,
    season_end_date DATE,
    price_multiplier DECIMAL(5,2),
    is_active BOOLEAN DEFAULT TRUE,
    
    CHECK (tier_name IS NOT NULL AND tier_name != '')
);

CREATE INDEX idx_pricing_tiers_name ON PricingTiers(tier_name);

-- ============================================================
-- HOTEL & ROOM INVENTORY TABLES
-- ============================================================

-- Table: Hotels
-- Description: Wedding destination hotels and venues
-- Purpose: Core hotel information with location and ratings
CREATE TABLE Hotels (
    hotel_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    wedding_highlights TEXT,
    address VARCHAR(255),
    city VARCHAR(100),
    state CHAR(2),
    zip_code VARCHAR(10),
    country VARCHAR(100) DEFAULT 'USA',
    phone VARCHAR(20),
    email VARCHAR(255),
    website VARCHAR(255),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    manager_user_id INTEGER,
    overall_rating DECIMAL(3,2) DEFAULT 0.00,
    total_reviews INTEGER DEFAULT 0,
    category_id INTEGER,
    location_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    verification_status TEXT DEFAULT 'pending' CHECK(verification_status IN ('pending', 'verified', 'suspended')),
    
    CONSTRAINT fk_hotels_manager FOREIGN KEY (manager_user_id) REFERENCES Users(user_id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_hotels_category FOREIGN KEY (category_id) REFERENCES HotelCategories(category_id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_hotels_location FOREIGN KEY (location_id) REFERENCES Locations(location_id) ON DELETE SET NULL ON UPDATE CASCADE,
    CHECK (name IS NOT NULL AND name != ''),
    CHECK (overall_rating >= 0 AND overall_rating <= 5)
);

CREATE INDEX idx_hotels_name ON Hotels(name);
CREATE INDEX idx_hotels_location_id ON Hotels(location_id);
CREATE INDEX idx_hotels_category_id ON Hotels(category_id);
CREATE INDEX idx_hotels_manager_id ON Hotels(manager_user_id);
CREATE INDEX idx_hotels_overall_rating ON Hotels(overall_rating);

-- Table: HotelPolicies
-- Description: Hotel-specific operational policies
-- Purpose: Store cancellation, group booking, and check-in policies
CREATE TABLE HotelPolicies (
    policy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_id INTEGER UNIQUE NOT NULL,
    cancellation_policy TEXT,
    cancellation_deadline INTEGER,
    group_booking_policy TEXT,
    minimum_group_size INTEGER,
    group_discount_percentage DECIMAL(5,2),
    check_in_time TIME,
    check_out_time TIME,
    pet_policy TEXT,
    accessibility_policy TEXT,
    wedding_service_policy TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_hotel_policies_hotel FOREIGN KEY (hotel_id) REFERENCES Hotels(hotel_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_hotel_policies_hotel_id ON HotelPolicies(hotel_id);

-- Table: Rooms
-- Description: Individual room inventory
-- Purpose: Room type instances with pricing and availability info
CREATE TABLE Rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_id INTEGER NOT NULL,
    room_type_id INTEGER NOT NULL,
    room_number VARCHAR(10),
    capacity_max_guests INTEGER,
    base_price_per_night DECIMAL(10,2),
    base_price_per_weekend DECIMAL(10,2),
    description TEXT,
    featured_image_url VARCHAR(255),
    total_rooms_available INTEGER,
    is_pet_friendly BOOLEAN,
    is_accessible BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    CONSTRAINT fk_rooms_hotel FOREIGN KEY (hotel_id) REFERENCES Hotels(hotel_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_rooms_type FOREIGN KEY (room_type_id) REFERENCES RoomTypes(room_type_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CHECK (capacity_max_guests > 0)
);

CREATE INDEX idx_rooms_hotel_id ON Rooms(hotel_id);
CREATE INDEX idx_rooms_room_type_id ON Rooms(room_type_id);

-- Table: RoomAmenities
-- Description: Bridge table linking rooms to amenities
-- Purpose: Many-to-Many relationship between Rooms and Amenities
CREATE TABLE RoomAmenities (
    room_amenity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    amenity_id INTEGER NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_room_amenities_room FOREIGN KEY (room_id) REFERENCES Rooms(room_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_room_amenities_amenity FOREIGN KEY (amenity_id) REFERENCES Amenities(amenity_id) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE(room_id, amenity_id)
);

CREATE INDEX idx_room_amenities_room_id ON RoomAmenities(room_id);
CREATE INDEX idx_room_amenities_amenity_id ON RoomAmenities(amenity_id);

-- Table: Availability
-- Description: Daily room availability and pricing
-- Purpose: Track inventory and dynamic pricing by date
CREATE TABLE Availability (
    availability_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    date DATE NOT NULL,
    available_count INTEGER NOT NULL,
    booked_count INTEGER DEFAULT 0,
    price_per_night DECIMAL(10,2),
    pricing_tier_id INTEGER,
    is_blocked BOOLEAN DEFAULT FALSE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id INTEGER,
    
    CONSTRAINT fk_availability_room FOREIGN KEY (room_id) REFERENCES Rooms(room_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_availability_tier FOREIGN KEY (pricing_tier_id) REFERENCES PricingTiers(pricing_tier_id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_availability_user FOREIGN KEY (updated_by_user_id) REFERENCES Users(user_id) ON DELETE SET NULL ON UPDATE CASCADE,
    UNIQUE(room_id, date),
    CHECK (available_count >= 0),
    CHECK (booked_count >= 0)
);

CREATE INDEX idx_availability_room_id ON Availability(room_id);
CREATE INDEX idx_availability_date ON Availability(date);
CREATE INDEX idx_availability_pricing_tier_id ON Availability(pricing_tier_id);

-- ============================================================
-- BOOKING & TRANSACTION TABLES
-- ============================================================

-- Table: Bookings
-- Description: Wedding hotel bookings
-- Purpose: Core booking information with dates, costs, and status
CREATE TABLE Bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_number VARCHAR(20) UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    hotel_id INTEGER NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    total_guests INTEGER NOT NULL,
    wedding_date DATE,
    special_requests TEXT,
    base_cost DECIMAL(12,2),
    tax_amount DECIMAL(10,2),
    service_fees DECIMAL(10,2),
    discount_amount DECIMAL(10,2) DEFAULT 0,
    total_cost DECIMAL(12,2),
    booking_status TEXT DEFAULT 'pending' CHECK(booking_status IN ('pending', 'confirmed', 'cancelled', 'completed')),
    payment_status TEXT DEFAULT 'pending' CHECK(payment_status IN ('pending', 'deposit_received', 'completed', 'refunded', 'disputed')),
    booking_type TEXT DEFAULT 'individual' CHECK(booking_type IN ('individual', 'group')),
    group_size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cancelled_at TIMESTAMP,
    cancellation_reason TEXT,
    
    CONSTRAINT fk_bookings_user FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_bookings_hotel FOREIGN KEY (hotel_id) REFERENCES Hotels(hotel_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CHECK (booking_number IS NOT NULL AND booking_number != ''),
    CHECK (total_guests > 0),
    CHECK (check_out_date > check_in_date)
);

CREATE INDEX idx_bookings_number ON Bookings(booking_number);
CREATE INDEX idx_bookings_user_id ON Bookings(user_id);
CREATE INDEX idx_bookings_hotel_id ON Bookings(hotel_id);
CREATE INDEX idx_bookings_status ON Bookings(booking_status);
CREATE INDEX idx_bookings_payment_status ON Bookings(payment_status);
CREATE INDEX idx_bookings_created_at ON Bookings(created_at);

-- Table: BookingRooms
-- Description: Bridge table linking bookings to specific rooms
-- Purpose: Many-to-Many relationship between Bookings and Rooms
CREATE TABLE BookingRooms (
    booking_room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price_per_night DECIMAL(10,2),
    total_nights INTEGER,
    subtotal_price DECIMAL(12,2),
    
    CONSTRAINT fk_booking_rooms_booking FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_booking_rooms_room FOREIGN KEY (room_id) REFERENCES Rooms(room_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CHECK (quantity > 0)
);

CREATE INDEX idx_booking_rooms_booking_id ON BookingRooms(booking_id);
CREATE INDEX idx_booking_rooms_room_id ON BookingRooms(room_id);

-- ============================================================
-- REVIEW & RATING TABLES
-- ============================================================

-- Table: Reviews
-- Description: Guest reviews and feedback for hotels
-- Purpose: Store verified reviews with ratings and moderation
CREATE TABLE Reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    booking_id INTEGER,
    overall_rating INTEGER NOT NULL,
    review_title VARCHAR(200),
    review_text TEXT,
    verified_booker BOOLEAN DEFAULT FALSE,
    helpful_count INTEGER DEFAULT 0,
    unhelpful_count INTEGER DEFAULT 0,
    moderation_status TEXT DEFAULT 'pending' CHECK(moderation_status IN ('pending', 'approved', 'rejected')),
    is_wedding_review BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hotel_response TEXT,
    hotel_response_date TIMESTAMP,
    
    CONSTRAINT fk_reviews_hotel FOREIGN KEY (hotel_id) REFERENCES Hotels(hotel_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_reviews_user FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_reviews_booking FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id) ON DELETE SET NULL ON UPDATE CASCADE,
    CHECK (overall_rating >= 1 AND overall_rating <= 5)
);

CREATE INDEX idx_reviews_hotel_id ON Reviews(hotel_id);
CREATE INDEX idx_reviews_user_id ON Reviews(user_id);
CREATE INDEX idx_reviews_overall_rating ON Reviews(overall_rating);
CREATE INDEX idx_reviews_moderation_status ON Reviews(moderation_status);
CREATE INDEX idx_reviews_created_at ON Reviews(created_at);

-- Table: ReviewRatings
-- Description: Multi-dimensional ratings for reviews
-- Purpose: Store detailed ratings across multiple dimensions
CREATE TABLE ReviewRatings (
    review_rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_id INTEGER NOT NULL,
    rating_dimension TEXT NOT NULL CHECK(rating_dimension IN ('amenities', 'service', 'value', 'wedding_coordination', 'cleanliness', 'location')),
    rating_score INTEGER NOT NULL,
    
    CONSTRAINT fk_review_ratings_review FOREIGN KEY (review_id) REFERENCES Reviews(review_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (rating_score >= 1 AND rating_score <= 5),
    UNIQUE(review_id, rating_dimension)
);

CREATE INDEX idx_review_ratings_review_id ON ReviewRatings(review_id);
CREATE INDEX idx_review_ratings_dimension ON ReviewRatings(rating_dimension);

-- ============================================================
-- SEARCH & ANALYTICS TABLES
-- ============================================================

-- Table: SearchQueries
-- Description: Logged search queries for analytics
-- Purpose: Track user searches, filters, and conversion
CREATE TABLE SearchQueries (
    search_query_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    search_location VARCHAR(255),
    location_id INTEGER,
    check_in_date DATE,
    check_out_date DATE,
    min_guests INTEGER,
    max_guests INTEGER,
    min_budget DECIMAL(10,2),
    max_budget DECIMAL(10,2),
    amenities_filter TEXT,
    results_count INTEGER,
    clicked_hotel_id INTEGER,
    lead_to_booking BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_search_queries_user FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_search_queries_location FOREIGN KEY (location_id) REFERENCES Locations(location_id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_search_queries_hotel FOREIGN KEY (clicked_hotel_id) REFERENCES Hotels(hotel_id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE INDEX idx_search_queries_user_id ON SearchQueries(user_id);
CREATE INDEX idx_search_queries_location_id ON SearchQueries(location_id);
CREATE INDEX idx_search_queries_created_at ON SearchQueries(created_at);

-- ============================================================
-- VIEWS FOR COMMON QUERIES (Optional but useful)
-- ============================================================

-- View: HotelAvailability
-- Purpose: Quick lookup of available rooms by date
CREATE VIEW HotelAvailability AS
SELECT 
    h.hotel_id,
    h.name AS hotel_name,
    r.room_id,
    r.room_number,
    rt.room_type_name,
    a.date,
    a.available_count,
    a.price_per_night,
    pt.tier_name AS pricing_tier
FROM Hotels h
JOIN Rooms r ON h.hotel_id = r.hotel_id
JOIN RoomTypes rt ON r.room_type_id = rt.room_type_id
JOIN Availability a ON r.room_id = a.room_id
LEFT JOIN PricingTiers pt ON a.pricing_tier_id = pt.pricing_tier_id
WHERE a.is_blocked = FALSE
  AND r.is_active = TRUE
  AND h.is_active = TRUE;

-- View: HotelRatingsSummary
-- Purpose: Quick lookup of hotel ratings and review stats
CREATE VIEW HotelRatingsSummary AS
SELECT 
    h.hotel_id,
    h.name AS hotel_name,
    COUNT(r.review_id) AS total_reviews,
    ROUND(AVG(r.overall_rating), 2) AS avg_rating,
    COUNT(CASE WHEN r.moderation_status = 'approved' THEN 1 END) AS approved_reviews,
    COUNT(CASE WHEN r.is_wedding_review = TRUE THEN 1 END) AS wedding_reviews
FROM Hotels h
LEFT JOIN Reviews r ON h.hotel_id = r.hotel_id
GROUP BY h.hotel_id, h.name;

-- View: BookingSummary
-- Purpose: Quick lookup of booking status and financial summary
CREATE VIEW BookingSummary AS
SELECT 
    b.booking_id,
    b.booking_number,
    u.first_name,
    u.last_name,
    h.name AS hotel_name,
    b.check_in_date,
    b.check_out_date,
    b.total_guests,
    b.total_cost,
    b.booking_status,
    b.payment_status,
    b.created_at
FROM Bookings b
JOIN Users u ON b.user_id = u.user_id
JOIN Hotels h ON b.hotel_id = h.hotel_id;

-- ============================================================
-- END OF SCHEMA DEFINITION
-- ============================================================
-- Total Tables: 18
-- Total Views: 3
-- Foreign Key Constraints: Enabled (PRAGMA foreign_keys = ON)
-- Relationships:
--   - 1:1 (Users <-> UserProfiles, Hotels <-> HotelPolicies)
--   - 1:Many (Multiple)
--   - Many:Many (Rooms <-> Amenities, Bookings <-> Rooms)
-- ============================================================
