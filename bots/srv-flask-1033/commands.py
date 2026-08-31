def handle_start(user_id, username):
    return f"👋 Welcome {username} to Aonik Hosting Bot Services! Use /help for available actions."

def handle_status():
    return {
        "status": "online",
        "load": "optimal",
        "version": "3.1-stable"
    }
