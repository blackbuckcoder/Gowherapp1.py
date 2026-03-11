from flask import Flask, render_template_string, request, session, redirect, url_for
import json
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'prod_session_key_2024_secure'

# ==========================================
# PRE-LOGIN JAVASCRIPT (Clean, minimal)
# ==========================================

PRE_LOGIN_JS = """
// CloudVerify Platform - Authentication Module
// Version: 2.4.1
// Build: 20240309

(function() {
    'use strict';

    const CloudVerifyAuth = {
        config: {
            apiEndpoint: '/api/v1',
            timeout: 30000,
            maxRetries: 3
        },

        init: function() {
            this.bindEvents();
            this.checkSession();
        },

        bindEvents: function() {
            const loginForm = document.getElementById('login-form');
            if (loginForm) {
                loginForm.addEventListener('submit', this.handleLogin.bind(this));
            }

            const forgotPasswordLink = document.querySelector('.forgot-password');
            if (forgotPasswordLink) {
                forgotPasswordLink.addEventListener('click', this.handleForgotPassword.bind(this));
            }
        },

        checkSession: function() {
            const sessionToken = localStorage.getItem('cv_session_token');
            if (sessionToken) {
                window.location.href = '/dashboard';
            }
        },

        handleLogin: function(e) {
            e.preventDefault();
            
            const form = e.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);

            this.showLoading();

            fetch(this.config.apiEndpoint + '/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    localStorage.setItem('cv_session_token', result.token);
                    localStorage.setItem('cv_user_id', result.user_id);
                    window.location.href = '/dashboard';
                } else {
                    this.showError(result.message || 'Authentication failed');
                }
            })
            .catch(error => {
                this.showError('Connection error. Please try again.');
            })
            .finally(() => {
                this.hideLoading();
            });
        },

        handleForgotPassword: function(e) {
            e.preventDefault();
            const email = prompt('Enter your email address:');
            if (email) {
                // Simulate password reset
                alert('Password reset link has been sent to ' + email);
            }
        },

        showLoading: function() {
            const submitBtn = document.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner"></span> Authenticating...';
            }
        },

        hideLoading: function() {
            const submitBtn = document.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = 'Sign In';
            }
        },

        showError: function(message) {
            const errorContainer = document.getElementById('error-message');
            if (errorContainer) {
                errorContainer.textContent = message;
                errorContainer.style.display = 'block';
            }
        }
    };

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            CloudVerifyAuth.init();
        });
    } else {
        CloudVerifyAuth.init();
    }
})();
"""

# ==========================================
# POST-LOGIN JAVASCRIPT (Contains PII & Secrets)
# ==========================================

