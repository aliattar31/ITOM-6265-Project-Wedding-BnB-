# Wedding Destination Hotel Finder - Backend API Specification

**Version**: 1.0  
**Date**: November 25, 2025  
**Framework**: Flask (Python) or Express (Node.js) - Choose one

---

## 1. Project Structure & Setup

### Option A: Python Flask Backend

```
backend/
├── app.py                      # Main Flask application
├── config.py                   # Configuration (dev, test, prod)
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (DO NOT COMMIT)
├── .flaskenv                   # Flask-specific env vars
├── Dockerfile                  # Container configuration
├── wsgi.py                     # Production entry point
├── models/
│   ├── __init__.py
│   ├── user.py                 # User model
│   ├── hotel.py                # Hotel model
│   ├── booking.py              # Booking model
│   ├── review.py               # Review model
│   └── amenity.py              # Amenity model
├── routes/
│   ├── __init__.py
│   ├── auth.py                 # Authentication endpoints
│   ├── hotels.py               # Hotel CRUD & search
│   ├── bookings.py             # Booking management
│   ├── reviews.py              # Reviews & ratings
│   ├── search.py               # Advanced search
│   ├── comparisons.py          # Hotel comparison
│   ├── analytics.py            # Analytics & reporting
│   └── admin.py                # Admin endpoints
├── services/
│   ├── __init__.py
│   ├── booking_service.py      # Booking logic
│   ├── search_service.py       # Search algorithm
│   ├── recommendation_service.py # Recommendation engine
│   ├── email_service.py        # Email notifications
│   └── payment_service.py      # Payment processing
├── utils/
│   ├── __init__.py
│   ├── decorators.py           # Auth decorators
│   ├── validators.py           # Input validation
│   ├── jwt_handler.py          # JWT token logic
│   └── helpers.py              # Utility functions
├── database/
│   ├── __init__.py
│   └── db.py                   # SQLAlchemy setup
└── tests/
    ├── __init__.py
    ├── test_auth.py
    ├── test_hotels.py
    ├── test_bookings.py
    └── test_search.py
```

### Option B: Node.js Express Backend

```
backend/
├── server.js                   # Main application
├── config/
│   ├── database.js
│   ├── env.js
│   └── jwt.js
├── controllers/
│   ├── authController.js
│   ├── hotelController.js
│   ├── bookingController.js
│   ├── reviewController.js
│   └── analyticsController.js
├── routes/
│   ├── index.js
│   ├── auth.js
│   ├── hotels.js
│   ├── bookings.js
│   ├── reviews.js
│   └── admin.js
├── models/
│   ├── User.js
│   ├── Hotel.js
│   ├── Booking.js
│   └── Review.js
├── middleware/
│   ├── auth.js
│   ├── validation.js
│   └── errorHandler.js
├── services/
│   ├── bookingService.js
│   ├── searchService.js
│   ├── emailService.js
│   └── recommendationService.js
├── utils/
│   ├── logger.js
│   ├── helpers.js
│   └── validators.js
└── tests/
```

---

## 2. Environment Variables (.env)

```env
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=wedding_hotel_finder
DB_POOL_SIZE=10

# Server
NODE_ENV=development
PORT=5000
LOG_LEVEL=debug

# JWT
JWT_SECRET=your_secret_key_min_32_chars
JWT_EXPIRATION=7d

# Email Service
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=noreply@wedding-hotel-finder.com

# Payment Processing
STRIPE_SECRET_KEY=sk_test_xxxxx
STRIPE_PUBLIC_KEY=pk_test_xxxxx

# AWS S3 (for image uploads)
AWS_ACCESS_KEY_ID=xxxxx
AWS_SECRET_ACCESS_KEY=xxxxx
AWS_REGION=us-east-1
S3_BUCKET_NAME=wedding-hotel-images

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000
FRONTEND_PROD_URL=https://wedding-hotel-finder.com

# API Base URL
API_BASE_URL=http://localhost:5000/api
```

