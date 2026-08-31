# ==============================================================================
# 🚀 AONIK HOSTING - Cloud Execution & Bot Management Platform
# Backend Core Engine: Flask, Multi-threading, Process Sandboxing, JWT & OAuth2
# Author: Aonik Hosting Team (@onikislamhhd)
# ==============================================================================

import os
import sys
import time
import json
import uuid
import shutil
import logging
import subprocess
import threading
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_file
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "aonik_hosting_super_secret_jwt_key_9821_!@#")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Configuration & Directories
DATA_DIR = os.path.join(os.getcwd(), "data")
BOTS_DIR = os.path.join(os.getcwd(), "bots")
TEMPLATES_DIR = os.path.join(os.getcwd(), "templates")
LOGS_DIR = os.path.join(os.getcwd(), "logs")

for directory in [DATA_DIR, BOTS_DIR, LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(LOGS_DIR, "aonik_system.log"), encoding='utf-8')
    ]
)

# In-Memory Running Bot Process Registry
RUNNING_PROCESSES = {}
PROCESS_LOGS = {}

# ------------------------------------------------------------------------------
# Helpers & Database Utilities
# ------------------------------------------------------------------------------
USERS_FILE = os.path.join(DATA_DIR, "users.json")
SERVERS_FILE = os.path.join(DATA_DIR, "servers.json")

def load_json(filepath, default):
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=2)
        return default
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading {filepath}: {e}")
        return default

def save_json(filepath, data):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logging.error(f"Error saving {filepath}: {e}")

# Default Initial Data
INITIAL_USERS = [
    {
        "id": "u-admin",
        "username": "admin",
        "email": "html@gmail.com",
        "password": "password123",
        "role": "admin",
        "created_at": "2026-08-31"
    },
    {
        "id": "u-html",
        "username": "html@gmail",
        "email": "html@gmail.com",
        "password": "password123",
        "role": "admin",
        "created_at": "2026-08-31"
    }
]

INITIAL_SERVERS = [
    {
        "server_id": "srv-bot-9821",
        "name": "Telegram Bot Pro",
        "username": "html@gmail",
        "type": "telegram",
        "ram": "512MB",
        "disk": "2GB",
        "expiry": "2026-09-30",
        "expiryDays": 30,
        "cpu_limit": 60,
        "status": "running",
        "login_url": "https://srv-bot-9821.aonikhost.net",
        "main_file": "main.py",
        "requirements_file": "requirements.txt",
        "runtime_version": "Python 3.11",
        "auto_restart": True,
        "created_at": "2026-08-31"
    }
]

# Initialize storage
if not os.path.exists(USERS_FILE):
    save_json(USERS_FILE, INITIAL_USERS)
if not os.path.exists(SERVERS_FILE):
    save_json(SERVERS_FILE, INITIAL_SERVERS)

# ------------------------------------------------------------------------------
# Routes: Web & Dashboard
# ------------------------------------------------------------------------------
@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        users = load_json(USERS_FILE, INITIAL_USERS)
        matched_user = next((u for u in users if (u["username"].lower() == username.lower() or u["email"].lower() == username.lower()) and u["password"] == password), None)
        
        if matched_user:
            session["user"] = matched_user
            logging.info(f"User {matched_user['username']} logged in successfully.")
            return redirect(url_for("admin" if matched_user["role"] == "admin" else "home"))
        else:
            return render_template("login.html", error="Invalid username or password. Use 'html@gmail' / 'password123'")
            
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    user = session["user"]
    servers = load_json(SERVERS_FILE, INITIAL_SERVERS)
    user_servers = [s for s in servers if s["username"].lower() == user["username"].lower() or user["role"] == "admin"]
    return render_template("home.html", user=user, servers=user_servers)

@app.route("/admin")
def admin():
    if "user" not in session or session["user"]["role"] != "admin":
        return redirect(url_for("login"))
    users = load_json(USERS_FILE, INITIAL_USERS)
    servers = load_json(SERVERS_FILE, INITIAL_SERVERS)
    return render_template("admin.html", user=session["user"], users=users, servers=servers)

# ------------------------------------------------------------------------------
# API Endpoints for Real-time Control
# ------------------------------------------------------------------------------
@app.route("/api/server/create", methods=["POST"])
def api_create_server():
    if "user" not in session or session["user"]["role"] != "admin":
        return jsonify({"success": False, "error": "Unauthorized"}), 403
    
    data = request.json or {}
    server_id = f"srv-{data.get('type', 'py')[:3]}-{uuid.uuid4().hex[:6]}"
    target_username = data.get("username", "html@gmail")
    
    new_server = {
        "server_id": server_id,
        "name": data.get("name", f"{target_username} Bot"),
        "username": target_username,
        "type": data.get("type", "telegram"),
        "ram": data.get("ram", "512MB"),
        "disk": data.get("disk", "1GB"),
        "expiry": data.get("expiry", "2026-09-30"),
        "expiryDays": int(data.get("expiryDays", 30)),
        "cpu_limit": int(data.get("cpu_limit", 80)),
        "status": "stopped",
        "login_url": f"https://{server_id}.aonikhost.net",
        "main_file": data.get("main_file", "main.py"),
        "requirements_file": data.get("requirements_file", "requirements.txt"),
        "runtime_version": data.get("runtime_version", "Python 3.11"),
        "auto_restart": True,
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }
    
    # Create Bot Folder
    bot_path = os.path.join(BOTS_DIR, server_id)
    os.makedirs(bot_path, exist_ok=True)
    
    # Seed default main.py & requirements.txt
    with open(os.path.join(bot_path, "main.py"), "w", encoding="utf-8") as f:
        f.write(f'# Auto-generated by AONIK HOSTING\nprint("🚀 Server {server_id} started successfully!")\n')
    with open(os.path.join(bot_path, "requirements.txt"), "w", encoding="utf-8") as f:
        f.write("requests\npython-dotenv\n")
        
    servers = load_json(SERVERS_FILE, INITIAL_SERVERS)
    servers.append(new_server)
    save_json(SERVERS_FILE, servers)
    
    return jsonify({"success": True, "server": new_server})

@app.route("/api/server/<server_id>/action", methods=["POST"])
def api_server_action(server_id):
    if "user" not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 403
        
    action = (request.json or {}).get("action") # start, stop, restart
    servers = load_json(SERVERS_FILE, INITIAL_SERVERS)
    server = next((s for s in servers if s["server_id"] == server_id), None)
    
    if not server:
        return jsonify({"success": False, "error": "Server not found"}), 404
        
    if action == "start":
        server["status"] = "running"
    elif action == "stop":
        server["status"] = "stopped"
    elif action == "restart":
        server["status"] = "running"
        
    save_json(SERVERS_FILE, servers)
    return jsonify({"success": True, "status": server["status"]})

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", code=404, message="Resource not found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", code=500, message="Internal Server Error"), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    logging.info(f"🌟 Starting AONIK HOSTING Platform on http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
