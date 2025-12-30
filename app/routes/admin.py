"""
Admin Routes Blueprint
Handles administrative functionality
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from app import db
from app.models import User, Course, Enrollment, Payment, Video, OnlineClass, SupportTicket
from app.utils.decorators import login_required, admin_required
import logging

bp = Blueprint('admin', __name__, url_prefix='/admin')
logger = logging.getLogger(__name__)

@bp.route('/profile')
@admin_required
def profile():
    """Admin profile page"""
    try:
        user = User.query.get(session['user_id'])
        stats = {
            'total_users': User.query.count(),
            'total_courses': Course.query.count(),
            'total_tickets': SupportTicket.query.count() if SupportTicket else 0
        }
        return render_template('shared/profile.html', user=user, stats=stats)
    except Exception as e:
        logger.error(f"Profile error: {str(e)}", exc_info=True)
        flash('An error occurred loading your profile.', 'danger')
        return redirect(url_for('admin.dashboard'))

@bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard with statistics"""
    try:
        # Get counts
        total_users = User.query.count()
        total_students = User.query.filter_by(role='student').count()
        total_faculty = User.query.filter_by(role='faculty').count()
        total_courses = Course.query.count()
        total_enrollments = Enrollment.query.count()
        
        # Calculate revenue
        total_revenue = db.session.query(db.func.sum(Payment.amount_npr)).filter(
            Payment.status == 'completed'
        ).scalar() or 0
        
        # Recent activity
        recent_enrollments = Enrollment.query.order_by(Enrollment.enrollment_date.desc()).limit(10).all()
        recent_payments = Payment.query.order_by(Payment.payment_date.desc()).limit(10).all()
        
        # Monthly revenue (last 6 months)
        monthly_revenue = []
        for i in range(6):
            start_date = datetime.utcnow().replace(day=1) - timedelta(days=30*i)
            end_date = (start_date + timedelta(days=32)).replace(day=1)
            
            revenue = db.session.query(db.func.sum(Payment.amount_npr)).filter(
                Payment.status == 'completed',
                Payment.payment_date >= start_date,
                Payment.payment_date < end_date
            ).scalar() or 0
            
            monthly_revenue.append({
                'month': start_date.strftime('%b %Y'),
                'revenue': revenue
            })
        
        monthly_revenue.reverse()
        
        # Get recent users for dashboard
        recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
        
        user = User.query.get(session['user_id'])
        
        return render_template('shared/dashboard.html',
                             user=user,
                             total_users=total_users,
                             total_students=total_students,
                             total_faculty=total_faculty,
                             total_courses=total_courses,
                             total_enrollments=total_enrollments,
                             total_revenue=total_revenue,
                             recent_users=recent_users,
                             recent_enrollments=recent_enrollments,
                             recent_payments=recent_payments,
                             monthly_revenue=monthly_revenue)
    except Exception as e:
        logger.error(f"Admin dashboard error: {str(e)}", exc_info=True)
        flash('An error occurred loading the dashboard.', 'danger')
        return redirect(url_for('auth.index'))

@bp.route('/users')
@admin_required
def users():
    """Manage users"""
    try:
        role_filter = request.args.get('role', 'all')
        
        if role_filter != 'all':
            users_list = User.query.filter_by(role=role_filter).all()
        else:
            users_list = User.query.all()
        
        return render_template('shared/users.html', users=users_list, role_filter=role_filter)
    except Exception as e:
        logger.error(f"Admin users error: {str(e)}", exc_info=True)
        flash('An error occurred loading users.', 'danger')
        return redirect(url_for('admin.dashboard'))