---

## 3. API Endpoints Overview

### Authentication (Public)
```
POST   /api/auth/register          Register new user
POST   /api/auth/login             Login user
POST   /api/auth/logout            Logout user
POST   /api/auth/refresh-token     Refresh JWT token
POST   /api/auth/forgot-password   Request password reset
POST   /api/auth/reset-password    Reset password with token
GET    /api/auth/verify-email      Verify email address
```

### Users (Protected)
```
GET    /api/users/profile          Get current user profile
PUT    /api/users/profile          Update user profile
PUT    /api/users/password         Change password
DELETE /api/users/account          Delete user account
GET    /api/users/:userId          Get user details (admin only)
```

### Hotels (Public)
```
GET    /api/hotels                 List all hotels (with filters)
GET    /api/hotels/:hotelId        Get hotel details
GET    /api/hotels/search          Advanced hotel search
GET    /api/hotels/:hotelId/amenities  Get hotel amenities
GET    /api/hotels/:hotelId/reviews    Get hotel reviews
GET    /api/hotels/:hotelId/images     Get hotel image gallery
```

### Hotel Management (Admin/Hotel Manager)
```
POST   /api/hotels                 Create new hotel
PUT    /api/hotels/:hotelId        Update hotel details
DELETE /api/hotels/:hotelId        Deactivate hotel
POST   /api/hotels/:hotelId/images Upload hotel images
PUT    /api/hotels/:hotelId/rooms  Manage room inventory
```

### Rooms (Public & Protected)
```
GET    /api/hotels/:hotelId/rooms  List hotel rooms
GET    /api/rooms/:roomId          Get room details
GET    /api/rooms/:roomId/availability  Check availability
GET    /api/rooms/:roomId/pricing     Get pricing info
```

### Availability & Pricing (Public)
```
GET    /api/availability           Check room availability
GET    /api/availability/:roomId/dates  Availability calendar
POST   /api/pricing                Add pricing (admin only)
PUT    /api/pricing/:pricingId     Update pricing
DELETE /api/pricing/:pricingId     Remove pricing
```

### Bookings (Protected)
```
POST   /api/bookings               Create new booking
GET    /api/bookings               List user's bookings
GET    /api/bookings/:bookingId    Get booking details
PUT    /api/bookings/:bookingId    Update booking
DELETE /api/bookings/:bookingId    Cancel booking
POST   /api/bookings/:bookingId/confirm  Confirm booking
POST   /api/bookings/:bookingId/payment  Process payment
GET    /api/bookings/:bookingId/invoice  Get booking invoice
```

### Booking Inquiries (Protected)
```
POST   /api/inquiries              Create booking inquiry
GET    /api/inquiries              Get user's inquiries
GET    /api/inquiries/:inquiryId   Get inquiry details
PUT    /api/inquiries/:inquiryId   Update inquiry
POST   /api/inquiries/:inquiryId/response  Respond to inquiry
```

### Reviews & Ratings (Protected)
```
GET    /api/reviews                List reviews
GET    /api/reviews/hotel/:hotelId Get hotel reviews
POST   /api/reviews                Create review
PUT    /api/reviews/:reviewId      Update review
DELETE /api/reviews/:reviewId      Delete review
POST   /api/reviews/:reviewId/helpful  Mark review as helpful
```

### Search & Discovery (Public)
```
GET    /api/search/hotels          Search with advanced filters
GET    /api/search/destinations    Popular destinations
GET    /api/search/trending        Trending wedding locations
POST   /api/search/save            Save search preferences
GET    /api/search/saved           Get saved searches
```

### Recommendations (Public/Protected)
```
POST   /api/recommendations/generate  Get hotel recommendations
GET    /api/recommendations/best-match  Best match hotel
POST   /api/comparisons             Create comparison report
GET    /api/comparisons/:comparisonId  Get comparison details
```

