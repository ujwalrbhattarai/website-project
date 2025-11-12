# Support Ticket System & Management Member Features - Documentation

## ✅ Completed Features

### 1. **Support Ticket System**

#### For Students:
- **Submit Support Tickets**: Students can submit help requests through a dedicated form
- **View All Tickets**: See all their submitted tickets with status tracking
- **Ticket Details**: View full conversation and responses from admin/faculty
- **Add Responses**: Continue conversation on open tickets
- **Categories**: Technical, Payment, Course Content, Other
- **Priority Levels**: Low, Medium, High

**Access**: Hamburger Menu → ACCOUNT → Help & Support

#### For Admin:
- **View All Tickets**: Dashboard showing all student support tickets
- **Statistics**: Open, In Progress, Closed, and Unassigned ticket counts
- **Assign to Faculty**: Forward tickets to specific faculty members
- **Update Status**: Change ticket status (Open → In Progress → Closed)
- **Respond**: Add admin responses to tickets
- **Manage Conversations**: View full conversation history

**Access**: Hamburger Menu → Support Tickets

#### For Faculty:
- **View Assigned Tickets**: See all tickets assigned by admin
- **Ticket Statistics**: Track open, in progress, and closed tickets
- **Respond to Students**: Add responses to assigned tickets
- **Cannot change status**: Only admin can update status and reassign

**Access**: Hamburger Menu → ACCOUNT → My Tickets

---

### 2. **Management Member System**

#### Admin Capabilities:
- **View All Members**: List of all admin and faculty members
- **Add New Members**: Create new faculty or admin accounts
  - Full Name
  - Username (must be unique)
  - Email (must be unique)
  - Password
  - Role (Faculty or Admin)
- **Remove Members**: Delete management members with safety checks
  - Cannot remove yourself
  - Cannot remove faculty with active courses
- **Statistics**: Count of administrators and faculty members

**Access**: Hamburger Menu → Management Members

---

## 🗃️ Database Models

### SupportTicket
- `id`: Ticket ID
- `student_id`: Student who created the ticket
- `title`: Brief description
- `description`: Detailed issue description
- `status`: open, in_progress, closed
- `priority`: low, medium, high
- `category`: technical, payment, course, other
- `assigned_to`: Faculty member (nullable)
- `created_at`: Timestamp
- `updated_at`: Timestamp

### TicketResponse
- `id`: Response ID
- `ticket_id`: Reference to ticket
- `user_id`: User who responded (student/faculty/admin)
- `message`: Response text
- `created_at`: Timestamp

---

## 📋 Routes Created

### Student Routes:
- `/student/support` - View all tickets
- `/student/support/new` - Submit new ticket
- `/student/support/<id>` - View ticket detail
- `/student/support/<id>/respond` - Add response (POST)

### Admin Routes:
- `/admin/support` - View all tickets
- `/admin/support/<id>` - View/manage ticket
- `/admin/support/<id>/assign` - Assign/update ticket (POST)
- `/admin/support/<id>/respond` - Add response (POST)
- `/admin/management` - View management members
- `/admin/management/add` - Add new member (POST)
- `/admin/management/<id>/remove` - Remove member (POST)

### Faculty Routes:
- `/faculty/support` - View assigned tickets
- `/faculty/support/<id>` - View ticket detail
- `/faculty/support/<id>/respond` - Add response (POST)

---

## 🎨 UI Features

### Support Ticket List
- Color-coded status badges (Open=Blue, In Progress=Yellow, Closed=Green)
- Priority indicators (High=Red, Medium=Yellow, Low=Blue)
- Category badges
- Responsive table design
- Quick view buttons

### Ticket Detail Page
- Full conversation thread
- User role badges (Admin, Faculty, Student)
- Highlighted own responses
- Response form (when ticket is open)
- Sidebar with ticket details
- Assigned faculty information

### Management Page
- Add member modal dialog
- Role selection (Faculty/Admin)
- Safety confirmations for removal
- Statistics cards
- Responsive table with actions
- "You" indicator for current admin

---

## 🔐 Security Features

1. **Access Control**:
   - Students can only view/respond to their own tickets
   - Faculty can only view tickets assigned to them
   - Admin has full access to all tickets

2. **Validation**:
   - Unique username/email for management members
   - Cannot remove yourself as admin
   - Cannot remove faculty with active courses
   - Required fields validation

3. **Role-Based Routing**:
   - All routes protected with login_required
   - Admin routes protected with admin_required
   - Faculty routes protected with faculty_required

---

## 📞 Contact Information Displayed

- Phone: +977-9862134951
- Support email: support@innovativegroup.edu.np
- Displayed on support ticket submission page

---

## 🚀 How to Use

### As a Student:
1. Login with your credentials
2. Click hamburger menu (☰) → ACCOUNT → Help & Support
3. Click "New Ticket" button
4. Fill in the form with your issue
5. Track your ticket and add responses

### As Admin:
1. Login as admin (username: admin, password: admin123)
2. Access "Support Tickets" from menu
3. Click on any ticket to view details
4. Assign to faculty members using the dropdown
5. Update status and add responses
6. Manage team members via "Management Members"

### As Faculty:
1. Login with faculty credentials
2. Access "My Tickets" from ACCOUNT menu
3. View assigned tickets
4. Respond to student inquiries

---

## ✅ Testing the Features

1. **Create a Support Ticket**:
   - Login as student1 (password: student123)
   - Go to Help & Support
   - Submit a new ticket

2. **Assign Ticket**:
   - Login as admin (password: admin123)
   - Go to Support Tickets
   - Open the ticket and assign it to teacher1

3. **Respond as Faculty**:
   - Login as teacher1 (password: teacher123)
   - Go to My Tickets
   - Open assigned ticket and add response

4. **Add Management Member**:
   - Login as admin
   - Go to Management Members
   - Click "Add Member" and create new faculty/admin

---

## 🎨 Theme Compatibility

All new pages support:
- ✅ Pure black/white theme toggle
- ✅ Hamburger menu navigation
- ✅ Dark mode with proper visibility
- ✅ Responsive design for mobile/desktop
- ✅ Consistent styling with existing pages

---

## 📝 Application Running

Server is running at: **http://127.0.0.1:5000**

Default Login Credentials:
- **Admin**: admin / admin123
- **Faculty**: teacher1 / teacher123  
- **Student**: student1 / student123
