from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from functools import wraps
from models import db, Lead, PortfolioItem, Testimonial
from config import config
import os
import re
from datetime import datetime
import io
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Upload configuration for admin-managed images
UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# ==================== Helper Functions ====================

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number"""
    phone = re.sub(r'\D', '', phone)
    return len(phone) >= 10

def login_required(f):
    """Decorator to require admin login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== Domain Redirect ====================

@app.before_request
def redirect_to_www():
    """Redirect bare domain (codilight.com) to www.codilight.com.

    register.lk does not support CNAME records at the apex, so the root
    domain is pointed at Railway via an A record while the www subdomain
    uses a CNAME.  This handler ensures visitors who land on the bare
    domain are transparently forwarded to the canonical www address,
    preserving the full path and query string.
    """
    host = request.host.split(':')[0]  # strip port if present
    if host == 'codilight.com':
        target = request.url.replace('://codilight.com', '://www.codilight.com', 1)
        return redirect(target, code=301)


# ==================== Main Website Routes ====================

@app.route('/')
def index():
    """Home page"""
    stats = {
        'projects': 150,
        'clients': 89,
        'experience': 5
    }
    return render_template('index.html', stats=stats)

@app.route('/api/submit-lead', methods=['POST'])
def submit_lead():
    """Handle lead form submission"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('email') or not data.get('phone'):
            return jsonify({'success': False, 'message': 'Name, email, and phone are required'}), 400
        
        # Validate email format
        if not validate_email(data.get('email')):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        
        # Validate phone format
        if not validate_phone(data.get('phone')):
            return jsonify({'success': False, 'message': 'Invalid phone number'}), 400
        
        # Check if email already exists
        existing_lead = Lead.query.filter_by(email=data.get('email')).first()
        if existing_lead:
            # Update existing lead
            existing_lead.phone = data.get('phone')
            existing_lead.project_details = data.get('project_details', '')
            existing_lead.updated_at = datetime.utcnow()
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Lead updated successfully. Our team will contact you soon!'
            }), 200
        
        # Create new lead
        lead = Lead(
            name=data.get('name'),
            company=data.get('company', ''),
            email=data.get('email'),
            phone=data.get('phone'),
            project_details=data.get('project_details', ''),
            status='new'
        )
        
        db.session.add(lead)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Thank you! Your request has been received. Our team will contact you within 24 hours.'
        }), 201
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred. Please try again later.'
        }), 500

# ==================== Admin Routes ====================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username', '')
        password = data.get('password', '')
        
        if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD']:
            session['admin_logged_in'] = True
            session.permanent = True
            
            if request.is_json:
                return jsonify({'success': True, 'redirect': url_for('admin_dashboard')})
            return redirect(url_for('admin_dashboard'))
        
        error = 'Invalid username or password'
        if request.is_json:
            return jsonify({'success': False, 'message': error}), 401
        return render_template('admin_login.html', error=error), 401
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Get filter parameters
    status_filter = request.args.get('status', 'all')
    search = request.args.get('search', '')
    
    query = Lead.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    if search:
        query = query.filter(
            (Lead.name.ilike(f'%{search}%')) |
            (Lead.email.ilike(f'%{search}%')) |
            (Lead.company.ilike(f'%{search}%'))
        )
    
    # Get pagination
    pagination = query.order_by(Lead.created_at.desc()).paginate(page=page, per_page=per_page)
    leads = pagination.items
    
    # Calculate statistics
    total_leads = Lead.query.count()
    new_leads = Lead.query.filter_by(status='new').count()
    contacted_leads = Lead.query.filter_by(status='contacted').count()
    converted_leads = Lead.query.filter_by(status='converted').count()
    
    stats = {
        'total': total_leads,
        'new': new_leads,
        'contacted': contacted_leads,
        'converted': converted_leads
    }
    
    return render_template('admin_dashboard.html', 
                         leads=leads,
                         pagination=pagination,
                         stats=stats,
                         status_filter=status_filter,
                         search=search)

@app.route('/admin/leads/<int:lead_id>')
@login_required
def view_lead(lead_id):
    """View individual lead details"""
    lead = Lead.query.get_or_404(lead_id)
    return render_template('view_lead.html', lead=lead)

@app.route('/admin/api/lead/<int:lead_id>/update', methods=['PUT'])
@login_required
def update_lead(lead_id):
    """Update lead status and notes"""
    try:
        lead = Lead.query.get_or_404(lead_id)
        data = request.get_json()
        
        if 'status' in data:
            lead.status = data['status']
        
        if 'notes' in data:
            lead.notes = data['notes']
        
        if 'budget' in data:
            lead.budget = data['budget']
        
        if 'timeline' in data:
            lead.timeline = data['timeline']
        
        lead.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Lead updated successfully'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/api/lead/<int:lead_id>/delete', methods=['DELETE'])
@login_required
def delete_lead(lead_id):
    """Delete a lead"""
    try:
        lead = Lead.query.get_or_404(lead_id)
        db.session.delete(lead)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Lead deleted successfully'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/api/leads/export', methods=['GET'])
@login_required
def export_leads():
    """Export leads as CSV"""
    try:
        import csv
        
        leads = Lead.query.all()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['ID', 'Name', 'Company', 'Email', 'Phone', 'Status', 'Created At', 'Project Details', 'Notes', 'Budget', 'Timeline'])
        
        # Write data
        for lead in leads:
            writer.writerow([
                lead.id,
                lead.name,
                lead.company,
                lead.email,
                lead.phone,
                lead.status,
                lead.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                lead.project_details,
                lead.notes,
                lead.budget,
                lead.timeline
            ])
        
        # Return CSV file
        output.seek(0)
        return output.getvalue(), 200, {
            'Content-Disposition': 'attachment; filename=leads_export.csv',
            'Content-Type': 'text/csv'
        }
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/api/stats')
@login_required
def get_stats():
    """Get dashboard statistics"""
    try:
        total_leads = Lead.query.count()
        new_leads = Lead.query.filter_by(status='new').count()
        contacted_leads = Lead.query.filter_by(status='contacted').count()
        converted_leads = Lead.query.filter_by(status='converted').count()
        
        return jsonify({
            'total': total_leads,
            'new': new_leads,
            'contacted': contacted_leads,
            'converted': converted_leads,
            'conversion_rate': round((converted_leads / total_leads * 100) if total_leads > 0 else 0, 2)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ------------------ Portfolio / Testimonials Admin ------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/admin/portfolio')
@login_required
def admin_portfolio():
    items = PortfolioItem.query.order_by(PortfolioItem.created_at.desc()).all()
    return render_template('admin_portfolio.html', items=items)


@app.route('/admin/api/portfolio', methods=['POST'])
@login_required
def create_portfolio():
    try:
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        file = request.files.get('image')

        filename = None
        if file and allowed_file(file.filename):
            filename = f"{int(datetime.utcnow().timestamp())}_" + secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

        item = PortfolioItem(title=title, description=description, image_filename=filename)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('admin_portfolio'))
    except Exception as e:
        return str(e), 500


@app.route('/admin/api/portfolio/<int:item_id>/delete', methods=['DELETE'])
@login_required
def delete_portfolio(item_id):
    try:
        item = PortfolioItem.query.get_or_404(item_id)
        # delete image file if exists
        if item.image_filename:
            path = os.path.join(app.config['UPLOAD_FOLDER'], item.image_filename)
            if os.path.exists(path):
                os.remove(path)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/admin/testimonials')
@login_required
def admin_testimonials():
    items = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('admin_testimonials.html', items=items)


@app.route('/admin/api/testimonials', methods=['POST'])
@login_required
def create_testimonial():
    try:
        name = request.form.get('name', '')
        role = request.form.get('role', '')
        message = request.form.get('message', '')
        file = request.files.get('image')

        filename = None
        if file and allowed_file(file.filename):
            filename = f"{int(datetime.utcnow().timestamp())}_" + secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

        t = Testimonial(name=name, role=role, message=message, image_filename=filename)
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('admin_testimonials'))
    except Exception as e:
        return str(e), 500


@app.route('/admin/api/testimonials/<int:item_id>/delete', methods=['DELETE'])
@login_required
def delete_testimonial(item_id):
    try:
        item = Testimonial.query.get_or_404(item_id)
        if item.image_filename:
            path = os.path.join(app.config['UPLOAD_FOLDER'], item.image_filename)
            if os.path.exists(path):
                os.remove(path)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

# ==================== Context Processors ====================

@app.context_processor
def inject_config():
    """Inject configuration variables into templates"""
    return {
        'current_year': datetime.now().year
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
