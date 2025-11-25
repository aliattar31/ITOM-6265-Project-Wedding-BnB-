-- Wedding Destination Hotel Finder - Sample Data Population
-- SQLite DML (Data Manipulation Language) Script
-- MVP Sample Data v1.0
-- Generated for populating 05_DDL_schema_v1.sql tables

-- ============================================================
-- PRAGMA SETTINGS
-- ============================================================

PRAGMA foreign_keys = ON;

-- ============================================================
-- USER MANAGEMENT DATA
-- ============================================================

-- Insert User Roles
INSERT INTO UserRoles (role_name, description, is_active) VALUES
('couple', 'End user couple planning a destination wedding', TRUE),
('planner', 'Professional wedding planner', TRUE),
('hotel_manager', 'Hotel staff managing property and bookings', TRUE),
('guest', 'Guest user browsing accommodations', TRUE),
('admin', 'Platform administrator with full access', TRUE);

-- Insert Users
INSERT INTO Users (email, password_hash, first_name, last_name, phone_number, user_role_id, account_status, created_at, updated_at) VALUES
('john.smith@email.com', '$2b$12$abcdefghijklmnopqrstuvwxyz', 'John', 'Smith', '5551234567', 1, 'active', '2025-01-15 10:30:00', '2025-01-15 10:30:00'),
('sarah.johnson@email.com', '$2b$12$abcdefghijklmnopqrstuvwxyz', 'Sarah', 'Johnson', '5552345678', 1, 'active', '2025-01-16 14:20:00', '2025-01-16 14:20:00'),
('emily.davis@email.com', '$2b$12$abcdefghijklmnopqrstuvwxyz', 'Emily', 'Davis', '5553456789', 2, 'active', '2025-01-10 08:15:00', '2025-01-10 08:15:00'),
('michael.wilson@email.com', '$2b$12$abcdefghijklmnopqrstuvwxyz', 'Michael', 'Wilson', '5554567890', 2, 'active', '2025-01-12 09:45:00', '2025-01-12 09:45:00'),
('robert.anderson@email.com', '$2b$12$abcdefghijklmnopqrstuvwxyz', 'Robert', 'Anderson', '5555678901', 3, 'active', '2024-12-01 11:00:00', '2025-01-20 16:30:00'),
('lisa.taylor@email.com', '$2b$12$abcdefghijklmnopqrstuvwxyz', 'Lisa', 'Taylor', '5556789012', 3, 'active', '2024-11-15 09:30:00', '2025-01-19 14:15:00'),
('david.brown@email.com', '$2b$12$abcdefghijklmnopqrstuvwxyz', 'David', 'Brown', '5557890123', 4, 'active', '2025-01-18 13:25:00', '2025-01-18 13:25:00'),
('jennifer.martinez@email.com', '$2b$12$abcdefghijklmnopqrstuvwxyz', 'Jennifer', 'Martinez', '5558901234', 1, 'active', '2025-01-17 15:40:00', '2025-01-17 15:40:00');

-- Insert User Profiles
INSERT INTO UserProfiles (user_id, preferred_location, preferred_budget_min, preferred_budget_max, company_name, years_in_business, profile_verified, created_at, updated_at) VALUES
(1, 'Hawaii', 5000.00, 15000.00, NULL, NULL, TRUE, '2025-01-15 10:30:00', '2025-01-15 10:30:00'),
(2, 'Caribbean', 7000.00, 20000.00, NULL, NULL, TRUE, '2025-01-16 14:20:00', '2025-01-16 14:20:00'),
(3, NULL, NULL, NULL, 'Premier Wedding Planning Co.', 8, TRUE, '2025-01-10 08:15:00', '2025-01-10 08:15:00'),
(4, NULL, NULL, NULL, 'Destination Weddings LLC', 5, TRUE, '2025-01-12 09:45:00', '2025-01-12 09:45:00'),
(5, NULL, NULL, NULL, 'Maui Grand Resort', 15, TRUE, '2024-12-01 11:00:00', '2025-01-20 16:30:00'),
(6, NULL, NULL, NULL, 'Bora Bora Luxury Villas', 12, TRUE, '2024-11-15 09:30:00', '2025-01-19 14:15:00'),
(7, 'Mexico', 3000.00, 8000.00, NULL, NULL, FALSE, '2025-01-18 13:25:00', '2025-01-18 13:25:00'),
(8, 'Florida', 4000.00, 10000.00, NULL, NULL, TRUE, '2025-01-17 15:40:00', '2025-01-17 15:40:00');

