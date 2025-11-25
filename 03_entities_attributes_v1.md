# Core MVP Entities & Attributes
## Wedding Destination Hotel Finder Platform

---

## 1. Users

- user_id (INT, PRIMARY KEY, AUTO_INCREMENT)
- email (VARCHAR(255), UNIQUE, NOT NULL)
- password_hash (VARCHAR(255), NOT NULL)
- first_name (VARCHAR(100))
- last_name (VARCHAR(100))
- phone_number (VARCHAR(20))
- user_role_id (INT, FOREIGN KEY → UserRoles)
- account_status (ENUM: active, suspended, deleted)
- profile_picture_url (VARCHAR(255))
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- last_login (TIMESTAMP)

---

## 2. UserRoles

- role_id (INT, PRIMARY KEY, AUTO_INCREMENT)
- role_name (VARCHAR(100), UNIQUE, NOT NULL)
- description (TEXT)
- is_active (BOOLEAN, DEFAULT TRUE)

---

## 3. UserProfiles

- profile_id (INT, PRIMARY KEY, AUTO_INCREMENT)
- user_id (INT, FOREIGN KEY → Users, UNIQUE, NOT NULL)
- preferred_location (VARCHAR(255))
- preferred_budget_min (DECIMAL(10,2))
- preferred_budget_max (DECIMAL(10,2))
- preferred_amenities (TEXT)
- bio_company_description (TEXT)
- company_name (VARCHAR(255))
- years_in_business (INT)
- website (VARCHAR(255))
- social_media_links (TEXT)
- profile_verified (BOOLEAN, DEFAULT FALSE)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

---

## 4. Hotels

- hotel_id (INT, PRIMARY KEY, AUTO_INCREMENT)
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
- manager_user_id (INT, FOREIGN KEY → Users)
- overall_rating (DECIMAL(3,2), DEFAULT 0.00)
- total_reviews (INT, DEFAULT 0)
- category_id (INT, FOREIGN KEY → HotelCategories)
- location_id (INT, FOREIGN KEY → Locations)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- is_active (BOOLEAN, DEFAULT TRUE)
- verification_status (ENUM: pending, verified, suspended)

---

## 5. Rooms

- room_id (INT, PRIMARY KEY, AUTO_INCREMENT)
- hotel_id (INT, FOREIGN KEY → Hotels, NOT NULL)
- room_type_id (INT, FOREIGN KEY → RoomTypes, NOT NULL)
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

---

## 6. RoomTypes

- room_type_id (INT, PRIMARY KEY, AUTO_INCREMENT)
- room_type_name (VARCHAR(100), UNIQUE, NOT NULL)
- description (TEXT)
- typical_capacity (INT)
- is_active (BOOLEAN, DEFAULT TRUE)

---

## 7. Locations

- location_id (INT, PRIMARY KEY, AUTO_INCREMENT)
- city (VARCHAR(100), NOT NULL)
- state (CHAR(2), NOT NULL)
- country (VARCHAR(100), DEFAULT 'USA')
- region (VARCHAR(100))
- latitude (DECIMAL(10,8))
- longitude (DECIMAL(11,8))
- popularity_score (INT)
- total_hotels (INT)
- is_featured (BOOLEAN, DEFAULT FALSE)

---

## 8. Amenities

- amenity_id (INT, PRIMARY KEY, AUTO_INCREMENT)
- amenity_name (VARCHAR(100), UNIQUE, NOT NULL)
- category (ENUM: room, facility, service, wedding-specific)
- description (TEXT)
- icon_url (VARCHAR(255))
- is_active (BOOLEAN, DEFAULT TRUE)

---

## 9. RoomAmenities

- room_amenity_id (INT, PRIMARY KEY, AUTO_INCREMENT)
- room_id (INT, FOREIGN KEY → Rooms, NOT NULL)
- amenity_id (INT, FOREIGN KEY → Amenities, NOT NULL)
- is_available (BOOLEAN, DEFAULT TRUE)
- added_at (TIMESTAMP)

---

## 10. Bookings

