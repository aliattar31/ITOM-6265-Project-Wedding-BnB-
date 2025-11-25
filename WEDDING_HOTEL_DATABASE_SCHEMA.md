# Wedding Destination Hotel Finder - Database Schema
## Entity Relationship Diagram & Complete Data Model

**Last Updated**: November 25, 2025

---

## 1. Database Overview

This database is designed for a comprehensive wedding destination hotel booking platform that allows:
- **Couples & Wedding Planners** to search and book wedding destination hotels
- **System Admins** to manage hotel inventory, pricing, and availability
- **Hotels** to manage their properties and participate in the platform
- **Analytics** to track booking trends, pricing, and recommendations

**Key Features Supported**:
- Multi-location hotel discovery with advanced filtering
- Real-time (or manually updated) availability tracking
- Dynamic pricing management
- Comprehensive booking workflow with cancellation support
- User reviews and ratings
- Hotel amenities and capacity management
- Automated recommendation engine based on guest preferences
- Analytics and reporting capabilities

---

## 2. Core Entities & Relationships

### 2.1 Users & Authentication
```
Users (Primary Identity)
├── UserRoles (Types: Admin, Customer, WeddingPlanner, HotelManager)
├── UserProfiles (Extended user information)
└── Sessions (Login tracking)
```

### 2.2 Hotel & Property Management
```
Hotels (Property Master)
├── HotelImages (Photo gallery for each hotel)
├── Amenities (Master list of amenities)
├── HotelAmenities (Hotel-to-Amenity mapping with descriptions)
├── RoomTypes (Bedroom types: Standard, Deluxe, Suite, Penthouse, etc.)
├── Rooms (Individual room inventory)
└── HotelCategories (Classification: Resort, Boutique, Historic, Luxury, Budget)
```

### 2.3 Availability & Pricing
```
Availability (Real-time room availability by date)
├── Pricing (Dynamic pricing by room type and date range)
└── SeasonalRates (Special pricing for peak seasons)
```

### 2.4 Booking & Reservations
```
Bookings (Main booking record)
├── BookingRooms (Individual rooms within a booking)
├── BookingHistory (Audit trail of booking changes)
└── BookingInquiries (Pre-booking inquiry system)
```

### 2.5 Reviews & Ratings
```
Reviews (User feedback on hotels)
├── ReviewRatings (Multi-dimensional ratings: cleanliness, service, value, etc.)
└── ReviewPhotos (Photos attached to reviews)
```

### 2.6 Locations & Geography
```
Locations (Geographic data)
├── Regions (State/region grouping)
└── CityAreaZones (City-level organization)
```

---

## 3. Complete Table Definitions

### 3.1 User Management Tables

#### Users
```
Table: Users
Purpose: Core user identity and authentication
Columns:
  - user_id (UUID/INT PRIMARY KEY)
  - email (VARCHAR(255) UNIQUE NOT NULL)
  - username (VARCHAR(100) UNIQUE NOT NULL)
  - password_hash (VARCHAR(255) NOT NULL)
  - first_name (VARCHAR(100))
  - last_name (VARCHAR(100))
  - phone_number (VARCHAR(20))
  - user_role_id (FK → UserRoles.user_role_id)
  - profile_picture_url (VARCHAR(500))
  - is_active (BOOLEAN DEFAULT TRUE)
  - email_verified (BOOLEAN DEFAULT FALSE)
  - last_login (TIMESTAMP)
  - created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
  - updated_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE)
  - deleted_at (TIMESTAMP NULL)
```

#### UserRoles
```
Table: UserRoles
Purpose: Define user types and permission levels
Columns:
  - user_role_id (INT PRIMARY KEY)
  - role_name (VARCHAR(50) UNIQUE) - Admin, Customer, WeddingPlanner, HotelManager
  - description (TEXT)
  - permission_level (INT) - 1=Customer, 2=WeddingPlanner, 3=HotelManager, 4=Admin
  - created_at (TIMESTAMP)
```