-- ============================================================
-- LOCATION & REFERENCE DATA
-- ============================================================

-- Insert Locations
INSERT INTO Locations (city, state, country, region, latitude, longitude, popularity_score, total_hotels, is_featured) VALUES
('Maui', 'HI', 'USA', 'Hawaii', 20.7881, -156.4730, 95, 45, TRUE),
('Honolulu', 'HI', 'USA', 'Hawaii', 21.3099, -157.8581, 92, 52, TRUE),
('Cancun', 'QR', 'Mexico', 'Caribbean', 21.1619, -86.8515, 88, 67, TRUE),
('Montego Bay', 'ST', 'Jamaica', 'Caribbean', 18.4891, -77.9221, 80, 38, TRUE),
('Key West', 'FL', 'USA', 'Florida', 24.5551, -81.7796, 75, 32, TRUE),
('Miami', 'FL', 'USA', 'Florida', 25.7617, -80.1918, 85, 78, TRUE),
('Cabo San Lucas', 'BCS', 'Mexico', 'Mexico', 22.8898, -109.9734, 82, 41, FALSE),
('San Juan', 'PR', 'Puerto Rico', 'Caribbean', 18.3664, -66.1034, 78, 35, FALSE),
('Scottsdale', 'AZ', 'USA', 'Southwest', 33.4942, -111.9260, 70, 28, FALSE),
('Charleston', 'SC', 'USA', 'Southeast', 32.7765, -79.9318, 72, 24, FALSE);

-- Insert Hotel Categories
INSERT INTO HotelCategories (category_name, description, is_active) VALUES
('Beachfront Resort', 'Full-service beachfront resort with wedding facilities', TRUE),
('Boutique Hotel', 'Luxury boutique hotel with personalized service', TRUE),
('All-Inclusive', 'All-inclusive resort with activities and meals included', TRUE),
('Golf Resort', 'Resort with championship golf courses', TRUE),
('Historic Inn', 'Historic property with charm and character', TRUE),
('Villa Resort', 'Private villa accommodations with personalized service', TRUE),
('Urban Luxury', 'Luxury hotel in city center', TRUE),
('Resort & Spa', 'Resort with full-service spa facilities', TRUE);

-- Insert Room Types
INSERT INTO RoomTypes (room_type_name, description, typical_capacity, is_active) VALUES
('Standard Room', 'Basic room with queen bed', 2, TRUE),
('Deluxe Room', 'Larger room with king bed and seating area', 2, TRUE),
('Ocean View Suite', 'Suite with ocean view balcony', 4, TRUE),
('Bridal Suite', 'Luxury suite perfect for honeymoon', 2, TRUE),
('Family Villa', 'Large villa with multiple bedrooms', 6, TRUE),
('Penthouse Suite', 'Top-floor luxury suite', 4, TRUE),
('Oceanfront Bungalow', 'Private beachfront bungalow', 2, TRUE),
('Garden Room', 'Room overlooking tropical gardens', 2, TRUE);

-- Insert Amenities
INSERT INTO Amenities (amenity_name, category, description, is_active) VALUES
('Free WiFi', 'facility', 'High-speed internet access throughout property', TRUE),
('Swimming Pool', 'facility', 'Outdoor heated swimming pool', TRUE),
('Spa Services', 'service', 'Full-service spa with massage and treatments', TRUE),
('Ceremony Space', 'wedding-specific', 'Dedicated indoor and outdoor ceremony venues', TRUE),
('Catering Services', 'wedding-specific', 'In-house catering for events and receptions', TRUE),
('Wedding Coordination', 'wedding-specific', 'Professional wedding coordinator on staff', TRUE),
('Parking', 'facility', 'Free or paid parking available', TRUE),
('Gym/Fitness Center', 'facility', 'Modern fitness equipment and classes', TRUE),
('Restaurant', 'service', 'On-site restaurant and bar', TRUE),
('Golf Course', 'facility', 'Championship golf course access', TRUE),
('Beach Access', 'facility', 'Private or semi-private beach access', TRUE),
('Accessible Rooms', 'facility', 'Wheelchair accessible accommodations', TRUE),
('Pet Friendly', 'service', 'Pets allowed with additional fees', TRUE),
('Concierge Service', 'service', '24/7 concierge assistance', TRUE),
('Event Planning', 'wedding-specific', 'Professional event planning services', TRUE);

