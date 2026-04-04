# Freelancera — A Service and Job Marketplace

A web-based platform that connects housewife freelancers with clients who need specific tasks completed. Built with Django 3.2.13 as an internship project.

---

## Project Structure

```
Intership_Project/
├── Project5/                        # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── application/                     # Main Django app
│   ├── models.py
│   └── views.py
├── templates/                       # HTML templates
│   ├── index.html                   # Homepage
│   ├── about.html                   # About page
│   ├── reg.html                     # Registration page
│   ├── login.html                   # Login page
│   ├── find_jobs.html               # Job listings with search & filter
│   ├── post_job.html                # Post a new job
│   ├── job_detail.html              # Single job detail & apply
│   ├── services.html                # Services overview page
│   ├── how_it_works.html            # How It Works page
│   ├── records.html                 # Basic enquiry records view
│   ├── header.html                  # Shared header/navbar
│   ├── footer.html                  # Shared footer
│   └── dashboard/
│       ├── index.html               # Client dashboard (Matrix Admin)
│       └── tables.html              # Enquiry details with DataTables
├── static/                          # Static assets
│   ├── assets/                      # Frontend assets (CSS, JS, images)
│   └── dashboard/                   # Matrix Admin dashboard assets
├── manage.py
└── db.sqlite3
```

---

## Tech Stack

| Layer        | Technology                                      |
|--------------|-------------------------------------------------|
| Backend      | Django 3.2.13 (Python)                          |
| Frontend     | HTML5, CSS3, Bootstrap 5, JavaScript (ES6+)     |
| Styling      | SCSS / SASS, custom CSS                         |
| Database     | SQLite3                                         |
| UI Template  | Matrix Admin (WrapPixel) for dashboards         |
| Fonts        | Google Fonts (Roboto, Open Sans, Poppins)       |
| Icons        | FontAwesome, Bootstrap Icons, RemixIcon (MDI)   |
| Animations   | AOS (Animate On Scroll), Animate.css            |
| JS Libraries | jQuery, DataTables, Swiper.js, GLightbox        |
| Live Chat    | Tawk.to (integrated on homepage)                |

---

## Database Models

### `enquiry_table`
Stores contact/registration enquiry submissions from users.

| Field   | Type       |
|---------|------------|
| name    | CharField  |
| email   | EmailField |
| phone   | CharField  |
| message | TextField  |

---

### `UserProfile`
Extends Django's default User model with role-based user types.

| Field           | Type           | Notes                          |
|-----------------|----------------|--------------------------------|
| user            | OneToOneField  | Links to Django's User model   |
| user_type       | CharField      | `housewife` or `client`        |
| phone           | CharField      |                                |
| address         | TextField      |                                |
| skills          | TextField      | For housewife freelancers      |
| experience      | TextField      | For housewife freelancers      |
| profile_picture | ImageField     | Uploads to `profiles/`         |
| is_verified     | BooleanField   | Default: False                 |
| created_at      | DateTimeField  | Auto-set on creation           |

---

### `JobPost`
Job listings created by clients.

| Field       | Type          | Notes                                                                           |
|-------------|---------------|---------------------------------------------------------------------------------|
| title       | CharField     |                                                                                 |
| category    | CharField     | cooking, cleaning, tutoring, beauty, childcare, craft, baking, digital          |
| description | TextField     |                                                                                 |
| budget      | CharField     | e.g. ₹300-500/day or ₹5000/month                                               |
| location    | CharField     |                                                                                 |
| posted_by   | ForeignKey    | Links to Django User                                                            |
| is_active   | BooleanField  | Default: True                                                                   |
| created_at  | DateTimeField | Auto-set on creation                                                            |

---

### `JobApplication`
Tracks applications submitted by housewife freelancers to job listings.