#### UserProfiles
```
Table: UserProfiles
Purpose: Extended user information for personalization
Columns:
  - profile_id (UUID PRIMARY KEY)
  - user_id (FK → Users.user_id)
  - bio (TEXT)
  - location_id (FK → Locations.location_id)
  - company_name (VARCHAR(255)) - For wedding planners/hotel managers
  - website_url (VARCHAR(500))
  - business_phone (VARCHAR(20))
  - preferences_json (JSON) - Stored preferences for searching
  - wedding_date (DATE) - For couples planning
  - guest_count (INT)
  - budget_range_min (DECIMAL(10,2))
  - budget_range_max (DECIMAL(10,2))
  - created_at (TIMESTAMP)
  - updated_at (TIMESTAMP)
```

---

### 3.2 Hotel & Property Management Tables

#### Locations
```
Table: Locations
Purpose: Geographic reference for hotels
Columns:
  - location_id (INT PRIMARY KEY)
  - city (VARCHAR(100) NOT NULL)
  - state (VARCHAR(2) NOT NULL) - US state code
  - region (VARCHAR(100)) - Geographic region (Northeast, Southwest, etc.)
  - country (VARCHAR(100) DEFAULT 'USA')
  - latitude (DECIMAL(10,8))
  - longitude (DECIMAL(11,8))
  - timezone (VARCHAR(50))
  - created_at (TIMESTAMP)
  - UNIQUE KEY unique_location (city, state, country)
```

#### HotelCategories
```
Table: HotelCategories
Purpose: Classification of hotel types
Columns:
  - category_id (INT PRIMARY KEY)
  - category_name (VARCHAR(100) UNIQUE) - Resort, Boutique, Historic, Luxury, Budget, Beachfront, Mountain, Urban
  - description (TEXT)
  - icon_url (VARCHAR(500))
  - created_at (TIMESTAMP)
```

#### Hotels
```
Table: Hotels
Purpose: Primary hotel/property master data
Columns:
  - hotel_id (INT PRIMARY KEY)
  - hotel_name (VARCHAR(255) NOT NULL)
  - description (TEXT)
  - location_id (FK → Locations.location_id)
  - category_id (FK → HotelCategories.category_id)
  - hotel_manager_user_id (FK → Users.user_id)
  - street_address (VARCHAR(255))
  - postal_code (VARCHAR(20))
  - phone_number (VARCHAR(20))
  - email (VARCHAR(255))
  - website_url (VARCHAR(500))
  - check_in_time (TIME DEFAULT '15:00:00')
  - check_out_time (TIME DEFAULT '11:00:00')
  - total_rooms (INT)
  - wedding_venues_count (INT DEFAULT 0) - Number of wedding venues/ballrooms
  - year_established (INT)
  - star_rating (DECIMAL(3,2)) - Calculated from reviews
  - average_price_per_night (DECIMAL(10,2))
  - cancellation_policy (TEXT) - Description of cancellation terms
  - is_wedding_venue (BOOLEAN DEFAULT TRUE) - Is suitable for weddings?
  - is_active (BOOLEAN DEFAULT TRUE)
  - verification_status (ENUM: 'unverified', 'pending', 'verified')
  - created_at (TIMESTAMP)
  - updated_at (TIMESTAMP)
  - INDEX idx_location (location_id)
  - INDEX idx_category (category_id)
  - INDEX idx_star_rating (star_rating)
```

#### HotelImages
```
Table: HotelImages
Purpose: Photo gallery for hotels
Columns:
  - image_id (INT PRIMARY KEY)
  - hotel_id (FK → Hotels.hotel_id)
  - image_url (VARCHAR(500) NOT NULL)
  - image_type (ENUM: 'exterior', 'lobby', 'room', 'ballroom', 'beach', 'pool', 'dining', 'other')
  - caption (VARCHAR(255))
  - display_order (INT)
  - is_primary (BOOLEAN DEFAULT FALSE)
  - uploaded_by_user_id (FK → Users.user_id)
  - created_at (TIMESTAMP)
  - INDEX idx_hotel (hotel_id)
```