### Analytics (Protected)
```
GET    /api/analytics/hotel/:hotelId  Hotel analytics
GET    /api/analytics/bookings       Booking statistics
GET    /api/analytics/revenue        Revenue reports
GET    /api/analytics/occupancy      Occupancy rates
POST   /api/analytics/export         Export analytics
```

### Admin (Admin Only)
```
GET    /api/admin/users             List all users
GET    /api/admin/hotels            Manage hotels
POST   /api/admin/report            Generate custom report
DELETE /api/admin/review/:reviewId  Remove inappropriate review
POST   /api/admin/email/send        Send admin email
```

---

## 4. Request/Response Format

### Standard Response Format

**Success Response (2xx)**
```json
{
  "success": true,
  "status": 200,
  "message": "Operation completed successfully",
  "data": {
    // Response data
  },
  "timestamp": "2025-11-25T10:30:00Z"
}
```

**Error Response (4xx, 5xx)**
```json
{
  "success": false,
  "status": 400,
  "error": "Invalid input",
  "message": "The check_in_date must be a valid date",
  "details": {
    "field": "check_in_date",
    "value": "invalid-date",
    "rule": "date"
  },
  "timestamp": "2025-11-25T10:30:00Z"
}
```

### Pagination Response

```json
{
  "success": true,
  "data": [
    // Array of items
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8,
    "hasNext": true,
    "hasPrev": false
  }
}
```

---

## 5. Authentication & Authorization

### JWT Token Structure

```
Header:
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload:
{
  "sub": "user_id_123",
  "email": "user@example.com",
  "role": "Customer",
  "iat": 1700000000,
  "exp": 1700604800
}
```

### Authorization Levels

```
1. Public: No authentication required
2. Customer: Logged-in users
3. Planner: Wedding planners
4. HotelManager: Hotel staff
5. Admin: System administrators
```

### Middleware Order

```
1. CORS
2. Body Parser
3. Logger
4. Auth (Extract JWT)
5. Route Handler
6. Error Handler
```

---

## 6. Core Endpoints - Detailed Specifications

### 6.1 Hotel Search Endpoint

**GET /api/search/hotels**

Query Parameters:
```
city (string, required): City name
state (string, required): State code
check_in_date (date, required): YYYY-MM-DD
check_out_date (date, required): YYYY-MM-DD
guests (integer): Number of guests
rooms (integer): Number of rooms
budget_min (decimal): Minimum price per night
budget_max (decimal): Maximum price per night
min_rating (decimal): Minimum star rating
amenities (array): Required amenities (comma-separated)
category (string): Hotel category
sort_by (string): 'rating', 'price', 'distance'
page (integer): Page number (default: 1)
limit (integer): Results per page (default: 20)
```

Response:
```json
{
  "success": true,
  "data": [
    {
      "hotel_id": 1,
      "hotel_name": "Oceanside Resort Miami",
      "city": "Miami",
      "state": "FL",
      "category": "Beach Resort",
      "star_rating": 4.7,
      "total_reviews": 234,
      "avg_rating": 4.7,
      "price_per_night": 450,
      "available_rooms": 5,
      "is_wedding_venue": true,
      "amenities": ["WiFi", "Pool", "Spa", "Ballroom"],
      "match_score": 92.5,
      "image_url": "url_to_main_image"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "pages": 3
  }
}
```

---

### 6.2 Booking Creation Endpoint

**POST /api/bookings**

Request:
```json
{
  "hotel_id": 1,
  "check_in_date": "2025-06-01",
  "check_out_date": "2025-06-05",
  "number_of_guests": 4,
  "number_of_rooms": 2,
  "rooms": [
    {
      "room_type_id": 2,
      "number_of_nights": 4,
      "guest_names": "John Doe, Jane Doe"
    },
    {
      "room_type_id": 1,
      "number_of_nights": 4,
      "guest_names": "Guest 3, Guest 4"
    }
  ],
  "wedding_event_name": "John & Jane's Wedding",
  "special_requests": "Room with ocean view preferred",
  "is_group_booking": false
}
```

