# Wedding Destination Hotel Finder - Frontend Application Specification

**Version**: 1.0  
**Date**: November 25, 2025  
**Framework**: React (or Vue.js/Angular as alternative)  
**Build Tool**: Vite or Create React App

---

## 1. Project Structure

```
frontend/
├── index.html
├── vite.config.js (or webpack.config.js)
├── package.json
├── .env
├── .env.local
├── public/
│   ├── favicon.ico
│   ├── images/
│   └── assets/
├── src/
│   ├── index.jsx
│   ├── App.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Search.jsx
│   │   ├── HotelDetail.jsx
│   │   ├── Comparison.jsx
│   │   ├── Booking.jsx
│   │   ├── BookingConfirmation.jsx
│   │   ├── MyBookings.jsx
│   │   ├── UserProfile.jsx
│   │   ├── UserReviews.jsx
│   │   ├── Analytics.jsx
│   │   ├── AdminDashboard.jsx
│   │   └── NotFound.jsx
│   ├── components/
│   │   ├── Common/
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── Navigation.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   ├── ErrorMessage.jsx
│   │   │   └── Pagination.jsx
│   │   ├── Search/
│   │   │   ├── SearchBar.jsx
│   │   │   ├── FilterPanel.jsx
│   │   │   ├── DateRangePicker.jsx
│   │   │   ├── GuestCounter.jsx
│   │   │   └── LocationSearch.jsx
│   │   ├── Hotels/
│   │   │   ├── HotelCard.jsx
│   │   │   ├── HotelGallery.jsx
│   │   │   ├── AmenitiesList.jsx
│   │   │   ├── RoomTypeSelector.jsx
│   │   │   └── HotelRating.jsx
│   │   ├── Booking/
│   │   │   ├── BookingForm.jsx
│   │   │   ├── RoomSelector.jsx
│   │   │   ├── GuestInfo.jsx
│   │   │   ├── PriceBreakdown.jsx
│   │   │   ├── SpecialRequests.jsx
│   │   │   └── PaymentForm.jsx
│   │   ├── Comparison/
│   │   │   ├── ComparisonTable.jsx
│   │   │   ├── PriceComparison.jsx
│   │   │   ├── RatingComparison.jsx
│   │   │   └── AmenityComparison.jsx
│   │   ├── Reviews/
│   │   │   ├── ReviewList.jsx
│   │   │   ├── ReviewCard.jsx
│   │   │   ├── ReviewForm.jsx
│   │   │   ├── RatingBreakdown.jsx
│   │   │   └── ReviewPhotos.jsx
│   │   ├── Analytics/
│   │   │   ├── Chart.jsx
│   │   │   ├── OccupancyChart.jsx
│   │   │   ├── RevenueChart.jsx
│   │   │   ├── PriceTrendChart.jsx
│   │   │   └── ReportGenerator.jsx
│   │   └── Auth/
│   │       ├── LoginForm.jsx
│   │       ├── RegisterForm.jsx
│   │       ├── PasswordReset.jsx
│   │       └── ProtectedRoute.jsx
│   ├── services/
│   │   ├── api.js              # Axios instance & base config
│   │   ├── authService.js      # Authentication API calls
│   │   ├── hotelService.js     # Hotel API calls
│   │   ├── bookingService.js   # Booking API calls
│   │   ├── searchService.js    # Search API calls
│   │   ├── reviewService.js    # Review API calls
│   │   ├── analyticsService.js # Analytics API calls
│   │   └── uploadService.js    # File upload handling
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── useSearch.js
│   │   ├── useBooking.js
│   │   ├── useFetch.js
│   │   ├── useLocalStorage.js
│   │   └── useForm.js
│   ├── context/
│   │   ├── AuthContext.jsx
│   │   ├── SearchContext.jsx
│   │   ├── BookingContext.jsx
│   │   └── NotificationContext.jsx
│   ├── store/
│   │   ├── actions/
│   │   │   ├── authActions.js
│   │   │   ├── hotelActions.js
│   │   │   └── bookingActions.js
│   │   ├── reducers/
│   │   │   ├── authReducer.js
│   │   │   ├── hotelReducer.js
│   │   │   └── bookingReducer.js
│   │   └── store.js            # Redux setup
│   ├── styles/
│   │   ├── index.css
│   │   ├── variables.css       # Colors, fonts, spacing
│   │   ├── layout.css
│   │   ├── components.css
│   │   └── responsive.css      # Media queries
│   ├── utils/
│   │   ├── validators.js
│   │   ├── formatters.js       # Date, currency, etc.
│   │   ├── helpers.js
│   │   ├── constants.js
│   │   └── errorHandler.js
│   ├── assets/
│   │   ├── images/
│   │   ├── icons/
│   │   └── fonts/
│   └── config/
│       ├── api.config.js
│       └── app.config.js
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── .gitignore
```