#### Amenities (Master List)
```
Table: Amenities
Purpose: Master list of available amenities
Columns:
  - amenity_id (INT PRIMARY KEY)
  - amenity_name (VARCHAR(100) UNIQUE) - WiFi, Pool, Gym, Spa, Conference Room, Parking, Pet-Friendly, etc.
  - category (ENUM: 'room', 'property', 'wedding')
  - icon_url (VARCHAR(500))
  - description (TEXT)
  - created_at (TIMESTAMP)
```

#### HotelAmenities
```
Table: HotelAmenities
Purpose: Amenities available at each hotel
Columns:
  - hotel_amenity_id (INT PRIMARY KEY)
  - hotel_id (FK → Hotels.hotel_id)
  - amenity_id (FK → Amenities.amenity_id)
  - availability_details (VARCHAR(500)) - E.g., "Available 24/7", "Fee applies", "3 locations"
  - is_complimentary (BOOLEAN)
  - additional_cost (DECIMAL(10,2)) - If there's a fee
  - created_at (TIMESTAMP)
  - UNIQUE KEY unique_hotel_amenity (hotel_id, amenity_id)
```

#### RoomTypes
```
Table: RoomTypes
Purpose: Categories of room types
Columns:
  - room_type_id (INT PRIMARY KEY)
  - room_type_name (VARCHAR(100)) - Standard, Deluxe, Suite, Penthouse, Honeymoon Suite, Group Room, Wedding Party Room
  - description (TEXT)
  - base_capacity (INT) - Standard occupancy
  - max_capacity (INT) - With extra beds
  - created_at (TIMESTAMP)
```

#### Rooms
```
Table: Rooms
Purpose: Individual rooms in each hotel
Columns:
  - room_id (INT PRIMARY KEY)
  - hotel_id (FK → Hotels.hotel_id)
  - room_type_id (FK → RoomTypes.room_type_id)
  - room_number (VARCHAR(10))
  - floor_number (INT)
  - occupancy_limit (INT)
  - square_footage (INT)
  - base_rate (DECIMAL(10,2)) - Base nightly rate
  - wedding_surcharge (DECIMAL(10,2)) - Additional cost for wedding bookings
  - description (TEXT)
  - is_active (BOOLEAN DEFAULT TRUE)
  - created_at (TIMESTAMP)
  - updated_at (TIMESTAMP)
  - INDEX idx_hotel_type (hotel_id, room_type_id)
  - UNIQUE KEY unique_room (hotel_id, room_number)
```

---

### 3.3 Availability & Pricing Tables

#### Availability
```
Table: Availability
Purpose: Real-time room availability by date
Columns:
  - availability_id (INT PRIMARY KEY)
  - room_id (FK → Rooms.room_id)
  - available_date (DATE NOT NULL)
  - total_rooms_available (INT)
  - is_blocked (BOOLEAN DEFAULT FALSE) - Block dates for maintenance
  - blocked_reason (VARCHAR(255))
  - last_updated (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
  - INDEX idx_room_date (room_id, available_date)
  - INDEX idx_available_date (available_date)
  - UNIQUE KEY unique_availability (room_id, available_date)
```

#### Pricing
```
Table: Pricing
Purpose: Dynamic pricing for rooms
Columns:
  - pricing_id (INT PRIMARY KEY)
  - room_id (FK → Rooms.room_id)
  - pricing_date (DATE NOT NULL)
  - nightly_rate (DECIMAL(10,2) NOT NULL)
  - weekend_surcharge (DECIMAL(10,2)) - Extra cost for weekends
  - holiday_surcharge (DECIMAL(10,2)) - Extra cost for holidays
  - peak_season_surcharge (DECIMAL(10,2)) - Extra cost during peak wedding season
  - discount_percentage (DECIMAL(5,2)) - For early bookings or bulk bookings
  - effective_from (DATE)
  - effective_until (DATE)
  - is_active (BOOLEAN DEFAULT TRUE)
  - created_at (TIMESTAMP)
  - INDEX idx_room_date (room_id, pricing_date)
  - UNIQUE KEY unique_pricing (room_id, pricing_date)
```

