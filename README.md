# Codilight - Premium Software Development Website

A modern, high-converting website for a software development and web development company built with Flask, Tailwind CSS, and vanilla JavaScript.

## 🎯 Features

### Website Sections
- ✨ **Hero Section** - Animated dashboard mockup with floating tech icons
- 🏢 **Trusted By Section** - Client logos showcase
- 💼 **Services Section** - 6 premium service cards with glassmorphism
- ⭐ **Why Choose Us** - Key benefits with icons
- 🎨 **Portfolio Section** - Project showcase with hover effects
- 📊 **Process Section** - 5-step development process visualization
- 💬 **Testimonials Section** - Client reviews with ratings
- 🔧 **Technologies Section** - Tech stack showcase (10+ technologies)
- 📈 **Statistics Section** - Animated counters
- 📞 **Contact/Lead Generation** - Advanced contact form with validation
- 🔗 **Footer** - Complete footer with links and social media

### Technical Features
- 🌙 **Dark Theme with Glassmorphism** - Premium 2026 SaaS design
- 📱 **Fully Responsive** - Works perfectly on all devices
- ⚡ **Smooth Animations** - Scroll animations and transitions
- 🎯 **SEO Optimized** - Meta tags, schema.org markup, Open Graph
- 🔐 **Secure Admin Dashboard** - Lead management system
- 💾 **SQLite Database** - Lead storage and management
- 📧 **Form Validation** - Client-side and server-side validation
- 📊 **Admin Analytics** - Dashboard with statistics
- 📥 **CSV Export** - Export leads for CRM integration
- 🚀 **Performance Optimized** - Lazy loading, minification ready

## 🏗️ Project Structure

```
codilight/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── templates/
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Home page
│   ├── admin_login.html  # Admin login page
│   ├── admin_dashboard.html  # Lead management dashboard
│   ├── view_lead.html    # Lead details page
│   ├── 404.html          # 404 error page
│   └── 500.html          # 500 error page
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   ├── js/
│   │   └── main.js       # Main JavaScript
│   └── images/           # Images folder
├── database/             # Database files
└── README.md             # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone or download the project**
```bash
cd codilight
```

2. **Create a virtual environment**
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create environment file**
```bash
# Copy and configure
copy .env.example .env
# Edit .env with your settings
```

5. **Initialize database**
```bash
# The database will be created automatically on first run
# Or create manually by running:
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

6. **Run the application**
```bash
python app.py
```

The website will be available at: **http://localhost:5000**

### Access Admin Dashboard
- URL: `http://localhost:5000/admin/login`
- Username: `admin`
- Password: `admin123`

⚠️ **Change credentials in production!** Edit them in `config.py`

## 📋 Configuration

### Environment Variables (.env)
```env
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=secure-password
DATABASE_URL=sqlite:///leads.db
```

### Update Configuration
Edit `config.py` to customize:
- Secret key
- Admin credentials
- Database URI
- Session settings
- Security settings

## 🎨 Customization

### Brand Colors
Edit the Tailwind config in `templates/base.html`:
```javascript
colors: {
    primary: {
        400: '#60a5fa',
        500: '#3b82f6',
        600: '#2563eb',
    },
    accent: {
        400: '#34d399',
        500: '#10b981',
    }
}
```

### Company Information
Update in `templates/base.html`:
- Company name (Codilight)
- Contact email
- Phone number
- Social media links
- Address

### Services
Edit the services section in `templates/index.html` to add/remove/modify services

### Portfolio Projects
Edit the portfolio section in `templates/index.html` to showcase your projects

### Testimonials
Modify the testimonials section in `templates/index.html` with real client feedback

## 🛠️ Admin Dashboard

### Features
- 📊 View all leads with pagination
- 🔍 Search leads by name, email, or company
- 🏷️ Filter by status (New, Contacted, Qualified, Converted, Rejected)
- 📝 Add internal notes to leads
- 💰 Track budget and timeline
- 📥 Export leads as CSV
- 🗑️ Delete leads
- 📈 View statistics and conversion rates

### Lead Status Workflow
1. **New** - Initial lead submission
2. **Contacted** - Your team has reached out
3. **Qualified** - Lead meets your criteria
4. **Converted** - Lead became a client
5. **Rejected** - Lead not suitable

## 📧 API Endpoints

### Public API
- `GET /` - Home page
- `POST /api/submit-lead` - Submit contact form

### Admin API (Requires Authentication)
- `GET /admin/login` - Admin login page
- `POST /admin/login` - Process login
- `GET /admin/logout` - Logout admin
- `GET /admin/dashboard` - View leads dashboard
- `GET /admin/leads/<id>` - View lead details
- `PUT /admin/api/lead/<id>/update` - Update lead
- `DELETE /admin/api/lead/<id>/delete` - Delete lead
- `GET /admin/api/leads/export` - Export leads as CSV
- `GET /admin/api/stats` - Get dashboard statistics