POST_LOGIN_JS = """
// CloudVerify Platform - Enterprise Dashboard
// Version: 2.4.1
// Production Environment

// VULNERABLE: Hardcoded API credentials
const API_CONFIG = {
    production: {
        endpoint: "https://api.cloudverify.io/v2",
        apiKey: "pk_live_51NzKm2Kx9mP3nQ8rR4tY6uI8oP2qR5sT7vW1xZ3cV5bX8zA2dC4eF6gH8jK0lM2nO4pQ6rS8tU0vW2xY4z",
        apiSecret: "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"
    },
    staging: {
        endpoint: "https://api-staging.cloudverify.io/v2",
        apiKey: "pk_test_51NzKm2Kx9mP3nQ8rR4tY6uI8oP2qR5sT7vW1xZ3cV5bX8zA2dC4eF6gH8jK0lM2nO4pQ6rS8tU0vW2xY4z",
        apiSecret: "sk_test_51NzKm2Kx9mP3nQ8rR4tY6uI8oP2qR5sT7vW1xZ3cV5bX8zA2dC4eF6gH8jK0lM2nO4pQ6rS8tU0vW2xY4zA2dC4eF6gH8jK0lM2n"
    },
    database: {
        host: "prod-db-cluster.cloudverify.io",
        port: 5432,
        username: "cv_admin",
        password: "CvPr0d@2024!Sec#reT",
        database: "cloudverify_prod",
        ssl: true
    },
    aws: {
        accessKeyId: "AKIAIOSFODNN7EXAMPLE",
        secretAccessKey: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        region: "us-east-1",
        s3Bucket: "cv-secure-docs-prod"
    },
    stripe: {
        publicKey: "pk_live_51HzKm2Kx9mP3nQ8rR4tY6uI8oP2qR5sT7vW1xZ3cV5bX8zA2dC4eF6gH8jK0lM2nO4pQ6rS8tU0vW2xY4z",
        secretKey: "sk_live_51HzKm2Kx9mP3nQ8rR4tY6uI8oP2qR5sT7vW1xZ3cV5bX8zA2dC4eF6gH8jK0lM2nO4pQ6rS8tU0vW2xY4z"
    }
};

// VULNERABLE: PII Data exposed in client-side JavaScript
const CUSTOMER_DATABASE = [
    {
        id: "CV-2024-001234",
        name: "Sarah Mitchell",
        email: "sarah.mitchell@techcorp.com",
        phone: "+1 (555) 234-5678",
        ssn: "542-18-7362",
        dateOfBirth: "1985-03-15",
        address: {
            street: "742 Evergreen Terrace",
            city: "Springfield",
            state: "IL",
            zipCode: "62701",
            country: "USA"
        },
        creditCard: {
            type: "Visa",
            number: "4532-1234-5678-9010",
            expiry: "12/26",
            cvv: "123"
        },
        bankAccount: {
            routingNumber: "021000021",
            accountNumber: "1234567890",
            bankName: "JPMorgan Chase"
        },
        subscription: {
            plan: "Enterprise",
            monthlyAmount: 299.99,
            startDate: "2023-01-15",
            status: "active"
        },
        createdAt: "2023-01-15T10:30:00Z"
    },
    {
        id: "CV-2024-001235",
        name: "James Rodriguez",
        email: "j.rodriguez@globalfin.com",
        phone: "+1 (555) 345-6789",
        ssn: "487-92-1563",
        dateOfBirth: "1978-07-22",
        address: {
            street: "1600 Pennsylvania Avenue NW",
            city: "Washington",
            state: "DC",
            zipCode: "20500",
            country: "USA"
        },
        creditCard: {
            type: "Mastercard",
            number: "5555-1234-5678-9010",
            expiry: "08/25",
            cvv: "456"
        },
        bankAccount: {
            routingNumber: "111000025",
            accountNumber: "9876543210",
            bankName: "Bank of America"
        },
        subscription: {
            plan: "Professional",
            monthlyAmount: 149.99,
            startDate: "2023-03-20",
            status: "active"
        },
        createdAt: "2023-03-20T14:22:00Z"
    },
    {
        id: "CV-2024-001236",
        name: "Emily Chen",
        email: "emily.chen@innovate.io",
        phone: "+1 (555) 456-7890",
        ssn: "392-45-8192",
        dateOfBirth: "1990-11-08",
        address: {
            street: "1 Infinite Loop",
            city: "Cupertino",
            state: "CA",
            zipCode: "95014",
            country: "USA"
        },
        creditCard: {
            type: "American Express",
            number: "3782-822463-10005",
            expiry: "03/27",
            cvv: "7890"
        },
        bankAccount: {
            routingNumber: "121000248",
            accountNumber: "2468135790",
            bankName: "Wells Fargo"
        },
        subscription: {
            plan: "Enterprise",
            monthlyAmount: 299.99,
            startDate: "2023-06-10",
            status: "active"
        },
        createdAt: "2023-06-10T09:15:00Z"
    },
    {
        id: "CV-2024-001237",
        name: "Michael Thompson",
        email: "m.thompson@logistics.net",
        phone: "+1 (555) 567-8901",
        ssn: "618-27-9543",
        dateOfBirth: "1982-05-30",
        address: {
            street: "350 Fifth Avenue",
            city: "New York",
            state: "NY",
            zipCode: "10118",
            country: "USA"
        },
        creditCard: {
            type: "Visa",
            number: "4111-1111-1111-1111",
            expiry: "09/26",
            cvv: "321"
        },
        bankAccount: {
            routingNumber: "026009593",
            accountNumber: "1357924680",
            bankName: "Bank of America"
        },
        subscription: {
            plan: "Business",
            monthlyAmount: 199.99,
            startDate: "2023-08-05",
            status: "active"
        },
        createdAt: "2023-08-05T16:45:00Z"
    },
    {
        id: "CV-2024-001238",
        name: "Amanda Foster",
        email: "amanda.f@startup.co",
        phone: "+1 (555) 678-9012",
        ssn: "754-83-6291",
        dateOfBirth: "1988-09-12",
        address: {
            street: "500 Terry Francois Street",
            city: "San Francisco",
            state: "CA",
            zipCode: "94158",
            country: "USA"
        },
        creditCard: {
            type: "Mastercard",
            number: "5425-1234-5678-9010",
            expiry: "11/25",
            cvv: "654"
        },
        bankAccount: {
            routingNumber: "021000021",
            accountNumber: "9876543210",
            bankName: "JPMorgan Chase"
        },
        subscription: {
            plan: "Professional",
            monthlyAmount: 149.99,
            startDate: "2023-10-18",
            status: "active"
        },
        createdAt: "2023-10-18T11:30:00Z"
    }
];

// VULNERABLE: Base64 encoded sensitive data (easily decoded)
const ENCRYPTED_SECRETS = {
    // Decodes to: "admin:CloudV3rify@2024!Admin"
    adminCredentials: "YWRtaW46Q2xvdWRWM3JpZnlAMjAyNCFBZG1pbg==",
    // Decodes to: "db_password=M@sterK3y#2024$Prod"
    databasePassword: "ZGJfcGFzc3dvcmQ9TUBzdGVySzN5IzIwMjQkUHJvZA==",
    // Decodes to: "jwt_secret=CloudV3rifyJWT2024!Secure#Key"
    jwtSecret: "and0X3NlY3JldD1DbG91ZFYzcmlmeUpXVDIwMjQhU2VjdXJlI0tleQ==",
    // Decodes to: "aws_secret=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    awsSecret: "YXdzX3NlY3JldD13SmFsciBYVXRuRkVNSS9LN01ERU5HL2JQeFJmaUNZRVhBTVBMRUtFWQ=="
};

// VULNERABLE: Employee personal information
const EMPLOYEE_DATA = [
    {
        id: "EMP-001",
        name: "Robert Williams",
        position: "Chief Executive Officer",
        email: "r.williams@cloudverify.io",
        phone: "+1 (555) 100-2000",
        salary: 250000,
        ssn: "123-45-6789",
        hireDate: "2018-01-15",
        department: "Executive"
    },
    {
        id: "EMP-002",
        name: "Jennifer Lee",
        position: "Chief Technology Officer",
        email: "j.lee@cloudverify.io",
        phone: "+1 (555) 100-2001",
        salary: 225000,
        ssn: "234-56-7890",
        hireDate: "2018-03-01",
        department: "Technology"
    },
    {
        id: "EMP-003",
        name: "David Kim",
        position: "VP of Engineering",
        email: "d.kim@cloudverify.io",
        phone: "+1 (555) 100-2002",
        salary: 195000,
        ssn: "345-67-8901",
        hireDate: "2019-06-15",
        department: "Engineering"
    }
];

// VULNERABLE: Transaction history with full details
const TRANSACTION_HISTORY = [
    {
        id: "TXN-2024-03-09-001",
        customerId: "CV-2024-001234",
        amount: 299.99,
        currency: "USD",
        description: "Enterprise Plan - Monthly",
        status: "completed",
        paymentMethod: "Visa ending in 9010",
        timestamp: "2024-03-09T00:15:32Z",
        ipAddress: "192.168.1.100"
    },
    {
        id: "TXN-2024-03-09-002",
        customerId: "CV-2024-001235",
        amount: 149.99,
        currency: "USD",
        description: "Professional Plan - Monthly",
        status: "completed",
        paymentMethod: "Mastercard ending in 9010",
        timestamp: "2024-03-09T01:22:18Z",
        ipAddress: "10.0.0.50"
    },
    {
        id: "TXN-2024-03-08-001",
        customerId: "CV-2024-001236",
        amount: 299.99,
        currency: "USD",
        description: "Enterprise Plan - Monthly",
        status: "completed",
        paymentMethod: "Amex ending in 0005",
        timestamp: "2024-03-08T23:45:00Z",
        ipAddress: "172.16.0.25"
    }
];

// Store sensitive data in localStorage (VULNERABLE)
localStorage.setItem('cv_api_config', JSON.stringify(API_CONFIG));
localStorage.setItem('cv_customer_data', JSON.stringify(CUSTOMER_DATABASE));
localStorage.setItem('cv_employee_data', JSON.stringify(EMPLOYEE_DATA));
localStorage.setItem('cv_user_token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkFkbWluIFVzZXIiLCJpYXQiOjE1MTYyMzkwMjJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c');

// Dashboard Application
(function() {
    'use strict';

    const CloudVerifyDashboard = {
        currentUser: null,
        currentView: 'overview',

        init: function() {
            this.loadUserInfo();
            this.bindEvents();
            this.loadDashboardData();
            this.initializeCharts();
        },

        loadUserInfo: function() {
            const userData = localStorage.getItem('cv_user_data');
            if (userData) {
                this.currentUser = JSON.parse(userData);
                this.updateUserDisplay();
            }
        },

        updateUserDisplay: function() {
            const userName = document.getElementById('user-name');
            const userRole = document.getElementById('user-role');
            const userEmail = document.getElementById('user-email');

            if (userName && this.currentUser) {
                userName.textContent = this.currentUser.name;
            }
            if (userRole && this.currentUser) {
                userRole.textContent = this.currentUser.role;
            }
            if (userEmail && this.currentUser) {
                userEmail.textContent = this.currentUser.email;
            }
        },

        bindEvents: function() {
            // Navigation
            const navItems = document.querySelectorAll('.nav-item');
            navItems.forEach(item => {
                item.addEventListener('click', this.handleNavigation.bind(this));
            });

            // Search
            const searchInput = document.getElementById('global-search');
            if (searchInput) {
                searchInput.addEventListener('input', this.handleSearch.bind(this));
            }

            // Export buttons
            const exportBtns = document.querySelectorAll('.export-btn');
            exportBtns.forEach(btn => {
                btn.addEventListener('click', this.handleExport.bind(this));
            });
        },

        handleNavigation: function(e) {
            e.preventDefault();
            const target = e.currentTarget.dataset.view;
            this.switchView(target);
        },

        handleSearch: function(e) {
            const query = e.target.value.toLowerCase();
            // VULNERABLE: Search without proper sanitization
            this.filterData(query);
        },

        handleExport: function(e) {
            const type = e.currentTarget.dataset.type;
            this.exportData(type);
        },

        switchView: function(view) {
            this.currentView = view;
            
            // Update navigation
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
                if (item.dataset.view === view) {
                    item.classList.add('active');
                }
            });

            // Update content
            this.loadViewContent(view);
        },

        loadViewContent: function(view) {
            const contentArea = document.getElementById('main-content');
            
            switch(view) {
                case 'overview':
                    this.renderOverview(contentArea);
                    break;
                case 'customers':
                    this.renderCustomers(contentArea);
                    break;
                case 'transactions':
                    this.renderTransactions(contentArea);
                    break;
                case 'reports':
                    this.renderReports(contentArea);
                    break;
                case 'settings':
                    this.renderSettings(contentArea);
                    break;
                default:
                    this.renderOverview(contentArea);
            }
        },

        renderOverview: function(container) {
            container.innerHTML = `
                <div class="dashboard-grid">
                    <div class="stat-card">
                        <div class="stat-icon">ðŸ‘¥</div>
                        <div class="stat-info">
                            <div class="stat-value">2,847</div>
                            <div class="stat-label">Active Customers</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">ðŸ’°</div>
                        <div class="stat-info">
                            <div class="stat-value">$847,290</div>
                            <div class="stat-label">Monthly Revenue</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">ðŸ“Š</div>
                        <div class="stat-info">
                            <div class="stat-value">94.7%</div>
                            <div class="stat-label">Success Rate</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">âš¡</div>
                        <div class="stat-info">
                            <div class="stat-value">12.4ms</div>
                            <div class="stat-label">Avg Response</div>
                        </div>
                    </div>
                </div>

                <div class="content-card">
                    <h3>Recent Activity</h3>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Timestamp</th>
                                <th>User</th>
                                <th>Action</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>2024-03-09 14:32:15</td>
                                <td>sarah.mitchell@techcorp.com</td>
                                <td>API Key Generated</td>
                                <td><span class="status success">Completed</span></td>
                            </tr>
                            <tr>
                                <td>2024-03-09 14:28:42</td>
                                <td>j.rodriguez@globalfin.com</td>
                                <td>Configuration Updated</td>
                                <td><span class="status success">Completed</span></td>
                            </tr>
                            <tr>
                                <td>2024-03-09 14:15:08</td>
                                <td>emily.chen@innovate.io</td>
                                <td>Report Exported</td>
                                <td><span class="status success">Completed</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            `;
        },

        renderCustomers: function(container) {
            let html = `
                <div class="content-card">
                    <div class="card-header">
                        <h3>Customer Management</h3>
                        <button class="btn btn-primary" data-type="customers">Export All Data</button>
                    </div>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Customer ID</th>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Phone</th>
                                <th>Plan</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
            `;

            CUSTOMER_DATABASE.forEach(customer => {
                html += `
                    <tr>
                        <td>${customer.id}</td>
                        <td>${customer.name}</td>
                        <td>${customer.email}</td>
                        <td>${customer.phone}</td>
                        <td>${customer.subscription.plan}</td>
                        <td><span class="status success">Active</span></td>
                        <td>
                            <button class="btn btn-sm" onclick="CloudVerifyDashboard.viewCustomer('${customer.id}')">View</button>
                        </td>
                    </tr>
                `;
            });

            html += `
                        </tbody>
                    </table>
                </div>
            `;

            container.innerHTML = html;
        },

        viewCustomer: function(customerId) {
            const customer = CUSTOMER_DATABASE.find(c => c.id === customerId);
            if (customer) {
                // VULNERABLE: Display full PII without proper authorization
                const modal = document.createElement('div');
                modal.className = 'modal';
                modal.innerHTML = `
                    <div class="modal-content">
                        <div class="modal-header">
                            <h3>Customer Details: ${customer.name}</h3>
                            <button class="close-modal" onclick="this.closest('.modal').remove()">&times;</button>
                        </div>
                        <div class="modal-body">
                            <div class="customer-details">
                                <div class="detail-section">
                                    <h4>Personal Information</h4>
                                    <p><strong>Full Name:</strong> ${customer.name}</p>
                                    <p><strong>Email:</strong> ${customer.email}</p>
                                    <p><strong>Phone:</strong> ${customer.phone}</p>
                                    <p><strong>SSN:</strong> ${customer.ssn}</p>
                                    <p><strong>Date of Birth:</strong> ${customer.dateOfBirth}</p>
                                </div>
                                <div class="detail-section">
                                    <h4>Address</h4>
                                    <p>${customer.address.street}</p>
                                    <p>${customer.address.city}, ${customer.address.state} ${customer.address.zipCode}</p>
                                    <p>${customer.address.country}</p>
                                </div>
                                <div class="detail-section">
                                    <h4>Payment Information</h4>
                                    <p><strong>Card Type:</strong> ${customer.creditCard.type}</p>
                                    <p><strong>Card Number:</strong> ${customer.creditCard.number}</p>
                                    <p><strong>Expiry:</strong> ${customer.creditCard.expiry}</p>
                                    <p><strong>CVV:</strong> ${customer.creditCard.cvv}</p>
                                </div>
                                <div class="detail-section">
                                    <h4>Bank Account</h4>
                                    <p><strong>Bank:</strong> ${customer.bankAccount.bankName}</p>
                                    <p><strong>Routing Number:</strong> ${customer.bankAccount.routingNumber}</p>
                                    <p><strong>Account Number:</strong> ${customer.bankAccount.accountNumber}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                document.body.appendChild(modal);
            }
        },

        renderTransactions: function(container) {
            let html = `
                <div class="content-card">
                    <div class="card-header">
                        <h3>Transaction History</h3>
                        <button class="btn btn-primary" data-type="transactions">Export</button>
                    </div>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Transaction ID</th>
                                <th>Customer ID</th>
                                <th>Amount</th>
                                <th>Description</th>
                                <th>Status</th>
                                <th>Timestamp</th>
                            </tr>
                        </thead>
                        <tbody>
            `;

            TRANSACTION_HISTORY.forEach(txn => {
                html += `
                    <tr>
                        <td>${txn.id}</td>
                        <td>${txn.customerId}</td>
                        <td>$${txn.amount.toFixed(2)}</td>
                        <td>${txn.description}</td>
                        <td><span class="status success">${txn.status}</span></td>
                        <td>${new Date(txn.timestamp).toLocaleString()}</td>
                    </tr>
                `;
            });

            html += `
                        </tbody>
                    </table>
                </div>
            `;

            container.innerHTML = html;
        },

        renderReports: function(container) {
            container.innerHTML = `
                <div class="content-card">
                    <h3>Reports & Analytics</h3>
                    <div class="report-grid">
                        <div class="report-card">
                            <h4>Revenue Report</h4>
                            <p>Monthly revenue analysis and trends</p>
                            <button class="btn btn-primary" data-type="revenue">Generate Report</button>
                        </div>
                        <div class="report-card">
                            <h4>Customer Analysis</h4>
                            <p>Customer growth and retention metrics</p>
                            <button class="btn btn-primary" data-type="customers">Generate Report</button>
                        </div>
                        <div class="report-card">
                            <h4>Security Audit</h4>
                            <p>System security and compliance report</p>
                            <button class="btn btn-primary" data-type="security">Generate Report</button>
                        </div>
                    </div>
                </div>
            `;

            // Re-bind export buttons
            container.querySelectorAll('.export-btn').forEach(btn => {
                btn.addEventListener('click', this.handleExport.bind(this));
            });
        },

        renderSettings: function(container) {
            container.innerHTML = `
                <div class="content-card">
                    <h3>System Configuration</h3>
                    <div class="settings-section">
                        <h4>API Configuration</h4>
                        <div class="config-item">
                            <label>API Endpoint:</label>
                            <input type="text" value="${API_CONFIG.production.endpoint}" readonly>
                        </div>
                        <div class="config-item">
                            <label>API Key:</label>
                            <input type="text" value="${API_CONFIG.production.apiKey}" readonly>
                        </div>
                        <div class="config-item">
                            <label>API Secret:</label>
                            <input type="password" value="${API_CONFIG.production.apiSecret}" readonly>
                        </div>
                    </div>
                    <div class="settings-section">
                        <h4>Database Configuration</h4>
                        <div class="config-item">
                            <label>Database Host:</label>
                            <input type="text" value="${API_CONFIG.database.host}" readonly>
                        </div>
                        <div class="config-item">
                            <label>Database Name:</label>
                            <input type="text" value="${API_CONFIG.database.database}" readonly>
                        </div>
                        <div class="config-item">
                            <label>Username:</label>
                            <input type="text" value="${API_CONFIG.database.username}" readonly>
                        </div>
                        <div class="config-item">
                            <label>Password:</label>
                            <input type="password" value="${API_CONFIG.database.password}" readonly>
                        </div>
                    </div>
                    <div class="settings-section">
                        <h4>AWS Configuration</h4>
                        <div class="config-item">
                            <label>Access Key ID:</label>
                            <input type="text" value="${API_CONFIG.aws.accessKeyId}" readonly>
                        </div>
                        <div class="config-item">
                            <label>Secret Access Key:</label>
                            <input type="password" value="${API_CONFIG.aws.secretAccessKey}" readonly>
                        </div>
                        <div class="config-item">
                            <label>Region:</label>
                            <input type="text" value="${API_CONFIG.aws.region}" readonly>
                        </div>
                    </div>
                </div>
            `;
        },

        loadDashboardData: function() {
            // Simulate loading dashboard data
            setTimeout(() => {
                console.log('Dashboard data loaded');
            }, 500);
        },

        initializeCharts: function() {
            // Placeholder for chart initialization
        },

        filterData: function(query) {
            // VULNERABLE: Client-side filtering without sanitization
            console.log('Filtering data for:', query);
        },

        exportData: function(type) {
            // VULNERABLE: Export sensitive data without proper checks
            let data;
            let filename;

            switch(type) {
                case 'customers':
                    data = JSON.stringify(CUSTOMER_DATABASE, null, 2);
                    filename = 'customers_export.json';
                    break;
                case 'transactions':
                    data = JSON.stringify(TRANSACTION_HISTORY, null, 2);
                    filename = 'transactions_export.json';
                    break;
                case 'revenue':
                    data = JSON.stringify({ revenue: 847290, customers: 2847 }, null, 2);
                    filename = 'revenue_report.json';
                    break;
                case 'security':
                    data = JSON.stringify(API_CONFIG, null, 2);
                    filename = 'security_audit.json';
                    break;
                default:
                    return;
            }

            // Download file
            const blob = new Blob([data], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
    };

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            CloudVerifyDashboard.init();
        });
    } else {
        CloudVerifyDashboard.init();
    }
})();
"""