#### SeasonalRates
```
Table: SeasonalRates
Purpose: Special rates for seasons
Columns:
  - seasonal_rate_id (INT PRIMARY KEY)
  - hotel_id (FK → Hotels.hotel_id)
  - season_name (VARCHAR(100)) - Summer, Winter, Spring, Fall, Wedding Season
  - start_date (DATE)
  - end_date (DATE)
  - rate_multiplier (DECIMAL(4,2)) - 1.5 = 50% increase
  - description (TEXT)
  - created_at (TIMESTAMP)
```

---

### 3.4 Booking & Reservation Tables

#### Bookings
```
Table: Bookings
Purpose: Main booking record for reservations
Columns:
  - booking_id (INT PRIMARY KEY)
  - booking_code (VARCHAR(20) UNIQUE) - Human-readable booking reference
  - user_id (FK → Users.user_id)
  - hotel_id (FK → Hotels.hotel_id)
  - check_in_date (DATE NOT NULL)
  - check_out_date (DATE NOT NULL)
  - number_of_guests (INT NOT NULL)
  - number_of_rooms (INT NOT NULL)
  - booking_status (ENUM: 'pending', 'confirmed', 'paid', 'cancelled', 'completed')
  - booking_date (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
  - confirmation_date (TIMESTAMP)
  - cancellation_date (TIMESTAMP)
  - cancellation_reason (TEXT)
  - total_booking_cost (DECIMAL(12,2))
  - tax_amount (DECIMAL(10,2))
  - discount_amount (DECIMAL(10,2))
  - final_amount_due (DECIMAL(12,2))
  - payment_method (ENUM: 'credit_card', 'bank_transfer', 'invoice')
  - payment_status (ENUM: 'pending', 'partial', 'paid', 'refunded')
  - special_requests (TEXT) - E.g., room preferences, dietary restrictions for wedding
  - notes (TEXT) - Internal notes for hotel
  - created_by_user_id (FK → Users.user_id) - Who created this booking
  - wedding_event_name (VARCHAR(255)) - Name of the wedding event
  - is_group_booking (BOOLEAN DEFAULT FALSE)
  - created_at (TIMESTAMP)
  - updated_at (TIMESTAMP)
  - INDEX idx_user (user_id)
  - INDEX idx_hotel (hotel_id)
  - INDEX idx_check_in (check_in_date)
  - INDEX idx_booking_status (booking_status)
```

#### BookingRooms
```
Table: BookingRooms
Purpose: Individual rooms within a booking (booking can have multiple rooms)
Columns:
  - booking_room_id (INT PRIMARY KEY)
  - booking_id (FK → Bookings.booking_id)
  - room_id (FK → Rooms.room_id)
  - check_in_date (DATE)
  - check_out_date (DATE)
  - nightly_rate (DECIMAL(10,2))
  - number_of_nights (INT)
  - subtotal (DECIMAL(12,2))
  - room_assignment_status (ENUM: 'unassigned', 'assigned', 'occupied', 'checked_out')
  - guest_names (VARCHAR(255)) - Guests assigned to this specific room
  - created_at (TIMESTAMP)
  - INDEX idx_booking (booking_id)
  - INDEX idx_room (room_id)
```

#### BookingHistory
```
Table: BookingHistory
Purpose: Audit trail of booking changes
Columns:
  - history_id (INT PRIMARY KEY)
  - booking_id (FK → Bookings.booking_id)
  - change_type (ENUM: 'created', 'modified', 'confirmed', 'cancelled', 'payment_received', 'room_assigned')
  - old_value (JSON)
  - new_value (JSON)
  - changed_by_user_id (FK → Users.user_id)
  - change_reason (TEXT)
  - created_at (TIMESTAMP)
  - INDEX idx_booking (booking_id)
```

