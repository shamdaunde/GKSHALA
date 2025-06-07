import sys
import os
import json
import base64
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QToolBar, QLineEdit,
    QAction, QWidget, QVBoxLayout, QPushButton, QHBoxLayout,
    QLabel, QMenu, QInputDialog, QSizePolicy, QStackedWidget,
    QFormLayout, QDialog, QDialogButtonBox, QMessageBox, QComboBox,
    QFileDialog, QSystemTrayIcon, QStyle, QScrollArea, QCheckBox
)
from PyQt5.QtGui import (QIcon, QPalette, QColor, QFont, QCursor, QPixmap, 
                         QPainter, QBrush, QPen, QKeySequence)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage, QWebEngineScript
from PyQt5.QtCore import QUrl, Qt, QSize, pyqtSignal, QTimer, QStandardPaths, QSettings
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
import webbrowser
import urllib.parse
import random
import time
from datetime import datetime
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence

class ColorfulLogo(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text
        self.colors = [
            QColor('#4285F4'),  # Blue
            QColor('#EA4335'),  # Red
            QColor('#FBBC05'),  # Yellow
            QColor('#4285F4'),  # Blue
            QColor('#34A853'),  # Green
            QColor('#EA4335'),  # Red
            QColor('#FBBC05'),  # Yellow
            QColor('#4285F4')   # Blue
        ]
        self.setFixedSize(180, 60)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        painter.setFont(font)
        
        for i, letter in enumerate(self.text):
            if i < len(self.colors):
                painter.setPen(self.colors[i])
            else:
                painter.setPen(Qt.black)
            
            painter.drawText(20 + i * 20, 40, letter)

class AccountManager:
    """Enhanced account manager with more features"""
    def __init__(self):
        self.accounts = {}
        self.logged_in_user = None
        self.load_accounts()
    
    def load_accounts(self):
        """Load accounts from file"""
        config_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation), "accounts.json")
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    self.accounts = json.load(f)
        except Exception as e:
            print(f"Error loading accounts: {e}")
    
    def save_accounts(self):
        """Save accounts to file"""
        config_dir = QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        config_path = os.path.join(config_dir, "accounts.json")
        try:
            with open(config_path, 'w') as f:
                json.dump(self.accounts, f)
        except Exception as e:
            print(f"Error saving accounts: {e}")
    
    def register(self, email, password, name):
        if email in self.accounts:
            return False, "Email already registered"
        if not self.validate_email(email):
            return False, "Invalid email format"
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        
        self.accounts[email] = {
            'password': password,
            'name': name,
            'verified': True,  # Skip verification for demo
            'created_at': datetime.now().isoformat(),
            'last_login': None,
            'settings': {}
        }
        self.save_accounts()
        return True, f"Welcome to GKBROWSER, {name}!"
    
    def login(self, email, password):
        if email not in self.accounts:
            return False, "Account not found"
        if self.accounts[email]['password'] != password:
            return False, "Incorrect password"
        
        self.logged_in_user = email
        self.accounts[email]['last_login'] = datetime.now().isoformat()
        self.save_accounts()
        return True, f"Welcome back, {self.accounts[email]['name']}!"
    
    def logout(self):
        if self.logged_in_user:
            self.logged_in_user = None
            return True, "Logged out successfully"
        return False, "No user logged in"
    
    def validate_email(self, email):
        return '@' in email and '.' in email.split('@')[-1]
    
    def get_user_settings(self, email):
        return self.accounts.get(email, {}).get('settings', {})
    
    def update_user_settings(self, email, settings):
        if email in self.accounts:
            self.accounts[email]['settings'] = settings
            self.save_accounts()
            return True
        return False

class ServerManager:
    """Manage different server configurations"""
    def __init__(self):
        self.servers = {
            'default': {
                'name': 'Default Server',
                'description': 'Standard browsing experience',
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'extensions': [],
                'features': ['standard_js', 'ad_blocker'],
                'homepage': 'about:home'
            },
            'privacy': {
                'name': 'Privacy Server',
                'description': 'Enhanced privacy with tracker blocking',
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'extensions': ['privacy_badger', 'https_everywhere'],
                'features': ['standard_js', 'ad_blocker', 'tracker_blocker'],
                'homepage': 'about:home'
            },
            'developer': {
                'name': 'Developer Server',
                'description': 'Tools for web development',
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'extensions': ['dev_tools'],
                'features': ['standard_js', 'developer_tools'],
                'homepage': 'about:home'
            },
            'custom': {
                'name': 'Custom Server',
                'description': 'User-configured server',
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'extensions': [],
                'features': [],
                'homepage': 'about:home',
                'custom': True
            }
        }
        self.current_server = 'default'
        self.load_custom_servers()
    
    def load_custom_servers(self):
        """Load custom servers from file"""
        config_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation), "servers.json")
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    custom_servers = json.load(f)
                    for name, config in custom_servers.items():
                        self.servers[name] = config
        except Exception as e:
            print(f"Error loading custom servers: {e}")
    
    def save_custom_servers(self):
        """Save custom servers to file"""
        config_dir = QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        config_path = os.path.join(config_dir, "servers.json")
        custom_servers = {k:v for k,v in self.servers.items() if v.get('custom', False)}
        try:
            with open(config_path, 'w') as f:
                json.dump(custom_servers, f)
        except Exception as e:
            print(f"Error saving custom servers: {e}")
    
    def get_server_names(self):
        """Get list of server names for UI"""
        return [(name, config['name']) for name, config in self.servers.items()]
    
    def set_current_server(self, server_id):
        """Set the current active server"""
        if server_id in self.servers:
            self.current_server = server_id
            return True
        return False
    
    def get_current_server(self):
        """Get current server configuration"""
        return self.servers.get(self.current_server, self.servers['default'])
    
    def add_custom_server(self, name, config):
        """Add a new custom server"""
        server_id = f"custom_{len([k for k in self.servers if k.startswith('custom_')]) + 1}"
        config['custom'] = True
        self.servers[server_id] = config
        self.save_custom_servers()
        return server_id
    
    def remove_custom_server(self, server_id):
        """Remove a custom server"""
        if server_id in self.servers and self.servers[server_id].get('custom', False):
            del self.servers[server_id]
            self.save_custom_servers()
            return True
        return False