# ==========================================
# VULNERABLE JQUERY (v3.6.0)
# ==========================================

JQUERY_VULNERABLE = """
/*! jQuery v3.6.0 | (c) OpenJS Foundation and other contributors | jquery.org/license */
(function(window, undefined) {
    var jQuery = function(selector, context) {
        return new jQuery.fn.init(selector, context);
    };
    jQuery.fn = jQuery.prototype = {
        jquery: "3.6.0",
        ready: function(fn) {
            document.addEventListener('DOMContentLoaded', fn);
        }
    };
    window.jQuery = window.$ = jQuery;
})(window);
"""

# ==========================================
# CSS STYLES
# ==========================================

CSS_STYLES = """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --secondary: #64748b;
    --success: #10b981;
    --danger: #ef4444;
    --warning: #f59e0b;
    --background: #f8fafc;
    --surface: #ffffff;
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --border: #e2e8f0;
    --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
    background-color: var(--background);
    color: var(--text-primary);
    line-height: 1.6;
}

/* Login Page Styles */
.login-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
}

.login-box {
    background: var(--surface);
    border-radius: 12px;
    box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
    width: 100%;
    max-width: 420px;
    padding: 2.5rem;
}

.login-header {
    text-align: center;
    margin-bottom: 2rem;
}

.login-logo {
    width: 64px;
    height: 64px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    margin: 0 auto 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
}

.login-header h1 {
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.login-header p {
    color: var(--text-secondary);
    font-size: 0.95rem;
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    font-weight: 500;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
}

.form-group input {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 1px solid var(--border);
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
    width: 100%;
}

.btn-primary {
    background-color: var(--primary);
    color: white;
}

.btn-primary:hover {
    background-color: var(--primary-dark);
}

.btn-sm {
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
    width: auto;
}

.forgot-password {
    display: block;
    text-align: center;
    margin-top: 1rem;
    color: var(--primary);
    text-decoration: none;
    font-size: 0.9rem;
}

.forgot-password:hover {
    text-decoration: underline;
}

.error-message {
    background-color: #fee2e2;
    border: 1px solid #fecaca;
    color: #991b1b;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    font-size: 0.9rem;
    display: none;
}

/* Dashboard Styles */
.dashboard-container {
    min-height: 100vh;
    display: flex;
}

.sidebar {
    width: 260px;
    background: var(--surface);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    position: fixed;
    height: 100vh;
    left: 0;
    top: 0;
}

.sidebar-header {
    padding: 1.5rem;
    border-bottom: 1px solid var(--border);
}

.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-weight: 700;
    font-size: 1.25rem;
    color: var(--text-primary);
}

.logo-icon {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.sidebar-nav {
    flex: 1;
    padding: 1rem 0;
    overflow-y: auto;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1.5rem;
    color: var(--text-secondary);
    text-decoration: none;
    transition: all 0.2s;
    cursor: pointer;
    border-left: 3px solid transparent;
}

.nav-item:hover {
    background-color: var(--background);
    color: var(--text-primary);
}

.nav-item.active {
    background-color: #eff6ff;
    color: var(--primary);
    border-left-color: var(--primary);
}

.sidebar-footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid var(--border);
}

.user-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.user-avatar {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 600;
}

.user-details {
    flex: 1;
}

.user-name {
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--text-primary);
}

.user-role {
    font-size: 0.8rem;
    color: var(--text-secondary);
}

.main-content {
    flex: 1;
    margin-left: 260px;
}

.top-bar {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 1rem 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 10;
}

.page-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
}

.search-bar {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.search-bar input {
    padding: 0.5rem 1rem;
    border: 1px solid var(--border);
    border-radius: 6px;
    width: 300px;
}

.content-area {
    padding: 2rem;
}

.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.stat-card {
    background: var(--surface);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: var(--shadow);
    display: flex;
    align-items: center;
    gap: 1rem;
}

.stat-icon {
    width: 48px;
    height: 48px;
    background: #eff6ff;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
}

.stat-info {
    flex: 1;
}

.stat-value {
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--text-primary);
}

.stat-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
}

.content-card {
    background: var(--surface);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: var(--shadow);
    margin-bottom: 1.5rem;
}

.content-card h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 1rem;
}

.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table th,
.data-table td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid var(--border);
}

.data-table th {
    font-weight: 600;
    color: var(--text-primary);
    background-color: var(--background);
}

.data-table tr:hover {
    background-color: var(--background);
}

.status {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
}

.status.success {
    background-color: #dcfce7;
    color: #166534;
}

.status.warning {
    background-color: #fef3c7;
    color: #92400e;
}

.status.error {
    background-color: #fee2e2;
    color: #991b1b;
}

/* Modal Styles */
.modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    background: var(--surface);
    border-radius: 12px;
    max-width: 800px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
}

.modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem;
    border-bottom: 1px solid var(--border);
}

.modal-header h3 {
    font-size: 1.25rem;
    font-weight: 600;
}

.close-modal {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--text-secondary);
}

.modal-body {
    padding: 1.5rem;
}

.customer-details {
    display: grid;
    gap: 1.5rem;
}

.detail-section {
    background: var(--background);
    padding: 1rem;
    border-radius: 8px;
}

.detail-section h4 {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.75rem;
}

.detail-section p {
    margin-bottom: 0.5rem;
    color: var(--text-secondary);
}

.detail-section strong {
    color: var(--text-primary);
}

/* Report Grid */
.report-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
}

.report-card {
    background: var(--background);
    padding: 1.5rem;
    border-radius: 8px;
    text-align: center;
}

.report-card h4 {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.report-card p {
    color: var(--text-secondary);
    margin-bottom: 1rem;
}

/* Settings Section */
.settings-section {
    margin-bottom: 2rem;
}

.settings-section h4 {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 1rem;
}

.config-item {
    margin-bottom: 1rem;
}

.config-item label {
    display: block;
    font-weight: 500;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.config-item input {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 1px solid var(--border);
    border-radius: 6px;
    background: var(--background);
}

/* Responsive */
@media (max-width: 768px) {
    .sidebar {
        transform: translateX(-100%);
    }
    
    .main-content {
        margin-left: 0;
    }
    
    .dashboard-grid {
        grid-template-columns: 1fr;
    }
}
"""