| Field      | Type          | Notes                                         |
|------------|---------------|-----------------------------------------------|
| job        | ForeignKey    | Links to JobPost                              |
| freelancer | ForeignKey    | Links to Django User                          |
| status     | CharField     | pending, accepted, rejected, completed        |
| amount     | CharField     | Copied from job budget at time of application |
| applied_at | DateTimeField | Auto-set on creation                          |

---

### `ServiceRequest`
Direct service requests submitted via the homepage quote form.

| Field        | Type          | Notes                                                              |
|--------------|---------------|--------------------------------------------------------------------|
| name         | CharField     |                                                                    |
| email        | EmailField    |                                                                    |
| phone        | CharField     |                                                                    |
| service_type | CharField     | cooking, cleaning, tutoring, craft, beauty, childcare, baking, digital |
| message      | TextField     |                                                                    |
| created_at   | DateTimeField | Auto-set on creation                                               |

---

## URL Routes

| URL                    | View Function    | Template                    | Description                                      |
|------------------------|------------------|-----------------------------|--------------------------------------------------|
| `/`                    | `home`           | `index.html`                | Homepage with carousel, services, jobs, testimonials |
| `/aboutus/`            | `aboutus`        | `about.html`                | About page with team & testimonials              |
| `/how-it-works/`       | `how_it_works`   | `how_it_works.html`         | 4-step process, FAQs, stats section              |
| `/services/`           | `services`       | `services.html`             | All 8 service categories in detail               |
| `/find-jobs/`          | `find_jobs`      | `find_jobs.html`            | Job listings with search & category filter       |
| `/post-job/`           | `post_job`       | `post_job.html`             | Job posting form (clients only)                  |
| `/job-detail/<id>/`    | `job_detail`     | `job_detail.html`           | Single job details with apply button             |
| `/apply-job/<id>/`     | `apply_for_job`  | —                           | Submit job application (redirects)               |
| `/request-quote/`      | `request_quote`  | —                           | Submit service request from homepage form        |
| `/reg/`                | `reg`            | `reg.html`                  | User registration (housewife or client)          |
| `/login/`              | `login_user`     | `login.html`                | User login with email or username                |
| `/logout/`             | `logout_user`    | —                           | Logs out and redirects to home                   |
| `/dashboard/`          | `dashboard`      | `dashboard/index.html`      | Client dashboard (Matrix Admin UI)               |
| `/records/`            | `records`        | `records.html`              | Basic enquiry records table                      |
| `/edit/<id>/`          | `edit_record`    | `dashboard/editrecord.html` | Edit an enquiry record                           |
| `/update/<id>/`        | `update_record`  | —                           | Save updated enquiry record                      |
| `/delete/<id>/`        | `delete`         | —                           | Delete an enquiry record (POST)                  |
| `/admin/`              | Django Admin     | —                           | Django admin panel                               |

---

## Templates Overview

### Public Pages

**`index.html` — Homepage**
- Hero section with 3-slide Bootstrap carousel (Find Services, Register as Freelancer, Post a Job)
- How It Works section with an inline service request form (posts to `request_quote`)
- 8 service category cards with FontAwesome icons
- Top rated freelancers section
- Recent job postings section (3 sample cards)
- Testimonials section using Swiper.js slider
- Tawk.to live chat widget integrated

**`about.html` — About Page**
- About section with image and story
- Stats counter (Happy Clients, Projects, Hours of Support, Hard Workers) using PureCounter
- Team section with 6 member cards and social links
- Testimonials section with Swiper.js

**`how_it_works.html` — How It Works**
- 4-step process cards: Register → Post/Find Jobs → Connect & Agree → Complete & Rate
- Platform statistics: 500+ Users, 1000+ Jobs, 50+ Cities, 4.8★ Rating
- Dedicated sections for Housewife Freelancers and Clients with feature lists
- FAQ section with 4 questions
- CTA section with Register Now and Browse Jobs buttons