#### BookingInquiries
```
Table: BookingInquiries
Purpose: Pre-booking inquiry system
Columns:
  - inquiry_id (INT PRIMARY KEY)
  - user_id (FK → Users.user_id)
  - hotel_id (FK → Hotels.hotel_id)
  - check_in_date (DATE)
  - check_out_date (DATE)
  - guest_count (INT)
  - rooms_needed (INT)
  - message (TEXT)
  - inquiry_status (ENUM: 'new', 'in_progress', 'responded', 'converted_to_booking', 'closed')
  - response_from_hotel (TEXT)
  - response_date (TIMESTAMP)
  - converted_booking_id (FK → Bookings.booking_id)
  - created_at (TIMESTAMP)
  - INDEX idx_hotel (hotel_id)
  - INDEX idx_user (user_id)
```

---

### 3.5 Reviews & Ratings Tables

#### Reviews
```
Table: Reviews
Purpose: User reviews of hotels
Columns:
  - review_id (INT PRIMARY KEY)
  - booking_id (FK → Bookings.booking_id)
  - hotel_id (FK → Hotels.hotel_id)
  - user_id (FK → Users.user_id)
  - review_title (VARCHAR(255))
  - review_text (TEXT)
  - overall_rating (DECIMAL(3,2)) - 1-5 scale
  - would_recommend (BOOLEAN)
  - reviewed_date (DATE)
  - review_date (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
  - is_verified_booking (BOOLEAN) - Confirmed the user actually stayed here
  - helpful_count (INT DEFAULT 0) - Upvotes
  - status (ENUM: 'pending', 'approved', 'rejected')
  - approved_by_user_id (FK → Users.user_id)
  - created_at (TIMESTAMP)
  - updated_at (TIMESTAMP)
  - INDEX idx_hotel (hotel_id)
  - INDEX idx_user (user_id)
  - INDEX idx_overall_rating (overall_rating)
```

#### ReviewRatings
```
Table: ReviewRatings
Purpose: Multi-dimensional ratings within a review
Columns:
  - review_rating_id (INT PRIMARY KEY)
  - review_id (FK → Reviews.review_id)
  - rating_aspect (ENUM: 'cleanliness', 'service', 'value_for_money', 'amenities', 'location', 'food_quality', 'wedding_coordination', 'room_comfort')
  - rating_value (DECIMAL(3,2)) - 1-5 scale
  - comment (TEXT)
  - INDEX idx_review (review_id)
```

#### ReviewPhotos
```
Table: ReviewPhotos
Purpose: Photos attached to reviews
Columns:
  - review_photo_id (INT PRIMARY KEY)
  - review_id (FK → Reviews.review_id)
  - photo_url (VARCHAR(500))
  - caption (TEXT)
  - display_order (INT)
  - created_at (TIMESTAMP)
```

---

### 3.6 Analytics & Reporting Tables

#### HotelAnalytics
```
Table: HotelAnalytics
Purpose: Cached analytics for performance
Columns:
  - analytics_id (INT PRIMARY KEY)
  - hotel_id (FK → Hotels.hotel_id)
  - snapshot_date (DATE)
  - total_bookings (INT)
  - average_booking_value (DECIMAL(12,2))
  - occupancy_rate (DECIMAL(5,2)) - Percentage
  - cancellation_rate (DECIMAL(5,2)) - Percentage
  - average_review_score (DECIMAL(3,2))
  - total_reviews (INT)
  - peak_booking_month (VARCHAR(20))
  - created_at (TIMESTAMP)
  - INDEX idx_hotel_date (hotel_id, snapshot_date)
```