Response:
```json
{
  "success": true,
  "status": 201,
  "message": "Booking created successfully",
  "data": {
    "booking_id": 1,
    "booking_code": "BK-20250601-001",
    "hotel_id": 1,
    "hotel_name": "Oceanside Resort Miami",
    "check_in_date": "2025-06-01",
    "check_out_date": "2025-06-05",
    "number_of_nights": 4,
    "rooms": [
      {
        "booking_room_id": 1,
        "room_id": 101,
        "room_number": "101",
        "nightly_rate": 250,
        "subtotal": 1000
      }
    ],
    "total_booking_cost": 2000,
    "tax_amount": 240,
    "final_amount_due": 2240,
    "booking_status": "pending",
    "payment_status": "pending",
    "created_at": "2025-11-25T10:30:00Z"
  }
}
```

---

### 6.3 Recommendation Endpoint

**POST /api/recommendations/generate**

Request:
```json
{
  "location": "Miami",
  "check_in_date": "2025-06-01",
  "check_out_date": "2025-06-05",
  "guest_count": 50,
  "budget_per_room": 300,
  "preferences": {
    "categories": ["Resort", "Beach"],
    "amenities": ["Ballroom", "Catering", "Wedding Coordinator"],
    "min_rating": 4.5,
    "priorities": ["rating", "wedding_coordination", "reviews"]
  }
}
```

Response:
```json
{
  "success": true,
  "data": {
    "best_match": {
      "hotel_id": 1,
      "hotel_name": "Oceanside Resort Miami",
      "match_score": 95.2,
      "reason": "Excellent for destination weddings with top-rated service",
      "star_rating": 4.7,
      "total_reviews": 234,
      "estimated_total_cost": 6000,
      "available_rooms": 25
    },
    "alternatives": [
      {
        "hotel_id": 2,
        "hotel_name": "Paradise Resort",
        "match_score": 88.3,
        "estimated_total_cost": 5500
      }
    ],
    "analysis": {
      "budget_fit": "Good - estimated $6000 for 50 guests",
      "availability": "Excellent - 25+ rooms available",
      "wedding_suitability": "Perfect - specialized wedding services"
    }
  }
}
```

---

### 6.4 Analytics Endpoint

**GET /api/analytics/hotel/:hotelId**

Query Parameters:
```
start_date (date): Start date for analytics
end_date (date): End date for analytics
metrics (array): Specific metrics to retrieve
granularity (string): 'daily', 'weekly', 'monthly'
```

Response:
```json
{
  "success": true,
  "data": {
    "hotel_id": 1,
    "hotel_name": "Oceanside Resort Miami",
    "summary": {
      "total_bookings": 45,
      "completed_bookings": 42,
      "cancelled_bookings": 3,
      "total_revenue": 95000,
      "avg_booking_value": 2111.11,
      "occupancy_rate": 78.5
    },
    "trends": [
      {
        "date": "2025-11-20",
        "bookings": 3,
        "revenue": 6500,
        "occupancy": 85
      }
    ],
    "charts": {
      "revenue_trend": [],
      "occupancy_trend": [],
      "booking_status_distribution": {}
    }
  }
}
```

---

## 7. Error Handling & Status Codes

### Standard HTTP Status Codes

```
200 OK                   - Request succeeded
201 Created             - Resource created successfully
204 No Content          - Successful request, no content to return
400 Bad Request         - Invalid input parameters
401 Unauthorized        - Missing or invalid authentication
403 Forbidden           - Authenticated but not authorized
404 Not Found           - Resource doesn't exist
409 Conflict            - Resource conflict (e.g., double booking)
422 Unprocessable       - Validation failed
429 Too Many Requests   - Rate limit exceeded
500 Server Error        - Unexpected server error
503 Service Unavailable - Service temporarily down
```

### Error Code Examples