**`services.html` — Services**
- 8 service cards with price ranges and direct category filter links to Find Jobs
- Detailed sections for Cooking, Cleaning, Tutoring, and Beauty with feature lists
- Each section links to category-filtered job results
- CTA section at bottom linking to Post Job and Browse Jobs

**`find_jobs.html` — Find Jobs**
- Search bar that queries title, description, and location using Django Q objects
- Category filter sidebar with radio buttons (auto-submits on change via `onchange`)
- Job cards displaying title, category badge, budget badge, location, and posted date
- Results count shown above listings
- Empty state with message and View All Jobs button when no results found
- Pagination placeholder displayed when jobs count exceeds 10
- CTA banner for unauthenticated users to register or login

**`post_job.html` — Post a Job**
- Form fields: Job Title, Service Category (dropdown with all 8 categories), Description, Budget, Location
- Role-based access control: login prompt for unauthenticated users, restriction alert for non-client users
- Tips section: Be Specific, Set Realistic Budget, Respond Quickly
- Benefits section highlighting free posting and verified freelancers

**`job_detail.html` — Job Detail**
- Header with job title, category badge, budget badge, and location badge
- Job description, posted date, and active/closed status displayed in info boxes
- Apply button visible only to authenticated housewife users who have not already applied
- "Already applied" info message for repeat visitors
- Client view shows "You posted this job" message instead of apply button
- Back to Jobs button
- Similar jobs placeholder cards

**`header.html` — Navigation**
- Fixed top navbar with logo image and site name
- Nav links: Home, How It Works, Find Jobs, Services
- Register Now button (green Bootstrap btn) and Login link
- Mobile responsive hamburger menu toggle

**`footer.html` — Footer**
- About column with contact details (phone, email) and social media icons
- Quick Links column: Home, How It Works, Services, Find Jobs, Contact Us
- Our Services column: all 8 service categories with emoji
- Support column: FAQ, Terms of Service, Privacy Policy, Refund Policy, Help Center
- For Freelancers column: Register as Housewife, How to Earn, Success Stories, Safety Tips, Payment Guide
- Copyright line with empowerment tagline

**`records.html` — Basic Enquiry Records**
- Bootstrap 3 layout with sidebar and main content area
- Sidebar: Dashboard, Master Page, Reports, Logout buttons
- Main table: displays all `enquiry_table` records with Sr. No., Name, Email, Phone, Message columns

---

### Auth Pages

**`reg.html` — Registration**
- Role selection at top: Housewife Freelancer or Client (radio buttons)
- Fields: Full Name, Email Address, Password, Confirm Password, Mobile Number, Tell us about yourself
- Password visibility toggle button (show/hide using Bootstrap Icons)
- Client-side password match validation on form submit
- Phone field with pattern validation for 10-digit Indian numbers starting with 6, 7, 8, or 9
- Terms & Conditions checkbox (required)
- Auto-dismiss flash messages after 5 seconds using JavaScript
- Link to login page for existing users

**`login.html` — Login**
- Accepts both username and email address (handled in view)
- Password visibility toggle button
- Remember Me checkbox
- Demo credentials shown at bottom of form
- Auto-dismiss flash messages (warnings) after 5 seconds
- Link to registration page for new users

---

### Dashboard Pages

**`dashboard/index.html` — Client Dashboard (Matrix Admin)**
- Matrix Admin vertical sidebar layout with `skin5` dark theme
- Topbar with sidebar toggle, notifications dropdown (3 items), and user profile dropdown showing `{{ username }}`
- Sidebar links: Dashboard, Find Jobs, My Applications, Reviews & Ratings, Enquiry Details, Change Password, Logout
- 4 stats cards: Available Jobs (`my_jobs`), Applications Sent (`applications`), Rating (4.8★), Total Earnings (₹0)
- Quick Actions row: Browse Jobs, Update Profile, Messages buttons
- Recent Job Postings scrollable panel — iterates `my_jobs` from context, shows title, description preview, category badge, budget, date, and View Applications button
- Empty state with Post Your First Job link if no jobs posted
- Recent Applications scrollable panel — iterates `applications` from context, shows job title, applied date, status badge (color-coded: warning/success/danger/info)
- Empty state with Browse Jobs link if no applications
- Tips for Success section: Complete Profile, Respond Quickly, Deliver Quality, Build Reputation

