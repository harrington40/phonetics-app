# Role-Based Authentication System

## Overview

The PhonicsLearn app now has a complete role-based access control system with two primary roles:
- **Students**: Access learning materials after payment verification
- **Teachers**: Create classes and manage enrolled students

## System Architecture

### User Roles

1. **Student**
   - Must have payment verified (`has_paid = true`) to access materials
   - Can enroll with a teacher using a class code
   - Redirected to payment page if not paid  
   - Access to: `dashboard.html`, lesson materials

2. **Teacher**
   - Can create classes with unique codes
   - View all enrolled students
   - Mark students as paid
   - Access to: `teacher-dashboard.html`, student management

3. **Admin** (future)
   - Full system access
   - Manage all users and payments

### Database Schema Updates

#### User Model Enhancements
```python
class User:
    role: String  # "student", "teacher", "admin"
    has_paid: Boolean  # Payment verification for students
    teacher_id: Integer  # For students enrolled with a teacher
    enrolled_students: Relationship  # Teacher's students
```

#### New TeacherClass Model
```python
class TeacherClass:
    teacher_id: Integer
    class_name: String
    class_code: String  # Unique code for student enrollment
    max_students: Integer
    is_active: Boolean
```

## API Endpoints

### Authentication

#### POST /auth/register
Register new user with role selection
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "full_name": "John Doe",
  "role": "student",  // or "teacher"
  "teacher_code": "ABC12345"  // Optional, for student enrollment
}
```

**Response:**
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "student",
    "has_paid": false,
    "teacher_id": null
  }
}
```

#### POST /auth/login
Login with automatic role-based redirection
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response includes:**
- `enrolled_students` array (if teacher)
- Payment status check (if student)
- HTTP 402 if student hasn't paid

#### GET /auth/check-access
Check user's access permissions
```bash
curl -H "Authorization: Bearer {token}" http://localhost:8000/auth/check-access
```

**Response:**
```json
{
  "user_id": 1,
  "email": "student@example.com",
  "role": "student",
  "has_paid": true,
  "can_access_materials": true,
  "access_message": "Full access"
}
```

### Teacher Endpoints

#### POST /auth/teacher/create-class
Create a new class (requires teacher role)
```json
{
  "class_name": "Grade 1 Phonics",
  "description": "Morning class",
  "max_students": 30
}
```

**Response:**
```json
{
  "message": "Class created successfully",
  "class_code": "ABC12345",
  "class_name": "Grade 1 Phonics",
  "max_students": 30
}
```

#### GET /auth/teacher/students
Get all enrolled students
```bash
curl -H "Authorization: Bearer {teacher_token}" \
  http://localhost:8000/auth/teacher/students
```

**Response:**
```json
{
  "total_students": 5,
  "students": [
    {
      "id": 1,
      "email": "student@example.com",
      "full_name": "Tommy Smith",
      "has_paid": true,
      "created_at": "2026-02-10T00:00:00"
    }
  ]
}
```

#### GET /auth/teacher/classes
Get all classes created by teacher
```bash
curl -H "Authorization: Bearer {teacher_token}" \
  http://localhost:8000/auth/teacher/classes
```

#### POST /auth/admin/mark-paid/{user_id}
Mark student as paid (teachers can mark their own students)
```bash
curl -X POST -H "Authorization: Bearer {teacher_token}" \
  http://localhost:8000/auth/admin/mark-paid/1
```

## User Flow

### Student Registration Flow

1. Student visits `role-login.html`
2. Selects "Student" role
3. (Optional) Enters teacher class code
4. Registers → `has_paid = false`
5. Redirected to `payment-required.html`
6. Completes payment OR teacher marks as paid
7. `has_paid = true` → Accesses `dashboard.html`

### Teacher Registration Flow

1. Teacher visits `role-login.html`
2. Selects "Teacher" role
3. Registers → Full access immediately
4. Redirected to `teacher-dashboard.html`
5. Creates class → Gets unique class code
6. Shares code with students
7. Manages enrolled students

### Login Flow