## 📱 Responsive Design

The website is fully responsive and optimized for:
- 📱 Mobile devices (320px+)
- 📱 Tablets (768px+)
- 🖥️ Desktop (1024px+)
- 🖥️ Large screens (1280px+)

## 🎯 SEO Optimization

The website includes:
- Meta tags for description, keywords, author
- Open Graph tags for social sharing
- Twitter Card meta tags
- Schema.org JSON-LD markup
- Mobile-friendly viewport
- Canonical URLs (add to base.html)
- Sitemap (generate and add)

## 🔐 Security Best Practices

1. **Change Admin Credentials** - Update in production
2. **CORS Configuration** - Add CORS headers if needed
3. **HTTPS** - Deploy with HTTPS only
4. **Environment Variables** - Keep sensitive data in .env
5. **Input Validation** - All inputs are validated
6. **SQL Injection Protection** - Using SQLAlchemy ORM
7. **CSRF Protection** - Add Flask-WTF for CSRF tokens

## 🚀 Deployment

### Heroku

1. Create `Procfile`:
```
web: python app.py
```

2. Deploy:
```bash
# Initialize git repo
git init
git add .
git commit -m "Initial commit"

# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-production-secret

# Deploy
git push heroku main
```

### AWS / DigitalOcean

1. Install dependencies
2. Configure Gunicorn as production server
3. Set up Nginx as reverse proxy
4. Configure SSL certificate
5. Set up automated backups

### General Deployment Checklist

- [ ] Change admin credentials
- [ ] Set `DEBUG = False`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure production `DATABASE_URL`
- [ ] Set up email notifications (optional)
- [ ] Configure CORS if needed
- [ ] Set up automated backups
- [ ] Monitor error logs
- [ ] Set up analytics

## 📊 Database

### Schema

**Leads Table:**
```
id (Integer, Primary Key)
name (String, Required)
company (String)
email (String, Required, Unique)
phone (String, Required)
project_details (Text)
status (String, Default: 'new')
budget (String)
timeline (String)
notes (Text)
created_at (DateTime, Auto)
updated_at (DateTime, Auto)
```

### Database Backup

```bash
# Backup SQLite database
cp database/leads.db database/leads.db.backup

# Restore
cp database/leads.db.backup database/leads.db
```

## 🐛 Troubleshooting

### Issue: Database not found
**Solution:** Ensure `database/` folder exists or is created automatically on first run

### Issue: Admin login fails
**Solution:** Check username and password in `config.py`. Default is admin/admin123

### Issue: Form submission not working
**Solution:** Check browser console for errors. Ensure `/api/submit-lead` endpoint is accessible

### Issue: Styles not loading
**Solution:** Clear browser cache (Ctrl+Shift+Del) and refresh. Check CDN availability

### Issue: Static files 404
**Solution:** Ensure `static/` folder structure is correct and Flask is serving static files

## 📝 License

This project is provided as-is for commercial and personal use.

## 🤝 Contributing

To contribute improvements:
1. Test changes thoroughly
2. Update documentation
3. Submit enhancements

## 📞 Support

For questions or issues:
- Email: hello@codilight.com
- Documentation: See README
- Check troubleshooting section

## 🎓 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://www.sqlalchemy.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [MDN Web Docs](https://developer.mozilla.org/)

## 🏆 Performance Tips

1. **Minimize CSS/JS** - Use tools like minifiers
2. **Cache Busting** - Add version numbers to static files
3. **Image Optimization** - Use WebP format
4. **CDN** - Serve static files from CDN
5. **Database Indexing** - Add indexes on frequently searched fields
6. **Monitoring** - Set up error tracking (Sentry)

## 📈 Analytics Integration

To add Google Analytics:
1. Get GA tracking ID from Google Analytics
2. Add to `base.html` before `</head>`
3. Track events using `trackEvent()` function in `main.js`

## 🎁 What's Included

✅ Complete Flask backend
✅ Responsive HTML templates
✅ Tailwind CSS styling
✅ Smooth animations
✅ Form validation
✅ Admin dashboard
✅ Lead management system
✅ SQLite database
✅ CSV export functionality
✅ Dark theme with glassmorphism
✅ SEO optimized
✅ Mobile friendly
✅ Production ready

## 🎯 Next Steps

1. Customize branding and colors
2. Update company information
3. Add your portfolio projects
4. Configure admin credentials
5. Set up email notifications (optional)
6. Deploy to production
7. Monitor analytics
8. Gather leads and convert!

---

**Made with ❤️ by Codilight**

© 2024 Codilight. All rights reserved.
#   c o d i l i g h t  
 