---

## 2. Environment Variables

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:5000/api
VITE_API_TIMEOUT=30000
VITE_MAX_FILE_SIZE=10485760

# Frontend Configuration
VITE_APP_NAME=Wedding Hotel Finder
VITE_APP_VERSION=1.0.0
VITE_ENVIRONMENT=development

# Feature Flags
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_PAYMENTS=true
VITE_ENABLE_REVIEWS=true

# Third-party Services
VITE_STRIPE_PUBLIC_KEY=pk_test_xxxxx
VITE_GOOGLE_MAPS_API_KEY=xxxxx
VITE_ANALYTICS_ID=UA-xxxxx

# Logging
VITE_LOG_LEVEL=debug
```

---

## 3. Pages & Routes

### Public Routes

```
/                          Home page with featured hotels
/search                    Search results page
/hotels/:hotelId          Hotel detail page
/hotels/:hotelId/reviews  Hotel reviews page
/comparison               Hotel comparison tool
/about                    About us page
/contact                  Contact form page
/login                    Login page
/register                 Registration page
/forgot-password          Password reset request
/reset-password/:token    Password reset form
```

### Protected Routes (Authenticated Users)

```
/booking/:hotelId         Booking page
/booking/confirm/:id      Booking confirmation
/my-bookings              User's bookings list
/booking/:bookingId       Booking details
/profile                  User profile
/profile/edit             Edit profile
/my-reviews               User's reviews
/reviews/create/:bookingId Create review
/inquiries                Booking inquiries
```

### Admin Routes (Admin Only)

```
/admin                    Admin dashboard
/admin/hotels             Manage hotels
/admin/users              Manage users
/admin/bookings           Manage bookings
/admin/reviews            Moderate reviews
/admin/analytics          Analytics dashboard
/admin/settings           System settings
```

---

## 4. Page Components & Features

### 4.1 Home Page

**Sections**:
- Hero banner with background image
- Featured destinations carousel
- Quick search form (city, dates, guests)
- Popular wedding hotels showcase
- Testimonials section
- Call-to-action buttons
- Footer

**Key Features**:
- Recent searches (from localStorage)
- Trending destinations
- Special offers banner
- Newsletter signup

---

### 4.2 Search Results Page

**Layout**:
- Left sidebar: Filters
- Center: Hotel listings
- Right sidebar: Map (optional)

**Filter Options**:
- Price range slider
- Star rating filter
- Amenities multi-select
- Hotel category
- Distance from city center
- Availability

**Sorting**:
- Best Match
- Price (Low to High)
- Price (High to Low)
- Rating (High to Low)
- Review Count
- Distance

**Hotel Cards Display**:
- Hotel image
- Hotel name & location
- Star rating & review count
- Price per night
- Key amenities (3-5)
- "View Details" button
- "Compare" checkbox

---

### 4.3 Hotel Detail Page

**Sections**:
1. **Image Gallery**
   - Main image viewer
   - Thumbnail carousel
   - Zoom functionality

2. **Hotel Information**
   - Name, location, category
   - Star rating & review count
   - Description
   - Check-in/out times
   - Contact information

3. **Amenities Section**
   - Full amenity list with icons
   - Grouped by category (room, property, wedding)
   - Cost indicators (complimentary, fee-based)

4. **Room Types**
   - Card for each room type
   - Occupancy info
   - Base rate
   - View, Book buttons

5. **Reviews Section**
   - Average rating breakdown
   - Review list with sorting
   - Photo gallery from reviews
   - Review filter (verified, rating range)

6. **Booking Widget** (Sticky)
   - Check-in/out date picker
   - Guest counter
   - Room selector
   - Price calculation
   - "Book Now" button

---

### 4.4 Comparison Page

**Features**:
- Select 2-5 hotels to compare
- Table view with key metrics
- Side-by-side price comparison
- Rating breakdown comparison
- Amenity comparison (checkmarks)
- Room type comparison
- "Book" button for each hotel

**Chart Types**:
- Price comparison bar chart
- Rating radar chart
- Amenity overlap diagram

---

### 4.5 Booking Page

**Steps**:
1. **Select Rooms**
   - Available room types for dates
   - Room details & images
   - Price per room
   - Guest assignment

2. **Enter Guest Information**
   - Names for each guest
   - Contact information
   - Special requests
   - Wedding event details (if applicable)

3. **Review & Confirm**
   - Booking summary
   - Price breakdown
   - Cancellation policy
   - Terms & conditions checkbox

4. **Payment**
   - Payment method selection
   - Card details input
   - Billing address
   - Payment processing

---

### 4.6 My Bookings Page

**Features**:
- List all user bookings
- Status badges (Pending, Confirmed, Completed, Cancelled)
- Quick info: Hotel, dates, cost
- Action buttons: View Details, Modify, Cancel
- Filter by status/date
- Download invoice
- Reorder hotel link

---

### 4.7 User Profile Page

**Sections**:
1. **Profile Information**
   - Avatar upload
   - Name, email, phone
   - Location preference
   - Wedding date (if applicable)

2. **Preferences**
   - Budget range
   - Preferred amenities
   - Hotel categories
   - Notification settings

3. **Account Management**
   - Change password
   - Email verification
   - Two-factor authentication
   - Delete account

4. **My Reviews**
   - List of written reviews
   - Edit/delete options
   - View helpful votes

---

### 4.8 Analytics Dashboard

**Charts & Metrics**:
- Occupancy rate (area chart)
- Revenue trend (line chart)
- Booking status distribution (pie chart)
- Peak seasons (bar chart)
- Guest feedback sentiment (gauge)
- Average rating trend
- Cancellation rate

**Export Options**:
- PDF report
- CSV data
- Email report scheduling

---

## 5. Key Components

### Search Bar Component

```jsx
<SearchBar 
  onSearch={(filters) => {}}
  initialValues={{
    city: '',
    checkInDate: '',
    checkOutDate: '',
    guests: 1,
    rooms: 1
  }}