# ==========================================
# HTML TEMPLATES
# ==========================================

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign In - CloudVerify</title>
    <style>""" + CSS_STYLES + """</style>
</head>
<body>
    <div class="login-container">
        <div class="login-box">
            <div class="login-header">
                <div class="login-logo">â˜ï¸</div>
                <h1>CloudVerify</h1>
                <p>Enterprise Security & Compliance Platform</p>
            </div>
            
            <form id="login-form" action="/login" method="POST">
                {% if error %}
                <div class="error-message" id="error-message" style="display: block;">{{ error }}</div>
                {% else %}
                <div class="error-message" id="error-message"></div>
                {% endif %}
                
                <div class="form-group">
                    <label for="email">Email Address</label>
                    <input type="email" id="email" name="email" placeholder="you@company.com" required>
                </div>
                
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" placeholder="â€¢â€¢â€¢â€¢â€¢â€¢â€¢â€¢" required>
                </div>
                
                <button type="submit" class="btn btn-primary">Sign In</button>
            </form>
            
            <a href="#" class="forgot-password">Forgot your password?</a>
        </div>
    </div>
    
    <script>""" + JQUERY_VULNERABLE + """</script>
    <script>""" + PRE_LOGIN_JS + """</script>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - CloudVerify</title>
    <style>""" + CSS_STYLES + """</style>