```javascript
// Student login check
if (user.role === 'student') {
  if (user.has_paid) {
    redirect('dashboard.html');  // ✅ Access granted
  } else {
    redirect('payment-required.html');  // ❌ Payment required
  }
}

// Teacher login
if (user.role === 'teacher') {
  redirect('teacher-dashboard.html');  // ✅ Access granted + student list
}
```

## Frontend Implementation

### New Pages

1. **role-login.html**
   - Combined login/register with role selection
   - Automatic redirection based on role
   - Teacher code input for students

2. **payment-required.html**
   - Payment information
   - Contact teacher option
   - Access blocked until payment

3. **teacher-dashboard.html** (existing, enhanced)
   - View enrolled students
   - Print class reports
   - Manage student payments

4. **dashboard.html** (existing, protected)
   - Only accessible to paid students
   - Full learning materials

### Authorization Checks

Example JavaScript to protect pages:
```javascript
async function checkAccess() {
  const token = localStorage.getItem('access_token');
  const response = await fetch('/auth/check-access', {
    headers: {'Authorization': `Bearer ${token}`}
  });
  
  const data = await response.json();
  
  if (!data.can_access_materials) {
    window.location.href = 'payment-required.html';
  }
}
```

## Setup Instructions

### 1. Database Migration

Run migration to add new columns:
```sql
ALTER TABLE users ADD COLUMN role VARCHAR DEFAULT 'student';
ALTER TABLE users ADD COLUMN has_paid BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN teacher_id INTEGER REFERENCES users(id);

CREATE TABLE teacher_classes (
  id SERIAL PRIMARY KEY,
  teacher_id INTEGER REFERENCES users(id),
  class_name VARCHAR NOT NULL,
  class_code VARCHAR UNIQUE NOT NULL,
  description TEXT,
  max_students INTEGER DEFAULT 30,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### 2. Testing

#### Register a Teacher
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teacher@school.com",
    "password": "Teacher123",
    "full_name": "Ms. Johnson",
    "role": "teacher"
  }'
```

#### Register a Student
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@school.com",
    "password": "Student123",
    "full_name": "Tommy Smith",
    "role": "student",
    "teacher_code": "ABC12345"
  }'
```

#### Teacher Creates Class
```bash
curl -X POST http://localhost:8000/auth/teacher/create-class \
  -H "Authorization: Bearer {teacher_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "class_name": "Grade 1 Phonics",
    "max_students": 30
  }'
```

#### Teacher Marks Student as Paid
```bash
curl -X POST http://localhost:8000/auth/admin/mark-paid/1 \
  -H "Authorization: Bearer {teacher_token}"
```

## Security Features

1. **JWT Token Authentication**: Secure token-based auth
2. **Role-Based Access Control**: Endpoint protection by role
3. **Payment Verification**: Automatic access restriction
4. **Teacher Scoping**: Teachers only see their students
5. **Password Validation**: Strong password requirements

## Error Handling

| Error Code | Meaning | Action |
|------------|---------|--------|
| 401 | Unauthorized | Login required |
| 402 | Payment Required | Redirect to payment page |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |

## Usage Examples

### Student Journey
1. Visit: http://localhost:3000/role-login.html
2. Register as student (with or without teacher code)
3. Complete payment or wait for teacher verification
4. Access learning materials

### Teacher Journey
1. Visit: http://localhost:3000/role-login.html
2. Register as teacher
3. Create class → Get class code
4. Share code with students
5. View/manage enrolled students in dashboard
6. Mark students as paid when they complete payment

## Configuration

Set environment variables:
```bash
JWT_SECRET=your-secret-key
JWT_EXPIRATION_HOURS=720  # 30 days
DATABASE_URL=postgresql://user:pass@localhost/phonicslearn
```

## Future Enhancements

- [ ] Stripe/PayPal integration for real payments
- [ ] Email notifications for enrollment
- [ ] Bulk student import for teachers
- [ ] Class schedules and assignments
- [ ] Progress reports per class
- [ ] Parent accounts linked to students
- [ ] Multi-language support