-- Insert Pricing Tiers
INSERT INTO PricingTiers (tier_name, tier_description, season_start_date, season_end_date, price_multiplier, is_active) VALUES
('Low Season', 'Off-peak travel season with lowest rates', '2025-06-01', '2025-08-31', 0.80, TRUE),
('Regular Season', 'Standard pricing period', '2025-01-01', '2025-05-31', 1.00, TRUE),
('High Season', 'Peak travel season with higher demand', '2025-09-01', '2025-12-15', 1.25, TRUE),
('Peak Season', 'Holiday and peak wedding season', '2025-12-16', '2025-12-31', 1.50, TRUE),
('Wedding Blackout', 'Premium pricing for popular wedding dates', '2025-10-01', '2025-10-31', 1.40, TRUE);

-- ============================================================
-- HOTEL & ROOM INVENTORY DATA
-- ============================================================

-- Insert Hotels
INSERT INTO Hotels (name, description, wedding_highlights, address, city, state, zip_code, country, phone, email, website, latitude, longitude, manager_user_id, overall_rating, total_reviews, category_id, location_id, is_active, verification_status, created_at, updated_at) VALUES
('Maui Grand Resort', 'Five-star beachfront resort with world-class amenities and comprehensive wedding services', 'Stunning ocean sunsets, multiple ceremony spaces, world-class catering, dedicated wedding coordinators', '3550 Wailea Alanui Drive', 'Maui', 'HI', '96753', 'USA', '8088790100', 'weddings@mauigrand.com', 'www.mauigrand.com', 20.6915, -156.4109, 5, 4.8, 247, 1, 1, TRUE, 'verified', '2024-06-15 08:00:00', '2025-01-20 16:30:00'),
('Bora Bora Luxury Villas', 'Exclusive overwater villa resort in French Polynesia', 'Overwater bungalows, romantic ceremony setups, exclusive beach venues, personal concierge', '12 Route de la Plage', 'Bora Bora', 'QR', '98730', 'USA', '6896040666', 'events@boraboravillas.com', 'www.boraboravillas.com', -16.5004, -151.7415, 6, 4.9, 189, 6, 1, TRUE, 'verified', '2024-05-20 10:30:00', '2025-01-19 14:15:00'),
('Cancun Resort & Spa', 'All-inclusive luxury resort in Cancun with world-class wedding facilities', 'Beachfront gazebo, multiple reception halls, spa packages, unlimited beverages', '1 Boulevard Kukulkan', 'Cancun', 'QR', '77500', 'Mexico', '9988816000', 'weddings@cancunresort.com', 'www.cancunresort.com', 21.1619, -86.8515, 5, 4.6, 312, 3, 3, TRUE, 'verified', '2024-07-10 09:00:00', '2025-01-20 10:15:00'),
('Jamaica Paradise Hotel', 'All-inclusive beachfront resort in Montego Bay', 'Beautiful sunset ceremonies, private beach events, included coordination', '1 Kent Avenue', 'Montego Bay', 'ST', '12345', 'Jamaica', '8765432100', 'events@jamaicaparadise.com', 'www.jamaicaparadise.com', 18.4891, -77.9221, 5, 4.5, 156, 3, 4, TRUE, 'verified', '2024-04-05 11:15:00', '2025-01-18 12:45:00'),
('Key West Ocean View', 'Boutique oceanfront hotel in Key West with intimate wedding spaces', 'Historic charm, sunset venue, personalized ceremonies, local flavor', '1435 Simonton Street', 'Key West', 'FL', '33040', 'USA', '3055961313', 'weddings@keywestoceanview.com', 'www.keywestoceanview.com', 24.5551, -81.7796, 6, 4.4, 98, 2, 5, TRUE, 'verified', '2024-08-20 14:30:00', '2025-01-17 15:20:00'),
('Miami Luxury Downtown', 'Urban luxury hotel in Miami with rooftop event space', 'Rooftop terrace, city views, modern aesthetics, flexible layouts', '500 Brickell Avenue', 'Miami', 'FL', '33131', 'USA', '3055352000', 'events@miamiluxury.com', 'www.miamiluxury.com', 25.7617, -80.1918, 5, 4.3, 87, 7, 6, TRUE, 'verified', '2024-03-15 10:00:00', '2025-01-16 09:30:00'),
('Scottsdale Desert Resort', 'Luxury golf resort with spa in Scottsdale', 'Desert ceremony spaces, championship golf, spa treatments, southwestern cuisine', '7575 East Princess Drive', 'Scottsdale', 'AZ', '85255', 'USA', '4808858555', 'weddings@scottsdale-resort.com', 'www.scottsdale-resort.com', 33.4942, -111.9260, 5, 4.2, 64, 4, 9, TRUE, 'verified', '2024-09-10 13:00:00', '2025-01-15 11:45:00'),
('Charleston Historic Inn', 'Historic boutique inn in downtown Charleston', 'Colonial charm, historic venues, southern hospitality, elegant receptions', '115 Meeting Street', 'Charleston', 'SC', '29401', 'USA', '8434226900', 'weddings@charlestoniinn.com', 'www.charlestoniinn.com', 32.7765, -79.9318, 6, 4.1, 52, 5, 10, TRUE, 'verified', '2024-10-05 15:30:00', '2025-01-14 13:20:00');

