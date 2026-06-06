# 🚀 Quick Start Guide

Get Codilight running in 5 minutes!

## Prerequisites
- Python 3.8+
- 500MB disk space
- Internet connection for CDN assets

## Windows Quick Start

```powershell
# 1. Navigate to project folder
cd codilight

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
.\venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
python app.py

# 6. Open browser
# Website: http://localhost:5000
# Admin: http://localhost:5000/admin/login
# Username: admin
# Password: admin123
```

## macOS/Linux Quick Start

```bash
# 1. Navigate to project folder
cd codilight

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
python app.py

# 6. Open browser
# Website: http://localhost:5000
# Admin: http://localhost:5000/admin/login
```

## Test the Website

1. **Hero Section** - See animated dashboard
2. **Scroll Down** - Watch animations trigger
3. **Open Contact Form** - Try submitting (it validates!)
4. **Check Admin** - Login and view submitted leads

## What You Get

✅ **Premium Website** - Modern, high-converting design
✅ **Lead Generation** - Capture visitor information
✅ **Admin Dashboard** - Manage leads easily
✅ **Database** - SQLite for data persistence
✅ **Responsive** - Works on all devices
✅ **SEO Ready** - Meta tags and schema markup
✅ **Dark Theme** - Professional glassmorphism design
✅ **Animations** - Smooth scrolling and transitions

## Admin Features

- 📊 Dashboard with statistics
- 🔍 Search and filter leads
- 📝 Add internal notes
- 💾 Track budget and timeline
- 📥 Export leads as CSV
- 🗑️ Manage lead status

## Customization

Edit these files to customize:
- **Colors**: `templates/base.html` (Tailwind config)
- **Content**: `templates/index.html` (All website sections)
- **Settings**: `config.py` (Admin credentials, etc.)
- **Styling**: `static/css/style.css` (Custom CSS)
- **JavaScript**: `static/js/main.js` (Interactivity)

## Stop the Server

```
Press Ctrl+C in terminal
```

## Deactivate Virtual Environment

```
deactivate
```

## Next Steps

1. Edit company information
2. Update portfolio projects
3. Change admin password
4. Customize colors and branding
5. Deploy to production (see SETUP.md)

## Common Issues

**Port already in use?**
```
Change port in app.py: app.run(port=5001)
```

**Database errors?**
```
Delete leads.db and restart app
```

**Styles not loading?**
```
Clear browser cache (Ctrl+Shift+Delete)
```

## Need Help?

- Read README.md for detailed documentation
- Check SETUP.md for deployment guide
- Review code comments for implementation details

---

**Enjoy building with Codilight!** 🎉
