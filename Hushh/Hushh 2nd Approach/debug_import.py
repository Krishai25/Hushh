try:
    import keys
    print("Successfully imported keys module:", keys)
    print("GMAIL_USER:", getattr(keys, 'GMAIL_USER', 'Not Found'))
    print("GMAIL_APP_PASSWORD:", getattr(keys, 'GMAIL_APP_PASSWORD', 'Not Found'))
except ImportError as e:
    print("ImportError:", e)
except Exception as e:
    print("Error:", e)