@bp.route('/user/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    """Create new user"""
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            full_name = request.form.get('full_name', '').strip()
            role = request.form.get('role', 'student')
            
            if not all([username, email, password, full_name]):
                flash('All fields are required.', 'danger')
                return render_template('shared/create_user.html')
            
            # Check for duplicates
            if User.query.filter_by(username=username).first():
                flash('Username already exists.', 'danger')
                return render_template('shared/create_user.html')
            
            if User.query.filter_by(email=email).first():
                flash('Email already exists.', 'danger')
                return render_template('shared/create_user.html')
            
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(
                username=username,
                email=email,
                password=hashed_password,
                full_name=full_name,
                role=role
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            logger.info(f"Admin created user: {username} ({role})")
            flash('✅ User created successfully!', 'success')
            return redirect(url_for('admin.users'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Create user error: {str(e)}", exc_info=True)
            flash('An error occurred creating the user.', 'danger')
    
    return render_template('shared/create_user.html')

@bp.route('/user/<int:user_id>/toggle', methods=['POST'])
@admin_required
def toggle_user(user_id):
    """Toggle user active status"""
    try:
        user = User.query.get_or_404(user_id)
        user.is_active = not user.is_active
        db.session.commit()
        
        status = 'activated' if user.is_active else 'deactivated'
        flash(f'User {user.username} has been {status}.', 'success')
        return redirect(url_for('admin.users'))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Toggle user error: {str(e)}", exc_info=True)
        flash('An error occurred updating the user.', 'danger')
        return redirect(url_for('admin.users'))

@bp.route('/courses')
@admin_required
def courses():
    """View all courses"""
    try:
        courses_list = Course.query.all()
        return render_template('shared/courses.html', courses=courses_list)
    except Exception as e:
        logger.error(f"Admin courses error: {str(e)}", exc_info=True)
        flash('An error occurred loading courses.', 'danger')
        return redirect(url_for('admin.dashboard'))

@bp.route('/course/<int:course_id>/delete', methods=['POST'])
@admin_required
def delete_course(course_id):
    """Delete a course"""
    try:
        course = Course.query.get_or_404(course_id)
        title = course.title
        
        db.session.delete(course)
        db.session.commit()
        
        logger.info(f"Admin deleted course: {title}")
        flash(f'Course "{title}" deleted successfully.', 'success')
        return redirect(url_for('admin.courses'))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Delete course error: {str(e)}", exc_info=True)
        flash('An error occurred deleting the course.', 'danger')
        return redirect(url_for('admin.courses'))

@bp.route('/enrollments')
@admin_required
def enrollments():
    """View all enrollments"""
    try:
        enrollments_list = Enrollment.query.order_by(Enrollment.enrollment_date.desc()).all()
        return render_template('shared/enrollments.html', enrollments=enrollments_list)
    except Exception as e:
        logger.error(f"Admin enrollments error: {str(e)}", exc_info=True)
        flash('An error occurred loading enrollments.', 'danger')
        return redirect(url_for('admin.dashboard'))

@bp.route('/payments')
@admin_required
def payments():
    """View all payments"""
    try:
        payments_list = Payment.query.order_by(Payment.payment_date.desc()).all()
        return render_template('shared/payments.html', payments=payments_list)
    except Exception as e:
        logger.error(f"Admin payments error: {str(e)}", exc_info=True)
        flash('An error occurred loading payments.', 'danger')
        return redirect(url_for('admin.dashboard'))

@bp.route('/reports')
@admin_required
def reports():
    """View reports and analytics"""
    try:
        # Course popularity
        popular_courses = db.session.query(
            Course, db.func.count(Enrollment.id).label('enrollment_count')
        ).join(Enrollment).group_by(Course.id).order_by(
            db.func.count(Enrollment.id).desc()
        ).limit(10).all()
        
        # Revenue by course
        revenue_by_course = db.session.query(
            Course, db.func.sum(Payment.amount_npr).label('revenue')
        ).join(Payment).filter(Payment.status == 'completed').group_by(
            Course.id
        ).order_by(db.func.sum(Payment.amount_npr).desc()).limit(10).all()
        
        return render_template('shared/reports.html',
                             popular_courses=popular_courses,
                             revenue_by_course=revenue_by_course)
    except Exception as e:
        logger.error(f"Admin reports error: {str(e)}", exc_info=True)
        flash('An error occurred loading reports.', 'danger')
        return redirect(url_for('admin.dashboard'))

@bp.route('/management')
@admin_required
def management():
    """Manage management team members"""
    management_users = User.query.filter_by(role='management').all()
    all_users = User.query.filter(User.role != 'management').all()
    return render_template('shared/management_team.html', management_users=management_users, all_users=all_users)

@bp.route('/management/add', methods=['POST'])
@admin_required
def management_add():
    """Add user to management team"""
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)
    if user:
        user.role = 'management'
        db.session.commit()
        flash(f'{user.full_name} added to management team.', 'success')
    return redirect(url_for('admin.management'))

@bp.route('/management/remove/<int:user_id>', methods=['POST'])
@admin_required
def management_remove(user_id):
    """Remove user from management team"""
    user = User.query.get(user_id)
    if user:
        user.role = 'student'
        db.session.commit()
        flash(f'{user.full_name} removed from management team.', 'success')
    return redirect(url_for('admin.management'))

@bp.route('/support')
@admin_required
def support():
    """View all support tickets"""
    tickets = SupportTicket.query.order_by(SupportTicket.created_at.desc()).all()
    return render_template('shared/support.html', tickets=tickets)

@bp.route('/support/<int:ticket_id>')
@admin_required
def support_detail(ticket_id):
    """View support ticket detail"""
    ticket = SupportTicket.query.get_or_404(ticket_id)
    return render_template('shared/support_detail.html', ticket=ticket)

@bp.route('/support/<int:ticket_id>/respond', methods=['POST'])
@admin_required
def support_respond(ticket_id):
    """Respond to support ticket"""
    from app.models import TicketResponse
    ticket = SupportTicket.query.get_or_404(ticket_id)
    response = TicketResponse(
        ticket_id=ticket.id,
        user_id=session['user_id'],
        message=request.form.get('message')
    )
    db.session.add(response)
    db.session.commit()
    flash('Response added!', 'success')
    return redirect(url_for('admin.support_detail', ticket_id=ticket_id))

@bp.route('/support/<int:ticket_id>/assign', methods=['POST'])
@admin_required
def support_assign(ticket_id):
    """Assign support ticket"""
    ticket = SupportTicket.query.get_or_404(ticket_id)
    ticket.assigned_to = request.form.get('assigned_to')
    ticket.status = request.form.get('status', 'in_progress')
    db.session.commit()
    flash('Ticket updated!', 'success')
    return redirect(url_for('admin.support_detail', ticket_id=ticket_id))

@bp.route('/user/add', methods=['GET', 'POST'])
@admin_required
def add_user():
    """Add new user"""
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            full_name = request.form.get('full_name', '').strip()
            role = request.form.get('role', 'student')
            
            if not all([username, email, password, full_name]):
                flash('All fields are required.', 'danger')
                return render_template('shared/add_user.html')
            
            # Check for duplicates
            if User.query.filter_by(username=username).first():
                flash('Username already exists.', 'danger')
                return render_template('shared/add_user.html')
            
            if User.query.filter_by(email=email).first():
                flash('Email already exists.', 'danger')
                return render_template('shared/add_user.html')
            
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(
                username=username,
                email=email,
                password=hashed_password,
                full_name=full_name,
                role=role
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            logger.info(f"Admin created user: {username} ({role})")
            flash('✅ User created successfully!', 'success')
            return redirect(url_for('admin.users'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Add user error: {str(e)}", exc_info=True)
            flash('An error occurred creating the user.', 'danger')
    
    return render_template('shared/add_user.html')

@bp.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    """Edit user"""
    edit_user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        try:
            edit_user.username = request.form.get('username', '').strip()
            edit_user.email = request.form.get('email', '').strip()
            edit_user.full_name = request.form.get('full_name', '').strip()
            edit_user.role = request.form.get('role', 'student')
            
            # Only update password if provided
            password = request.form.get('password', '').strip()
            if password:
                edit_user.password = generate_password_hash(password, method='pbkdf2:sha256')
            
            db.session.commit()
            
            logger.info(f"Admin updated user: {edit_user.username}")
            flash('✅ User updated successfully!', 'success')
            return redirect(url_for('admin.users'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Edit user error: {str(e)}", exc_info=True)
            flash('An error occurred updating the user.', 'danger')
    
    return render_template('shared/edit_user.html', edit_user=edit_user)

@bp.route('/user/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Delete user"""
    try:
        user = User.query.get_or_404(user_id)
        
        if user.id == session['user_id']:
            flash('You cannot delete your own account.', 'danger')
            return redirect(url_for('admin.users'))
        
        username = user.username
        db.session.delete(user)
        db.session.commit()
        
        logger.info(f"Admin deleted user: {username}")
        flash(f'🗑️ User "{username}" deleted successfully!', 'success')
        return redirect(url_for('admin.users'))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Delete user error: {str(e)}", exc_info=True)
        flash('An error occurred deleting the user.', 'danger')
        return redirect(url_for('admin.users'))