#### ComparisonReports
```
Table: ComparisonReports
Purpose: Store generated hotel comparisons
Columns:
  - comparison_id (INT PRIMARY KEY)
  - user_id (FK → Users.user_id)
  - hotel_ids (JSON) - Array of compared hotel IDs
  - comparison_criteria (JSON) - Fields compared (price, rating, amenities, etc.)
  - generated_at (TIMESTAMP)
  - is_shared (BOOLEAN DEFAULT FALSE)
  - share_token (VARCHAR(100) UNIQUE)
  - created_at (TIMESTAMP)
```

---

## 4. Key Relationships & Constraints

### One-to-Many Relationships
- `Locations` (1) → `Hotels` (M)
- `HotelCategories` (1) → `Hotels` (M)
- `Hotels` (1) → `Rooms` (M)
- `Hotels` (1) → `HotelImages` (M)
- `Hotels` (1) → `HotelAmenities` (M)
- `Hotels` (1) → `Reviews` (M)
- `RoomTypes` (1) → `Rooms` (M)
- `Rooms` (1) → `Availability` (M)
- `Rooms` (1) → `Pricing` (M)
- `Users` (1) → `Bookings` (M)
- `Hotels` (1) → `Bookings` (M)
- `Bookings` (1) → `BookingRooms` (M)
- `Reviews` (1) → `ReviewRatings` (M)
- `Reviews` (1) → `ReviewPhotos` (M)

### Many-to-Many Relationships
- `Hotels` ↔ `Amenities` (via `HotelAmenities`)

### Self-Referencing
- `Locations.region` may reference location groupings
- `HotelCategories` can have parent-child for hierarchy

---

## 5. Important Constraints & Rules

### Data Integrity
```sql
-- Check-out date must be after check-in date
ALTER TABLE Bookings ADD CONSTRAINT check_dates CHECK (check_out_date > check_in_date);

-- Room capacity constraints
ALTER TABLE Rooms ADD CONSTRAINT capacity_check CHECK (max_capacity >= base_capacity);

-- Rating values between 1-5
ALTER TABLE Reviews ADD CONSTRAINT rating_range CHECK (overall_rating BETWEEN 1 AND 5);

-- Pricing must be positive
ALTER TABLE Pricing ADD CONSTRAINT positive_rate CHECK (nightly_rate > 0);

-- No double bookings (enforced through application logic & unique availability records)
```

### Cascading Rules
- Delete a `Hotel` → Cascade delete related `Rooms`, `HotelImages`, `HotelAmenities`, `Bookings`
- Delete a `User` → Set user_id to NULL in reviews (preserve history), but mark bookings for audit
- Delete a `Room` → Cancel associated bookings if future dates

### Business Rules
1. **Availability**: A room cannot be double-booked
2. **Pricing**: Must be updated before or on the date it applies
3. **Bookings**: Can only be cancelled up to X days before check-in (configurable)
4. **Reviews**: Can only be posted after stay completion (verified booking)
5. **Payments**: Must be processed before check-in confirmation

---

## 6. Indexes for Performance

```sql
-- Hotel search optimization
CREATE INDEX idx_hotels_location_category ON Hotels(location_id, category_id, star_rating);
CREATE INDEX idx_hotels_active_status ON Hotels(is_active, verification_status);

-- Availability queries
CREATE INDEX idx_availability_hotel_date ON Availability(room_id, available_date);
CREATE INDEX idx_availability_date_range ON Availability(available_date);

-- Booking queries
CREATE INDEX idx_bookings_user_status ON Bookings(user_id, booking_status);
CREATE INDEX idx_bookings_hotel_dates ON Bookings(hotel_id, check_in_date, check_out_date);

-- Review queries
CREATE INDEX idx_reviews_hotel_rating ON Reviews(hotel_id, overall_rating);
```

---

## 7. Sample Data Scenarios

### Scenario 1: Couple Searching
- User searches for: Miami, June 2025, 30 guests, $200-300/night
- System queries: Hotels in Miami with categories → Filter by availability June 1-8 → Filter by price range → Calculate recommendations based on reviews and amenities