- booking_id (INT, PRIMARY KEY, AUTO_INCREMENT)
- booking_number (VARCHAR(20), UNIQUE, NOT NULL)
- user_id (INT, FOREIGN KEY → Users, NOT NULL)
- hotel_id (INT, FOREIGN KEY → Hotels, NOT NULL)
- check_in_date (DATE, NOT NULL)
- check_out_date (DATE, NOT NULL)
- total_guests (INT, NOT NULL)
- wedding_date (DATE)
- special_requests (TEXT)
- base_cost (DECIMAL(12,2))
- tax_amount (DECIMAL(10,2))
- service_fees (DECIMAL(10,2))
- discount_amount (DECIMAL(10,2), DEFAULT 0)
- total_cost (DECIMAL(12,2))
- booking_status (ENUM: pending, confirmed, cancelled, completed)
- payment_status (ENUM: pending, deposit_received, completed, refunded, disputed)
- booking_type (ENUM: individual, group)
- group_size (INT)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- cancelled_at (TIMESTAMP)
- cancellation_reason (TEXT)

---

## 11. BookingRooms

- booking_room_id (INT, PRIMARY KEY, AUTO_INCREMENT)
- booking_id (INT, FOREIGN KEY → Bookings, NOT NULL)
- room_id (INT, FOREIGN KEY → Rooms, NOT NULL)
- quantity (INT, NOT NULL)
- price_per_night (DECIMAL(10,2))
- total_nights (INT)
- subtotal_price (DECIMAL(12,2))

---

## 12. Availability

- availability_id (INT, PRIMARY KEY, AUTO_INCREMENT)
- room_id (INT, FOREIGN KEY → Rooms, NOT NULL)
- date (DATE, NOT NULL)
- available_count (INT, NOT NULL)
- booked_count (INT, DEFAULT 0)
- price_per_night (DECIMAL(10,2))
- pricing_tier_id (INT, FOREIGN KEY → PricingTiers)
- is_blocked (BOOLEAN, DEFAULT FALSE)
- last_updated (TIMESTAMP)
- updated_by_user_id (INT, FOREIGN KEY → Users)

---

## 13. Reviews

- review_id (INT, PRIMARY KEY, AUTO_INCREMENT)
- hotel_id (INT, FOREIGN KEY → Hotels, NOT NULL)
- user_id (INT, FOREIGN KEY → Users, NOT NULL)
- booking_id (INT, FOREIGN KEY → Bookings)
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

---

## 14. ReviewRatings

- review_rating_id (INT, PRIMARY KEY, AUTO_INCREMENT)
- review_id (INT, FOREIGN KEY → Reviews, NOT NULL)
- rating_dimension (ENUM: amenities, service, value, wedding_coordination, cleanliness, location)
- rating_score (INT, 1-5, NOT NULL)

---

## 15. SearchQueries

- search_query_id (INT, PRIMARY KEY, AUTO_INCREMENT)
- user_id (INT, FOREIGN KEY → Users)
- search_location (VARCHAR(255))
- location_id (INT, FOREIGN KEY → Locations)
- check_in_date (DATE)
- check_out_date (DATE)
- min_guests (INT)
- max_guests (INT)
- min_budget (DECIMAL(10,2))
- max_budget (DECIMAL(10,2))
- amenities_filter (TEXT)
- results_count (INT)
- clicked_hotel_id (INT, FOREIGN KEY → Hotels)
- lead_to_booking (BOOLEAN, DEFAULT FALSE)
- created_at (TIMESTAMP)

---

## 16. HotelCategories

- category_id (INT, PRIMARY KEY, AUTO_INCREMENT)
- category_name (VARCHAR(100), UNIQUE, NOT NULL)
- description (TEXT)
- icon_url (VARCHAR(255))
- is_active (BOOLEAN, DEFAULT TRUE)

---

## 17. PricingTiers

- pricing_tier_id (INT, PRIMARY KEY, AUTO_INCREMENT)
- tier_name (VARCHAR(100), UNIQUE, NOT NULL)
- tier_description (TEXT)
- season_start_date (DATE)
- season_end_date (DATE)
- price_multiplier (DECIMAL(5,2))
- is_active (BOOLEAN, DEFAULT TRUE)

---

## 18. HotelPolicies

- policy_id (INT, PRIMARY KEY, AUTO_INCREMENT)
- hotel_id (INT, FOREIGN KEY → Hotels, UNIQUE, NOT NULL)
- cancellation_policy (TEXT)
- cancellation_deadline (INT)
- group_booking_policy (TEXT)
- minimum_group_size (INT)
- group_discount_percentage (DECIMAL(5,2))
- check_in_time (TIME)
- check_out_time (TIME)
- pet_policy (TEXT)
- accessibility_policy (TEXT)
- wedding_service_policy (TEXT)
- updated_at (TIMESTAMP)

---