-- Insert Hotel Policies
INSERT INTO HotelPolicies (hotel_id, cancellation_policy, cancellation_deadline, group_booking_policy, minimum_group_size, group_discount_percentage, check_in_time, check_out_time, pet_policy, accessibility_policy, wedding_service_policy, updated_at) VALUES
(1, 'Free cancellation up to 14 days before arrival', 14, 'Groups of 10+ receive special rates and dedicated coordinator', 10, 15.00, '15:00:00', '11:00:00', 'Pets allowed with $100 fee', 'ADA compliant rooms available', 'Complimentary wedding coordination for groups over 50 rooms', '2025-01-20 16:30:00'),
(2, 'Non-refundable deposits required, balance due 30 days prior', 30, 'Exclusive group experiences available for 15+ guests', 15, 20.00, '14:00:00', '11:00:00', 'No pets allowed', 'Limited accessibility, contact for information', 'Premium coordination included', '2025-01-19 14:15:00'),
(3, 'Free cancellation up to 7 days before arrival', 7, 'All-inclusive groups receive beverage upgrades', 8, 10.00, '16:00:00', '12:00:00', 'Select pet-friendly rooms available', 'Full ADA accessibility', 'Wedding packages available', '2025-01-18 12:45:00'),
(4, 'Refundable deposit, 21-day cancellation policy', 21, 'Large groups eligible for customized packages', 20, 25.00, '15:00:00', '11:00:00', 'Pets allowed in select areas', 'Accessible accommodations available', 'Wedding specialist on staff', '2025-01-17 15:20:00'),
(5, 'Free cancellation up to 10 days before arrival', 10, 'Group discounts available for 5+ rooms', 5, 12.00, '14:00:00', '10:00:00', 'No pets', 'Limited accessibility', 'Coordination available for fee', '2025-01-16 09:30:00'),
(6, 'Flexible cancellation policy with notice', 5, 'Corporate and wedding groups welcome', 10, 18.00, '16:00:00', '12:00:00', 'Small pets allowed with deposit', 'Fully accessible facility', 'Event planning services included', '2025-01-15 11:45:00'),
(7, 'Standard cancellation with 7-day notice', 7, 'Golf packages available for groups', 12, 14.00, '15:00:00', '11:00:00', 'Pet-friendly with fee', 'Accessible rooms available', 'Golf and spa packages for groups', '2025-01-14 13:20:00'),
(8, 'Historic property - non-refundable bookings', 45, 'Exclusive small group events only', 6, 8.00, '14:00:00', '10:00:00', 'No pets', 'Historic property limitations', 'Boutique coordination service', '2025-01-13 10:00:00');