/>
```

**Features**:
- Location autocomplete
- Date range picker
- Guest/room counter
- Search button
- Advanced filters toggle

### Hotel Card Component

```jsx
<HotelCard
  hotel={{
    id, name, image, rating, reviews,
    pricePerNight, amenities, category
  }}
  onBook={() => {}}
  onCompare={() => {}}
  isSelectable={true}
/>
```

### Booking Form Component

```jsx
<BookingForm
  hotelId={1}
  checkInDate="2025-06-01"
  checkOutDate="2025-06-05"
  onSubmit={(bookingData) => {}}
  isLoading={false}
/>
```

### Price Breakdown Component

```jsx
<PriceBreakdown
  subtotal={1000}
  taxRate={0.12}
  discountAmount={100}
  finalTotal={1080}
  currencyCode="USD"
/>
```

### Chart Components

```jsx
// Occupancy Chart
<OccupancyChart
  data={occupancyData}
  period="monthly"
  title="Hotel Occupancy"
/>

// Revenue Chart
<RevenueChart
  data={revenueData}
  startDate="2025-01-01"
  endDate="2025-12-31"
/>
```

---

## 6. State Management

### Redux Store Structure

```javascript
{
  auth: {
    isLoading: false,
    isAuthenticated: false,
    user: null,
    token: null,
    error: null
  },
  search: {
    filters: {
      city: '',
      checkInDate: '',
      checkOutDate: '',
      guests: 1,
      budget: { min: 0, max: 1000 },
      amenities: [],
      rating: 0
    },
    results: [],
    isLoading: false,
    totalResults: 0,
    page: 1,
    error: null
  },
  hotels: {
    selected: null,
    details: {},
    isLoading: false,
    error: null
  },
  booking: {
    current: null,
    userBookings: [],
    isLoading: false,
    error: null
  },
  ui: {
    notifications: [],
    sidebarOpen: false,
    theme: 'light'
  }
}
```

---

## 7. API Integration

### Axios Configuration

```javascript
// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: import.meta.env.VITE_API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor - add token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor - handle errors
api.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response?.status === 401) {
      // Redirect to login
    }
    return Promise.reject(error);
  }
);

