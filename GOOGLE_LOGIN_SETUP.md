# 🔐 Google OAuth2 Login Setup Guide for AONIK HOSTING

This document guides you through setting up Google Authentication for your cloud panel.

### Step 1: Google Cloud Console
1. Visit [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project named **AONIK Hosting**.
3. Go to **APIs & Services > Credentials**.
4. Click **Create Credentials > OAuth client ID**.
5. Application type: **Web application**.

### Step 2: Authorized URIs
- **Authorized JavaScript origins**:
  - `http://localhost:5000`
  - `https://your-domain.aonikhost.net`
- **Authorized redirect URIs**:
  - `http://localhost:5000/auth/google/callback`
  - `https://your-domain.aonikhost.net/auth/google/callback`

### Step 3: Configure .env
Copy Client ID and Client Secret into your `.env` file:
```env
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_secret_key
```

### Step 4: Admin Access
- Direct admin account: `html@gmail` (or `html@gmail.com`) with password `password123`.
