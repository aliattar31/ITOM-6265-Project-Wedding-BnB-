# Entities Extracted from PRD v1.0
## Wedding Destination Hotel Finder Platform

**Document Version**: 1.0  
**Date**: November 25, 2025  
**Purpose**: Identify all entities needed for ERD development based on PRD requirements

---

## 📋 Table of Contents

1. [Entity List Overview](#entity-list-overview)
2. [Core Entity Categories](#core-entity-categories)
3. [Detailed Entity Definitions](#detailed-entity-definitions)
4. [Entity Relationships](#entity-relationships)
5. [Attributes by Entity](#attributes-by-entity)
6. [Implementation Priority](#implementation-priority)

---

## Entity List Overview

### Total Entities: 31

**Categories:**
- **User Management**: 4 entities
- **Hotel & Accommodation**: 8 entities
- **Booking & Transactions**: 5 entities
- **Reviews & Ratings**: 3 entities
- **Search & Discovery**: 3 entities
- **Wishlists & Comparisons**: 2 entities
- **Analytics & Reporting**: 3 entities
- **Supporting/Reference**: 3 entities

---

## Core Entity Categories

### 1. User Management (4 Entities)

#### 1.1 Users
**Purpose**: Core user accounts for all user types  
**User Types**: Couples, Wedding Planners, Hotel Managers, Guests

#### 1.2 UserRoles
**Purpose**: Define role types and permissions  
**Role Types**: Couple, Planner, HotelManager, Guest, Admin

#### 1.3 UserProfiles
**Purpose**: Extended user information and preferences  
**Includes**: Preferences (location, budget, amenities), company info, etc.

#### 1.4 Sessions
**Purpose**: Track user login sessions for authentication  
**Includes**: Session tokens, login timestamps, device info

---

### 2. Hotel & Accommodation (8 Entities)

#### 2.1 Hotels
**Purpose**: Core hotel/venue information  
**Key Info**: Name, location, description, contact, manager, ratings

#### 2.2 Rooms
**Purpose**: Individual room types and configurations  
**Includes**: Room type, capacity, amenities, photos, pricing

#### 2.3 RoomTypes
**Purpose**: Reference entity for room categories  
**Examples**: Suite, Deluxe, Ocean View, Ballroom, Bridal Suite

#### 2.4 RoomAmenities (Bridge/Junction Table)
**Purpose**: Link rooms to available amenities  
**Relationship**: Many-to-Many (Rooms ↔ Amenities)

#### 2.5 Amenities
**Purpose**: Reference entity for all possible amenities  
**Examples**: WiFi, AC, Parking, Ceremony Space, Catering, Accessible Rooms

#### 2.6 HotelImages
**Purpose**: Store hotel photos and media  
**Includes**: Image URLs, upload date, order/sequence

#### 2.7 Availability
**Purpose**: Track room availability by date and pricing  
**Key Info**: Available count per date, dynamic pricing, last updated

#### 2.8 HotelPolicies
**Purpose**: Hotel-specific policies (cancellation, check-in, special requests)  
**Includes**: Cancellation policy, check-in time, group booking terms

---

### 3. Booking & Transactions (5 Entities)

#### 3.1 Bookings
**Purpose**: Core booking record  
**Key Info**: User, hotel, dates, guests, status, pricing, payment status

#### 3.2 BookingRooms (Bridge/Junction Table)
**Purpose**: Link bookings to specific rooms and quantities  
**Relationship**: Many-to-Many (Bookings ↔ Rooms)

#### 3.3 BookingPayments
**Purpose**: Track payment details and transactions  
**Includes**: Payment method, amount, transaction ID, status, timestamp

#### 3.4 BookingInquiries
**Purpose**: Track group inquiry requests (before formal booking)  
**Key Info**: Inquiry details, requested rooms, status, hotel response

#### 3.5 BookingHistory
**Purpose**: Audit trail for booking modifications  
**Includes**: Change timestamp, what changed, who made change, reason

---

### 4. Reviews & Ratings (3 Entities)

#### 4.1 Reviews
**Purpose**: Guest reviews and feedback  
**Key Info**: Reviewer, hotel, booking reference, ratings, text, verified badge

#### 4.2 ReviewRatings
**Purpose**: Multi-dimensional ratings (separate from overall review)  
**Dimensions**: Amenity Quality, Service, Value, Wedding Coordination, Overall

#### 4.3 ReviewPhotos
**Purpose**: Photos uploaded by reviewers as part of reviews  
**Includes**: Photo URL, upload date, moderation status

---

### 5. Search & Discovery (3 Entities)

#### 5.1 SearchQueries (SearchLogs)
**Purpose**: Log and track all search queries  
**Key Info**: User, search parameters (location, dates, budget), timestamp, results count

#### 5.2 SearchFilters
**Purpose**: Reference/cache commonly used filter combinations  
**Includes**: Filter sets, popularity, conversion rate

#### 5.3 UserSearchHistory
**Purpose**: Track individual user's saved searches  
**Key Info**: User, search criteria, name, created date, saved date

---

### 6. Wishlists & Comparisons (2 Entities)

#### 6.1 Wishlists
**Purpose**: User-created wishlists of favorite hotels  
**Key Info**: User, wishlist name, description, created/updated dates

#### 6.2 WishlistHotels (Bridge/Junction Table)
**Purpose**: Associate hotels with wishlists  
**Relationship**: Many-to-Many (Wishlists ↔ Hotels)

---

### 7. Analytics & Reporting (3 Entities)

#### 7.1 HotelAnalytics
**Purpose**: Aggregated analytics for hotels  
**Key Info**: Monthly/quarterly search volume, views, inquiry count, conversion rates

#### 7.2 ComparisonReports
**Purpose**: Track which hotels are compared together  
**Key Info**: Compared hotel pairs/groups, frequency, booking outcomes

#### 7.3 UserAnalytics
**Purpose**: User engagement and behavior analytics  
**Key Info**: Search frequency, booking patterns, revenue contribution

---

### 8. Supporting/Reference Entities (3 Entities)

#### 8.1 Locations
**Purpose**: Reference list of supported wedding destinations  
**Key Info**: City, state, country, region, popularity rating, coordinates

#### 8.2 HotelCategories
**Purpose**: Hotel classification types  
**Examples**: Beachfront Resort, Mountain Lodge, Urban Hotel, Boutique, All-Inclusive

#### 8.3 PricingTiers
**Purpose**: Reference for dynamic pricing rules  
**Examples**: Low Season, High Season, Peak Season, Off-Peak

---

## Detailed Entity Definitions

### Entity: Users
```
Primary Key: user_id (INT, AUTO_INCREMENT)
Attributes:
  - email (VARCHAR(255), UNIQUE, NOT NULL)
  - password_hash (VARCHAR(255), NOT NULL)
  - first_name (VARCHAR(100))
  - last_name (VARCHAR(100))
  - phone_number (VARCHAR(20))
  - user_role_id (FK → UserRoles)
  - account_status (ENUM: active, suspended, deleted)
  - profile_picture_url (VARCHAR(255))
  - created_at (TIMESTAMP)
  - updated_at (TIMESTAMP)
  - last_login (TIMESTAMP)

Relationships:
  - 1:1 with UserProfiles
  - 1:Many with Bookings
  - 1:Many with Reviews
  - 1:Many with Wishlists
  - 1:Many with SearchQueries
  - 1:Many with Sessions
  - 1:Many with UserAnalytics
```

---

### Entity: Hotels
```
Primary Key: hotel_id (INT, AUTO_INCREMENT)
Attributes:
  - name (VARCHAR(255), NOT NULL)
  - description (TEXT)
  - wedding_highlights (TEXT)
  - address (VARCHAR(255))
  - city (VARCHAR(100))
  - state (CHAR(2))
  - zip_code (VARCHAR(10))
  - country (VARCHAR(100), DEFAULT 'USA')
  - phone (VARCHAR(20))
  - email (VARCHAR(255))
  - website (VARCHAR(255))
  - latitude (DECIMAL(10,8))
  - longitude (DECIMAL(11,8))
  - manager_user_id (FK → Users)
  - overall_rating (DECIMAL(3,2), DEFAULT 0.00)
  - total_reviews (INT, DEFAULT 0)
  - category_id (FK → HotelCategories)
  - location_id (FK → Locations)
  - created_at (TIMESTAMP)
  - updated_at (TIMESTAMP)
  - is_active (BOOLEAN, DEFAULT TRUE)
  - verification_status (ENUM: pending, verified, suspended)

Relationships:
  - 1:Many with Rooms
  - 1:Many with Reviews
  - 1:Many with Bookings
  - 1:Many with HotelImages
  - 1:Many with HotelAnalytics
  - 1:1 with HotelPolicies
  - Many:Many with Amenities (via RoomAmenities)
  - Many:Many with Wishlists (via WishlistHotels)
```

---

### Entity: Rooms
```
Primary Key: room_id (INT, AUTO_INCREMENT)
Attributes:
  - hotel_id (FK → Hotels, NOT NULL)
  - room_type_id (FK → RoomTypes, NOT NULL)
  - room_number (VARCHAR(10))
  - capacity_max_guests (INT)
  - base_price_per_night (DECIMAL(10,2))
  - base_price_per_weekend (DECIMAL(10,2))
  - description (TEXT)
  - featured_image_url (VARCHAR(255))
  - total_rooms_available (INT)
  - is_pet_friendly (BOOLEAN)
  - is_accessible (BOOLEAN)
  - created_at (TIMESTAMP)
  - updated_at (TIMESTAMP)
  - is_active (BOOLEAN, DEFAULT TRUE)

Relationships:
  - Many:1 with Hotels
  - Many:1 with RoomTypes
  - 1:Many with Availability
  - Many:Many with Bookings (via BookingRooms)
  - Many:Many with Amenities (via RoomAmenities)
```

---

### Entity: Bookings
```
Primary Key: booking_id (INT, AUTO_INCREMENT)
Attributes:
  - booking_number (VARCHAR(20), UNIQUE, NOT NULL)
  - user_id (FK → Users, NOT NULL)
  - hotel_id (FK → Hotels, NOT NULL)
  - check_in_date (DATE, NOT NULL)
  - check_out_date (DATE, NOT NULL)
  - total_guests (INT, NOT NULL)
  - wedding_date (DATE) [wedding date being planned for]
  - special_requests (TEXT)
  - base_cost (DECIMAL(12,2))
  - tax_amount (DECIMAL(10,2))
  - service_fees (DECIMAL(10,2))
  - discount_amount (DECIMAL(10,2), DEFAULT 0)
  - total_cost (DECIMAL(12,2))
  - booking_status (ENUM: pending, confirmed, cancelled, completed)
  - payment_status (ENUM: pending, deposit_received, completed, refunded, disputed)
  - booking_type (ENUM: individual, group)
  - group_size (INT) [for group bookings]
  - created_at (TIMESTAMP)
  - updated_at (TIMESTAMP)
  - cancelled_at (TIMESTAMP)
  - cancellation_reason (TEXT)

Relationships:
  - Many:1 with Users
  - Many:1 with Hotels
  - 1:Many with BookingRooms
  - 1:Many with BookingPayments
  - 1:Many with Reviews
  - 1:Many with BookingHistory
  - 0:1 with BookingInquiries
```

---

### Entity: Reviews
```
Primary Key: review_id (INT, AUTO_INCREMENT)
Attributes:
  - hotel_id (FK → Hotels, NOT NULL)
  - user_id (FK → Users, NOT NULL)
  - booking_id (FK → Bookings) [proof of stay]
  - overall_rating (INT, 1-5, NOT NULL)
  - review_title (VARCHAR(200))
  - review_text (TEXT)
  - verified_booker (BOOLEAN, DEFAULT FALSE)
  - helpful_count (INT, DEFAULT 0)
  - unhelpful_count (INT, DEFAULT 0)
  - moderation_status (ENUM: pending, approved, rejected)
  - is_wedding_review (BOOLEAN, DEFAULT FALSE)
  - created_at (TIMESTAMP)
  - updated_at (TIMESTAMP)
  - hotel_response (TEXT)
  - hotel_response_date (TIMESTAMP)

Relationships:
  - Many:1 with Hotels
  - Many:1 with Users
  - 0:1 with Bookings
  - 1:Many with ReviewRatings
  - 1:Many with ReviewPhotos
```

---

### Entity: Availability
```
Primary Key: availability_id (INT, AUTO_INCREMENT)
Attributes:
  - room_id (FK → Rooms, NOT NULL)
  - date (DATE, NOT NULL)
  - available_count (INT, NOT NULL)
  - booked_count (INT, DEFAULT 0)
  - price_per_night (DECIMAL(10,2))
  - pricing_tier_id (FK → PricingTiers)
  - is_blocked (BOOLEAN, DEFAULT FALSE) [for maintenance/events]
  - last_updated (TIMESTAMP)
  - updated_by_user_id (FK → Users)

Relationships:
  - Many:1 with Rooms
  - Many:1 with PricingTiers
  - Many:1 with Users (who updated)
```

---

### Entity: Wishlists
```
Primary Key: wishlist_id (INT, AUTO_INCREMENT)
Attributes:
  - user_id (FK → Users, NOT NULL)
  - wishlist_name (VARCHAR(255), NOT NULL)
  - description (TEXT)
  - is_shared (BOOLEAN, DEFAULT FALSE)
  - shared_token (VARCHAR(50)) [for sharing via link]
  - created_at (TIMESTAMP)
  - updated_at (TIMESTAMP)

Relationships:
  - Many:1 with Users
  - Many:Many with Hotels (via WishlistHotels)
```

---

### Entity: SearchQueries (SearchLogs)
```
Primary Key: search_query_id (INT, AUTO_INCREMENT)
Attributes:
  - user_id (FK → Users) [NULL for anonymous searches]
  - search_location (VARCHAR(255))
  - location_id (FK → Locations)
  - check_in_date (DATE)
  - check_out_date (DATE)
  - min_guests (INT)
  - max_guests (INT)
  - min_budget (DECIMAL(10,2))
  - max_budget (DECIMAL(10,2))
  - amenities_filter (TEXT) [JSON array of amenity_ids]
  - results_count (INT)
  - clicked_hotel_id (FK → Hotels) [which result was clicked]
  - lead_to_booking (BOOLEAN, DEFAULT FALSE)
  - created_at (TIMESTAMP)
  - session_id (FK → Sessions)

Relationships:
  - Many:1 with Users (optional)
  - Many:1 with Locations
  - Many:1 with Hotels (optional)
  - Many:1 with Sessions
```

---

### Entity: BookingRooms (Bridge/Junction)
```
Primary Key: booking_room_id (INT, AUTO_INCREMENT)
Attributes:
  - booking_id (FK → Bookings, NOT NULL)
  - room_id (FK → Rooms, NOT NULL)
  - quantity (INT, NOT NULL)
  - price_per_night (DECIMAL(10,2))
  - total_nights (INT)
  - subtotal_price (DECIMAL(12,2))

Relationships:
  - Many:1 with Bookings
  - Many:1 with Rooms
```

---

### Entity: HotelAnalytics
```
Primary Key: analytics_id (INT, AUTO_INCREMENT)
Attributes:
  - hotel_id (FK → Hotels, NOT NULL)
  - analytics_date (DATE)
  - analytics_period (ENUM: daily, weekly, monthly, quarterly)
  - total_searches (INT, DEFAULT 0)
  - total_views (INT, DEFAULT 0)
  - total_inquiries (INT, DEFAULT 0)
  - total_bookings (INT, DEFAULT 0)
  - conversion_rate (DECIMAL(5,2)) [% of views → bookings]
  - avg_occupancy_rate (DECIMAL(5,2))
  - avg_nightly_rate (DECIMAL(10,2))
  - total_revenue (DECIMAL(12,2))
  - total_reviews_count (INT)
  - avg_rating (DECIMAL(3,2))

Relationships:
  - Many:1 with Hotels
```

---

### Entity: UserProfiles
```
Primary Key: profile_id (INT, AUTO_INCREMENT)
Attributes:
  - user_id (FK → Users, UNIQUE, NOT NULL)
  - preferred_location (VARCHAR(255))
  - preferred_budget_min (DECIMAL(10,2))
  - preferred_budget_max (DECIMAL(10,2))
  - preferred_amenities (TEXT) [JSON array]
  - bio/company_description (TEXT)
  - company_name (VARCHAR(255)) [for planners]
  - years_in_business (INT) [for planners/hotels]
  - website (VARCHAR(255))
  - social_media_links (TEXT) [JSON object]
  - profile_verified (BOOLEAN, DEFAULT FALSE)
  - created_at (TIMESTAMP)
  - updated_at (TIMESTAMP)

Relationships:
  - 1:1 with Users
```

---

### Entity: RoomTypes (Reference)
```
Primary Key: room_type_id (INT, AUTO_INCREMENT)
Attributes:
  - room_type_name (VARCHAR(100), UNIQUE, NOT NULL)
  - description (TEXT)
  - typical_capacity (INT)
  - is_active (BOOLEAN, DEFAULT TRUE)

Relationships:
  - 1:Many with Rooms
```

---

### Entity: Amenities (Reference)
```
Primary Key: amenity_id (INT, AUTO_INCREMENT)
Attributes:
  - amenity_name (VARCHAR(100), UNIQUE, NOT NULL)
  - category (ENUM: room, facility, service, wedding-specific)
  - description (TEXT)
  - icon_url (VARCHAR(255))
  - is_active (BOOLEAN, DEFAULT TRUE)

Relationships:
  - Many:Many with Rooms (via RoomAmenities)
  - Many:Many with Hotels (via RoomAmenities)
```

---

### Entity: Locations (Reference)
```
Primary Key: location_id (INT, AUTO_INCREMENT)
Attributes:
  - city (VARCHAR(100), NOT NULL)
  - state (CHAR(2), NOT NULL)
  - country (VARCHAR(100), DEFAULT 'USA')
  - region (VARCHAR(100)) [e.g., "Caribbean", "Hawaii", "Southwest"]
  - latitude (DECIMAL(10,8))
  - longitude (DECIMAL(11,8))
  - popularity_score (INT) [based on search/booking volume]
  - total_hotels (INT)
  - is_featured (BOOLEAN, DEFAULT FALSE)
  - unique_key (city_state_country UNIQUE)

Relationships:
  - 1:Many with Hotels
  - 1:Many with SearchQueries
```

---

### Entity: HotelCategories (Reference)
```
Primary Key: category_id (INT, AUTO_INCREMENT)
Attributes:
  - category_name (VARCHAR(100), UNIQUE, NOT NULL)
  - description (TEXT)
  - icon_url (VARCHAR(255))
  - is_active (BOOLEAN, DEFAULT TRUE)

Relationships:
  - 1:Many with Hotels
```

---

### Entity: BookingPayments
```
Primary Key: payment_id (INT, AUTO_INCREMENT)
Attributes:
  - booking_id (FK → Bookings, NOT NULL)
  - payment_method (ENUM: credit_card, debit_card, paypal, bank_transfer)
  - amount (DECIMAL(12,2), NOT NULL)
  - currency (CHAR(3), DEFAULT 'USD')
  - transaction_id (VARCHAR(100), UNIQUE)
  - payment_status (ENUM: pending, completed, failed, refunded)
  - payment_type (ENUM: deposit, partial, full)
  - processed_at (TIMESTAMP)
  - refunded_at (TIMESTAMP)
  - refund_reason (TEXT)
  - stripe_payment_intent_id (VARCHAR(100)) [for stripe integration]

Relationships:
  - Many:1 with Bookings
```

---

### Entity: HotelPolicies
```
Primary Key: policy_id (INT, AUTO_INCREMENT)
Attributes:
  - hotel_id (FK → Hotels, UNIQUE, NOT NULL)
  - cancellation_policy (TEXT)
  - cancellation_deadline (INT) [days before check-in]
  - group_booking_policy (TEXT)
  - minimum_group_size (INT)
  - group_discount_percentage (DECIMAL(5,2))
  - check_in_time (TIME)
  - check_out_time (TIME)
  - pet_policy (TEXT)
  - accessibility_policy (TEXT)
  - wedding_service_policy (TEXT)
  - updated_at (TIMESTAMP)

Relationships:
  - 1:1 with Hotels
```

---

### Entity: Sessions
```
Primary Key: session_id (INT, AUTO_INCREMENT)
Attributes:
  - user_id (FK → Users) [NULL for guest sessions]
  - session_token (VARCHAR(255), UNIQUE, NOT NULL)
  - ip_address (VARCHAR(45))
  - device_info (VARCHAR(255))
  - user_agent (TEXT)
  - created_at (TIMESTAMP)
  - expires_at (TIMESTAMP)
  - last_activity (TIMESTAMP)
  - is_active (BOOLEAN, DEFAULT TRUE)

Relationships:
  - Many:1 with Users (optional)
  - 1:Many with SearchQueries
```

---

### Entity: BookingInquiries
```
Primary Key: inquiry_id (INT, AUTO_INCREMENT)
Attributes:
  - inquiry_number (VARCHAR(20), UNIQUE, NOT NULL)
  - user_id (FK → Users, NOT NULL)
  - hotel_id (FK → Hotels, NOT NULL)
  - check_in_date (DATE)
  - check_out_date (DATE)
  - guest_count (INT)
  - wedding_date (DATE)
  - room_types_needed (TEXT) [JSON array]
  - special_requests (TEXT)
  - inquiry_status (ENUM: new, responded, negotiating, converted_to_booking, declined)
  - hotel_response (TEXT)
  - custom_quote (DECIMAL(12,2))
  - created_at (TIMESTAMP)
  - responded_at (TIMESTAMP)
  - responded_by_user_id (FK → Users)

Relationships:
  - Many:1 with Users
  - Many:1 with Hotels
  - 0:1 with Bookings [when converted]
  - Many:1 with Users [who responded]
```

---

### Entity: ReviewRatings (Multi-dimensional)
```
Primary Key: review_rating_id (INT, AUTO_INCREMENT)
Attributes:
  - review_id (FK → Reviews, NOT NULL)
  - rating_dimension (ENUM: amenities, service, value, wedding_coordination, cleanliness, location)
  - rating_score (INT, 1-5, NOT NULL)

Relationships:
  - Many:1 with Reviews
```

---

### Entity: ReviewPhotos
```
Primary Key: review_photo_id (INT, AUTO_INCREMENT)
Attributes:
  - review_id (FK → Reviews, NOT NULL)
  - photo_url (VARCHAR(255), NOT NULL)
  - caption (VARCHAR(255))
  - upload_date (TIMESTAMP)
  - moderation_status (ENUM: pending, approved, rejected)

Relationships:
  - Many:1 with Reviews
```

---

### Entity: HotelImages
```
Primary Key: image_id (INT, AUTO_INCREMENT)
Attributes:
  - hotel_id (FK → Hotels, NOT NULL)
  - image_url (VARCHAR(255), NOT NULL)
  - image_alt_text (VARCHAR(255))
  - image_category (ENUM: exterior, lobby, room, ceremony_space, dining, amenity)
  - display_order (INT) [for ordering on hotel page]
  - uploaded_by_user_id (FK → Users)
  - upload_date (TIMESTAMP)
  - is_primary (BOOLEAN, DEFAULT FALSE)

Relationships:
  - Many:1 with Hotels
  - Many:1 with Users
```

---

### Entity: WishlistHotels (Bridge/Junction)
```
Primary Key: wishlist_hotel_id (INT, AUTO_INCREMENT)
Attributes:
  - wishlist_id (FK → Wishlists, NOT NULL)
  - hotel_id (FK → Hotels, NOT NULL)
  - added_at (TIMESTAMP)
  - notes (TEXT) [user notes about this hotel]
  - priority (INT) [1=highest, 5=lowest]

Relationships:
  - Many:1 with Wishlists
  - Many:1 with Hotels
```

---

### Entity: RoomAmenities (Bridge/Junction)
```
Primary Key: room_amenity_id (INT, AUTO_INCREMENT)
Attributes:
  - room_id (FK → Rooms, NOT NULL)
  - amenity_id (FK → Amenities, NOT NULL)
  - is_available (BOOLEAN, DEFAULT TRUE)
  - added_at (TIMESTAMP)

Relationships:
  - Many:1 with Rooms
  - Many:1 with Amenities
```

---

### Entity: PricingTiers (Reference)
```
Primary Key: pricing_tier_id (INT, AUTO_INCREMENT)
Attributes:
  - tier_name (VARCHAR(100), UNIQUE, NOT NULL)
  - tier_description (TEXT)
  - season_start_date (DATE)
  - season_end_date (DATE)
  - price_multiplier (DECIMAL(5,2)) [1.0 = base price, 1.5 = 50% markup]
  - is_active (BOOLEAN, DEFAULT TRUE)

Relationships:
  - 1:Many with Availability
```

---

### Entity: ComparisonReports
```
Primary Key: report_id (INT, AUTO_INCREMENT)
Attributes:
  - user_id (FK → Users)
  - comparison_date (TIMESTAMP)
  - compared_hotel_ids (TEXT) [JSON array of hotel_ids]
  - comparison_criteria (TEXT) [JSON of filters used]
  - selected_hotel_id (FK → Hotels) [which hotel was ultimately booked]
  - lead_to_booking (BOOLEAN, DEFAULT FALSE)
  - created_at (TIMESTAMP)

Relationships:
  - Many:1 with Users (optional)
  - Many:1 with Hotels (optional)
```

---

### Entity: UserAnalytics
```
Primary Key: user_analytics_id (INT, AUTO_INCREMENT)
Attributes:
  - user_id (FK → Users, NOT NULL)
  - analytics_period (ENUM: daily, monthly, yearly)
  - analytics_date (DATE)
  - total_searches (INT, DEFAULT 0)
  - total_bookings (INT, DEFAULT 0)
  - total_spent (DECIMAL(12,2), DEFAULT 0)
  - avg_booking_value (DECIMAL(10,2))
  - repeat_visitor (BOOLEAN)
  - days_since_last_activity (INT)
  - reviews_submitted (INT, DEFAULT 0)

Relationships:
  - Many:1 with Users
```

---

## Entity Relationships

### Summary of Relationships

#### One-to-One (1:1)
- Users ↔ UserProfiles
- Users ↔ UserRoles (implicit)
- Hotels ↔ HotelPolicies
- Bookings ↔ BookingInquiries (optional)

#### One-to-Many (1:Many)
- Users → Bookings
- Users → Reviews
- Users → Wishlists
- Users → SearchQueries
- Users → Sessions
- Users → UserAnalytics
- Hotels → Rooms
- Hotels → Reviews
- Hotels → Bookings
- Hotels → HotelImages
- Hotels → HotelAnalytics
- Rooms → Availability
- Rooms → BookingRooms
- BookingRooms (pivot) → Bookings
- Bookings → BookingPayments
- Bookings → BookingHistory
- Reviews → ReviewRatings
- Reviews → ReviewPhotos
- Wishlists → WishlistHotels
- Locations → Hotels
- Locations → SearchQueries
- HotelCategories → Hotels
- RoomTypes → Rooms
- PricingTiers → Availability
- Sessions → SearchQueries

#### Many-to-Many (Many:Many)
- Rooms ↔ Amenities (via RoomAmenities)
- Hotels ↔ Wishlists (via WishlistHotels)
- Bookings ↔ Rooms (via BookingRooms)

---

## Attributes by Entity

### High-Priority Entities (MVP Development)

**Tier 1 - Core System (Weeks 1-4)**
1. Users
2. UserRoles
3. Hotels
4. Rooms
5. RoomTypes
6. Locations
7. Amenities
8. Bookings
9. BookingRooms

**Tier 2 - Functionality (Weeks 5-8)**
10. Availability
11. Reviews
12. ReviewRatings
13. SearchQueries
14. HotelPolicies
15. HotelCategories

**Tier 3 - Enhancement (Weeks 9-12)**
16. Wishlists
17. WishlistHotels
18. BookingPayments
19. HotelImages
20. UserProfiles

**Tier 4 - Advanced Features (Phase 2)**
21. HotelAnalytics
22. UserAnalytics
23. ComparisonReports
24. BookingInquiries
25. BookingHistory
26. ReviewPhotos
27. Sessions
28. RoomAmenities
29. PricingTiers
30. HotelCategories
31. ReviewPhotos

---

## Implementation Priority

### Phase 1: MVP (Months 1-4)

#### Must-Have Entities (15 entities)
1. Users
2. UserRoles
3. UserProfiles
4. Hotels
5. Rooms
6. RoomTypes
7. Locations
8. Amenities
9. RoomAmenities (bridge)
10. Bookings
11. BookingRooms (bridge)
12. Availability
13. Reviews
14. ReviewRatings
15. SearchQueries

**Why These?** Enable complete search, comparison, booking, and review workflows.

---

### Phase 2: Growth Features (Months 5-9)

#### Add Entities (8 entities)
16. Wishlists
17. WishlistHotels (bridge)
18. BookingPayments (separate from Bookings)
19. HotelImages
20. HotelAnalytics
21. ComparisonReports
22. Sessions
23. BookingInquiries

**Why These?** Enable saved searches, advanced analytics, payment tracking, and group inquiry management.

---

### Phase 3+: Scale & Advanced (Months 10+)

#### Add Entities (8 entities)
24. UserAnalytics
25. BookingHistory
26. ReviewPhotos
27. HotelPolicies
28. PricingTiers
29. HotelCategories
30. [Future features]
31. [Future features]

**Why These?** Enable dynamic pricing, advanced reporting, audit trails, and future integrations.

---

## Diagram: Entity Count by Category

```
User Management (4):
  ├─ Users
  ├─ UserRoles
  ├─ UserProfiles
  └─ Sessions

Hotel & Accommodation (8):
  ├─ Hotels
  ├─ Rooms
  ├─ RoomTypes
  ├─ RoomAmenities (bridge)
  ├─ Amenities
  ├─ HotelImages
  ├─ Availability
  └─ HotelPolicies

Booking & Transactions (5):
  ├─ Bookings
  ├─ BookingRooms (bridge)
  ├─ BookingPayments
  ├─ BookingInquiries
  └─ BookingHistory

Reviews & Ratings (3):
  ├─ Reviews
  ├─ ReviewRatings
  └─ ReviewPhotos

Search & Discovery (3):
  ├─ SearchQueries
  ├─ SearchFilters
  └─ UserSearchHistory

Wishlists & Comparisons (2):
  ├─ Wishlists
  └─ WishlistHotels (bridge)

Analytics & Reporting (3):
  ├─ HotelAnalytics
  ├─ ComparisonReports
  └─ UserAnalytics

Supporting/Reference (3):
  ├─ Locations
  ├─ HotelCategories
  └─ PricingTiers
```

---

## Key Relationship Diagram (Text-based)

```
                              ┌─────────────────┐
                              │     Users       │
                              │ (user_id, PK)  │
                              └────────┬────────┘
                                       │
                 ┌─────────────────────┼─────────────────────┐
                 │                     │                     │
           ┌─────▼──────┐    ┌─────────▼────────┐    ┌──────▼────────┐
           │UserProfiles│    │   UserRoles      │    │   Sessions    │
           └────────────┘    │  (reference)     │    └──────┬────────┘
                             └──────────────────┘          │
                                                           │
    ┌────────────────────────────────────────────────────┐ │
    │                                                    │ │
┌───▼──────────┐                                  ┌──────▼──────────┐
│SearchQueries │                                  │  Bookings       │
│ (log search) │                                  │  (order)        │
└──────────────┘                                  └──────┬──────────┘
                                                         │
    ┌─────────────────────────────────────────────────┐ │
    │                                                 │ │
┌───▼────────────┐    ┌──────────────┐    ┌─────────▼─────────┐
│    Hotels      │    │   Reviews    │    │  BookingRooms     │
│  (venue)       │    │  (feedback)  │    │  (junction table) │
└───┬────────────┘    │              │    └────────┬──────────┘
    │                 └──────────────┘             │
    │                                               │
┌───▼────────────┐    ┌──────────────┐    ┌────────▼─────┐
│    Rooms       │    │  Locations   │    │   Rooms      │
│  (inventory)   │    │  (reference) │    │  (inventory) │
└───┬────────────┘    └──────────────┘    └──────────────┘
    │
┌───▼──────────────┐    ┌──────────────────┐
│ Availability     │    │  RoomAmenities   │
│ (daily rates)    │    │  (junction table)│
└──────────────────┘    └────────┬─────────┘
                                 │
                        ┌────────▼─────────┐
                        │   Amenities      │
                        │  (reference)     │
                        └──────────────────┘

┌──────────────┐    ┌──────────────────┐
│ Wishlists    │────│ WishlistHotels   │────► Hotels
│ (saved list) │    │ (junction table) │
└──────────────┘    └──────────────────┘
```

---

## Summary

This document identifies **31 core entities** organized into 8 categories:

1. **User Management**: 4 entities (Users, Roles, Profiles, Sessions)
2. **Hotel & Accommodation**: 8 entities (Hotels, Rooms, Types, Amenities, Policies, Images, Availability, Categories)
3. **Booking & Transactions**: 5 entities (Bookings, BookingRooms, Payments, Inquiries, History)
4. **Reviews & Ratings**: 3 entities (Reviews, Ratings, Photos)
5. **Search & Discovery**: 3 entities (SearchQueries, SearchFilters, History)
6. **Wishlists & Comparisons**: 2 entities (Wishlists, WishlistHotels)
7. **Analytics**: 3 entities (HotelAnalytics, ComparisonReports, UserAnalytics)
8. **Reference/Supporting**: 3 entities (Locations, HotelCategories, PricingTiers)

**MVP Phase 1 should focus on the 15 highest-priority entities** to enable core search, comparison, booking, and review functionality.

---

**Document Status**: ✅ Ready for ERD Development  
**Next Step**: Create detailed ERD diagrams based on these entity definitions
