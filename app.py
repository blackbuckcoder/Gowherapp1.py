from flask import Flask, render_template_string, request, session, redirect, url_for
import base64

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_sessions'

# ==========================================
# 1. STATIC FILE CONTENTS (Simulating External Files)
# ==========================================

# ---  JQUERY (v3.6.0 -  ) ---
JQUERY_CONTENT = """
/*! jQuery v3.6.0 | (c) OpenJS Foundation and other contributors | jquery.org/license */
// This is a simulated file for testing purposes.
// In a real scenario, this file contains the full library code.
// Version 3.6.0 is known to have CVE-2020-11022, CVE-2020-11023, etc.
(function(window, undefined) {
    // Vulnerable .htmlPrefilter function simulation
    var jQuery = function(selector, context) {
        return new jQuery.fn.init(selector, context);
    };
    jQuery.fn = jQuery.prototype = {};
    window.jQuery = window.$ = jQuery;
})(window);
"""

# ---  BOOTSTRAP CSS (v4.6.0 -  ) ---
BOOTSTRAP_CONTENT = """
/*!
 * Bootstrap v4.6.0 (https://getbootstrap.com/)
 * Copyright 2011-2021 The Bootstrap Authors
 * Copyright 2011-2021 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
 */
/* Simulated CSS content */
body { font-family: sans-serif; }
.btn { padding: 10px; }
"""

# --- MAIN APP CSS (Custom Styling) ---
CUSTOM_CSS = """
:root {
    --primary-color: #007bff;
    --bg-color: #f4f6f9;
    --card-bg: #ffffff;
    --text-color: #333333;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

.navbar {
    background-color: #343a40;
    color: white;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar-brand {
    font-size: 1.5rem;
    font-weight: bold;
    color: white;
    text-decoration: none;
}

.navbar-search {
    display: flex;
    gap: 10px;
}

.navbar-search input {
    padding: 8px 12px;
    border-radius: 4px;
    border: 1px solid #ccc;
    width: 300px;
}

.navbar-search button {
    padding: 8px 16px;
    background-color: var(--primary-color);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.container {
    max-width: 900px;
    margin: 2rem auto;
    padding: 0 1rem;
    flex: 1;
}

.card {
    background: var(--card-bg);
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}

.card h2 {
    margin-top: 0;
    color: #343a40;
    border-bottom: 2px solid var(--primary-color);
    padding-bottom: 10px;
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.form-group input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ced4da;
    border-radius: 4px;
    box-sizing: border-box;
}

.btn {
    display: inline-block;
    padding: 10px 20px;
    font-size: 1rem;
    font-weight: 600;
    text-align: center;
    border-radius: 4px;
    cursor: pointer;
    width: 100%;
    border: none;
}

.btn-primary {
    color: #fff;
    background-color: var(--primary-color);
}

.alert {
    padding: 1rem;
    border-radius: 4px;
    margin-bottom: 1rem;
}

.alert-danger {
    color: #721c24;
    background-color: #f8d7da;
    border-color: #f5c6cb;
}

.alert-success {
    color: #155724;
    background-color: #d4edda;
    border-color: #c3e6cb;
}

.dashboard-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}

.stat-box {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 4px;
    text-align: center;
    border: 1px solid #dee2e6;
}

.footer {
    text-align: center;
    padding: 1rem;
    background: #e9ecef;
    color: #6c757d;
    margin-top: auto;
}
"""

# --- VULNERABLE APP JS (Logic) ---
APP_JS_CONTENT = """
// Main Application Logic

// Simulated Backend Libraries for Vulnerability Scanning
// These comments are inserted to simulate library detection
/*! undertow v2.3.14 */
/*! apache tomcat v10.1.42 */
/*! netty project v4.1.122 */
/*! netty v4.1.122.Final */
/*! logback v1.4.11 */
/*! jackson-databind v2.17.2 */
/*! spring boot v3.4.0 */
/*! Spring Framework v6.2.10 */
/*! spring framework v6.2.10 */
/*! spring web v6.2.10 */
/*! spring security v6.5.3 */

// VULNERABLE: Hardcoded API Key in clear text
const API_CONFIG = {
    endpoint: "https://api.galaxy-preorder.com/v1",
    key: "AKIAIOSFODNN7EXAMPLE" // Exposed Key
};

document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
    setupUnlock();
});

function loadDashboard() {
    const userInfo = document.getElementById('user-info');
    
    // VULNERABLE: User info extracted from DOM or local storage without validation
    // In this demo, we simulate a fetch from an internal endpoint
    fetch('/api/user/me') // This endpoint doesn't exist, simulating behavior
        .then(res => res.json())
        .then(data => {
            if(data && data.user) {
                userInfo.innerHTML = `
                    <h3>Welcome back, ${data.user.name}!</h3>
                    <p>Role: <strong>${data.user.role}</strong></p>
                `;
            }
        })
        .catch(() => {
            // Fallback for demo
            userInfo.innerHTML = `
                <h3>Welcome back, Admin!</h3>
                <p>Role: <strong>Administrator</strong></p>
            `;
        });
}

function setupUnlock() {
    const unlockBtn = document.getElementById('unlock-btn');
    const keyInput = document.getElementById('admin-key');
    const errorMsg = document.getElementById('unlock-error');
    
    if(unlockBtn) {
        unlockBtn.addEventListener('click', () => {
            const key = keyInput.value;
            // VULNERABLE: Client-side secret check
            if(key === 'admin123') {
                loadSecrets();
                document.getElementById('unlock-form').style.display = 'none';
                errorMsg.style.display = 'none';
            } else {
                errorMsg.style.display = 'block';
                errorMsg.textContent = 'Access Denied.';
            }
        });
    }
}

function loadSecrets() {
    // Load secrets from the vulnerable external file
    const script = document.createElement('script');
    script.src = '/static/secret_data.js';
    document.body.appendChild(script);
}
"""

