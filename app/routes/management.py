"""
Management Routes Blueprint
Handles management/support functionality
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from app import db
from app.models import User, SupportTicket, TicketResponse, Payment, Enrollment, Course
from app.utils.decorators import login_required, management_required
import logging

bp = Blueprint('management', __name__, url_prefix='/management')
logger = logging.getLogger(__name__)

@bp.route('/profile')
@management_required
def profile():
    """Management profile page"""
    try:
        user = User.query.get(session['user_id'])
        stats = {
            'total_students': User.query.filter_by(role='student').count(),
            'total_courses': Course.query.count(),
            'total_tickets': SupportTicket.query.count()
        }
        return render_template('shared/profile.html', user=user, stats=stats)
    except Exception as e:
        logger.error(f"Profile error: {str(e)}", exc_info=True)
        flash('An error occurred loading your profile.', 'danger')
        return redirect(url_for('management.dashboard'))

@bp.route('/dashboard')
@management_required
def dashboard():
    """Management dashboard"""
    try:
        # Get statistics
        total_students = User.query.filter_by(role='student').count()
        total_faculty = User.query.filter_by(role='faculty').count()
        total_courses = Course.query.count()
        total_tickets = SupportTicket.query.count()
        
        # Get ticket statistics
        open_tickets = SupportTicket.query.filter_by(status='open').count()
        in_progress_tickets = SupportTicket.query.filter_by(status='in_progress').count()
        closed_tickets = SupportTicket.query.filter_by(status='closed').count()
        
        # Get my assigned tickets
        user = User.query.get(session['user_id'])
        my_tickets = SupportTicket.query.filter_by(assigned_to=user.id).all()
        
        # Recent tickets
        recent_tickets = SupportTicket.query.order_by(
            SupportTicket.created_at.desc()
        ).limit(10).all()
        
        # Recent enrollments
        recent_enrollments = Enrollment.query.order_by(
            Enrollment.enrollment_date.desc()
        ).limit(10).all()
        
        return render_template('shared/dashboard.html',
                             user=user,
                             total_students=total_students,
                             total_faculty=total_faculty,
                             total_courses=total_courses,
                             total_tickets=total_tickets,
                             open_tickets=open_tickets,
                             in_progress_tickets=in_progress_tickets,
                             closed_tickets=closed_tickets,
                             my_tickets=my_tickets,
                             recent_tickets=recent_tickets,
                             recent_enrollments=recent_enrollments)
    except Exception as e:
        logger.error(f"Management dashboard error: {str(e)}", exc_info=True)
        flash('An error occurred loading the dashboard.', 'danger')
        return redirect(url_for('auth.index'))

@bp.route('/tickets')
@management_required
def tickets():
    """View all support tickets"""
    try:
        status_filter = request.args.get('status', 'all')
        
        if status_filter != 'all':
            tickets_list = SupportTicket.query.filter_by(status=status_filter).order_by(
                SupportTicket.created_at.desc()
            ).all()
        else:
            tickets_list = SupportTicket.query.order_by(
                SupportTicket.created_at.desc()
            ).all()
        
        return render_template('shared/tickets.html', 
                             tickets=tickets_list, 
                             status_filter=status_filter)
    except Exception as e:
        logger.error(f"Management tickets error: {str(e)}", exc_info=True)
        flash('An error occurred loading tickets.', 'danger')
        return redirect(url_for('management.dashboard'))

@bp.route('/ticket/<int:ticket_id>')
@management_required
def ticket_detail(ticket_id):
    """View ticket details and responses"""
    try:
        ticket = SupportTicket.query.get_or_404(ticket_id)
        responses = TicketResponse.query.filter_by(ticket_id=ticket_id).order_by(
            TicketResponse.created_at
        ).all()
        
        # Get available management users for assignment
        management_users = User.query.filter(
            User.role.in_(['admin', 'management'])
        ).all()
        
        return render_template('shared/support_detail.html',
                             ticket=ticket,
                             responses=responses,
                             management_users=management_users)
    except Exception as e:
        logger.error(f"Ticket detail error: {str(e)}", exc_info=True)
        flash('An error occurred loading the ticket.', 'danger')
        return redirect(url_for('management.tickets'))

@bp.route('/ticket/<int:ticket_id>/respond', methods=['POST'])
@management_required
def respond_to_ticket(ticket_id):
    """Add response to ticket"""
    try:
        ticket = SupportTicket.query.get_or_404(ticket_id)
        user = User.query.get(session['user_id'])
        
        message = request.form.get('message', '').strip()
        if not message:
            flash('Response message is required.', 'danger')
            return redirect(url_for('management.ticket_detail', ticket_id=ticket_id))
        
        response = TicketResponse(
            ticket_id=ticket_id,
            user_id=user.id,
            message=message
        )
        
        # Update ticket status
        new_status = request.form.get('status', ticket.status)
        ticket.status = new_status
        ticket.updated_at = datetime.utcnow()
        
        db.session.add(response)
        db.session.commit()
        
        logger.info(f"Management user {user.username} responded to ticket #{ticket_id}")
        flash('✅ Response added successfully!', 'success')
        return redirect(url_for('management.ticket_detail', ticket_id=ticket_id))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Respond to ticket error: {str(e)}", exc_info=True)
        flash('An error occurred adding the response.', 'danger')
        return redirect(url_for('management.ticket_detail', ticket_id=ticket_id))

@bp.route('/ticket/<int:ticket_id>/assign', methods=['POST'])
@management_required
def assign_ticket(ticket_id):
    """Assign ticket to user"""
    try:
        ticket = SupportTicket.query.get_or_404(ticket_id)
        assigned_to_id = request.form.get('assigned_to')
        
        if assigned_to_id:
            ticket.assigned_to = int(assigned_to_id)
            ticket.status = 'in_progress'
            ticket.updated_at = datetime.utcnow()
            db.session.commit()
            
            flash('✅ Ticket assigned successfully!', 'success')
        else:
            flash('Please select a user to assign.', 'danger')
        
        return redirect(url_for('management.ticket_detail', ticket_id=ticket_id))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Assign ticket error: {str(e)}", exc_info=True)
        flash('An error occurred assigning the ticket.', 'danger')
        return redirect(url_for('management.ticket_detail', ticket_id=ticket_id))

@bp.route('/payments')
@management_required
def payments():
    """View payment transactions"""
    try:
        payments_list = Payment.query.order_by(Payment.payment_date.desc()).all()
        
        # Calculate total revenue
        total_revenue = db.session.query(db.func.sum(Payment.amount_npr)).filter(
            Payment.status == 'completed'
        ).scalar() or 0
        
        pending_revenue = db.session.query(db.func.sum(Payment.amount_npr)).filter(
            Payment.status == 'pending'
        ).scalar() or 0
        
        return render_template('shared/payments.html',
                             payments=payments_list,
                             total_revenue=total_revenue,
                             pending_revenue=pending_revenue)
    except Exception as e:
        logger.error(f"Management payments error: {str(e)}", exc_info=True)
        flash('An error occurred loading payments.', 'danger')
        return redirect(url_for('management.dashboard'))

@bp.route('/students')
@management_required
def students():
    """View all students"""
    try:
        students_list = User.query.filter_by(role='student').all()
        
        return render_template('shared/students.html', students=students_list)
    except Exception as e:
        logger.error(f"Management students error: {str(e)}", exc_info=True)
        flash('An error occurred loading students.', 'danger')
        return redirect(url_for('management.dashboard'))

@bp.route('/courses')
@management_required
def courses():
    """View all courses"""
    courses_list = Course.query.all()
    return render_template('shared/courses.html', courses=courses_list)

@bp.route('/reports')
@management_required
def reports():
    """Reports and analytics"""
    courses = Course.query.all()
    payments = Payment.query.filter_by(status='completed').all()
    return render_template('shared/reports.html', 
                          courses=courses,
                          payments=payments)

@bp.route('/support')
@management_required
def support():
    """View support tickets"""
    tickets = SupportTicket.query.order_by(SupportTicket.created_at.desc()).all()
    return render_template('shared/support.html', tickets=tickets)
