# Second Approach – Kai Campus Event Management System

## 📌 Project Overview

Kai Campus is a Streamlit-based event management platform designed for college clubs and students.

This system provides:

- Student authentication and dashboard
- Club leader event management
- Interest-based event matching
- Event registration tracking
- Automated email reminder system (Guilt-Trap Strategy)
- Admin control panel

The entire system runs using:
- Python
- Streamlit
- JSON-based data storage
- Gmail SMTP automation
- Google Generative AI (Gemini integration ready)

---

# 🏗️ System Architecture

The system consists of four main modules:

1. Student Module
2. Leader Module
3. Admin Email Reminder System
4. JSON-Based Database Layer

All data is stored locally using structured JSON files.

---

# 🎓 Student Module

## 🔐 Authentication

Students can:
- Sign up (if approved)
- Log in
- Select event interests dynamically

Student authentication is handled using:

authentication.json  
students.json  → :contentReference[oaicite:8]{index=8}

Students must be present in the approved list:

all_mails.json → :contentReference[oaicite:9]{index=9}

---

## 📅 Student Dashboard

Once logged in, students can:

- View events matching their selected interests
- Register for events
- Track registered events
- See event details (venue, time, description)

Event matching is based on:

Student interests (event title-based matching)  
Events stored in → :contentReference[oaicite:10]{index=10}

When a student registers:
- Their record is updated in students.json
- The event's registered_count is incremented
- Their email status is updated in all_mails.json

---

# 🛡️ Leader Module (Club Dashboard)

Club leaders authenticate using:

authentication.json → :contentReference[oaicite:11]{index=11}

After login, leaders can:

- Post new events
- Categorize events
- Manage active events
- Delete events
- View registration count

Events are stored in:

events.json → :contentReference[oaicite:12]{index=12}

Each event contains:
- Event ID
- Title
- Category
- Description
- Venue
- Date
- Time
- Club name
- Registered count

---

# 🔐 Admin Control Panel

Admin interface:

admin.py → :contentReference[oaicite:13]{index=13}

This module:

- Checks approved students list
- Identifies students who:
  - Have not registered
  - Have registered but joined 0 events
- Sends automated reminder emails
- Displays logs and recipients

---

# 📧 Guilt-Trap Email Automation

Email automation logic is handled in:

email_service.py → :contentReference[oaicite:14]{index=14}

## 🎯 Purpose

To increase student participation using a subtle psychological trigger:

- Social pressure
- Fear of Missing Out (FOMO)
- Peer comparison

## 🧠 How It Works

1. Approved students are tracked in:
   all_mails.json → :contentReference[oaicite:15]{index=15}

2. The system checks:
   - If student exists in students.json
   - If they have registered for any events

3. If status = "pending":
   - Email is sent
   - Status updated to "sent"

4. If student registers:
   - Status updated to "registered"

---

## 📬 Email Content Strategy

The email includes:

- Reminder tone
- Mention of peer participation
- Encouragement to log in
- Call-to-action

Example Concept:

“Most of your peers are already participating in workshops and cultural events. Don’t miss out!”

This increases conversion rates.

---

# 🗂️ Data Structure Overview

## 📁 students.json → :contentReference[oaicite:16]{index=16}

Stores:
- Name
- Password
- Interests
- Registered events

---

## 📁 events.json → :contentReference[oaicite:17]{index=17}

Stores:
- Club-wise events
- Registration count

---

## 📁 all_mails.json → :contentReference[oaicite:18]{index=18}

Tracks:
- Approved emails
- Status:
  - pending
  - sent
  - registered

---

## 📁 authentication.json → :contentReference[oaicite:19]{index=19}

Stores:
- Leader login credentials
- Club ID
- Club name

---

# ⚙️ Dependencies

requirements.txt → :contentReference[oaicite:20]{index=20}

Includes:
- streamlit
- google-generativeai

---

# 🚀 Key Features

- Role-based authentication
- Interest-driven event feed
- Double-sided registration update logic
- Admin-triggered email reminders
- Guilt-trap persuasion strategy
- JSON-based persistent storage
- Real-time registration tracking
- Modular and scalable design

---

# 🧠 Design Philosophy – Second Approach

This first approach focuses on:

- Simplicity
- Automation-first architecture
- JSON as lightweight database
- Psychological engagement strategy
- Clear separation of roles
- Easy expandability

It avoids complex database setups and backend frameworks while delivering a fully functional campus event ecosystem.

---

# 📈 Future Improvements

- Password hashing
- Role-based permissions
- AI-generated dynamic email content (Gemini integration ready)
- Event analytics dashboard
- WhatsApp notifications
- Admin monitoring tools
- Database migration to SQL
- Deployment to cloud environment

---

# 🏁 Conclusion

Kai Campus demonstrates how a fully functional event management system can be built using:

- Streamlit UI
- Structured JSON data
- Automation logic
- Email engagement strategy
- Role-based workflows

This project showcases practical implementation of:

- Authentication
- Data synchronization
- Event matching
- Registration tracking
- Psychological marketing automation


Built using automation-first principles.
