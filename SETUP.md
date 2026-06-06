# Codilight - Setup & Deployment Guide

## 🖥️ System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: 512MB minimum (1GB recommended)
- **Disk Space**: 100MB
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

## 💻 Local Development Setup (Windows)

### Step 1: Prepare Your System

```powershell
# Update pip
python -m pip install --upgrade pip

# Verify Python version
python --version  # Should be 3.8+
```

### Step 2: Create Project Directory

```powershell
# Navigate to desired location
cd C:\Users\YourName\Documents

# Clone or create project
git clone https://github.com/yourusername/codilight.git
cd codilight
```

### Step 3: Set Up Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# You should see (venv) in your terminal
```

### Step 4: Install Dependencies

```powershell
# Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# Install requirements
pip install -r requirements.txt

# Verify installation
pip list
```

### Step 5: Configure Environment

```powershell
# Copy example env file
copy .env.example .env

# Edit .env with your settings (optional for development)
# notepad .env
```

### Step 6: Initialize Database

```powershell
# The database creates automatically, but you can initialize with:
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"
```

### Step 7: Run the Application

```powershell
# Start Flask development server
python app.py

# You should see:
# WARNING in app.run() This is a development server...
# Running on http://127.0.0.1:5000
```

### Step 8: Access the Website

- **Website**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin/login
- **Admin Credentials**: admin / admin123

## 🍎 macOS Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

## 🐧 Linux Setup (Ubuntu/Debian)

```bash
# Install Python development packages
sudo apt-get update
sudo apt-get install python3-pip python3-venv python3-dev build-essential

# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

## 🚀 Production Deployment

### Option 1: Heroku Deployment

1. **Install Heroku CLI**
   - Download from https://devcenter.heroku.com/articles/heroku-cli
   - Verify: `heroku --version`

2. **Create Heroku App**
```bash
# Login to Heroku
heroku login

# Create new app
heroku create codilight-app

# Or use existing app
heroku apps:create --app=codilight-app
```

3. **Create Procfile**
```
Create file named `Procfile` (no extension):
web: gunicorn app:app
```

4. **Update Requirements**
```bash
# Add gunicorn for production
pip install gunicorn
pip freeze > requirements.txt
```

5. **Configure Environment**
```bash
# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
heroku config:set ADMIN_USERNAME=admin
heroku config:set ADMIN_PASSWORD=YourSecurePassword123
```

6. **Deploy**
```bash
# Git setup (if not already)
git init
git add .
git commit -m "Initial commit"

# Add Heroku remote
heroku git:remote -a codilight-app

# Deploy
git push heroku main
```

7. **Verify Deployment**
```bash
# View logs
heroku logs --tail

# Open app
heroku open
```

### Option 2: AWS Deployment (EC2)

1. **Launch EC2 Instance**
   - Instance Type: t2.micro or t3.micro
   - OS: Ubuntu 20.04 LTS
   - Security Group: Allow ports 80, 443, 22

2. **SSH into Server**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. **Install Dependencies**
```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and tools
sudo apt-get install -y python3-pip python3-venv nginx supervisor

# Install Let's Encrypt
sudo apt-get install -y certbot python3-certbot-nginx
```

4. **Deploy Application**
```bash
# Clone repository
git clone https://github.com/yourusername/codilight.git
cd codilight

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create .env file
nano .env
# Add your configuration
```

5. **Configure Supervisor**
```bash
# Create supervisor config
sudo nano /etc/supervisor/conf.d/codilight.conf
```

Add:
```ini
[program:codilight]
directory=/home/ubuntu/codilight
command=/home/ubuntu/codilight/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 app:app
autostart=true
autorestart=true
stderr_logfile=/var/log/codilight/err.log
stdout_logfile=/var/log/codilight/out.log
```

6. **Configure Nginx**
```bash
# Create nginx config
sudo nano /etc/nginx/sites-available/codilight
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static/ {
        alias /home/ubuntu/codilight/static/;
    }
}
```

7. **Enable and Start Services**
```bash
# Enable nginx site
sudo ln -s /etc/nginx/sites-available/codilight /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Start supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start codilight
```

