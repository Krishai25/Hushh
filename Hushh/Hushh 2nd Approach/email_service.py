import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
import sys

# DEBUGGING: Print where we are looking for keys
print(f"Debug: searching for keys in {os.getcwd()}")
sys.path.append(os.getcwd())

try:
    import keys
    # Force reload in case of caching
    import importlib
    importlib.reload(keys)
    
    from keys import GMAIL_USER, GMAIL_APP_PASSWORD
    safe_pwd = len(GMAIL_APP_PASSWORD) if GMAIL_APP_PASSWORD else 0
    print(f"Debug: Keys loaded. User={GMAIL_USER}, PwdLen={safe_pwd}")
except ImportError as e:
    print(f"Debug: ImportError loading keys: {e}")
    GMAIL_USER = None
    GMAIL_APP_PASSWORD = None
except Exception as e:
    print(f"Debug: Other error loading keys: {e}")
    GMAIL_USER = None
    GMAIL_APP_PASSWORD = None

def load_json(filename, default=None):
    if default is None: default = []
    if not os.path.exists(filename): return default
    try:
        with open(filename, 'r') as f:
            content = f.read().strip()
            return json.loads(content) if content else default
    except:
        return default

def send_single_email(to_email, subject, body):
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        safe_pwd = "Set" if GMAIL_APP_PASSWORD else "None"
        return False, f"Gmail credentials missing. User={GMAIL_USER}, Pwd={safe_pwd}"
        
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        text = msg.as_string()
        server.sendmail(GMAIL_USER, to_email, text)
        server.quit()
        return True, "Sent"
    except Exception as e:
        return False, str(e)

def process_reminders(all_mails_file='all_mails.json', students_file='students.json'):
    # 1. Load Data
    all_mails_data = load_json(all_mails_file, default={})
    students_data = load_json(students_file, default={}) # dict
    
    # Check structure of all_mails.json
    approved_students = all_mails_data.get('APPROVED_STUDENTS', {})
    if not approved_students and isinstance(all_mails_data, list):
        # Fallback if file is still a list (though user said it's changed)
        approved_students = {email: {"status": "pending"} for email in all_mails_data}
    
    log_output = []
    
    def log(msg):
        print(msg)
        log_output.append(msg)
        
    log("Debug: Process started.")
    
    # 2. Identify Targets
    # ...
    
    # First, let's update statuses based on current student data
    # Create a clean dictionary to avoid modification while iterating issues
    original_students = list(approved_students.items())
    
    for email_raw, info in original_students:
        email = email_raw.strip()
        current_status = info.get('status', 'unknown')
        log(f"Debug: Pre-check {email} (raw: '{email_raw}') status: {current_status}")
        
        # Check if they have registered for events
        if email in students_data:
            regs = students_data[email].get('registered_events', [])
            if regs:
                # User has events, so they are active.
                if current_status != 'registered':
                    info['status'] = 'registered'
                    log(f"Synced {email}: pending -> registered")
            else:
                # User is in system but no events.
                if current_status != 'sent':
                     info['status'] = 'pending'
        else:
             # User not even in system.
             if current_status != 'sent':
                 info['status'] = 'pending'
                 
    # Now collect targets who are still 'pending'
    targets = []
    for email_raw, info in approved_students.items():
        status = info.get('status')
        log(f"Debug: Post-check {email_raw} status: {status}")
        if status == 'pending':
            targets.append(email_raw.strip())
            
    log(f"Debug: Pending targets found: {targets}")
            
    log(f"Debug: Pending targets found: {targets}")
            
    if not targets:
        # Save updates like 'registered' status even if no emails to send
        log("Debug: No targets found. Saving updated statuses anyway.")
        try:
            with open(all_mails_file, 'w') as f:
                json.dump(all_mails_data, f, indent=4)
        except Exception as e:
            log(f"Error saving file: {e}")
            
        return {"status": "success", "message": "No pending students found.", "sent_count": 0, "failed_count": 0, "logs": log_output}

    # 3. Send Emails
    subject = "Don't Miss Out! Join Us at Kai Campus Events 🚀"
    body = """
Hello!

We noticed you haven't registered for any upcoming events on Kai Campus yet.

Most of your peers are eagerly participating in our workshops, hackathons, and cultural meets! 
It's a great opportunity to learn, network, and have fun.

Log in to your dashboard now and check out what's happening.

Best Regards,
Kai Campus Team
"""
    
    sent_count = 0
    failed_count = 0
    
    for email in targets:
        success, msg = send_single_email(email, subject, body)
        if success:
            sent_count += 1
            approved_students[email]['status'] = 'sent'
            log(f"Sent email to {email}. Status updated to 'sent'.")
        else:
            failed_count += 1
            log(f"Failed to send to {email}: {msg}")
            
    # 4. Save updated statuses back to all_mails.json
    all_mails_data['APPROVED_STUDENTS'] = approved_students
    log("Debug: Saving updated statuses to disk...")
    try:
        # Use absolute path to be sure
        abs_path = os.path.abspath(all_mails_file)
        with open(abs_path, 'w') as f:
            json.dump(all_mails_data, f, indent=4)
        log(f"Debug: File write successful to {abs_path}")
        
    except Exception as e:
        log(f"Debug: File write FAILED: {e}")
        return {"status": "error", "message": f"File write failed: {e}", "sent_count": sent_count, "failed_count": failed_count, "logs": log_output}
            
    return {
        "status": "success", 
        "message": f"Process complete. Sent: {sent_count}, Failed: {failed_count}",
        "sent_count": sent_count,
        "failed_count": failed_count,
        "targets": targets,
        "logs": log_output
    }