# --- VULNERABLE SECRET DATA JS (PII: Plain & Base64) ---
SECRET_JS_CONTENT = """
// VULNERABLE: Exposing PII and Sensitive Config
// Some data is plain text, some is encoded (weak obfuscation)

// 1. Plain Text PII
const CUSTOMER_DATABASE = [
    { "id": 8821, "name": "Alice Johnson", "email": "alice.j@corp.com", "ssn": "123-45-6789" },
    { "id": 8822, "name": "Bob Smith", "email": "bob.smith@corp.com", "ssn": "987-65-4321" }
];

// 2. Base64 Encoded PII (Decoded: "admin:SuperSecretPass123!")
const BACKUP_CREDENTIALS = "YWRtaW46U3VwZXJTZWNyZXRQYXNzMTIhIQ==";

// 3. Base64 Encoded Config (Decoded: "db_host=prod-db.internal; port=3306")
const DB_CONFIG_OBFUSCATED = "ZGJfaG9zdD1wcm9kLWRiLmludGVybmFsOyBwb3J0PTMzMDY=";

// Function to display secrets
function renderSecrets() {
    const container = document.getElementById('secret-info');
    if(!container) return;

    let html = '<h4>System Configuration:</h4><ul>';
    
    // API Key from app.js
    html += `<li><strong>API Key:</strong> ${API_CONFIG.key}</li>`;
    
    // Plain Text Data
    html += `<li><strong>DB User (Plain):</strong> admin</li>`;
    
    // Base64 Data (Simulating "hidden" data)
    html += `<li><strong>Backup Creds (Enc):</strong> ${BACKUP_CREDENTIALS}</li>`;
    
    html += '</ul>';
    
    // Warning for testers
    html += '<p style="font-size:0.8rem; color:#666;">* Some credentials are Base64 encoded.</p>';
    
    container.innerHTML = html;
    container.style.display = 'block';
}

// Execute render
renderSecrets();
"""


# ==========================================
# 2. HTML TEMPLATES
# ==========================================

BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Galaxy Pre-order 2026 - Portal</title>
    
    <!-- External CSS References (Real Site Look) -->
    <link rel="stylesheet" href="/static/bootstrap.css">
    <link rel="stylesheet" href="/static/style.css">
    
    <!-- Simulated Backend Libraries for Vulnerability Scanning -->
    <!-- These comments are inserted to simulate library detection -->
    <!-- undertow v2.3.14 -->
    <!-- apache tomcat v10.1.42 -->
    <!-- netty project v4.1.122 -->
    <!-- netty v4.1.122.Final -->
    <!-- logback v1.4.11 -->
    <!-- jackson-databind v2.17.2 -->
    <!-- spring boot v3.4.0 -->
    <!-- Spring Framework v6.2.10 -->
    <!-- spring framework v6.2.10 -->
    <!-- spring web v6.2.10 -->
    <!-- spring security v6.5.3 -->
</head>
<body>
    <nav class="navbar">
        <a href="/" class="navbar-brand">
            <span>Galaxy</span> Pre-order
        </a>
        
        <!-- Search Bar -->
        <div class="navbar-search">
            <form action="/search" method="GET" style="display:flex; gap:10px; width:100%;">
                <input type="text" name="q" placeholder="Search products..." value="{{ search_query }}">
                <button type="submit">Search</button>
            </form>
        </div>

        {% if session.get('logged_in') %}
        <div style="margin-left: 20px;">
            <a href="/logout" style="color: white; text-decoration: none; font-weight: bold;">Logout</a>
        </div>
        {% endif %}
    </nav>

    <main class="container">
        {% block content %}{% endblock %}
    </main>

    <footer class="footer">
        &copy; 2026 Galaxy Pre-order. Internal Portal.
    </footer>

    <!-- External JS References -->
    <script src="/static/jquery.js"></script>
    <script src="/static/app.js"></script>