### Scenario 2: Booking Flow
1. User selects 2 suites for 3 nights (June 5-8)
2. System checks availability in `Availability` table
3. Creates `Booking` record with status='pending'
4. Creates 2 `BookingRooms` records
5. Updates `Availability.total_rooms_available` for those dates
6. Awaits payment → Updates `Bookings.payment_status` → Changes `booking_status` to 'confirmed'

### Scenario 3: Analytics Query
- Hotel manager wants to see: Occupancy rate for last 30 days
- Query joins: `Bookings` → `BookingRooms` → `Rooms` → group by date → calculate occupancy

---

## 8. Future Enhancements

- **Dynamic Pricing AI**: Machine learning for price optimization
- **Multi-Property Management**: Support for hotel chains
- **Vendor Integration**: Connect with caterers, photographers, florists
- **Payment Processing**: Direct payment gateway integration
- **Review Moderation System**: ML-based spam/fake review detection
- **Mobile App Schema**: Push notifications, offline caching
- **Guest Communication**: Built-in messaging between guests and hotels
- **Group Rate Management**: Negotiate rates for large bookings
- **Destination Guides**: Integration with local attractions, restaurants

---

## 9. ER Diagram (Text-Based)

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER MANAGEMENT                         │
├──────────────┬──────────────────────┬──────────────────────────┤
│  UserRoles   │      Users           │    UserProfiles          │
│  (role_id)   │  (user_id) [FK role] │  (profile_id) [FK user]  │
└──────────────┴──────────────────────┴──────────────────────────┘
                                ↓
┌──────────────────────────────────────────────────────────────────┐
│                    HOTEL & PROPERTY MGMT                         │
├──────────┬────────────┬──────────┬──────────┬────────────────────┤
│Locations │   Hotels   │  Rooms   │RoomTypes│   HotelImages      │
│(loc_id)  │ [FK loc]   │[FK hotel]│(rt_id)  │  [FK hotel]        │
└──────────┴────────────┴──────────┴──────────┴────────────────────┘
                          ↓              ↓
        ┌─────────────────┴──────────────┴──────────────┐
        │                                               │
┌───────────────────────────────┐  ┌──────────────────────────────┐
│      AMENITIES MAPPING        │  │  AVAILABILITY & PRICING      │
│  HotelAmenities [FK both]     │  │  Availability [FK room]      │
│  Amenities (amenity_id)       │  │  Pricing [FK room]           │
│                               │  │  SeasonalRates [FK hotel]    │
└───────────────────────────────┘  └──────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                    BOOKING & RESERVATIONS                        │
├──────────────┬──────────────┬─────────────┬──────────────────────┤
│  Bookings    │ BookingRooms │BookingHistory│ BookingInquiries   │
│(booking_id)  │[FK booking]  │ [FK booking] │ [FK hotel, user]   │
│[FK user,     │[FK room]     │             │                    │
│ hotel]       │             │             │                    │
└──────────────┴──────────────┴─────────────┴──────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                    REVIEWS & RATINGS                             │
├──────────────┬──────────────┬─────────────┬──────────────────────┤
│  Reviews     │ReviewRatings │ReviewPhotos │  HotelAnalytics    │
│(review_id)  │[FK review]   │[FK review]  │  (analytics_id)    │
│[FK booking, │             │             │  [FK hotel]        │
│ hotel, user]│             │             │                    │
└──────────────┴──────────────┴─────────────┴──────────────────────┘
```

---

## 10. Next Steps

1. **Implement SQL DDL**: Execute CREATE TABLE statements
2. **Create Sample Data**: Insert test hotels, rooms, pricing, availability
3. **Build Stored Procedures**: For complex queries (recommendations, analytics)
4. **Design API Endpoints**: Map endpoints to table operations
5. **Implement ORM Models**: Create application-layer models (SQLAlchemy, TypeORM, etc.)
6. **Set up Views**: Create database views for common reporting queries
