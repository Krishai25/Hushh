# First Approach

## 📌 Project Overview

This project is an AI-Powered Event Recommendation and Automation System built using:

- n8n (Workflow Automation)
- Google Sheets (Database)
- AI Chatbot
- Webhooks
- HTML UI Forms
- Email Automation (Guilt-Trap Strategy)

The system allows users to:

1. Chat with an AI assistant.
2. Retrieve their interest field from a database using their name.
3. View events related to their interests.
4. Register for events.
5. Receive psychologically persuasive "Guilt-Trap" emails for high-demand events.
6. Allow coordinators to add new events dynamically.

This system runs completely on automation workflows inside n8n without requiring a traditional backend server.

---

## 🧠 System Architecture

The system is divided into three major modules:

1. AI Chatbot Workflow
2. User Registration Webhook
3. Event Creation Webhook
4. Guilt-Trap Email Automation

Google Sheets acts as the centralized database.

---

# 🤖 1. AI Chatbot Workflow

## 🔄 Flow

User → Chat UI → Webhook → AI Agent → Google Sheets → Event Matching → Chat Response

## 🧩 How It Works

1. The chatbot greets the user.
2. It asks for the user’s name.
3. The system checks the **User Details Google Sheet**.
4. If the user exists:
   - The interest field is retrieved automatically.
5. If the user does not exist:
   - The chatbot asks for their interest and stores it.
6. The system searches the **Events Google Sheet**.
7. Events matching the user’s interest are displayed.
8. The chatbot asks the user if they would like to register.

This makes the chatbot function as an intelligent event assistant.

---

# 📊 Database Structure (Google Sheets)

## 1️⃣ User Details Sheet

Stores:
- Name
- Email
- Interest Field

This acts as the user database.

---

## 2️⃣ Events Sheet

Stores:
- Event Name
- Interest Field
- Event Date
- Description
- Registration Count

This acts as the event database.

---

# 🌐 2. User Registration Webhook

## 🎯 Purpose

To collect and store new user information.

## 🔄 Flow

User Form → Webhook → Google Sheets (Append Row)

## 📌 Function

- Stores new users.
- Saves their interest field.
- Updates the database in real time.

This ensures every user is permanently stored for future event recommendations.

---

# 🏢 3. Event Creation Webhook (Club Coordinator)

## 🎯 Purpose

To allow event coordinators to add events dynamically.

## 🔄 Flow

Coordinator Form → Webhook → Google Sheets (Append Row)

## 📌 Function

- Adds new events.
- Categorizes them by interest field.
- Updates registration tracking data.

This ensures event data remains current and scalable.

---

# 🔥 4. Guilt-Trap Email Automation

## 🎯 Purpose

To increase event registrations using psychological motivation.

## 🧠 Strategy Used

The system uses a **Guilt-Trap + FOMO (Fear of Missing Out)** strategy.

When:
- An event’s registration count crosses a certain threshold,

The system automatically triggers an AI-generated email.

---

## 📧 How It Works

1. After matching users with events,
2. The system checks the event’s registration count.
3. If the count is high,
4. An AI Agent generates:
   - A persuasive subject line
   - A psychologically motivating email body
5. The Gmail node sends the email.

---

## 🧠 Guilt-Trap Logic

The email content:

- Mentions the student’s name.
- Mentions how many peers have already registered.
- Highlights that others in the same interest field are participating.
- Creates subtle social pressure.
- Encourages immediate action.

Example Concept:

“45 students interested in AI have already registered. Many of your peers are already gaining the advantage. Don’t be the one left behind.”

This increases urgency and conversion rate.

---

# 🔄 Overall Automation Logic

The system performs:

- Name-based user lookup
- Interest-based event filtering
- Event recommendation
- Registration prompting
- High-demand event detection
- AI-based persuasive email generation
- Real-time Google Sheets updates

All handled inside n8n workflows.

---

# 🏗️ Why This First Approach?

This approach focuses on:

- Low-code automation
- Simplicity
- Modularity using webhooks
- Real-time database updates
- AI-driven personalization
- Scalable architecture

It avoids complex backend development while maintaining intelligent behavior.

---

# 🚀 Key Features

- AI-powered chatbot assistant
- Dynamic event recommendation
- Google Sheets as a database
- Separate modular webhooks
- Automated user storage
- Automated event creation
- Guilt-Trap marketing emails
- Fully workflow-based backend
- No traditional server required

---

# 📈 Future Improvements

- Login and authentication system
- Event confirmation emails
- WhatsApp notifications
- Admin analytics dashboard
- Event popularity tracking
- Personalized AI recommendations
- Behavior-based targeting
- Role-based coordinator dashboard

---

# 🏁 Conclusion

The First Approach demonstrates how automation tools like n8n, combined with AI and Google Sheets, can build a complete event management and marketing system without writing backend code.

This system showcases:

- Intelligent chat interaction
- Database-driven automation
- Psychological marketing integration
- Real-time updates
- Scalable event management architecture

Built using automation-first design principles.