-- Insert Rooms
INSERT INTO Rooms (hotel_id, room_type_id, room_number, capacity_max_guests, base_price_per_night, base_price_per_weekend, description, is_pet_friendly, is_accessible, is_active, created_at, updated_at) VALUES
(1, 1, '101', 2, 250.00, 350.00, 'Standard room with garden view', FALSE, FALSE, TRUE, '2024-06-15 08:00:00', '2025-01-20 16:30:00'),
(1, 2, '201', 2, 350.00, 450.00, 'Deluxe room with partial ocean view', FALSE, FALSE, TRUE, '2024-06-15 08:00:00', '2025-01-20 16:30:00'),
(1, 3, '301', 4, 550.00, 750.00, 'Ocean view suite with lanai', FALSE, FALSE, TRUE, '2024-06-15 08:00:00', '2025-01-20 16:30:00'),
(1, 4, '401', 2, 750.00, 1000.00, 'Bridal suite with jacuzzi and ocean views', FALSE, TRUE, TRUE, '2024-06-15 08:00:00', '2025-01-20 16:30:00'),
(2, 5, 'V01', 6, 1200.00, 1600.00, 'Overwater family villa', FALSE, FALSE, TRUE, '2024-05-20 10:30:00', '2025-01-19 14:15:00'),
(2, 4, 'B01', 2, 950.00, 1300.00, 'Overwater bridal bungalow', FALSE, TRUE, TRUE, '2024-05-20 10:30:00', '2025-01-19 14:15:00'),
(3, 3, 'CV101', 4, 400.00, 550.00, 'Cancun oceanfront suite', TRUE, FALSE, TRUE, '2024-07-10 09:00:00', '2025-01-20 10:15:00'),
(3, 1, 'C101', 2, 200.00, 300.00, 'Standard all-inclusive room', FALSE, FALSE, TRUE, '2024-07-10 09:00:00', '2025-01-20 10:15:00'),
(4, 2, 'JM201', 2, 300.00, 400.00, 'Deluxe Jamaica beachfront room', TRUE, FALSE, TRUE, '2024-04-05 11:15:00', '2025-01-18 12:45:00'),
(5, 2, 'KW301', 2, 450.00, 600.00, 'Key West ocean view deluxe', FALSE, FALSE, TRUE, '2024-08-20 14:30:00', '2025-01-17 15:20:00'),
(6, 7, 'MB01', 2, 500.00, 700.00, 'Miami rooftop suite', FALSE, TRUE, TRUE, '2024-03-15 10:00:00', '2025-01-16 09:30:00'),
(7, 6, 'SD01', 4, 600.00, 800.00, 'Scottsdale penthouse with desert view', FALSE, FALSE, TRUE, '2024-09-10 13:00:00', '2025-01-15 11:45:00'),
(8, 8, 'CH01', 2, 400.00, 550.00, 'Charleston historic garden room', FALSE, FALSE, TRUE, '2024-10-05 15:30:00', '2025-01-14 13:20:00');

-- Insert Room Amenities
INSERT INTO RoomAmenities (room_id, amenity_id, is_available, added_at) VALUES
(1, 1, TRUE, '2024-06-15 08:00:00'),
(1, 8, TRUE, '2024-06-15 08:00:00'),
(1, 14, TRUE, '2024-06-15 08:00:00'),
(2, 1, TRUE, '2024-06-15 08:00:00'),
(2, 3, TRUE, '2024-06-15 08:00:00'),
(2, 14, TRUE, '2024-06-15 08:00:00'),
(3, 1, TRUE, '2024-06-15 08:00:00'),
(3, 4, TRUE, '2024-06-15 08:00:00'),
(3, 5, TRUE, '2024-06-15 08:00:00'),
(3, 14, TRUE, '2024-06-15 08:00:00'),
(4, 1, TRUE, '2024-06-15 08:00:00'),
(4, 3, TRUE, '2024-06-15 08:00:00'),
(4, 6, TRUE, '2024-06-15 08:00:00'),
(4, 14, TRUE, '2024-06-15 08:00:00'),
(5, 1, TRUE, '2024-05-20 10:30:00'),
(5, 2, TRUE, '2024-05-20 10:30:00'),
(5, 3, TRUE, '2024-05-20 10:30:00'),
(5, 4, TRUE, '2024-05-20 10:30:00'),
(5, 6, TRUE, '2024-05-20 10:30:00'),
(6, 1, TRUE, '2024-05-20 10:30:00'),
(6, 3, TRUE, '2024-05-20 10:30:00'),
(6, 14, TRUE, '2024-05-20 10:30:00'),
(7, 1, TRUE, '2024-07-10 09:00:00'),
(7, 2, TRUE, '2024-07-10 09:00:00'),
(7, 9, TRUE, '2024-07-10 09:00:00'),
(8, 1, TRUE, '2024-07-10 09:00:00'),
(8, 14, TRUE, '2024-07-10 09:00:00'),
(9, 1, TRUE, '2024-04-05 11:15:00'),
(9, 2, TRUE, '2024-04-05 11:15:00'),
(9, 11, TRUE, '2024-04-05 11:15:00'),
(9, 14, TRUE, '2024-04-05 11:15:00'),
(10, 1, TRUE, '2024-08-20 14:30:00'),
(10, 11, TRUE, '2024-08-20 14:30:00'),
(10, 14, TRUE, '2024-08-20 14:30:00'),
(11, 1, TRUE, '2024-03-15 10:00:00'),
(11, 8, TRUE, '2024-03-15 10:00:00'),
(11, 9, TRUE, '2024-03-15 10:00:00'),
(12, 1, TRUE, '2024-09-10 13:00:00'),
(12, 3, TRUE, '2024-09-10 13:00:00'),
(12, 10, TRUE, '2024-09-10 13:00:00'),
(13, 1, TRUE, '2024-10-05 15:30:00'),
(13, 8, TRUE, '2024-10-05 15:30:00'),
(13, 14, TRUE, '2024-10-05 15:30:00');