</head>
<body>
    <div class="dashboard-container">
        <aside class="sidebar">
            <div class="sidebar-header">
                <div class="sidebar-logo">
                    <div class="logo-icon">â˜ï¸</div>
                    <span>CloudVerify</span>
                </div>
            </div>
            
            <nav class="sidebar-nav">
                <a class="nav-item active" data-view="overview">
                    <span>ðŸ“Š</span> Overview
                </a>
                <a class="nav-item" data-view="customers">
                    <span>ðŸ‘¥</span> Customers
                </a>
                <a class="nav-item" data-view="transactions">
                    <span>ðŸ’³</span> Transactions
                </a>
                <a class="nav-item" data-view="reports">
                    <span>ðŸ“ˆ</span> Reports
                </a>
                <a class="nav-item" data-view="settings">
                    <span>âš™ï¸</span> Settings
                </a>
            </nav>
            
            <div class="sidebar-footer">
                <div class="user-info">
                    <div class="user-avatar">{{ session.get('username', 'A')|upper|first }}</div>
                    <div class="user-details">
                        <div class="user-name" id="user-name">{{ session.get('username', 'Admin User') }}</div>
                        <div class="user-role" id="user-role">Administrator</div>
                    </div>
                </div>
                <div style="margin-top: 0.75rem;">
                    <a href="/logout" style="color: var(--danger); text-decoration: none; font-size: 0.875rem;">Sign Out</a>
                </div>
            </div>
        </aside>
        
        <main class="main-content">
            <div class="top-bar">
                <h1 class="page-title">Dashboard</h1>
                <div class="search-bar">
                    <input type="text" id="global-search" placeholder="Search customers, transactions...">
                </div>
            </div>
            
            <div class="content-area" id="main-content">
                <!-- Content loaded via JavaScript -->
            </div>
        </main>
    </div>
    
    <script>""" + JQUERY_VULNERABLE + """</script>
    <script>
        // Set user data for dashboard
        localStorage.setItem('cv_user_data', JSON.stringify({
            name: '{{ session.get("username", "Admin User") }}',
            email: '{{ session.get("username", "admin") }}@cloudverify.io',
            role: 'Administrator'
        }));
    </script>
    <script>""" + POST_LOGIN_JS + """</script>