class BrowserTab(QWidget):
    def __init__(self, parent=None, server_config=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Create browser view with server configuration
        self.browser = QWebEngineView()
        self.profile = QWebEngineProfile.defaultProfile()
        
        # Apply server configuration
        self.server_config = server_config or {}
        self.apply_server_config()
        
        # Enable browser features
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
        
        # Set custom homepage
        self.browser.setUrl(QUrl(self.server_config.get('homepage', 'about:home')))
        self.layout.addWidget(self.browser)
        self.setLayout(self.layout)
        
        # Inject scripts based on features
        self.inject_feature_scripts()
    
    def apply_server_config(self):
        """Apply server configuration to this tab"""
        if 'user_agent' in self.server_config:
            self.profile.setHttpUserAgent(self.server_config['user_agent'])
    
    def inject_feature_scripts(self):
        """Inject JavaScript based on enabled features"""
        if 'ad_blocker' in self.server_config.get('features', []):
            self.inject_ad_blocker()
        
        if 'tracker_blocker' in self.server_config.get('features', []):
            self.inject_tracker_blocker()
        
        if 'developer_tools' in self.server_config.get('features', []):
            self.inject_developer_tools()
    
    def inject_ad_blocker(self):
        """Inject ad blocking script"""
        script = """
        // Simple ad blocker - blocks common ad domains
        const adDomains = [
            'doubleclick.net', 'googleadservices.com', 'googlesyndication.com',
            'adsense.com', 'adservice.google.com', 'adnxs.com', 'amazon-adsystem.com'
        ];
        
        document.addEventListener('DOMContentLoaded', function() {
            adDomains.forEach(domain => {
                const elements = document.querySelectorAll(`[href*="${domain}"], [src*="${domain}"]`);
                elements.forEach(el => el.remove());
            });
            
            // Block iframes from ad domains
            const iframes = document.getElementsByTagName('iframe');
            for (let i = iframes.length - 1; i >= 0; i--) {
                if (adDomains.some(domain => iframes[i].src.includes(domain))) {
                    iframes[i].parentNode.removeChild(iframes[i]);
                }
            }
        });
        """
        self.inject_script(script, "ad_blocker")
    
    def inject_tracker_blocker(self):
        """Inject tracker blocking script"""
        script = """
        // Simple tracker blocker
        const trackerDomains = [
            'facebook.com', 'facebook.net', 'fb.com', 'analytics.google.com',
            'google-analytics.com', 'googletagmanager.com', 'twitter.com',
            'connect.facebook.net', 'tr.snapchat.com', 'pinterest.com'
        ];
        
        document.addEventListener('DOMContentLoaded', function() {
            trackerDomains.forEach(domain => {
                const elements = document.querySelectorAll(`[href*="${domain}"], [src*="${domain}"]`);
                elements.forEach(el => el.remove());
            });
            
            // Block trackers in network requests
            const originalFetch = window.fetch;
            window.fetch = function(url, options) {
                if (trackerDomains.some(domain => url.includes(domain))) {
                    return Promise.reject(new Error('Tracker blocked'));
                }
                return originalFetch(url, options);
            };
        });
        """
        self.inject_script(script, "tracker_blocker")
    
    def inject_developer_tools(self):
        """Inject developer tools script"""
        script = """
        // Add a simple console log catcher
        const originalConsole = {
            log: console.log,
            warn: console.warn,
            error: console.error
        };
        
        console.log = function() {
            originalConsole.log.apply(console, arguments);
            window._browser_console_logs = window._browser_console_logs || [];
            window._browser_console_logs.push(['log', ...arguments]);
        };
        
        console.warn = function() {
            originalConsole.warn.apply(console, arguments);
            window._browser_console_logs = window._browser_console_logs || [];
            window._browser_console_logs.push(['warn', ...arguments]);
        };
        
        console.error = function() {
            originalConsole.error.apply(console, arguments);
            window._browser_console_logs = window._browser_console_logs || [];
            window._browser_console_logs.push(['error', ...arguments]);
        };
        """
        self.inject_script(script, "developer_tools")
    
    def inject_script(self, script, name):
        """Inject a script into the page"""
        web_script = QWebEngineScript()
        web_script.setSourceCode(script)
        web_script.setName(name)
        web_script.setWorldId(QWebEngineScript.MainWorld)
        web_script.setInjectionPoint(QWebEngineScript.DocumentReady)
        web_script.setRunsOnSubFrames(True)
        self.browser.page().scripts().insert(web_script)

# Custom homepage HTML
HOMEPAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GKBROWSER - Your Secure, Customizable Browser</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        :root {
            --primary: #4285f4;
            --secondary: #34a853;
            --accent: #ea4335;
            --warning: #fbbc05;
            --dark: #202124;
            --light: #f8f9fa;
            --gray: #5f6368;
            --card-bg: rgba(255, 255, 255, 0.85);
            --transition: all 0.3s ease;
        }

        body {
            background: linear-gradient(135deg, #1a2a6c, #b21f1f, #1a2a6c);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            color: var(--dark);
            min-height: 100vh;
            overflow-x: hidden;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Header Styles */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 0;
            margin-bottom: 40px;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-icon {
            font-size: 2.5rem;
            color: var(--primary);
            background: var(--light);
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        .logo-text {
            font-size: 2.2rem;
            font-weight: 800;
            color: white;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }

        .logo-text span:nth-child(1) { color: var(--primary); }
        .logo-text span:nth-child(2) { color: var(--accent); }
        .logo-text span:nth-child(3) { color: var(--warning); }
        .logo-text span:nth-child(4) { color: var(--secondary); }

        nav ul {
            display: flex;
            gap: 25px;
            list-style: none;
        }

        nav a {
            color: rgba(255, 255, 255, 0.9);
            text-decoration: none;
            font-weight: 500;
            font-size: 1.1rem;
            padding: 8px 15px;
            border-radius: 30px;
            transition: var(--transition);
        }

        nav a:hover {
            background: rgba(255, 255, 255, 0.15);
            transform: translateY(-3px);
        }

        nav a.active {
            background: var(--primary);
            color: white;
        }

        /* Hero Section */
        .hero {
            text-align: center;
            margin-bottom: 60px;
            padding: 40px 0;
            animation: fadeIn 1s ease;
        }

        .hero h1 {
            font-size: 3.5rem;
            color: white;
            margin-bottom: 20px;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }

        .hero p {
            font-size: 1.4rem;
            color: rgba(255, 255, 255, 0.9);
            max-width: 800px;
            margin: 0 auto 40px;
            line-height: 1.6;
        }

        /* Features Section */
        .section-title {
            text-align: center;
            color: white;
            font-size: 2.5rem;
            margin-bottom: 50px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }

        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 30px;
            margin-bottom: 60px;
        }

        .feature-card {
            background: var(--card-bg);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
            transition: var(--transition);
            text-align: center;
            backdrop-filter: blur(10px);
        }

        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        }

        .feature-icon {
            font-size: 3.5rem;
            margin-bottom: 20px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .feature-card h3 {
            font-size: 1.6rem;
            margin-bottom: 15px;
            color: var(--dark);
        }

        .feature-card p {
            color: var(--gray);
            line-height: 1.6;
        }

        /* Stats Section */
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-bottom: 60px;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            transition: var(--transition);
        }

        .stat-card:hover {
            transform: scale(1.05);
        }

        .stat-value {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 10px;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .stat-label {
            font-size: 1.2rem;
            color: var(--gray);
        }

        /* Footer */
        footer {
            background: rgba(0, 0, 0, 0.25);
            padding: 40px 0;
            margin-top: 60px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(5px);
        }

        .footer-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
        }

        .footer-column h3 {
            color: white;
            margin-bottom: 20px;
            font-size: 1.4rem;
        }

        .footer-links {
            list-style: none;
        }

        .footer-links li {
            margin-bottom: 12px;
        }

        .footer-links a {
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .footer-links a:hover {
            color: white;
            transform: translateX(5px);
        }

        .copyright {
            text-align: center;
            color: rgba(255, 255, 255, 0.7);
            padding-top: 30px;
            margin-top: 30px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .feature-card:nth-child(1) { animation: fadeIn 0.5s ease; }
        .feature-card:nth-child(2) { animation: fadeIn 0.7s ease; }
        .feature-card:nth-child(3) { animation: fadeIn 0.9s ease; }
        .feature-card:nth-child(4) { animation: fadeIn 1.1s ease; }

        /* Responsive Design */
        @media (max-width: 768px) {
            header {
                flex-direction: column;
                gap: 20px;
            }
            
            .hero h1 {
                font-size: 2.5rem;
            }
            
            .hero p {
                font-size: 1.1rem;
            }
            
            nav ul {
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .section-title {
                font-size: 2rem;
            }
        }

        /* Particle Background */
        #particles-js {
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: -1;
        }
    </style>
</head>
<body>
    <!-- Particle Background -->
    <div id="particles-js"></div>
    
    <div class="container">
        <!-- Header -->
        <header>
            <div class="logo">
                <div class="logo-icon">
                    <i class="fas fa-globe-americas"></i>
                </div>
                <div class="logo-text">
                    <span>G</span><span>K</span><span>B</span><span>ROWSER</span>
                </div>
            </div>
            <nav>
                <ul>
                    <li><a href="#" class="active">Home</a></li>
                    <li><a href="#">Features</a></li>
                    <li><a href="#">Download</a></li>
                    <li><a href="#">Support</a></li>
                    <li><a href="#">About</a></li>
                </ul>
            </nav>
        </header>
        
        <!-- Hero Section -->
        <section class="hero">
            <h1>Experience the Web, Reimagined</h1>
            <p>GKBROWSER is a next-generation browser focused on speed, security, and customization. Built for the modern web.</p>
        </section>
        
        <!-- Features Section -->
        <h2 class="section-title">Why Choose GKBROWSER?</h2>
        <section class="features">
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-bolt"></i>
                </div>
                <h3>Lightning Fast</h3>
                <p>Experience browsing at the speed of light with our optimized rendering engine and minimal resource usage.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-shield-alt"></i>
                </div>
                <h3>Military-Grade Security</h3>
                <p>Advanced privacy protection, tracker blocking, and encrypted connections keep your data safe.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-cogs"></i>
                </div>
                <h3>Complete Customization</h3>
                <p>Personalize every aspect of your browser with themes, extensions, and layout options.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-sync-alt"></i>
                </div>
                <h3>Seamless Sync</h3>
                <p>Access your bookmarks, history, and settings across all your devices with end-to-end encryption.</p>
            </div>
        </section>
        
        <!-- Stats Section -->
        <h2 class="section-title">GKBROWSER By The Numbers</h2>
        <section class="stats">
            <div class="stat-card">
                <div class="stat-value">5M+</div>
                <div class="stat-label">Active Users</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-value">87%</div>
                <div class="stat-label">Faster Page Loads</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-value">99.9%</div>
                <div class="stat-label">Tracking Blocked</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-value">500+</div>
                <div class="stat-label">Custom Themes</div>
            </div>
        </section>
        
        <!-- Footer -->
        <footer>
            <div class="footer-content">
                <div class="footer-column">
                    <h3>GKBROWSER</h3>
                    <p style="color: rgba(255, 255, 255, 0.8); line-height: 1.6;">
                        The next generation web browser focused on speed, security, and user experience.
                    </p>
                </div>
                
                <div class="footer-column">
                    <h3>Features</h3>
                    <ul class="footer-links">
                        <li><a href="#"><i class="fas fa-arrow-right"></i> Turbo Mode</a></li>
                        <li><a href="#"><i class="fas fa-arrow-right"></i> Privacy Center</a></li>
                        <li><a href="#"><i class="fas fa-arrow-right"></i> Theme Gallery</a></li>
                        <li><a href="#"><i class="fas fa-arrow-right"></i> Extension Store</a></li>
                    </ul>
                </div>
                
                <div class="footer-column">
                    <h3>Resources</h3>
                    <ul class="footer-links">
                        <li><a href="#"><i class="fas fa-arrow-right"></i> Help Center</a></li>
                        <li><a href="#"><i class="fas fa-arrow-right"></i> Community Forum</a></li>
                        <li><a href="#"><i class="fas fa-arrow-right"></i> Developer Tools</a></li>
                        <li><a href="#"><i class="fas fa-arrow-right"></i> Release Notes</a></li>
                    </ul>
                </div>
                
                <div class="footer-column">
                    <h3>Download</h3>
                    <ul class="footer-links">
                        <li><a href="#"><i class="fab fa-windows"></i> Windows</a></li>
                        <li><a href="#"><i class="fab fa-apple"></i> macOS</a></li>
                        <li><a href="#"><i class="fab fa-linux"></i> Linux</a></li>
                        <li><a href="#"><i class="fab fa-android"></i> Android</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="copyright">
                <p>&copy; 2023 GKBROWSER Technologies. All rights reserved.</p>
            </div>
        </footer>
    </div>

    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        // Initialize particles background
        particlesJS("particles-js", {
            particles: {
                number: { value: 80, density: { enable: true, value_area: 800 } },
                color: { value: "#ffffff" },
                shape: { type: "circle" },
                opacity: { value: 0.2, random: true },
                size: { value: 3, random: true },
                line_linked: {
                    enable: true,
                    distance: 150,
                    color: "#ffffff",
                    opacity: 0.1,
                    width: 1
                },
                move: {
                    enable: true,
                    speed: 2,
                    direction: "none",
                    random: true,
                    straight: false,
                    out_mode: "out",
                    bounce: false
                }
            },
            interactivity: {
                detect_on: "canvas",
                events: {
                    onhover: { enable: true, mode: "grab" },
                    onclick: { enable: true, mode: "push" },
                    resize: true
                }
            },
            retina_detect: true
        });

        // Feature card animations on scroll
        document.addEventListener('DOMContentLoaded', function() {
            const featureCards = document.querySelectorAll('.feature-card');
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.animation = 'fadeIn 0.8s ease forwards';
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });
            
            featureCards.forEach(card => {
                observer.observe(card);
            });
            
            // Dynamic stats counting
            const statCards = document.querySelectorAll('.stat-card');
            statCards.forEach(card => {
                const statValue = card.querySelector('.stat-value');
                const target = parseInt(statValue.textContent);
                let count = 0;
                const duration = 2000;
                const increment = target / (duration / 16);
                
                const updateCount = () => {
                    if (count < target) {
                        count += increment;
                        statValue.textContent = Math.ceil(count) + (statValue.textContent.includes('%') ? '%' : '+');
                        setTimeout(updateCount, 16);
                    } else {
                        statValue.textContent = target + (statValue.textContent.includes('%') ? '%' : '+');
                    }
                };
                
                setTimeout(updateCount, 500);
            });
        });
    </script>
</body>
</html>
"""

class AccountPage(QWidget):
    account_changed = pyqtSignal(bool)  # Emits True when logged in, False when logged out
    
    def __init__(self, account_manager, parent=None):
        super().__init__(parent)
        self.account_manager = account_manager
        self.setup_ui()
    
    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Stacked widget to switch between logged in/out views
        self.stack = QStackedWidget()
        
        # Logged out view
        self.logged_out_widget = QWidget()
        logged_out_layout = QVBoxLayout()
        
        logo = ColorfulLogo("GKBROWSER")
        logo.setAlignment(Qt.AlignCenter)
        logged_out_layout.addWidget(logo)
        
        title_label = QLabel("Sign in to GKBROWSER")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_label.setFont(title_font)
        logged_out_layout.addWidget(title_label)
        
        subtitle_label = QLabel("to sync your bookmarks, history, and settings across devices")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setWordWrap(True)
        logged_out_layout.addWidget(subtitle_label)
        
        sign_in_btn = QPushButton("Sign in")
        sign_in_btn.clicked.connect(lambda: self.parent().show_login_dialog())
        logged_out_layout.addWidget(sign_in_btn)
        
        create_account_btn = QPushButton("Create account")
        create_account_btn.clicked.connect(lambda: self.parent().show_register_dialog())
        logged_out_layout.addWidget(create_account_btn)
        
        self.logged_out_widget.setLayout(logged_out_layout)
        
        # Logged in view
        self.logged_in_widget = QWidget()
        logged_in_layout = QVBoxLayout()
        
        self.profile_label = QLabel()
        self.profile_label.setAlignment(Qt.AlignCenter)
        logged_in_layout.addWidget(self.profile_label)
        
        self.welcome_label = QLabel()
        self.welcome_label.setAlignment(Qt.AlignCenter)
        welcome_font = QFont()
        welcome_font.setPointSize(16)
        self.welcome_label.setFont(welcome_font)
        logged_in_layout.addWidget(self.welcome_label)
        
        email_label = QLabel()
        email_label.setAlignment(Qt.AlignCenter)
        self.email_label = email_label
        logged_in_layout.addWidget(email_label)
        
        sync_status = QLabel("Sync is on")
        sync_status.setAlignment(Qt.AlignCenter)
        logged_in_layout.addWidget(sync_status)
        
        sign_out_btn = QPushButton("Sign out")
        sign_out_btn.clicked.connect(self.sign_out)
        logged_in_layout.addWidget(sign_out_btn)
        
        self.logged_in_widget.setLayout(logged_in_layout)
        
        # Add widgets to stack
        self.stack.addWidget(self.logged_out_widget)
        self.stack.addWidget(self.logged_in_widget)
        
        self.layout.addWidget(self.stack)
        self.setLayout(self.layout)
        
        # Set initial state
        self.update_account_status()
    
    def update_account_status(self):
        if self.account_manager.logged_in_user:
            self.show_logged_in_view()
        else:
            self.show_logged_out_view()
    
    def show_logged_in_view(self):
        account = self.account_manager.accounts[self.account_manager.logged_in_user]
        
        # Create profile icon with first letter of name
        profile_pixmap = QPixmap(80, 80)
        profile_pixmap.fill(Qt.transparent)
        
        painter = QPainter(profile_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(66, 133, 244)))
        painter.setPen(QPen(Qt.NoPen))
        painter.drawEllipse(0, 0, 80, 80)
        
        painter.setFont(QFont("Arial", 32))
        painter.setPen(QPen(Qt.white))
        painter.drawText(profile_pixmap.rect(), Qt.AlignCenter, account['name'][0].upper())
        painter.end()
        
        self.profile_label.setPixmap(profile_pixmap)
        self.welcome_label.setText(f"Welcome, {account['name']}!")
        self.email_label.setText(self.account_manager.logged_in_user)
        
        self.stack.setCurrentWidget(self.logged_in_widget)
        self.account_changed.emit(True)
    
    def show_logged_out_view(self):
        self.stack.setCurrentWidget(self.logged_out_widget)
        self.account_changed.emit(False)
    
    def sign_out(self):
        self.account_manager.logout()
        self.update_account_status()
        QMessageBox.information(self, "Signed out", "You have been signed out.")

class GKBROWSER(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GKBROWSER")
        self.setWindowIcon(QIcon.fromTheme("web-browser"))
        self.setGeometry(50, 50, 1200, 800)
        
        # Initialize settings
        self.settings = QSettings("GKBROWSER", "GKBROWSER")
        
        # Account management
        self.account_manager = AccountManager()
        
        # Server management
        self.server_manager = ServerManager()
        
        # Custom configuration
        self.default_homepage = self.settings.value("homepage", "about:home")
        self.dark_mode = self.settings.value("dark_mode", False, type=bool)
        
        # Set theme based on settings
        if self.dark_mode:
            self.set_dark_theme()
        else:
            self.set_light_theme()
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        
        self.setCentralWidget(self.tabs)
        
        # Create navigation toolbar
        self.create_toolbar()
        
        # Create status bar
        self.status = self.statusBar()
        self.status.showMessage("GKBROWSER - Ready")
        
        # Add first tab
        self.add_new_tab(QUrl(self.default_homepage))
        
        # Create system tray icon
        self.create_system_tray()
        
        # Window controls
        self.showMaximized()
        
        # Bookmarks/history
        self.bookmarks = []
        self.history = []
        self.load_bookmarks()
        self.load_history()
        
        # Initialize download manager (placeholder)
        self.downloads = []
        
        # Initialize extensions
        self.extensions = []
        
        # Initialize shortcuts
        self.setup_shortcuts()
    
    def create_system_tray(self):
        """Create system tray icon with menu"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return
            
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        
        tray_menu = QMenu()
        
        restore_action = QAction("Restore", self)
        restore_action.triggered.connect(self.showNormal)
        tray_menu.addAction(restore_action)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # New tab
        new_tab_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        new_tab_shortcut.activated.connect(lambda: self.add_new_tab(QUrl(self.default_homepage)))
        
        # Close tab
        close_tab_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        close_tab_shortcut.activated.connect(self.close_current_tab)
        
        # Next tab
        next_tab_shortcut = QShortcut(QKeySequence("Ctrl+Tab"), self)
        next_tab_shortcut.activated.connect(self.next_tab)
        
        # Previous tab
        prev_tab_shortcut = QShortcut(QKeySequence("Ctrl+Shift+Tab"), self)
        prev_tab_shortcut.activated.connect(self.previous_tab)
        
        # Find in page
        find_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        find_shortcut.activated.connect(self.show_find_dialog)
    
    def close_current_tab(self):
        """Close the current tab"""
        current_index = self.tabs.currentIndex()
        self.close_tab(current_index)
    
    def next_tab(self):
        """Switch to next tab"""
        current_index = self.tabs.currentIndex()
        next_index = (current_index + 1) % self.tabs.count()
        self.tabs.setCurrentIndex(next_index)
    
    def previous_tab(self):
        """Switch to previous tab"""
        current_index = self.tabs.currentIndex()
        prev_index = (current_index - 1) % self.tabs.count()
        self.tabs.setCurrentIndex(prev_index)
    
    def show_find_dialog(self):
        """Show find in page dialog"""
        # This would be implemented with a QDialog and QWebEnginePage.findText()
        pass
    
    def load_bookmarks(self):
        """Load bookmarks from file"""
        config_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation), "bookmarks.json")
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    self.bookmarks = json.load(f)
        except Exception as e:
            print(f"Error loading bookmarks: {e}")
    
    def save_bookmarks(self):
        """Save bookmarks to file"""
        config_dir = QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        config_path = os.path.join(config_dir, "bookmarks.json")
        try:
            with open(config_path, 'w') as f:
                json.dump(self.bookmarks, f)
        except Exception as e:
            print(f"Error saving bookmarks: {e}")
    
    def load_history(self):
        """Load history from file"""
        config_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation), "history.json")
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"Error loading history: {e}")
    
    def save_history(self):
        """Save history to file"""
        config_dir = QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        config_path = os.path.join(config_dir, "history.json")
        try:
            with open(config_path, 'w') as f:
                json.dump(self.history, f)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def set_light_theme(self):
        """Apply a light theme similar to Chrome"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f1f1f1;
            }
            QTabWidget::pane {
                border: 0;
                background: white;
            }
            QTabBar::tab {
                background: #f1f1f1;
                color: #333;
                padding: 8px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                border: 1px solid #ccc;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
            }
            QTabBar::tab:hover {
                background: #e0e0e0;
            }
            QToolBar {
                background: #f1f1f1;
                border: none;
                padding: 2px;
            }
            QLineEdit {
                background: white;
                color: #333;
                border: 1px solid #ddd;
                border-radius: 15px;
                padding: 5px 15px;
                selection-background-color: #1a73e8;
                selection-color: white;
            }
            QPushButton {
                background: transparent;
                border: none;
                padding: 5px;
                color: #5f6368;
            }
            QPushButton:hover {
                background: #e8e8e8;
                border-radius: 4px;
            }
            QMenu {
                background: white;
                border: 1px solid #ccc;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background: #e8e8e8;
            }
        """)
        self.dark_mode = False
        self.settings.setValue("dark_mode", False)
    
    def set_dark_theme(self):
        """Apply a dark theme"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #202124;
            }
            QTabWidget::pane {
                border: 0;
                background: #35363a;
            }
            QTabBar::tab {
                background: #202124;
                color: #e8eaed;
                padding: 8px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                border: 1px solid #5f6368;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #35363a;
                border-bottom-color: #35363a;
            }
            QTabBar::tab:hover {
                background: #303134;
            }
            QToolBar {
                background: #202124;
                border: none;
                padding: 2px;
            }
            QLineEdit {
                background: #303134;
                color: #e8eaed;
                border: 1px solid #5f6368;
                border-radius: 15px;
                padding: 5px 15px;
                selection-background-color: #1a73e8;
                selection-color: white;
            }
            QPushButton {
                background: transparent;
                border: none;
                padding: 5px;
                color: #9aa0a6;
            }
            QPushButton:hover {
                background: #303134;
                border-radius: 4px;
            }
            QMenu {
                background: #35363a;
                border: 1px solid #5f6368;
                color: #e8eaed;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background: #303134;
            }
        """)
        self.dark_mode = True
        self.settings.setValue("dark_mode", True)
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        if self.dark_mode:
            self.set_light_theme()
        else:
            self.set_dark_theme()
    
    def create_toolbar(self):
        """Create the navigation toolbar with buttons."""
        toolbar = QToolBar("Navigation")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(20, 20))
        self.addToolBar(toolbar)
        
        # Menu button
        menu_btn = QPushButton()
        menu_btn.setIcon(QIcon.fromTheme("application-menu"))
        menu_btn.setToolTip("Menu")
        menu_btn.setFixedSize(30, 30)
        menu_btn.clicked.connect(self.show_main_menu)
        toolbar.addWidget(menu_btn)
        
        # Back button
        back_btn = QAction(QIcon.fromTheme("go-previous"), "Back", self)
        back_btn.triggered.connect(self.go_back)
        back_btn.setShortcut("Alt+Left")
        toolbar.addAction(back_btn)
        
        # Forward button
        forward_btn = QAction(QIcon.fromTheme("go-next"), "Forward", self)
        forward_btn.triggered.connect(self.go_forward)
        forward_btn.setShortcut("Alt+Right")
        toolbar.addAction(forward_btn)
        
        # Reload button
        reload_btn = QAction(QIcon.fromTheme("view-refresh"), "Reload", self)
        reload_btn.triggered.connect(self.reload_page)
        reload_btn.setShortcut("F5")
        toolbar.addAction(reload_btn)
        
        # Home button
        home_btn = QAction(QIcon.fromTheme("go-home"), "Home", self)
        home_btn.triggered.connect(self.navigate_home)
        toolbar.addAction(home_btn)
        
        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter website URL")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setClearButtonEnabled(True)
        toolbar.addWidget(self.url_bar)
        
        # Add spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar.addWidget(spacer)
        
        # Server selection
        self.server_combo = QComboBox()
        self.server_combo.setToolTip("Select Server Configuration")
        for server_id, server_name in self.server_manager.get_server_names():
            self.server_combo.addItem(server_name, server_id)
        self.server_combo.currentIndexChanged.connect(self.change_server)
        toolbar.addWidget(self.server_combo)
        
        # New tab button
        new_tab_btn = QPushButton("+")
        new_tab_btn.setFixedSize(30, 30)
        new_tab_btn.setStyleSheet("""
            QPushButton {
                background: #e8e8e8;
                color: #333;
                border: none;
                border-radius: 15px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: #d0d0d0;
            }
        """)
        new_tab_btn.setCursor(Qt.PointingHandCursor)
        new_tab_btn.clicked.connect(lambda: self.add_new_tab(QUrl(self.default_homepage)))
        toolbar.addWidget(new_tab_btn)
    
    def show_main_menu(self):
        """Show the main menu"""
        menu = QMenu(self)
        
        # File menu
        file_menu = menu.addMenu("File")
        file_menu.addAction("New Window", self.new_window, "Ctrl+N")
        file_menu.addAction("New Tab", lambda: self.add_new_tab(QUrl(self.default_homepage)), "Ctrl+T")
        file_menu.addSeparator()
        file_menu.addAction("Open File...", self.open_file)
        file_menu.addAction("Save Page As...", self.save_page)
        file_menu.addSeparator()
        file_menu.addAction("Print...", self.print_page)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)
        
        # Edit menu
        edit_menu = menu.addMenu("Edit")
        edit_menu.addAction("Cut", self.cut, "Ctrl+X")
        edit_menu.addAction("Copy", self.copy, "Ctrl+C")
        edit_menu.addAction("Paste", self.paste, "Ctrl+V")
        edit_menu.addSeparator()
        edit_menu.addAction("Select All", self.select_all, "Ctrl+A")
        edit_menu.addAction("Find...", self.show_find_dialog, "Ctrl+F")
        
        # View menu
        view_menu = menu.addMenu("View")
        view_menu.addAction("Zoom In", self.zoom_in, "Ctrl++")
        view_menu.addAction("Zoom Out", self.zoom_out, "Ctrl+-")
        view_menu.addAction("Reset Zoom", self.zoom_reset, "Ctrl+0")
        view_menu.addSeparator()
        view_menu.addAction("Toggle Fullscreen", self.toggle_fullscreen, "F11")
        view_menu.addAction("Toggle Dark Mode", self.toggle_theme)
        view_menu.addSeparator()
        view_menu.addAction("Developer Tools", self.show_dev_tools, "F12")
        
        # History menu
        history_menu = menu.addMenu("History")
        history_menu.addAction("Back", self.go_back, "Alt+Left")
        history_menu.addAction("Forward", self.go_forward, "Alt+Right")
        history_menu.addSeparator()
        history_menu.addAction("Home", self.navigate_home)
        history_menu.addSeparator()
        history_menu.addAction("Show History", self.show_history)
        history_menu.addAction("Clear History", self.clear_history)
        
        # Bookmarks menu
        bookmarks_menu = menu.addMenu("Bookmarks")
        bookmarks_menu.addAction("Add Bookmark", self.add_bookmark, "Ctrl+D")
        bookmarks_menu.addAction("Show Bookmarks", self.show_bookmarks)
        bookmarks_menu.addAction("Manage Bookmarks", self.manage_bookmarks)
        
        # Tools menu
        tools_menu = menu.addMenu("Tools")
        tools_menu.addAction("Downloads", self.show_downloads)
        tools_menu.addAction("Extensions", self.manage_extensions)
        tools_menu.addAction("Settings", self.show_settings)
        
        # Help menu
        help_menu = menu.addMenu("Help")
        help_menu.addAction("About GKBROWSER", self.show_about)
        help_menu.addAction("Check for Updates", self.check_updates)
        
        # Account menu if logged in
        if self.account_manager.logged_in_user:
            account_menu = menu.addMenu(f"Account ({self.account_manager.logged_in_user})")
            account_menu.addAction("Account Settings", self.show_account_settings)
            account_menu.addAction("Logout", self.account_logout)
        else:
            account_menu = menu.addMenu("Account")
            account_menu.addAction("Login", self.account_login)
            account_menu.addAction("Register", self.account_register)
        
        menu.exec_(QCursor.pos())
    
    def change_server(self, index):
        """Change the current server configuration"""
        server_id = self.server_combo.itemData(index)
        self.server_manager.set_current_server(server_id)
        
        # Update current tab with new server configuration
        current_tab = self.tabs.currentWidget()
        if current_tab:
            # For simplicity, we'll just reload the page with the new server config
            current_url = current_tab.browser.url()
            self.tabs.removeTab(self.tabs.currentIndex())
            self.add_new_tab(current_url)
    
    def add_new_tab(self, qurl=None, label="New Tab"):
        """Add a new browser tab with current server configuration."""
        if qurl is None:
            qurl = QUrl(self.default_homepage)
        
        server_config = self.server_manager.get_current_server()
        tab = BrowserTab(server_config=server_config)
        
        if qurl.toString() == "about:home":
            tab.browser.setHtml(HOMEPAGE_HTML)
        else:
            tab.browser.setUrl(qurl)
        
        i = self.tabs.addTab(tab, label)
        self.tabs.setCurrentIndex(i)
        
        # Connect signals
        tab.browser.urlChanged.connect(lambda qurl, tab=tab: self.update_urlbar(qurl, tab))
        tab.browser.loadFinished.connect(lambda _, i=i, tab=tab: self.update_tab_title(i, tab))
        tab.browser.loadProgress.connect(self.update_progress)
        
        # Update URL bar when tab changes
        if self.tabs.currentWidget() == tab:
            self.url_bar.setText(qurl.toString() if qurl.toString() != "about:home" else "")
    
    def update_progress(self, progress):
        """Update progress in status bar."""
        if progress < 100:
            self.status.showMessage(f"Loading... {progress}%")
        else:
            self.status.showMessage("GKBROWSER - Ready")
    
    def update_tab_title(self, index, tab):
        """Update tab title based on page title."""
        title = tab.browser.page().title()
        if title:
            self.tabs.setTabText(index, title[:15] + "..." if len(title) > 15 else title)
    
    def update_urlbar(self, qurl, tab=None):
        """Update the URL bar with the current URL."""
        if tab != self.tabs.currentWidget():
            return
        
        self.url_bar.setText(qurl.toString())
        self.url_bar.setCursorPosition(0)
        
        # Add to history
        self.history.append({
            "url": qurl.toString(),
            "title": tab.browser.page().title() if tab else "",
            "timestamp": datetime.now().isoformat()
        })
        
        # Save history periodically
        if len(self.history) % 10 == 0:
            self.save_history()
    
    def current_tab_changed(self, index):
        """Handle tab change events."""
        if index == -1:
            return
        
        tab = self.tabs.widget(index)
        if tab:
            self.url_bar.setText(tab.browser.url().toString())
    
    def close_tab(self, index):
        """Close tab at the given index."""
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()
    
    def navigate_to_url(self):
        """Navigate to the URL in the URL bar."""
        text = self.url_bar.text().strip()
        
        # If empty, just return
        if not text:
            return
        
        # If it's a complete URL with scheme, use it directly
        if text.startswith(('http://', 'https://', 'ftp://', 'file://')):
            qurl = QUrl(text)
        else:
            # Try to parse as a domain name
            if '.' in text and ' ' not in text:
                # Add https:// if not present
                if not text.startswith(('http://', 'https://')):
                    text = 'https://' + text
                qurl = QUrl(text)
            else:
                # Treat as a search query - redirect to the website directly
                # For simplicity, we'll just try to construct a URL
                # In a real app, you might want to implement a proper search system
                qurl = QUrl(f"https://{text.split()[0]}.com")
        
        if not qurl.isValid():
            QMessageBox.warning(self, "Invalid URL", "The URL you entered is not valid.")
            return
        
        self.current_browser().setUrl(qurl)
    
    def navigate_home(self):
        """Navigate to the home page."""
        current_browser = self.current_browser()
        current_browser.setHtml(HOMEPAGE_HTML)
    
    def current_browser(self):
        """Get the current browser widget."""
        return self.tabs.currentWidget().browser
    
    def go_back(self):
        """Go back in browser history."""
        self.current_browser().back()
    
    def go_forward(self):
        """Go forward in browser history."""
        self.current_browser().forward()
    
    def reload_page(self):
        """Reload the current page."""
        self.current_browser().reload()
    
    def new_window(self):
        """Open a new browser window."""
        new_window = GKBROWSER()
        new_window.show()
    
    def open_file(self):
        """Open a local file in the browser."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", 
            "HTML Files (*.html *.htm);;All Files (*)"
        )
        
        if file_path:
            url = QUrl.fromLocalFile(file_path)
            self.add_new_tab(url, os.path.basename(file_path))
    
    def save_page(self):
        """Save the current page to a file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Page", "", 
            "HTML Files (*.html *.htm);;All Files (*)"
        )
        
        if file_path:
            # In a real implementation, you would save the page content
            QMessageBox.information(self, "Save Page", "Page save functionality would be implemented here")
    
    def print_page(self):
        """Print the current page."""
        # In a real implementation, you would show a print dialog
        QMessageBox.information(self, "Print", "Print functionality would be implemented here")
    
    def cut(self):
        """Cut selected text."""
        self.current_browser().triggerPageAction(QWebEnginePage.Cut)
    
    def copy(self):
        """Copy selected text."""
        self.current_browser().triggerPageAction(QWebEnginePage.Copy)
    
    def paste(self):
        """Paste text."""
        self.current_browser().triggerPageAction(QWebEnginePage.Paste)
    
    def select_all(self):
        """Select all text."""
        self.current_browser().triggerPageAction(QWebEnginePage.SelectAll)
    
    def zoom_in(self):
        """Zoom in the page."""
        current_zoom = self.current_browser().zoomFactor()
        self.current_browser().setZoomFactor(current_zoom + 0.1)
    
    def zoom_out(self):
        """Zoom out the page."""
        current_zoom = self.current_browser().zoomFactor()
        self.current_browser().setZoomFactor(max(0.1, current_zoom - 0.1))
    
    def zoom_reset(self):
        """Reset zoom level."""
        self.current_browser().setZoomFactor(1.0)
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    def show_dev_tools(self):
        """Show developer tools."""
        # In a real implementation, you would show dev tools
        QMessageBox.information(self, "Developer Tools", "Developer tools would be implemented here")
    
    def show_history(self):
        """Show browsing history."""
        dialog = QDialog(self)
        dialog.setWindowTitle("History")
        dialog.resize(600, 400)
        
        layout = QVBoxLayout()
        
        # Add search box
        search_box = QLineEdit()
        search_box.setPlaceholderText("Search history...")
        layout.addWidget(search_box)
        
        # Add history list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        
        for item in reversed(self.history[-100:]):  # Show last 100 items
            btn = QPushButton(f"{item['title']} - {item['url']}")
            btn.setStyleSheet("text-align: left;")
            btn.clicked.connect(lambda _, url=item['url']: self.add_new_tab(QUrl(url)))
            history_layout.addWidget(btn)
        
        scroll.setWidget(history_widget)
        layout.addWidget(scroll)
        
        # Add buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def clear_history(self):
        """Clear browsing history."""
        reply = QMessageBox.question(
            self, "Clear History", 
            "Are you sure you want to clear your browsing history?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.history = []
            self.save_history()
            QMessageBox.information(self, "History Cleared", "Your browsing history has been cleared.")
    
    def add_bookmark(self):
        """Add current page to bookmarks."""
        current_url = self.current_browser().url().toString()
        current_title = self.current_browser().page().title()
        
        if not current_url or current_url == "about:blank":
            QMessageBox.warning(self, "Cannot Bookmark", "No page is currently loaded to bookmark.")
            return
        
        # Check if already bookmarked
        for bookmark in self.bookmarks:
            if bookmark['url'] == current_url:
                QMessageBox.information(self, "Already Bookmarked", "This page is already in your bookmarks.")
                return
        
        # Add to bookmarks
        self.bookmarks.append({
            'url': current_url,
            'title': current_title,
            'created': datetime.now().isoformat()
        })
        self.save_bookmarks()
        
        QMessageBox.information(self, "Bookmark Added", "The current page has been added to your bookmarks.")
    
    def show_bookmarks(self):
        """Show bookmarks manager."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Bookmarks")
        dialog.resize(600, 400)
        
        layout = QVBoxLayout()
        
        # Add search box
        search_box = QLineEdit()
        search_box.setPlaceholderText("Search bookmarks...")
        layout.addWidget(search_box)
        
        # Add bookmarks list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        bookmarks_widget = QWidget()
        bookmarks_layout = QVBoxLayout(bookmarks_widget)
        
        for item in self.bookmarks:
            btn = QPushButton(f"{item['title']} - {item['url']}")
            btn.setStyleSheet("text-align: left;")
            btn.clicked.connect(lambda _, url=item['url']: self.add_new_tab(QUrl(url)))
            bookmarks_layout.addWidget(btn)
        
        scroll.setWidget(bookmarks_widget)
        layout.addWidget(scroll)
        
        # Add buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def manage_bookmarks(self):
        """Manage bookmarks with edit/delete options."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Manage Bookmarks")
        dialog.resize(600, 400)
        
        layout = QVBoxLayout()
        
        # Add search box
        search_box = QLineEdit()
        search_box.setPlaceholderText("Search bookmarks...")
        layout.addWidget(search_box)
        
        # Add bookmarks list with checkboxes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        bookmarks_widget = QWidget()
        bookmarks_layout = QVBoxLayout(bookmarks_widget)
        
        self.bookmark_checkboxes = []
        
        for item in self.bookmarks:
            hbox = QHBoxLayout()
            
            cb = QCheckBox()
            self.bookmark_checkboxes.append((cb, item))
            hbox.addWidget(cb)
            
            label = QLabel(f"{item['title']} - {item['url']}")
            hbox.addWidget(label)
            
            bookmarks_layout.addLayout(hbox)
        
        scroll.setWidget(bookmarks_widget)
        layout.addWidget(scroll)
        
        # Add buttons
        button_box = QDialogButtonBox()
        delete_btn = button_box.addButton("Delete Selected", QDialogButtonBox.DestructiveRole)
        delete_btn.clicked.connect(lambda: self.delete_selected_bookmarks(dialog))
        button_box.addButton(QDialogButtonBox.Close)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def delete_selected_bookmarks(self, dialog):
        """Delete selected bookmarks."""
        selected = [item for cb, item in self.bookmark_checkboxes if cb.isChecked()]
        
        if not selected:
            QMessageBox.warning(dialog, "No Selection", "Please select bookmarks to delete.")
            return
        
        reply = QMessageBox.question(
            dialog, "Delete Bookmarks", 
            f"Are you sure you want to delete {len(selected)} bookmark(s)?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.bookmarks = [item for item in self.bookmarks if item not in selected]
            self.save_bookmarks()
            QMessageBox.information(dialog, "Bookmarks Deleted", "The selected bookmarks have been deleted.")
            dialog.accept()
    
    def show_downloads(self):
        """Show downloads manager."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Downloads")
        dialog.resize(600, 400)
        
        layout = QVBoxLayout()
        
        if not self.downloads:
            layout.addWidget(QLabel("No downloads yet."))
        else:
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            
            downloads_widget = QWidget()
            downloads_layout = QVBoxLayout(downloads_widget)
            
            for download in self.downloads:
                label = QLabel(f"{download['filename']} - {download['status']}")
                downloads_layout.addWidget(label)
            
            scroll.setWidget(downloads_widget)
            layout.addWidget(scroll)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def manage_extensions(self):
        """Manage browser extensions."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Extensions")
        dialog.resize(600, 400)
        
        layout = QVBoxLayout()
        
        if not self.extensions:
            layout.addWidget(QLabel("No extensions installed."))
        else:
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            
            extensions_widget = QWidget()
            extensions_layout = QVBoxLayout(extensions_widget)
            
            for ext in self.extensions:
                hbox = QHBoxLayout()
                
                label = QLabel(ext['name'])
                hbox.addWidget(label)
                
                toggle_btn = QPushButton("Disable" if ext['enabled'] else "Enable")
                toggle_btn.clicked.connect(lambda _, e=ext: self.toggle_extension(e))
                hbox.addWidget(toggle_btn)
                
                extensions_layout.addLayout(hbox)
            
            scroll.setWidget(extensions_widget)
            layout.addWidget(scroll)
        
        install_btn = QPushButton("Install Extension...")
        install_btn.clicked.connect(self.install_extension)
        layout.addWidget(install_btn)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def toggle_extension(self, extension):
        """Toggle extension enabled/disabled state."""
        extension['enabled'] = not extension['enabled']
        QMessageBox.information(self, "Extension", 
                              f"Extension {extension['name']} has been {'enabled' if extension['enabled'] else 'disabled'}.")
    
    def install_extension(self):
        """Install a new extension."""
        QMessageBox.information(self, "Install Extension", "Extension installation would be implemented here")
    
    def show_settings(self):
        """Show browser settings dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")
        dialog.resize(600, 400)
        
        layout = QVBoxLayout()
        
        # Create tab widget for different settings categories
        tabs = QTabWidget()
        
        # General settings
        general_tab = QWidget()
        general_layout = QFormLayout()
        
        homepage_edit = QLineEdit(self.default_homepage)
        general_layout.addRow("Homepage:", homepage_edit)
        
        dark_mode_cb = QCheckBox("Enable Dark Mode")
        dark_mode_cb.setChecked(self.dark_mode)
        general_layout.addRow(dark_mode_cb)
        
        general_tab.setLayout(general_layout)
        tabs.addTab(general_tab, "General")
        
        # Privacy settings
        privacy_tab = QWidget()
        privacy_layout = QVBoxLayout()
        
        cookies_cb = QCheckBox("Allow Cookies")
        cookies_cb.setChecked(True)
        privacy_layout.addWidget(cookies_cb)
        
        tracking_cb = QCheckBox("Block Trackers")
        tracking_cb.setChecked(True)
        privacy_layout.addWidget(tracking_cb)
        
        privacy_tab.setLayout(privacy_layout)
        tabs.addTab(privacy_tab, "Privacy")
        
        # Server settings
        server_tab = QWidget()
        server_layout = QVBoxLayout()
        
        server_label = QLabel("Current Server: " + self.server_manager.get_current_server()['name'])
        server_layout.addWidget(server_label)
        
        add_server_btn = QPushButton("Add Custom Server")
        add_server_btn.clicked.connect(self.add_custom_server)
        server_layout.addWidget(add_server_btn)
        
        server_tab.setLayout(server_layout)
        tabs.addTab(server_tab, "Servers")
        
        layout.addWidget(tabs)
        
        # Add buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.save_settings(
            homepage_edit.text(),
            dark_mode_cb.isChecked(),
            dialog
        ))
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def add_custom_server(self):
        """Add a custom server configuration."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Custom Server")
        dialog.resize(400, 300)
        
        layout = QFormLayout()
        
        name_edit = QLineEdit()
        layout.addRow("Server Name:", name_edit)
        
        desc_edit = QLineEdit()
        layout.addRow("Description:", desc_edit)
        
        user_agent_edit = QLineEdit()
        user_agent_edit.setText("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        layout.addRow("User Agent:", user_agent_edit)
        
        homepage_edit = QLineEdit("about:home")
        layout.addRow("Homepage:", homepage_edit)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.create_custom_server(
            name_edit.text(),
            desc_edit.text(),
            user_agent_edit.text(),
            homepage_edit.text(),
            dialog
        ))
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def create_custom_server(self, name, description, user_agent, homepage, dialog):
        """Create a new custom server configuration."""
        if not name:
            QMessageBox.warning(dialog, "Missing Name", "Please enter a server name.")
            return
        
        config = {
            'name': name,
            'description': description,
            'user_agent': user_agent,
            'homepage': homepage,
            'extensions': [],
            'features': [],
            'custom': True
        }
        
        self.server_manager.add_custom_server(name, config)
        QMessageBox.information(dialog, "Server Added", "Custom server configuration has been added.")
        dialog.accept()
    
    def save_settings(self, homepage, dark_mode, dialog):
        """Save browser settings."""
        self.default_homepage = homepage
        self.settings.setValue("homepage", homepage)
        
        if dark_mode != self.dark_mode:
            self.dark_mode = dark_mode
            self.settings.setValue("dark_mode", dark_mode)
            if dark_mode:
                self.set_dark_theme()
            else:
                self.set_light_theme()
        
        QMessageBox.information(dialog, "Settings Saved", "Your settings have been saved.")
        dialog.accept()
    
    def account_login(self):
        """Show login dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Login")
        
        layout = QFormLayout()
        
        email_edit = QLineEdit()
        email_edit.setPlaceholderText("your@email.com")
        layout.addRow("Email:", email_edit)
        
        password_edit = QLineEdit()
        password_edit.setPlaceholderText("Password")
        password_edit.setEchoMode(QLineEdit.Password)
        layout.addRow("Password:", password_edit)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.perform_login(
            email_edit.text(),
            password_edit.text(),
            dialog
        ))
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def perform_login(self, email, password, dialog):
        """Perform login with provided credentials."""
        success, message = self.account_manager.login(email, password)
        if success:
            QMessageBox.information(dialog, "Login Successful", message)
            dialog.accept()
        else:
            QMessageBox.warning(dialog, "Login Failed", message)
    
    def account_register(self):
        """Show registration dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Register")
        
        layout = QFormLayout()
        
        name_edit = QLineEdit()
        name_edit.setPlaceholderText("Your Name")
        layout.addRow("Name:", name_edit)
        
        email_edit = QLineEdit()
        email_edit.setPlaceholderText("your@email.com")
        layout.addRow("Email:", email_edit)
        
        password_edit = QLineEdit()
        password_edit.setPlaceholderText("Password (min 8 characters)")
        password_edit.setEchoMode(QLineEdit.Password)
        layout.addRow("Password:", password_edit)
        
        confirm_edit = QLineEdit()
        confirm_edit.setPlaceholderText("Confirm Password")
        confirm_edit.setEchoMode(QLineEdit.Password)
        layout.addRow("Confirm:", confirm_edit)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.perform_register(
            name_edit.text(),
            email_edit.text(),
            password_edit.text(),
            confirm_edit.text(),
            dialog
        ))
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def perform_register(self, name, email, password, confirm, dialog):
        """Perform registration with provided details."""
        if password != confirm:
            QMessageBox.warning(dialog, "Registration Failed", "Passwords do not match.")
            return
        
        success, message = self.account_manager.register(email, password, name)
        if success:
            QMessageBox.information(dialog, "Registration Successful", message)
            dialog.accept()
        else:
            QMessageBox.warning(dialog, "Registration Failed", message)
    
    def account_logout(self):
        """Logout current user."""
        success, message = self.account_manager.logout()
        QMessageBox.information(self, "Logout", message)
    
    def show_account_settings(self):
        """Show account settings dialog."""
        QMessageBox.information(self, "Account Settings", "Account settings would be implemented here")
    
    def check_updates(self):
        """Check for browser updates."""
        QMessageBox.information(self, "Check for Updates", "Update checking would be implemented here")
    
    def show_about(self):
        """Show about dialog."""
        about_text = """
        <h1>GKBROWSER</h1>
        <p>Version 1.0</p>
        <p>A customizable browser with enhanced features</p>
        <p>© 2023 GKBROWSER Team</p>
        """
        
        msg = QMessageBox()
        msg.setWindowTitle("About GKBROWSER")
        msg.setText(about_text)
        msg.setIconPixmap(QPixmap(":/icons/gkbrowser.png").scaled(64, 64))
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("GKBROWSER")
    app.setApplicationDisplayName("GKBROWSER")
    app.setWindowIcon(QIcon.fromTheme("web-browser"))
    
    # Set organization details for QSettings
    app.setOrganizationName("GKBROWSER")
    app.setOrganizationDomain("gkbrowser.example.com")
    
    window = GKBROWSER()
    window.show()
    sys.exit(app.exec_())