-- Insert Availability
INSERT INTO Availability (room_id, date, available_count, booked_count, price_per_night, pricing_tier_id, is_blocked, last_updated, updated_by_user_id) VALUES
(1, '2025-02-14', 3, 0, 250.00, 2, FALSE, '2025-01-20 12:00:00', 5),
(1, '2025-02-15', 3, 0, 250.00, 2, FALSE, '2025-01-20 12:00:00', 5),
(1, '2025-03-01', 3, 0, 250.00, 2, FALSE, '2025-01-20 12:00:00', 5),
(2, '2025-02-14', 2, 0, 350.00, 2, FALSE, '2025-01-20 12:00:00', 5),
(2, '2025-02-15', 2, 0, 350.00, 2, FALSE, '2025-01-20 12:00:00', 5),
(3, '2025-02-14', 1, 0, 550.00, 2, FALSE, '2025-01-20 12:00:00', 5),
(3, '2025-02-15', 1, 0, 550.00, 2, FALSE, '2025-01-20 12:00:00', 5),
(4, '2025-02-14', 1, 0, 750.00, 2, FALSE, '2025-01-20 12:00:00', 5),
(4, '2025-02-15', 1, 0, 750.00, 2, FALSE, '2025-01-20 12:00:00', 5),
(5, '2025-04-01', 1, 0, 1200.00, 3, FALSE, '2025-01-19 12:00:00', 6),
(5, '2025-04-02', 1, 0, 1200.00, 3, FALSE, '2025-01-19 12:00:00', 6),
(6, '2025-04-01', 1, 0, 950.00, 3, FALSE, '2025-01-19 12:00:00', 6),
(7, '2025-03-15', 2, 0, 400.00, 2, FALSE, '2025-01-20 12:00:00', 5),
(8, '2025-03-15', 4, 0, 200.00, 2, FALSE, '2025-01-20 12:00:00', 5),
(9, '2025-05-10', 3, 0, 300.00, 2, FALSE, '2025-01-18 12:00:00', 5),
(10, '2025-06-01', 2, 0, 450.00, 1, FALSE, '2025-01-17 12:00:00', 6),
(11, '2025-07-04', 1, 0, 500.00, 1, FALSE, '2025-01-16 12:00:00', 5),
(12, '2025-05-20', 1, 0, 600.00, 2, FALSE, '2025-01-15 12:00:00', 5),
(13, '2025-04-12', 2, 0, 400.00, 2, FALSE, '2025-01-14 12:00:00', 6);

-- ============================================================
-- BOOKING DATA
-- ============================================================

