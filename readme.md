# Railway Management System

## Project Overview
This is a Flask-based Railway Management System that allows users to register, login, check train seat availability, and book seats. The system supports role-based access with admin and user roles.Uses Pessimistic Locking to handle race around condition.

## Tech Stack
- Backend: Flask
- Database: PostgreSQL
- Authentication: Flask-JWT-Extended
- Password Hashing: Flask-Bcrypt
- ORM: SQLAlchemy
- Migrations: Flask-Migrate

## Prerequisites
- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/railway-management-system.git
cd railway-management-system
```

### 2. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root with the following variables:
```
DATABASE_URI=postgresql://username:password@localhost/railway_db
ADMIN_API_KEY=your_secret_admin_api_key
JWT_SECRET=your_jwt_secret_key
```

### 5. Database Setup
```bash
# Create the database
createdb railway_db

# Initialize migrations
flask db init

# Create database tables
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```

### 6. Run the Application
```bash
python app.py
```

## API Endpoints

### User Registration
- **URL**: `/register`
- **Method**: POST
- **Request Body**:
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

### User Login
- **URL**: `/login`
- **Method**: POST
- **Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```

### Add Train (Admin Only)
- **URL**: `/add_train`
- **Method**: POST
- **Headers**: `X-API-Key: [Admin API Key]`
- **Request Body**:
```json
{
  "train_name": "string",
  "source": "string",
  "destination": "string",
  "total_seats": "integer"
}
```

### Check Seat Availability
- **URL**: `/seat_availability`
- **Method**: GET
- **Query Parameters**: 
  - `source`: string
  - `destination`: string

### Book Seat
- **URL**: `/book_seat`
- **Method**: POST
- **Headers**: `Authorization: Bearer [JWT Token]`
- **Request Body**:
```json
{
  "train_id": "integer",
  "seat_count": "integer"
}
```

### Get Booking Details
- **URL**: `/booking_details`
- **Method**: GET
- **Headers**: `Authorization: Bearer [JWT Token]`

## Security Features
- Password hashing with bcrypt
- JWT-based authentication
- Admin API key protection
- Race condition handling for seat bookings

## Assumptions

- Bookings are confirmed instantly upon successful seat allocation
- Train is automatically marked inactive if no seats are available


## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.