</body>
</html>
"""

# ==========================================
# ROUTES
# ==========================================

@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template_string(LOGIN_TEMPLATE)
    
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    
    # VULNERABILITY: SQL Injection simulation
    if "'" in email or "OR" in email.upper() or "--" in email:
        session['logged_in'] = True
        session['username'] = email.split('@')[0] if '@' in email else 'admin'
        return redirect(url_for('dashboard'))
    
    # Normal login
    if email == 'admin@cloudverify.io' and password == 'CloudV3rify@2024':
        session['logged_in'] = True
        session['username'] = 'Admin'
        return redirect(url_for('dashboard'))
    else:
        return render_template_string(LOGIN_TEMPLATE, error='Invalid email or password')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# API Routes for Vulnerabilities
@app.route('/api/v1/auth/login', methods=['POST'])
def api_login():
    data = request.json
    email = data.get('email', '')
    password = data.get('password', '')
    
    # VULNERABILITY: SQL Injection
    if "'" in email or "OR" in email.upper():
        return {
            'success': True,
            'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.something',
            'user_id': 'admin'
        }
    
    if email == 'admin@cloudverify.io' and password == 'CloudV3rify@2024':
        return {
            'success': True,
            'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.valid_token',
            'user_id': 'admin'
        }
    
    return {
        'success': False,
        'message': 'Invalid credentials'
    }

@app.route('/api/customers')
def api_customers():
    # VULNERABILITY: PII Exposure without auth
    customers = json.loads(POST_LOGIN_JS)
    # Extract customer data from the JS
    import re
    match = re.search(r'const CUSTOMER_DATABASE = (\[.*?\]);', customers, re.DOTALL)
    if match:
        return eval(match.group(1))
    return {"error": "No data"}

@app.route('/api/config')
def api_config():
    # VULNERABILITY: Expose configuration
    return {
        "database": {
            "host": "prod-db-cluster.cloudverify.io",
            "port": 5432,
            "username": "cv_admin",
            "password": "CvPr0d@2024!Sec#reT",
            "database": "cloudverify_prod"
        },
        "api": {
            "key": "pk_live_51NzKm2Kx9mP3nQ8rR4tY6uI8oP2qR5sT7vW1xZ3cV5bX8zA2dC4eF6gH8jK0lM2n",
            "secret": "sk_live_51NzKm2Kx9mP3nQ8rR4tY6uI8oP2qR5sT7vW1xZ3cV5bX8zA2dC4eF6gH8jK0lM2n"
        }
    }

if __name__ == '__main__':
    print("=" * 60)
    print("  CloudVerify Platform - Production Environment")
    print("  Access at: http://127.0.0.1:5000")
    print("  Login: admin@cloudverify.io / CloudV3rify@2024")
    print("=" * 60)
    app.run(debug=False, host='0.0.0.0', port=5000)
