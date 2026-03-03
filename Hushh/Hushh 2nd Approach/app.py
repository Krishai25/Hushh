import streamlit as st
import json
import os
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Kai Campus", page_icon="🏛️", layout="wide")

# --- CONSTANTS ---
INTEREST_CATEGORIES = [
    "Coding", "Dancing", "Painting", "Design (UI/UX)", "Film", 
    "Sports", "Gaming", "Debate", "Leadership", "Workshop"
]

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    /* Global Styles */
    .reportview-container { background: #f7faf8 url("https://images.unsplash.com/photo-1541339907198-e08756dedf3f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80") no-repeat center fixed; background-size: cover; }
    .main { background-color: #f7faf8 !important; }
    h1, h2, h3 { color: #1a9e5c; font-family: 'Segoe UI', sans-serif; }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #1a9e5c;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #15844d;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    /* Input Fields */
    div[data-baseweb="input"] > div {
        background-color: white;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }

    /* Cards/Containers */
    .css-1r6slb0, .css-12oz5g7 {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e3ede7;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #e8f5e9;
        border-radius: 8px;
        color: #1a9e5c !important;
    }
    
    /* Event Card Style */
    .event-card {
        background-color: white;
        border: 1px solid #e3ede7;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 5px solid #1a9e5c;
    }
    </style>
""", unsafe_allow_html=True)

# --- JSON HELPERS ---
def load_data(filename, default=None):
    if default is None: default = {}
    if not os.path.exists(filename): return default
    try:
        with open(filename, 'r') as f:
            content = f.read().strip()
            return json.loads(content) if content else default
    except:
        return default

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

FILES = {
    'leaders': 'authentication.json',
    'students': 'students.json',
    'events': 'events.json' 
}

# --- SESSION STATE ---
if 'user' not in st.session_state: st.session_state.user = None
if 'role' not in st.session_state: st.session_state.role = None
if 'page' not in st.session_state: st.session_state.page = 'landing'

# --- MAIN APP ---
def main():
    if st.session_state.user:
        if st.session_state.role == 'Leader':
            leader_dashboard()
        elif st.session_state.role == 'Student':
            student_dashboard()
    else:
        # Check if navigating within landing page logic
        if st.session_state.page == 'landing':
            landing_page()
        elif st.session_state.page == 'leader_login':
            leader_login()
        elif st.session_state.page == 'student_auth':
            student_auth()

def landing_page():
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem;'>Kai.Campus <span style='color:#1a9e5c;'>.</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #555; font-size: 1.2rem;'>Your unified platform for clubs, events, and community.</p>", unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎓 Student Access", type="primary"):
                st.session_state.page = "student_auth"
                st.rerun()
        with col2:
            if st.button("🛡️ Club Leader", type="secondary"):
                st.session_state.page = "leader_login"
                st.rerun()

def leader_login():
    st.button("← Back", on_click=lambda: st.session_state.update(page='landing'))
    st.markdown("## Club Leader Sign In")
    
    with st.form("leader_login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            leaders = load_data(FILES['leaders'], default=[])
            # Handle list structure of existing authentication.json
            user = next((l for l in leaders if l['email'] == email and l['password'] == password), None)
            
            if user:
                st.session_state.user = user
                st.session_state.role = "Leader"
                st.rerun()
            else:
                st.error("Invalid credentials")

def student_auth():
    st.button("← Back", on_click=lambda: st.session_state.update(page='landing'))
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        with st.form("student_login"):
            email = st.text_input("Student Email")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                students = load_data(FILES['students'], default={})
                # students is a dict now: {email: {data}}
                if email in students:
                    student_data = students[email]
                    # Check plain password (in production, use hash!)
                    if student_data.get('password') == password:
                        st.session_state.user = student_data
                        st.session_state.user['email'] = email
                        st.session_state.role = "Student"
                        st.rerun()
                    else:
                        st.error("Invalid password.")
                else:
                    st.error("Email not found. Please sign up.")

    with tab2:
        with st.form("student_signup"):
            name = st.text_input("Full Name")
            new_email = st.text_input("College Email")
            new_pass = st.text_input("Create Password", type="password")
            
            st.write("Select Events You Are Interested In:")
            
            # --- DYNAMIC INTERESTS FROM EVENT TITLES ---
            all_events_data = load_data(FILES['events'], default={})
            available_titles = set()
            for club_events in all_events_data.values():
                for ev in club_events:
                    if 'title' in ev:
                        available_titles.add(ev['title'])
            
            # Convert to sorted list for display
            dynamic_options = sorted(list(available_titles))
            
            if not dynamic_options:
                st.info("No active events to choose from yet.")
            
            c1, c2 = st.columns(2)
            selected_interests = []
            
            # Divide into two columns
            mid = len(dynamic_options) // 2 + 1 if dynamic_options else 0
            
            with c1:
                for opt in dynamic_options[:mid]:
                    if st.checkbox(opt): selected_interests.append(opt)
            with c2:
                for opt in dynamic_options[mid:]:
                    if st.checkbox(opt): selected_interests.append(opt)
            
            if st.form_submit_button("Register"):
                # --- CHECK ALL_MAILS PERMISSION ---
                all_raw = load_data('all_mails.json', default={})
                # Handle simplified list vs object structure
                if isinstance(all_raw, list):
                    allowed_emails = all_raw
                else:
                    allowed_emails = all_raw.get('APPROVED_STUDENTS', {}).keys()
                
                if new_email not in allowed_emails:
                     st.error("Sorry, this email is not in the approved list.")
                     st.stop()
                
                students = load_data(FILES['students'], default={})
                if new_email in students:
                    st.warning("Email already registered.")
                else:
                    students[new_email] = {
                        "name": name,
                        "password": new_pass,
                        "interests": selected_interests,
                        "registered_events": []
                    }
                    save_data(FILES['students'], students)
                    st.success("Registration Successful! Please login.")

def leader_dashboard():
    user = st.session_state.user
    
    # Ensure we use club_id
    club_id = user.get('club_id')
    club_name = user.get('club_name')

    # Sidebar
    with st.sidebar:
        st.header(f"{club_name}")
        st.write(f"Logged in as: {user['email']}")
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.role = None
            st.session_state.page = 'landing'
            st.rerun()

    st.title("Club Management Dashboard")

    tab1, tab2 = st.tabs(["➕ Post New Event", "📋 Manage Events"])

    with tab1:
        st.subheader("Create a New Event")
        with st.form("new_event"):
            title = st.text_input("Event Title")
            # --- CRITICAL CHANGE: Categorizing events ensures accurate matching ---
            category = st.selectbox("Event Category (For Matching Interests)", INTEREST_CATEGORIES)
            
            desc = st.text_area("Description")
            venue = st.text_input("Venue")
            col1, col2 = st.columns(2)
            date = col1.date_input("Date")
            time = col2.time_input("Time")
            
            if st.form_submit_button("Publish Event"):
                all_events = load_data(FILES['events'], default={})
                if club_id not in all_events:
                    all_events[club_id] = []
                
                new_event = {
                    "id": f"{club_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "title": title,
                    "category": category, 
                    "description": desc,
                    "venue": venue,
                    "date": str(date),
                    "time": str(time),
                    "club_name": club_name,
                    "club_id": club_id,
                    "registered_count": 0 # Track registrations
                }
                
                all_events[club_id].append(new_event)
                save_data(FILES['events'], all_events)
                st.success(f"Event '{title}' Published under {category}!")

    with tab2:
        st.subheader("Your Active Events")
        all_events = load_data(FILES['events'], default={})
        my_events = all_events.get(club_id, [])
        
        if not my_events:
            st.info("No events created yet.")
        else:
            # Iterate backwards to allow deletion without index shifting
            for i in range(len(my_events) - 1, -1, -1):
                event = my_events[i]
                r_count = event.get('registered_count', 0)
                
                with st.expander(f"{event['title']} ({event['date']}) - {r_count} Registered"):
                    st.write(f"**Category:** {event.get('category', 'General')}")
                    st.write(f"**Venue:** {event['venue']} | **Time:** {event['time']}")
                    st.write(event['description'])
                    
                    if st.button("Delete Event", key=f"del_{event['id']}"):
                        del my_events[i]
                        all_events[club_id] = my_events
                        save_data(FILES['events'], all_events)
                        st.rerun()

def register_for_event(student_email, event_id, club_id):
    # This function handles the double-sided registration update
    start_time = datetime.now()
    
    # 1. Update Student Record
    students = load_data(FILES['students'], default={})
    
    events_data = load_data(FILES['events'], default={})
    
    # Check if key exists; if club_id not in events_data, return safely
    if club_id not in events_data:
        st.error("Error: Club ID not found for this event.")
        return

    # Determine the event object from the fresh file data
    if club_id in events_data:
        target_event = next((e for e in events_data[club_id] if e['id'] == event_id), None)
    
    if not target_event:
        st.error("Event no longer exists.")
        return

    if student_email in students:
        if 'registered_events' not in students[student_email]:
             students[student_email]['registered_events'] = []

        # Check dupes
        current_regs = students[student_email]['registered_events']
        if any(e.get('id') == event_id for e in current_regs):
            st.warning("You are already registered.")
            return

        # Add to student JSON
        students[student_email]['registered_events'].append({
            "id": target_event['id'],
            "title": target_event['title'],
            "date": target_event['date'],
            "venue": target_event['venue'],
            "registered_at": str(start_time)
        })
        save_data(FILES['students'], students)
        
        # --- NEW: Update Email Status in all_mails.json ---
        # If they registered successfully, change status from 'pending' (or 'sent') to 'registered'
        try:
             all_mail_data = load_data('all_mails.json', default={})
             # Handle structure
             if isinstance(all_mail_data, dict) and 'APPROVED_STUDENTS' in all_mail_data:
                 if student_email in all_mail_data['APPROVED_STUDENTS']:
                     # Only update if not already registered (though harmless to overwrite)
                     all_mail_data['APPROVED_STUDENTS'][student_email]['status'] = 'registered'
                     save_data('all_mails.json', all_mail_data)
        except Exception as e:
            st.error(f"Error updating email status: {e}")
        
        # 2. Update Event Record (Increment Count)
        # We need to find the event in the list and update it
        for e in events_data[club_id]:
            if e['id'] == event_id:
                current_count = e.get('registered_count', 0)
                e['registered_count'] = current_count + 1
                break
        
        save_data(FILES['events'], events_data)

        st.toast(f"✅ Registered for {target_event['title']}!")
        
        # Refresh session user
        st.session_state.user = students[student_email] 
        st.session_state.user['email'] = student_email
        st.rerun()
    else:
        st.error("Error finding student record.")

def student_dashboard():
    user = st.session_state.user
    email = user.get('email')
    my_interests = user.get('interests', [])
    
    # Sidebar
    with st.sidebar:
        st.header(f"👋 {user.get('name', 'Student')}")
        st.write("**Your Interests:**")
        if not my_interests:
            st.warning("No interests selected.")
        else:
            for i in my_interests:
                st.caption(f"• {i}")
            
        st.divider()
        st.write("**Registered Events:**")
        regs = user.get('registered_events', [])
        if regs:
            for r in regs:
                st.markdown(f"**{r['title']}**\n{r['date']}")
        else:
            st.caption("No events yet.")
            
        st.divider()
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.role = None
            st.session_state.page = 'landing'
            st.rerun()

    st.title("Campus Event Feed 📅")
    st.info(f"Welcome back! Showing events matching: **{', '.join(my_interests)}**")
    
    # 1. Load All Events
    all_events_data = load_data(FILES['events'], default={})
    
    # 2. Filter Events based on interests
    matched_events = []
    
    # Iterate over every club's list of events
    for c_id, events_list in all_events_data.items():
        if isinstance(events_list, list):
            for ev in events_list:
                # Check if event TITLE is in the student's selected interests
                if ev.get('title') in my_interests:
                    matched_events.append(ev)
    
    if not matched_events:
        st.warning("No events found matching your interests right now. Check back later!")
        # If no matched events, show all events section? (Optional, but user asked for strict matching)
    else:
        # Sort by date (optional)
        # matched_events.sort(key=lambda x: x['date'])
        
        for ev in matched_events:
            # Create a nice card for the event
            st.markdown(f"""
            <div class="event-card">
                <h3 style="margin:0; color:#1a9e5c;">{ev['title']}</h3>
                <p style="color:#666; font-size:0.9rem;">Hosted by: {ev.get('club_name', 'Club')} | <b>{ev.get('category')}</b></p>
                <hr>
                <p><b>📅 Date:</b> {ev['date']} | <b>⏰ Time:</b> {ev['time']}</p>
                <p><b>📍 Venue:</b> {ev['venue']}</p>
                <p><i>{ev['description']}</i></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Check if already registered
            is_registered_locally = any(r['id'] == ev['id'] for r in user.get('registered_events', []))
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if is_registered_locally:
                    st.button("✅ Registered", key=f"btn_{ev['id']}", disabled=True)
                else:
                    if st.button(f"Register", key=f"reg_{ev['id']}"):
                        register_for_event(email, ev['id'], ev.get('club_id'))

if __name__ == "__main__":
    main()