export default api;
```

### Hotel Service

```javascript
// src/services/hotelService.js
export const hotelService = {
  searchHotels: (filters) => 
    api.get('/search/hotels', { params: filters }),
    
  getHotelDetails: (hotelId) => 
    api.get(`/hotels/${hotelId}`),
    
  getHotelReviews: (hotelId, page = 1) => 
    api.get(`/hotels/${hotelId}/reviews`, { 
      params: { page, limit: 10 } 
    }),
    
  getAmenities: (hotelId) => 
    api.get(`/hotels/${hotelId}/amenities`)
};
```

---

## 8. Form Handling

### Custom useForm Hook

```javascript
const useForm = (initialValues, onSubmit) => {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setValues(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleBlur = (e) => {
    const { name } = e.target;
    setTouched(prev => ({ ...prev, [name]: true }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      await onSubmit(values);
    } finally {
      setIsSubmitting(false);
    }
  };

  return {
    values,
    errors,
    touched,
    isSubmitting,
    handleChange,
    handleBlur,
    handleSubmit,
    setValues
  };
};
```

---

## 9. Authentication Flow

### Login Flow

```javascript
// 1. User submits login form
const handleLogin = async (credentials) => {
  try {
    const response = await authService.login(credentials);
    
    // 2. Store token
    localStorage.setItem('authToken', response.data.token);
    localStorage.setItem('refreshToken', response.data.refreshToken);
    
    // 3. Update Redux state
    dispatch(setUser(response.data.user));
    
    // 4. Redirect
    navigate('/my-bookings');
  } catch (error) {
    setError(error.message);
  }
};
```

### Protected Route Component

```javascript
const ProtectedRoute = ({ children, requiredRole = null }) => {
  const { isAuthenticated, user } = useAuth();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  if (requiredRole && user.role !== requiredRole) {
    return <Navigate to="/" replace />;
  }
  
  return children;
};

// Usage
<Routes>
  <Route 
    path="/my-bookings" 
    element={
      <ProtectedRoute>
        <MyBookings />
      </ProtectedRoute>
    } 
  />
  <Route 
    path="/admin" 
    element={
      <ProtectedRoute requiredRole="Admin">
        <AdminDashboard />
      </ProtectedRoute>
    } 
  />
</Routes>
```

---

## 10. Responsive Design

### Breakpoints

```css
/* Mobile First Approach */
/* Extra Small Devices */
@media (max-width: 576px) {
  /* Mobile styles */
}

/* Small Devices (tablets) */
@media (min-width: 576px) {
  /* Tablet styles */
}

/* Medium Devices (small desktops) */
@media (min-width: 768px) {
  /* Small desktop styles */
}

/* Large Devices (desktops) */
@media (min-width: 992px) {
  /* Desktop styles */
}

/* Extra Large Devices (large desktops) */
@media (min-width: 1200px) {
  /* Large desktop styles */
}
```

### Mobile Optimizations

- **Touch-Friendly**: Min 44px button/link size
- **Flexible Images**: max-width: 100%
- **Stack Layouts**: Single column on mobile
- **Simplified Forms**: Fewer fields on mobile
- **Optimized Navigation**: Hamburger menu
- **Fast Load Times**: Lazy load images

---

## 11. Performance Optimization

### Code Splitting

```javascript
import { lazy, Suspense } from 'react';

const Home = lazy(() => import('./pages/Home'));
const Search = lazy(() => import('./pages/Search'));
const Booking = lazy(() => import('./pages/Booking'));

export default function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/search" element={<Search />} />
        <Route path="/booking" element={<Booking />} />
      </Routes>
    </Suspense>
  );
}
```

### Image Optimization

```javascript
// Use next-gen formats
<picture>
  <source srcSet="image.webp" type="image/webp" />
  <source srcSet="image.jpg" type="image/jpeg" />
  <img src="image.jpg" alt="Hotel" loading="lazy" />