8. **Setup SSL Certificate**
```bash
sudo certbot --nginx -d your-domain.com
```

### Option 3: DigitalOcean Deployment

1. **Create Droplet**
   - Size: 1GB / 1 CPU
   - OS: Ubuntu 20.04 LTS

2. **Follow AWS steps above** (very similar process)

3. **Configure Domain**
   - Point A record to Droplet IP
   - Configure DNS from DigitalOcean dashboard

## 📊 Database Management

### Backup Database

```bash
# Backup SQLite database
cp database/leads.db database/leads.db.backup.$(date +%Y%m%d)

# Or use Windows
copy database\leads.db database\leads.db.backup
```

### Restore Database

```bash
# Restore from backup
cp database/leads.db.backup database/leads.db
```

### Export Leads

```bash
# Use admin panel to export as CSV
# Or manually query:
python -c "
from app import app, db
from models import Lead
app.app_context().push()
for lead in Lead.query.all():
    print(lead.to_dict())
"
```

## 🔐 Security Hardening

### For Production

1. **Update Admin Credentials**
```python
# In config.py
ADMIN_USERNAME = 'your-secure-username'
ADMIN_PASSWORD = 'your-very-secure-password'
```

2. **Generate Strong Secret Key**
```bash
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"
```

3. **Enable HTTPS**
```bash
# Use Let's Encrypt (free SSL)
sudo certbot certonly --standalone -d yourdomain.com
```

4. **Configure Firewall**
```bash
# Ubuntu
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# Allow only specific IPs to admin
# Configure in Nginx or application
```

5. **Database Security**
```bash
# Restrict database file permissions
chmod 600 database/leads.db
chown www-data:www-data database/leads.db
```

## 📈 Monitoring & Maintenance

### Log Monitoring

```bash
# View application logs
tail -f logs/app.log

# View error logs
tail -f logs/error.log

# View supervisor logs
sudo tail -f /var/log/codilight/out.log
sudo tail -f /var/log/codilight/err.log
```

### Performance Optimization

1. **Enable Caching**
```python
# In app.py
@app.after_request
def add_header(response):
    response.cache_control.max_age = 300
    return response
```

2. **Minify Static Files**
```bash
# Install tools
pip install cssmin jsmin

# Minify CSS and JS
```

3. **Enable Gzip Compression**
```bash
# In Nginx configuration
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

### Regular Maintenance

- Weekly: Review error logs
- Monthly: Backup database
- Quarterly: Update dependencies
- Annually: Security audit

## 🧪 Testing

### Run Unit Tests

```bash
# Install pytest
pip install pytest

# Create tests/test_app.py
# Run tests
pytest tests/
```

### Load Testing

```bash
# Install Apache Bench
# Simulate 1000 requests with 100 concurrent
ab -n 1000 -c 100 http://localhost:5000/
```

## 📱 Mobile Testing

```bash
# Find your IP
ipconfig getifaddr en0  # macOS
hostname -I             # Linux
ipconfig               # Windows

# Access from mobile on same network
http://your-ip:5000
```

## 🆘 Troubleshooting

### Port 5000 Already in Use
```bash
# Find process using port
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process
kill -9 PID  # macOS/Linux
taskkill /PID PID /F  # Windows
```

### Database Locked
```bash
# Delete database and restart
rm database/leads.db
# App will recreate on next run
```

### 500 Internal Server Error
- Check logs for detailed error
- Verify imports are correct
- Check database connectivity
- Review recent changes

### Static Files Not Loading
- Clear browser cache
- Check static folder exists
- Verify Nginx configuration (if using)
- Check file permissions

## 📚 Useful Commands

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate   # Windows

# Deactivate virtual environment
deactivate

# Install new package
pip install package-name

# Update requirements
pip freeze > requirements.txt

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +

# Database shell
sqlite3 database/leads.db
```

## 📞 Support & Resources

- **Flask Docs**: https://flask.palletsprojects.com/
- **Gunicorn Docs**: https://gunicorn.org/
- **Nginx Docs**: https://nginx.org/
- **Supervisor Docs**: https://supervisor.readthedocs.io/

---

**Deployment Complete!** 🎉

Your premium software company website is now live and ready to generate leads.
