import getpass

USERS = {"admin": "1234"}  # replace this with your own user store

def login():
    """
    Prompt for username/password.
    Returns True if credentials match, False otherwise.
    """
    print("🔐 Login Required")
    username = input("Username: ")
    password = input("Password: ")

    if USERS.get(username) == password:
        print("✅ Login Successful!")
        return True
    else:
        print("❌ Login Failed.")
        return False

def logout():
    """
    Notify user of logout.
    """
    print("👋 Logged out.")