-- Insert Bookings
INSERT INTO Bookings (booking_number, user_id, hotel_id, check_in_date, check_out_date, total_guests, wedding_date, special_requests, base_cost, tax_amount, service_fees, discount_amount, total_cost, booking_status, payment_status, booking_type, group_size, created_at, updated_at) VALUES
('BK-2025-001', 1, 1, '2025-02-14', '2025-02-17', 6, '2025-02-14', 'Early check-in if possible', 1700.00, 170.00, 100.00, 0.00, 1970.00, 'confirmed', 'completed', 'group', 6, '2025-01-10 10:00:00', '2025-01-15 14:30:00'),
('BK-2025-002', 2, 3, '2025-03-15', '2025-03-20', 12, '2025-03-17', 'Special setup for ceremonies', 2400.00, 240.00, 150.00, 0.00, 2790.00, 'confirmed', 'completed', 'group', 12, '2025-01-12 11:15:00', '2025-01-16 09:45:00'),
('BK-2025-003', 1, 2, '2025-04-01', '2025-04-04', 2, '2025-04-02', 'Honeymoon package requested', 2850.00, 285.00, 100.00, 150.00, 3085.00, 'confirmed', 'deposit_received', 'individual', NULL, '2025-01-14 13:30:00', '2025-01-18 15:00:00'),
('BK-2025-004', 8, 5, '2025-06-01', '2025-06-04', 5, '2025-06-02', 'Late checkout requested', 1500.00, 150.00, 75.00, 0.00, 1725.00, 'pending', 'pending', 'individual', NULL, '2025-01-17 14:45:00', '2025-01-17 14:45:00'),
('BK-2025-005', 2, 7, '2025-05-20', '2025-05-23', 8, '2025-05-21', 'Groom golf outing requested', 1800.00, 180.00, 100.00, 0.00, 2080.00, 'confirmed', 'completed', 'group', 8, '2025-01-13 09:00:00', '2025-01-19 11:30:00');

-- Insert Booking Rooms
INSERT INTO BookingRooms (booking_id, room_id, quantity, price_per_night, total_nights, subtotal_price) VALUES
(1, 1, 2, 250.00, 3, 1500.00),
(1, 2, 1, 350.00, 3, 1050.00),
(2, 7, 3, 400.00, 5, 6000.00),
(2, 8, 4, 200.00, 5, 4000.00),
(3, 6, 1, 950.00, 3, 2850.00),
(4, 10, 1, 450.00, 3, 1350.00),
(5, 12, 1, 600.00, 3, 1800.00);

-- ============================================================
-- REVIEW & RATING DATA
-- ============================================================

-- Insert Reviews
INSERT INTO Reviews (hotel_id, user_id, booking_id, overall_rating, review_title, review_text, verified_booker, helpful_count, moderation_status, is_wedding_review, created_at, updated_at, hotel_response, hotel_response_date) VALUES
(1, 1, 1, 5, 'Perfect Wedding Destination!', 'Amazing experience! The hotel staff was incredibly helpful with our wedding coordination. Beautiful venue, excellent food, and stunning ocean views. Highly recommend for destination weddings.', TRUE, 18, 'approved', TRUE, '2025-01-18 10:30:00', '2025-01-18 10:30:00', 'Thank you for choosing us! We loved being part of your special day.', '2025-01-19 09:00:00'),
(3, 2, 2, 4, 'Great All-Inclusive Resort', 'Wonderful wedding reception venue. Excellent coordination team, great food variety. Only minor issue with room temperature control. Would stay again.', TRUE, 12, 'approved', TRUE, '2025-01-16 14:20:00', '2025-01-16 14:20:00', 'We appreciate your feedback and will address the HVAC issue.', '2025-01-17 10:15:00'),
(2, 1, 3, 5, 'Honeymoon Paradise', 'Absolutely breathtaking! The overwater bungalow was the most romantic setting we could have imagined. Perfect for our honeymoon. Staff was attentive and professional.', TRUE, 24, 'approved', FALSE, '2025-01-15 16:45:00', '2025-01-15 16:45:00', 'So glad you had an unforgettable honeymoon with us!', '2025-01-16 14:00:00'),
(7, 2, 5, 4, 'Excellent Golf & Wedding Venue', 'Great property for our destination wedding. Golf course was in excellent condition, spa services top-notch. Some coordination issues but overall very happy.', TRUE, 8, 'approved', TRUE, '2025-01-19 11:00:00', '2025-01-19 11:00:00', 'Thank you! We will improve our coordination processes.', '2025-01-20 08:30:00'),
(4, 2, 2, 4, 'Beautiful Jamaica Resort', 'Fantastic beachfront location for our wedding guests. All-inclusive was convenient. Friendly staff. A few areas could use updating but overall excellent.', TRUE, 6, 'approved', TRUE, '2025-01-17 13:15:00', '2025-01-17 13:15:00', 'We appreciate your business and look forward to your next visit!', '2025-01-18 09:30:00');