```
ERR_INVALID_DATES        - Check-out before check-in
ERR_NO_AVAILABILITY      - No rooms available for dates
ERR_DOUBLE_BOOKING       - Room already booked
ERR_INVALID_GUEST_COUNT  - Guest count exceeds room capacity
ERR_UNAUTHORIZED_BOOKING - User cannot modify this booking
ERR_PAYMENT_FAILED       - Payment processing failed
ERR_INVALID_COUPON       - Coupon code invalid or expired
```

---

## 8. Input Validation Rules

### User Registration

```
email:
  - Required
  - Valid email format
  - Unique in database
  - Max 255 characters

password:
  - Required
  - Min 8 characters
  - Must include: uppercase, lowercase, number, special char
  - Not common/breached passwords

first_name, last_name:
  - Required
  - 2-100 characters
  - Letters, spaces, hyphens only

phone_number:
  - Optional
  - Valid phone format
  - 10-20 characters
```

### Hotel Search

```
city, state:
  - Required
  - Valid format
  - Max 100 characters

check_in_date:
  - Required
  - Valid date format (YYYY-MM-DD)
  - Must be >= today
  - Must be < check_out_date

check_out_date:
  - Required
  - Valid date format
  - Must be > check_in_date
  - Max 365 days in future

guests, rooms:
  - Integer
  - >= 1
  - <= 999

budget_min, budget_max:
  - Decimal with 2 places
  - >= 0
  - budget_min <= budget_max
```

### Booking Creation

```
hotel_id:
  - Required
  - Integer
  - Hotel must exist and be active

check_in_date, check_out_date:
  - Required
  - Valid dates
  - >= today
  - Hotel must have availability

rooms:
  - Required
  - Array with 1+ items
  - Each room must exist
  - Total capacity >= guests

special_requests:
  - Optional
  - Max 1000 characters
```

---

## 9. Database Integration

### SQLAlchemy (Python Flask)

```python
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}

db = SQLAlchemy(app)
```

### Sequelize/TypeORM (Node.js)

```javascript
// Sequelize example
const sequelize = new Sequelize(
  process.env.DB_NAME,
  process.env.DB_USER,
  process.env.DB_PASSWORD,
  {
    host: process.env.DB_HOST,
    port: process.env.DB_PORT,
    dialect: 'mysql',
    pool: {
      max: 10,
      min: 0,
      acquire: 30000,
      idle: 10000
    }
  }
);
```

---

## 10. Key Features Implementation

### Real-Time Availability Checking

```python
def check_availability(room_id, check_in, check_out):
    """
    Check if room is available for date range
    """
    conflicts = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.booking_status.in_(['confirmed', 'paid']),
        Booking.check_in_date < check_out,
        Booking.check_out_date > check_in
    ).count()
    
    return conflicts == 0
```

### Price Calculation with Surcharges

```python
def calculate_booking_cost(room_id, check_in, check_out):
    """
    Calculate total cost including weekend/peak surcharges
    """
    nights = (check_out - check_in).days
    total = 0
    
    for day in range(nights):
        current_date = check_in + timedelta(days=day)
        pricing = Pricing.query.filter_by(
            room_id=room_id,
            pricing_date=current_date
        ).first()
        
        nightly_rate = pricing.nightly_rate
        
        # Add weekend surcharge
        if current_date.weekday() >= 4:  # Friday=4, Saturday=5
            nightly_rate += pricing.weekend_surcharge or 0
        
        total += nightly_rate
    
    return total
```

### Recommendation Algorithm