**`dashboard/tables.html` — Enquiry Details (Matrix Admin)**
- Same Matrix Admin layout and sidebar as `index.html`
- DataTables-powered table (`#zero_config`) with built-in search, sorting, and pagination
- Columns: Sr. No., Full Name, Email Id, Mobile, Message, Edit, Delete
- Edit button links to `edit_record` view
- Delete button uses a POST form with `confirm()` dialog before submission

---

## Key Features

### User Registration & Login
- Separate registration flow for housewife freelancers and clients via radio button selection
- Email uniqueness checked before account creation
- Username auto-generated from email prefix; appends user count if already taken
- Password validation: frontend match check + backend minimum 6 character check
- Login supports both email address and username lookup
- Role-based redirect after login: housewives → housewife dashboard, clients → client dashboard
- Session stores `username` key for display in dashboard templates

### Job Marketplace
- Clients can post jobs with title, category, description, budget, and location
- Post job form enforces role-based access: non-clients see a restriction message
- Freelancers browse all active (`is_active=True`) job listings on the Find Jobs page
- Search queries title, description, and location simultaneously using Django Q objects
- Category sidebar filter with radio buttons that auto-submit on selection change
- One-click apply with duplicate check — shows warning if already applied
- Job detail page shows apply button only to housewife users who have not yet applied

### Dashboards
- **Client Dashboard:** Displays posted jobs, submitted applications, stats cards, and quick action buttons
- **Housewife Dashboard:** Displays applied jobs, available jobs excluding already-applied ones, completed job count, and total earnings calculated by parsing budget strings from completed applications

### Service Requests
- Homepage quote form lets any visitor request a service without logging in
- Fields: name, email, phone, service type, message
- Data saved to `ServiceRequest` model; success flash message shown on redirect

### Enquiry Record Management (CRUD)
- Create: registration form data saved to `enquiry_table`
- Read: `records.html` (basic Bootstrap 3 table) and `dashboard/tables.html` (DataTables)
- Update: edit form at `/edit/<id>/`, saved via POST to `/update/<id>/`
- Delete: POST form at `/delete/<id>/` with confirm dialog

---

## How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/bagadeanushka07-a11y/Intership_Project.git
cd Intership_Project
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

**3. Install Django**
```bash
pip install django==3.2.13
```

**4. Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

**5. Create a superuser (for Django admin access)**
```bash
python manage.py createsuperuser
```

**6. Run the development server**
```bash
python manage.py runserver
```

**7. Open in browser**
```
http://127.0.0.1:8000/
```

**8. Access Django Admin**
```
http://127.0.0.1:8000/admin/
```

---

## Django Settings Overview

| Setting              | Value                                  |
|----------------------|----------------------------------------|
| `DEBUG`              | `True`                                 |
| `ALLOWED_HOSTS`      | `[]` (localhost only)                  |
| `DATABASE ENGINE`    | `django.db.backends.sqlite3`           |
| `DATABASE NAME`      | `db.sqlite3`                           |
| `STATIC_URL`         | `/static/`                             |
| `STATICFILES_DIRS`   | `[BASE_DIR, 'static']`                 |
| `TEMPLATES DIRS`     | `['templates']`                        |
| `INSTALLED APPS`     | Default Django apps + `application`    |
| `DEFAULT_AUTO_FIELD` | `BigAutoField`                         |
| `TIME_ZONE`          | `UTC`                                  |
| `LANGUAGE_CODE`      | `en-us`                                |

---

## Developer

**Anushka Bagade**
Internship Project — Freelancera (A Service and Job Marketplace)
