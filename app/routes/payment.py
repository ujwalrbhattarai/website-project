"""
Payment Routes Blueprint
Handles payment gateway integration
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from app import db
from app.models import User, Course, Payment, Enrollment
from app.utils.decorators import login_required
import logging

bp = Blueprint('payment', __name__, url_prefix='/payment')
logger = logging.getLogger(__name__)

@bp.route('/initiate/<method>/<int:course_id>')
@login_required
def initiate(method, course_id):
    """Initiate payment process"""
    try:
        user = User.query.get(session['user_id'])
        course = Course.query.get_or_404(course_id)
        
        if method == 'esewa':
            return initiate_esewa(user, course)
        elif method == 'khalti':
            return initiate_khalti(user, course)
        else:
            flash('Invalid payment method.', 'danger')
            return redirect(url_for('student.courses'))
            
    except Exception as e:
        logger.error(f"Payment initiation error: {str(e)}", exc_info=True)
        flash('An error occurred initiating payment.', 'danger')
        return redirect(url_for('student.courses'))

def initiate_esewa(user, course):
    """Initialize eSewa payment"""
    # eSewa Configuration (Test Mode)
    transaction_uuid = f'TXN-{user.id}-{course.id}-{datetime.utcnow().strftime("%Y%m%d%H%M%S")}'
    
    esewa_config = {
        'merchant_code': 'EPAYTEST',  # Replace with actual merchant code
        'success_url': url_for('payment.esewa_success', _external=True),
        'failure_url': url_for('payment.esewa_failure', _external=True),
        'amount': course.price_npr,
        'tax_amount': 0,
        'service_charge': 0,
        'product_delivery_charge': 0,
        'total_amount': course.price_npr,
        'transaction_uuid': transaction_uuid,
        'product_code': f'COURSE-{course.id}',
        'product_service_charge': 0
    }
    
    # Store transaction in session
    session['payment_transaction'] = {
        'course_id': course.id,
        'transaction_uuid': transaction_uuid,
        'amount': course.price_npr,
        'method': 'esewa'
    }
    
    return render_template('payment/esewa_redirect.html', 
                         config=esewa_config, 
                         course=course)

def initiate_khalti(user, course):
    """Initialize Khalti payment"""
    # Khalti Configuration
    transaction_uuid = f'TXN-{user.id}-{course.id}-{datetime.utcnow().strftime("%Y%m%d%H%M%S")}'
    
    khalti_config = {
        'public_key': 'test_public_key',  # Replace with actual public key
        'product_identity': f'COURSE-{course.id}',
        'product_name': course.title,
        'product_url': url_for('student.course_detail', course_id=course.id, _external=True),
        'amount': int(course.price_npr * 100),  # Khalti uses paisa (1 NPR = 100 paisa)
        'transaction_uuid': transaction_uuid
    }
    
    # Store transaction in session
    session['payment_transaction'] = {
        'course_id': course.id,
        'transaction_uuid': transaction_uuid,
        'amount': course.price_npr,
        'method': 'khalti'
    }
    
    return render_template('payment/khalti_redirect.html', 
                         config=khalti_config, 
                         course=course)

@bp.route('/esewa/success')
@login_required
def esewa_success():
    """Handle eSewa payment success"""
    try:
        # Get transaction details from query parameters
        transaction_code = request.args.get('refId')
        transaction_uuid = request.args.get('oid')
        amount = request.args.get('amt')
        
        # Get stored transaction from session
        payment_transaction = session.get('payment_transaction')
        
        if not payment_transaction or payment_transaction.get('method') != 'esewa':
            flash('Payment verification failed. Transaction not found.', 'danger')
            return redirect(url_for('student.courses'))
        
        course_id = payment_transaction['course_id']
        user = User.query.get(session['user_id'])
        course = Course.query.get_or_404(course_id)
        
        # Check if already enrolled
        existing = Enrollment.query.filter_by(student_id=user.id, course_id=course_id).first()
        if not existing:
            # Create payment record
            payment = Payment(
                student_id=user.id,
                course_id=course_id,
                amount_npr=course.price_npr,
                payment_method='esewa',
                status='completed',
                transaction_id=transaction_code or transaction_uuid
            )
            db.session.add(payment)
            
            # Create enrollment
            enrollment = Enrollment(student_id=user.id, course_id=course_id)
            db.session.add(enrollment)
            db.session.commit()
            
            logger.info(f"eSewa payment successful for user {user.username}, course {course.title}")
        
        # Clear session
        session.pop('payment_transaction', None)
        session.pop('pending_enrollment', None)
        
        flash(f'🎉 Payment successful! You are now enrolled in {course.title}!', 'success')
        return redirect(url_for('student.course_detail', course_id=course_id))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"eSewa success handler error: {str(e)}", exc_info=True)
        flash('An error occurred processing your payment.', 'danger')
        return redirect(url_for('student.courses'))

@bp.route('/esewa/failure')
@login_required
def esewa_failure():
    """Handle eSewa payment failure"""
    # Clear session
    session.pop('payment_transaction', None)
    session.pop('pending_enrollment', None)
    
    logger.warning(f"eSewa payment failed for user {session.get('username')}")
    flash('❌ Payment failed or was cancelled. Please try again.', 'danger')
    return redirect(url_for('student.courses'))

@bp.route('/khalti/verify', methods=['POST'])
@login_required
def khalti_verify():
    """Verify Khalti payment"""
    try:
        # Get payment token from request
        token = request.form.get('token')
        amount = request.form.get('amount')
        
        # Get stored transaction from session
        payment_transaction = session.get('payment_transaction')
        
        if not payment_transaction or payment_transaction.get('method') != 'khalti':
            return {'success': False, 'message': 'Transaction not found'}, 400
        
        course_id = payment_transaction['course_id']
        user = User.query.get(session['user_id'])
        course = Course.query.get_or_404(course_id)
        
        # In production, verify with Khalti API here
        # For now, process as successful
        
        # Check if already enrolled
        existing = Enrollment.query.filter_by(student_id=user.id, course_id=course_id).first()
        if not existing:
            # Create payment record
            payment = Payment(
                student_id=user.id,
                course_id=course_id,
                amount_npr=course.price_npr,
                payment_method='khalti',
                status='completed',
                transaction_id=token
            )
            db.session.add(payment)
            
            # Create enrollment
            enrollment = Enrollment(student_id=user.id, course_id=course_id)
            db.session.add(enrollment)
            db.session.commit()
            
            logger.info(f"Khalti payment successful for user {user.username}, course {course.title}")
        
        # Clear session
        session.pop('payment_transaction', None)
        session.pop('pending_enrollment', None)
        
        return {'success': True, 'course_id': course_id}
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Khalti verify error: {str(e)}", exc_info=True)
        return {'success': False, 'message': str(e)}, 500
