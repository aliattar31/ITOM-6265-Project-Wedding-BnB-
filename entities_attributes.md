
# Entities & Attributes (With Datatypes)

---

# **1. Users**
Stores planners, customers, and admin accounts.

| Attribute | Datatype | Description |
|----------|----------|-------------|
| user_id (PK) | INT AUTO_INCREMENT | Unique identifier |
| role | ENUM('admin','planner','customer') | User category |
| first_name | VARCHAR(50) | First name |
| last_name | VARCHAR(50) | Last name |
| email | VARCHAR(100), UNIQUE | Login email |
| password_hash | VARCHAR(255) | Encrypted password |
| phone_number | VARCHAR(20) | Contact |
| is_active | TINYINT(1) | Active or disabled |
| created_at | DATETIME | Timestamp |
| updated_at | DATETIME | Timestamp |

---

# **2. Hotels**
Basic hotel/destination information.

| Attribute | Datatype | Description |
|----------|----------|-------------|
| hotel_id (PK) | INT AUTO_INCREMENT | Unique hotel ID |
| hotel_name | VARCHAR(150) | Name |
| city | VARCHAR(100) | City |
| state | VARCHAR(100) | State |
| country | VARCHAR(100) | Country |
| address | VARCHAR(255) | Full address |
| description | TEXT | Hotel overview |
| base_price | DECIMAL(10,2) | Starting price per night |
| total_rooms | INT | Total rooms available |
| average_rating | DECIMAL(3,2) | Computed from Ratings table |
| main_image_url | VARCHAR(255) | Optional image URL |
| created_at | DATETIME | Timestamp |
| updated_at | DATETIME | Timestamp |

---

# **3. Rooms**
Simplified — instead of various room types, we keep a single room pool per hotel.

| Attribute | Datatype | Description |
|----------|----------|-------------|
| room_id (PK) | INT AUTO_INCREMENT | Unique ID |
| hotel_id (FK) | INT | Linked to Hotels |
| date | DATE | Date availability applies |
| available_rooms | INT | Rooms free on this date |
| price | DECIMAL(10,2) | Price per night (can vary by date) |
| created_at | DATETIME | Timestamp |
| updated_at | DATETIME | Timestamp |

---

# **4. Bookings**
Tracks reservations made by users.

| Attribute | Datatype | Description |
|----------|----------|-------------|
| booking_id (PK) | INT AUTO_INCREMENT | Booking ID |
| user_id (FK) | INT | Who booked |
| hotel_id (FK) | INT | Hotel |
| check_in_date | DATE | Start date |
| check_out_date | DATE | End date |
| number_of_rooms | INT | Rooms booked |
| number_of_guests | INT | Guests |
| total_price | DECIMAL(10,2) | Final price |
| booking_status | ENUM('pending','confirmed','cancelled') | Status |
| created_at | DATETIME | Timestamp |
| updated_at | DATETIME | Timestamp |

---

# **5. Ratings** (Replaces Reviews)
Used for analytics, comparisons, and average-rating calculations.

| Attribute | Datatype | Description |
|----------|----------|-------------|
| rating_id (PK) | INT AUTO_INCREMENT | Unique ID |
| hotel_id (FK) | INT | Hotel being rated |
| user_id (FK) | INT | Who rated |
| rating_value | INT CHECK (rating_value BETWEEN 1 AND 5) | Rating (1–5 stars) |
| rating_date | DATE | When user rated |
| created_at | DATETIME | Timestamp |

---

# **6. Booking_Requests** (Optional but lightweight)
For planners who want to request before confirming.

| Attribute | Datatype | Description |
|----------|----------|-------------|
| request_id (PK) | INT AUTO_INCREMENT | Unique ID |
| user_id (FK) | INT | Planner/customer |
| hotel_id (FK) | INT | Hotel |
| desired_check_in | DATE | Preferred |
| desired_check_out | DATE | Preferred |
| guests | INT | Guest count |
| status | ENUM('pending','approved','rejected') | Request state |
| created_at | DATETIME | Timestamp |

---