```python
def generate_recommendations(location, guests, budget, preferences):
    """
    AI-based hotel recommendation engine
    Scoring: Rating (40%) + Reviews (30%) + Wedding Suitability (20%) + Value (10%)
    """
    hotels = Hotel.query.filter_by(
        location_id=location.location_id,
        is_active=True
    ).all()
    
    scored_hotels = []
    
    for hotel in hotels:
        score = 0
        
        # Rating score (0-40)
        score += hotel.star_rating * 8.5 if hotel.star_rating else 0
        
        # Review count score (0-30)
        review_score = min(hotel.total_reviews / 10, 30)
        score += review_score
        
        # Wedding suitability (0-20)
        if hotel.is_wedding_venue:
            score += 20
        
        # Value score (0-10)
        if hotel.average_price_per_night <= budget:
            score += 10
        
        scored_hotels.append({
            'hotel': hotel,
            'score': score,
            'value': hotel.average_price_per_night
        })
    
    return sorted(scored_hotels, key=lambda x: x['score'], reverse=True)[:5]
```

---

## 11. Performance Considerations

### Database Indexing Strategy

```sql
-- Fast search queries
CREATE INDEX idx_search_primary ON Hotels(location_id, is_active, star_rating);

-- Booking conflict detection
CREATE INDEX idx_booking_conflicts ON Bookings(hotel_id, check_in_date, check_out_date);

-- Availability queries
CREATE INDEX idx_availability_fast ON Availability(room_id, available_date, is_blocked);

-- Analytics queries
CREATE INDEX idx_analytics_fast ON Bookings(hotel_id, created_at, booking_status);
```

### Caching Strategy

```
- Cache hotel listings by city (1 hour)
- Cache hotel details (2 hours)
- Cache reviews (1 hour)
- Cache pricing data (15 minutes)
- Cache availability (Real-time - no cache)
- Cache user profiles (On login)
```

---

## 12. Security Best Practices

### Password Security
- Hash with bcrypt (cost: 12)
- Never store plain text
- Min 8 chars: uppercase, lowercase, number, special

### API Security
- CORS enabled only for frontend
- Rate limiting: 100 requests/minute per IP
- Input validation on all endpoints
- SQL injection prevention (parameterized queries)
- XSS protection (sanitize outputs)

### JWT Security
- Secret key: Min 32 random characters
- Expiration: 7 days
- Refresh tokens stored in httpOnly cookies
- No sensitive data in JWT payload

### File Uploads
- Only images allowed
- Max file size: 10MB
- Store in S3, not local disk
- Virus scanning for uploads

---

## 13. Testing Strategy

### Unit Tests
```
- Model validation
- Utility functions
- Business logic
- Target: 80%+ coverage
```

### Integration Tests
```
- Database operations
- API endpoints
- Service interactions
- Payment processing
```

### End-to-End Tests
```
- Complete booking flow
- Search and recommendation
- User authentication
- Admin functions
```

---

## 14. Deployment Checklist

```
Database:
  ✓ Create production database
  ✓ Run all migrations
  ✓ Seed initial data
  ✓ Verify backups configured
  ✓ Test recovery procedures

Backend:
  ✓ Environment variables configured
  ✓ SSL certificate installed
  ✓ Rate limiting enabled
  ✓ Error logging setup
  ✓ Monitoring/alerts configured
  ✓ Caching setup (Redis)
  ✓ Email service tested
  ✓ Payment processing configured

Security:
  ✓ Password hashing working
  ✓ JWT signing verified
  ✓ CORS properly configured
  ✓ SQL injection protection
  ✓ Rate limiting active
  ✓ Input validation enabled

Frontend:
  ✓ API base URL updated
  ✓ Authentication flow tested
  ✓ Error handling verified
  ✓ Analytics integrated
```

---

## 15. Next Steps

1. **Choose Framework**: Flask (Python) or Express (Node.js)
2. **Set Up Project**: Initialize with dependencies
3. **Create Models**: Define SQLAlchemy/TypeORM models
4. **Implement Auth**: Registration, login, JWT
5. **Build Search**: Hotel search with filters
6. **Develop Booking**: Complete booking workflow
7. **Add Analytics**: Reporting and dashboards
8. **Frontend Integration**: Build React/Vue frontend
9. **Testing**: Write comprehensive test suite
10. **Deployment**: Deploy to production server

---

**API Version**: 1.0  
**Last Updated**: November 25, 2025