</body>
</html>
"""

LOGIN_PAGE = BASE_LAYOUT.replace("{% block content %}{% endblock %}", """
<div class="card" style="max-width: 400px; margin: 4rem auto;">
    <h2 style="text-align: center;">Admin Login</h2>
    
    {% if error %}
    <div class="alert alert-danger">{{ error }}</div>
    {% endif %}

    <form action="/login" method="POST">
        <div class="form-group">
            <label for="username">Username</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
    </form>
    
    <div style="margin-top: 1rem; text-align: center;">
        <a href="#" style="color: var(--primary-color); text-decoration: none;">Forgot password?</a>
    </div>
</div>
""")

DASHBOARD_PAGE = BASE_LAYOUT.replace("{% block content %}{% endblock %}", """
<div class="card">
    <div id="user-info">
        <!-- Loaded via app.js -->
    </div>
</div>

<div class="card">
    <h2>Recent Orders</h2>
    <div class="dashboard-stats">
        <div class="stat-box">
            <h3>Total Orders</h3>
            <p>1,240</p>
        </div>
        <div class="stat-box">
            <h3>Pending</h3>
            <p>45</p>
        </div>
        <div class="stat-box">
            <h3>Revenue</h3>
            <p>$1.2M</p>
        </div>
    </div>
</div>

<div class="card">
    <h2>System Status</h2>
    
    <!-- Unlock Form -->
    <div id="unlock-form" style="margin-bottom: 1rem;">
        <p style="color: #666; font-size: 0.9rem;">
            This section contains sensitive configuration data. Please enter your Admin Key to view.
        </p>
        <div style="display: flex; gap: 10px; max-width: 300px;">
            <input type="password" id="admin-key" placeholder="Enter Admin Key" style="margin-bottom: 0; padding: 8px;">
            <button id="unlock-btn" class="btn btn-primary" style="width: auto;">Unlock</button>
        </div>
        <div id="unlock-error" class="alert alert-danger" style="display: none; margin-top: 10px;"></div>
    </div>

    <!-- Secret Info (Hidden by default) -->
    <div id="secret-info" style="display: none;">
        <!-- Loaded via secret_data.js -->
    </div>
</div>
""")

SEARCH_RESULTS = BASE_LAYOUT.replace("{% block content %}{% endblock %}", """
<div class="card">
    <h2>Search Results</h2>
    
    {% if query %}
    <div class="alert alert-success">
        You searched for: <strong>{{ query|safe }}</strong>
    </div>
    {% endif %}

    <div style="padding: 1rem; background: #f8f9fa; border-radius: 4px;">
        <p>No results found for "{{ query|safe }}" in our database.</p>
        <p>Try searching for: <em>Galaxy S25, Watch, Buds</em></p>
    </div>
</div>
""")

# ==========================================
# 3. ROUTES
# ==========================================

@app.route('/')
def index():
    if session.get('logged_in'):
        return render_template_string(DASHBOARD_PAGE, search_query="")
    else:
        return render_template_string(LOGIN_PAGE, search_query="", error=None)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # VULNERABILITY: SQL Injection (Simulated)
    if "'" in username or "OR" in username.upper():
        session['logged_in'] = True
        session['username'] = 'Hacker/Admin'
        return redirect(url_for('index'))
    
    # Normal Logic
    if username == 'admin' and password == 'password':
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('index'))
    else:
        return render_template_string(LOGIN_PAGE, search_query="", error="Invalid credentials.")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('q', '')
    # VULNERABILITY: Reflected XSS
    return render_template_string(SEARCH_RESULTS, query=query, search_query=query)

# --- Static File Routes ---

@app.route('/static/jquery.js')
def serve_jquery():
    return JQUERY_CONTENT, 200, {'Content-Type': 'text/javascript'}

@app.route('/static/bootstrap.css')
def serve_bootstrap():
    return BOOTSTRAP_CONTENT, 200, {'Content-Type': 'text/css'}

@app.route('/static/style.css')
def serve_style():
    return CUSTOM_CSS, 200, {'Content-Type': 'text/css'}

@app.route('/static/app.js')
def serve_app_js():
    return APP_JS_CONTENT, 200, {'Content-Type': 'text/javascript'}

@app.route('/static/secret_data.js')
def serve_secret_js():
    return SECRET_JS_CONTENT, 200, {'Content-Type': 'text/javascript'}

if __name__ == '__main__':
    print("=================================================")
    print("  UPDATED VULNERABLE DEMO SITE STARTED")
    print("  Access at: http://127.0.0.1:5000")
    print("  Features:")
    print("  - External JS/CSS files (View Source looks real)")
    print("  - Outdated jQuery (v3.6.0)")
    print("  - PII in Plain Text AND Base64")
    print("  - Working XSS & SQLi")
    print("=================================================")
    app.run(debug=True, port=5000)