-- Insert Review Ratings
INSERT INTO ReviewRatings (review_id, rating_dimension, rating_score) VALUES
(1, 'amenities', 5),
(1, 'service', 5),
(1, 'value', 5),
(1, 'wedding_coordination', 5),
(1, 'cleanliness', 5),
(1, 'location', 5),
(2, 'amenities', 4),
(2, 'service', 5),
(2, 'value', 4),
(2, 'wedding_coordination', 4),
(2, 'cleanliness', 4),
(2, 'location', 5),
(3, 'amenities', 5),
(3, 'service', 5),
(3, 'value', 5),
(3, 'cleanliness', 5),
(3, 'location', 5),
(4, 'amenities', 4),
(4, 'service', 4),
(4, 'value', 4),
(4, 'wedding_coordination', 4),
(4, 'cleanliness', 4),
(4, 'location', 4),
(5, 'amenities', 4),
(5, 'service', 4),
(5, 'value', 4),
(5, 'wedding_coordination', 3),
(5, 'cleanliness', 4),
(5, 'location', 5);

-- ============================================================
-- SEARCH QUERY DATA
-- ============================================================

-- Insert Search Queries
INSERT INTO SearchQueries (user_id, search_location, location_id, check_in_date, check_out_date, min_guests, max_guests, min_budget, max_budget, amenities_filter, results_count, clicked_hotel_id, lead_to_booking, created_at) VALUES
(1, 'Maui, Hawaii', 1, '2025-02-14', '2025-02-17', 4, 8, 5000.00, 15000.00, '["4", "5", "6"]', 8, 1, TRUE, '2025-01-10 09:30:00'),
(2, 'Cancun, Mexico', 3, '2025-03-15', '2025-03-20', 10, 20, 8000.00, 25000.00, '["4", "5", "6", "14", "15"]', 12, 3, TRUE, '2025-01-12 10:15:00'),
(1, 'Bora Bora, French Polynesia', 1, '2025-04-01', '2025-04-05', 2, 2, 7000.00, 20000.00, '["6", "14"]', 3, 2, TRUE, '2025-01-14 11:45:00'),
(8, 'Key West, Florida', 5, '2025-06-01', '2025-06-05', 3, 6, 3000.00, 8000.00, '["4", "11"]', 6, 5, TRUE, '2025-01-17 13:20:00'),
(7, 'Hawaii', 1, '2025-05-01', '2025-05-10', 5, 10, 6000.00, 18000.00, '["4", "5", "7", "8"]', 10, 1, FALSE, '2025-01-15 14:00:00'),
(4, 'Cancun, Mexico', 3, '2025-06-20', '2025-06-25', 8, 15, 5000.00, 15000.00, '["3", "5", "6"]', 9, 3, FALSE, '2025-01-16 15:30:00'),
(3, 'Charleston, South Carolina', 10, '2025-04-10', '2025-04-13', 6, 12, 4000.00, 10000.00, '["4", "5"]', 4, 8, FALSE, '2025-01-13 16:45:00'),
(1, 'Miami, Florida', 6, '2025-07-04', '2025-07-07', 4, 8, 6000.00, 15000.00, '["4", "9", "14", "15"]', 7, 6, FALSE, '2025-01-11 09:00:00');

-- ============================================================
-- END OF DATA POPULATION
-- ============================================================
-- Total Records Inserted:
-- UserRoles: 5
-- Users: 8
-- UserProfiles: 8
-- Locations: 10
-- HotelCategories: 8
-- RoomTypes: 8
-- Amenities: 15
-- PricingTiers: 5
-- Hotels: 8
-- HotelPolicies: 8
-- Rooms: 14
-- RoomAmenities: 47
-- Availability: 19
-- Bookings: 5
-- BookingRooms: 7
-- Reviews: 5
-- ReviewRatings: 29
-- SearchQueries: 8
--
-- Total: 203 records across 18 tables
-- ============================================================
