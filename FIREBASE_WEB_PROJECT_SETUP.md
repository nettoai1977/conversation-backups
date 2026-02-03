# Firebase Web Project Setup with Authentication

## Overview
This document outlines the steps to create a web project on netto-ai.web.app with login/password authentication to access your dashboard.

## Prerequisites
- Firebase project `netto-ai-85b6b` (already configured)
- Firebase CLI tools (available via npx)
- Dashboard HTML file (dashboard.html in your workspace)

## Step 1: Initialize Firebase Hosting in your project

First, let's create a basic Firebase web project structure:

```bash
mkdir firebase-web-project
cd firebase-web-project
npx firebase-tools init hosting
```

This will create the necessary Firebase configuration files.

## Step 2: Create the login page

Create a simple login page that will protect access to your dashboard:

### public/index.html (login page):
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Netto.AI Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-container {
            background-color: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 400px;
        }
        .form-group {
            margin-bottom: 1rem;
        }
        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: bold;
        }
        input {
            width: 100%;
            padding: 0.5rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 0.75rem;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 1rem;
        }
        button:hover {
            background-color: #0056b3;
        }
        .error {
            color: red;
            margin-top: 0.5rem;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Netto.AI Dashboard Login</h2>
        <form id="loginForm">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">Login</button>
            <div id="errorMessage" class="error"></div>
        </form>
    </div>

    <script src="/__/firebase/12.8.0/firebase-app-compat.js"></script>
    <script src="/__/firebase/12.8.0/firebase-auth-compat.js"></script>
    <script src="/__/firebase/init.js"></script>
    
    <script>
        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const errorMessage = document.getElementById('errorMessage');
            
            // Simple authentication - in production, you'd use Firebase Auth or a backend service
            if(username === 'admin' && password === 'password123') {
                // Successful login - redirect to dashboard
                sessionStorage.setItem('isLoggedIn', 'true');
                window.location.href = '/dashboard.html';
            } else {
                errorMessage.textContent = 'Invalid username or password';
            }
        });
    </script>
</body>
</html>
```

### public/dashboard.html (protected dashboard):
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Netto.AI Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background-color: #007bff;
            color: white;
            padding: 1rem;
            border-radius: 4px;
            margin-bottom: 2rem;
        }
        .logout-btn {
            background-color: #dc3545;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            cursor: pointer;
            float: right;
        }
        .dashboard-content {
            background-color: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Netto.AI Dashboard</h1>
        <button class="logout-btn" onclick="logout()">Logout</button>
    </div>
    
    <div class="dashboard-content">
        <!-- Your existing dashboard content will go here -->
        <!-- Loading your dashboard.html content -->
    </div>

    <script src="/__/firebase/12.8.0/firebase-app-compat.js"></script>
    <script src="/__/firebase/12.8.0/firebase-auth-compat.js"></script>
    <script src="/__/firebase/init.js"></script>
    
    <script>
        // Check if user is logged in
        if(!sessionStorage.getItem('isLoggedIn')) {
            window.location.href = '/';
        }
        
        function logout() {
            sessionStorage.removeItem('isLoggedIn');
            window.location.href = '/';
        }
        
        // Load the actual dashboard content
        fetch('/original-dashboard.html')
            .then(response => response.text())
            .then(data => {
                document.querySelector('.dashboard-content').innerHTML = data;
            })
            .catch(error => {
                console.error('Error loading dashboard:', error);
            });
    </script>
</body>
</html>
```

### public/original-dashboard.html (your existing dashboard):
```html
<!-- This will contain your existing dashboard.html content -->
<!-- Copied from your workspace dashboard.html file -->
```

## Step 3: Create Firebase configuration files

### firebase.json:
```json
{
  "hosting": {
    "public": "public",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
```

## Step 4: Deploy to Firebase Hosting

```bash
# Copy your existing dashboard to the public directory
cp ../dashboard.html public/original-dashboard.html

# Replace the placeholder content in dashboard.html with the actual dashboard content
# Then deploy:
npx firebase-tools deploy --only hosting
```

## Step 5: Set up Firebase Authentication (recommended approach)

For a more robust solution, you should use Firebase Authentication:

1. Enable Email/Password authentication in Firebase Console
2. Update the login logic to use Firebase Auth instead of simple username/password check

This setup will give you a protected dashboard accessible at https://netto-ai-85b6b.web.app with login authentication.