</picture>

// Responsive images
<img 
  srcSet="image-sm.jpg 480w, image-md.jpg 768w, image-lg.jpg 1200w"
  sizes="(max-width: 480px) 480px, (max-width: 768px) 768px, 1200px"
  src="image-lg.jpg"
  alt="Hotel"
/>
```

### Bundle Analysis

```bash
npm install --save-dev webpack-bundle-analyzer
# Check bundle size and optimize
```

---

## 12. Testing Strategy

### Unit Tests

```javascript
// test: HotelCard.test.jsx
import { render, screen } from '@testing-library/react';
import HotelCard from './HotelCard';

describe('HotelCard', () => {
  const mockHotel = {
    id: 1,
    name: 'Test Hotel',
    rating: 4.5,
    pricePerNight: 250
  };

  test('renders hotel name', () => {
    render(<HotelCard hotel={mockHotel} />);
    expect(screen.getByText('Test Hotel')).toBeInTheDocument();
  });

  test('displays correct price', () => {
    render(<HotelCard hotel={mockHotel} />);
    expect(screen.getByText('$250/night')).toBeInTheDocument();
  });
});
```

### E2E Tests (Cypress)

```javascript
// cypress/e2e/booking.cy.js
describe('Booking Flow', () => {
  it('should complete a booking', () => {
    cy.visit('/search');
    cy.get('input[name="city"]').type('Miami');
    cy.get('button[type="submit"]').click();
    cy.get('[data-testid="hotel-card"]').first().click();
    cy.get('button:contains("Book Now")').click();
    // ... continue flow
  });
});
```

---

## 13. Browser Support

- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

---

## 14. Accessibility (WCAG 2.1 AA)

### Key Guidelines

- **Semantic HTML**: Use proper heading hierarchy
- **ARIA Labels**: For screen readers
- **Keyboard Navigation**: Tab through all interactive elements
- **Color Contrast**: Min 4.5:1 ratio for text
- **Form Labels**: Every input has associated label
- **Alt Text**: All images have descriptive alt text
- **Focus Visible**: Clear focus indicators

```jsx
// Example accessible form
<form onSubmit={handleSubmit}>
  <label htmlFor="email">Email Address</label>
  <input
    id="email"
    name="email"
    type="email"
    aria-describedby="email-error"
    required
  />
  {errors.email && (
    <div id="email-error" role="alert">
      {errors.email}
    </div>
  )}
  <button type="submit">Login</button>
</form>
```

---

## 15. Deployment

### Build Process

```bash
npm run build        # Production build
npm run preview      # Test build locally
npm run lint         # Check for errors
npm run format       # Format code
```

### Hosting Options

- **Vercel**: Optimized for React, automatic deployments
- **Netlify**: Simple deployment, good free tier
- **AWS S3 + CloudFront**: Cost-effective, scalable
- **Firebase Hosting**: Easy setup, free tier available

---

## 16. Performance Targets

- **First Contentful Paint (FCP)**: < 1.5s
- **Largest Contentful Paint (LCP)**: < 2.5s
- **Cumulative Layout Shift (CLS)**: < 0.1
- **Time to Interactive**: < 3.5s
- **Bundle Size**: < 150KB (gzipped)

---

## Summary

This frontend specification provides a complete blueprint for building a modern, responsive web application for wedding hotel planning. The focus is on:

✓ User Experience
✓ Performance
✓ Accessibility
✓ Maintainability
✓ Scalability

**Next Steps**: Choose React/Vue, set up development environment, and start building components!
