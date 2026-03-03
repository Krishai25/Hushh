import streamlit as st
import email_service

st.set_page_config(page_title="Kai Campus Admin", page_icon="🔐")

st.title("Admin Control Panel 🔐")
st.markdown("---")

st.header("📢 Email Reminder System")
st.write("This tool checks for students who are in `all_mails.json` but have either:")
st.write("1. Not registered on the platform at all.")
st.write("2. Registered but have signed up for **0 events**.")

if st.button("Check & Send Reminders", type="primary"):
    with st.spinner("Checking records and sending emails..."):
        # Reload module to ensure fresh code
        import importlib
        importlib.reload(email_service)
        result = email_service.process_reminders(
            all_mails_file='all_mails.json',
            students_file='students.json'
        )
        
    if result.get("status") == "success":
        st.success(result["message"])
        
        # Display logs
        logs = result.get("logs", [])
        if logs:
             st.expander("Process Logs").write(logs)
        
        if result.get("targets"):
            st.expander("View Recipients").write(result["targets"])
    else:
        st.error(f"Error: {result.get('message')}")
        logs = result.get("logs", [])
        if logs:
             st.expander("Process Logs").write(logs)

st.markdown("---")
st.caption("Secure Admin Panel for Kai Campus")
