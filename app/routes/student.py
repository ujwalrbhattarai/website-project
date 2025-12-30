"""
Student Routes Blueprint
Handles all student-related functionality
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
from app import db
from app.models import User, Course, Video, Enrollment, Payment, StudyHistory, OnlineClass, TodoItem, Certificate, SupportTicket, TicketResponse
from app.utils.decorators import login_required, student_required
import logging

bp = Blueprint('student', __name__, url_prefix='/student')
logger = logging.getLogger(__name__)

@bp.route('/profile')
@login_required
def profile():
    """Student profile page"""
    try:
        user = User.query.get(session['user_id'])
        enrollments = Enrollment.query.filter_by(student_id=user.id).all()
        stats = {
            'enrolled_courses': len(enrollments),
            'certificates': Certificate.query.filter_by(student_id=user.id).count() if Certificate else 0,
            'videos_watched': len(user.study_history.all()) if user.study_history else 0
        }
        return render_template('shared/profile.html', user=user, enrollments=enrollments, stats=stats)
    except Exception as e:
        logger.error(f"Profile error: {str(e)}", exc_info=True)
        flash('An error occurred loading your profile.', 'danger')
        return redirect(url_for('student.dashboard'))

@bp.route('/settings')
@login_required
def settings():
    """Student settings page"""
    user = User.query.get(session['user_id'])
    return render_template('shared/settings.html', user=user, enrollments=[])

@bp.route('/support')
@login_required
def support():
    """Student support tickets"""
    user = User.query.get(session['user_id'])
    tickets = SupportTicket.query.filter_by(user_id=user.id).order_by(SupportTicket.created_at.desc()).all()
    return render_template('shared/support.html', tickets=tickets)

@bp.route('/support/new', methods=['GET', 'POST'])
@login_required
def support_new():
    """Create new support ticket"""
    if request.method == 'POST':
        user = User.query.get(session['user_id'])
        ticket = SupportTicket(
            user_id=user.id,
            subject=request.form.get('subject'),
            message=request.form.get('message'),
            priority=request.form.get('priority', 'medium')
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Support ticket created successfully!', 'success')
        return redirect(url_for('student.support'))
    return render_template('shared/support_new.html')

@bp.route('/support/<int:ticket_id>')
@login_required
def support_detail(ticket_id):
    """View support ticket detail"""
    ticket = SupportTicket.query.get_or_404(ticket_id)
    return render_template('shared/support_detail.html', ticket=ticket)

@bp.route('/support/<int:ticket_id>/respond', methods=['POST'])
@login_required
def support_respond(ticket_id):
    """Respond to support ticket"""
    ticket = SupportTicket.query.get_or_404(ticket_id)
    response = TicketResponse(
        ticket_id=ticket.id,
        user_id=session['user_id'],
        message=request.form.get('message')
    )
    db.session.add(response)
    db.session.commit()
    flash('Response added!', 'success')
    return redirect(url_for('student.support_detail', ticket_id=ticket_id))

@bp.route('/dashboard')
@login_required
def dashboard():
    """Student dashboard with overview"""
    try:
        user = User.query.get(session['user_id'])
        enrollments = Enrollment.query.filter_by(student_id=user.id).all()
        payments = Payment.query.filter_by(student_id=user.id).order_by(Payment.payment_date.desc()).limit(5).all()
        
        # Calculate statistics
        total_courses = len(enrollments)
        completed_courses = len([e for e in enrollments if e.completion_percentage >= 100])
        in_progress = total_courses - completed_courses
        
        # Get recent activity
        recent_videos = StudyHistory.query.filter_by(student_id=user.id).order_by(StudyHistory.last_watched.desc()).limit(5).all()
        
        return render_template('shared/dashboard.html', 
                             user=user, 
                             enrollments=enrollments,
                             payments=payments,
                             total_payments=len(payments),
                             total_courses=total_courses,
                             completed_courses=completed_courses,
                             in_progress=in_progress,
                             recent_videos=recent_videos)
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}", exc_info=True)
        flash('An error occurred loading the dashboard.', 'danger')
        return redirect(url_for('auth.index'))

@bp.route('/courses')
@login_required
def courses():
    """Browse available courses"""
    try:
        user = User.query.get(session['user_id'])
        enrolled_course_ids = [e.course_id for e in user.enrollments]
        available_courses = Course.query.filter(
            ~Course.id.in_(enrolled_course_ids),
            Course.is_published == True
        ).all()
        
        return render_template('shared/courses.html', courses=available_courses)
    except Exception as e:
        logger.error(f"Courses list error: {str(e)}", exc_info=True)
        flash('An error occurred loading courses.', 'danger')
        return redirect(url_for('student.dashboard'))

@bp.route('/course/<int:course_id>')
@login_required
def course_detail(course_id):
    """View course details"""
    try:
        course = Course.query.get_or_404(course_id)
        user = User.query.get(session['user_id'])
        enrollment = Enrollment.query.filter_by(student_id=user.id, course_id=course_id).first()
        videos = Video.query.filter_by(course_id=course_id).order_by(Video.order).all()
        
        # Get study progress for each video if enrolled
        video_progress = {}
        if enrollment:
            for video in videos:
                history = StudyHistory.query.filter_by(student_id=user.id, video_id=video.id).first()
                video_progress[video.id] = history
        
        return render_template('shared/course_detail.html', 
                             course=course, 
                             enrollment=enrollment,
                             videos=videos,
                             video_progress=video_progress)
    except Exception as e:
        logger.error(f"Course detail error: {str(e)}", exc_info=True)
        flash('An error occurred loading the course.', 'danger')
        return redirect(url_for('student.courses'))

@bp.route('/enroll/<int:course_id>', methods=['POST'])
@login_required
def enroll(course_id):
    """Enroll in a course"""
    try:
        user = User.query.get(session['user_id'])
        course = Course.query.get_or_404(course_id)
        
        # Check if already enrolled
        existing = Enrollment.query.filter_by(student_id=user.id, course_id=course_id).first()
        if existing:
            flash('You are already enrolled in this course.', 'info')
            return redirect(url_for('student.course_detail', course_id=course_id))
        
        payment_method = request.form.get('payment_method', 'cash')
        
        # Store pending enrollment for payment gateways
        if payment_method in ['esewa', 'khalti']:
            session['pending_enrollment'] = {
                'course_id': course_id,
                'payment_method': payment_method,
                'amount': course.price_npr
            }
            return redirect(url_for('payment.initiate', method=payment_method, course_id=course_id))
        
        # Process immediate enrollment for cash/demo
        payment = Payment(
            student_id=user.id,
            course_id=course_id,
            amount_npr=course.price_npr,
            payment_method=payment_method,
            status='completed',
            transaction_id=f'TXN-{payment_method.upper()}-{datetime.utcnow().strftime("%Y%m%d%H%M%S")}'
        )
        db.session.add(payment)
        
        enrollment = Enrollment(student_id=user.id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        
        logger.info(f"User {user.username} enrolled in course {course.title}")
        flash(f'🎉 Successfully enrolled in {course.title}!', 'success')
        return redirect(url_for('student.course_detail', course_id=course_id))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Enrollment error: {str(e)}", exc_info=True)
        flash('An error occurred during enrollment. Please try again.', 'danger')
        return redirect(url_for('student.courses'))

@bp.route('/video/<int:video_id>')
@login_required
def watch_video(video_id):
    """Watch a video"""
    try:
        video = Video.query.get_or_404(video_id)
        user = User.query.get(session['user_id'])
        
        # Check enrollment
        enrollment = Enrollment.query.filter_by(
            student_id=user.id, 
            course_id=video.course_id
        ).first()
        
        if not enrollment and not video.is_free:
            flash('You need to enroll in this course first.', 'warning')
            return redirect(url_for('student.courses'))
        
        # Get or create study history
        history = StudyHistory.query.filter_by(student_id=user.id, video_id=video_id).first()
        if not history:
            history = StudyHistory(student_id=user.id, video_id=video_id)
            db.session.add(history)
            db.session.commit()
        
        # Get course and all videos for navigation
        course = video.course
        all_videos = Video.query.filter_by(course_id=course.id).order_by(Video.order).all()
        
        return render_template('shared/watch_video.html', 
                             video=video, 
                             history=history,
                             course=course,
                             all_videos=all_videos)
    except Exception as e:
        logger.error(f"Watch video error: {str(e)}", exc_info=True)
        flash('An error occurred loading the video.', 'danger')
        return redirect(url_for('student.dashboard'))

@bp.route('/update_progress/<int:video_id>', methods=['POST'])
@login_required
def update_progress(video_id):
    """Update video watch progress via AJAX"""
    try:
        user = User.query.get(session['user_id'])
        data = request.json
        
        watch_duration = data.get('watch_duration', 0)
        total_duration = data.get('total_duration', 1)
        
        completion_percentage = (watch_duration / total_duration) * 100 if total_duration > 0 else 0
        
        history = StudyHistory.query.filter_by(student_id=user.id, video_id=video_id).first()
        
        if history:
            history.watch_duration = watch_duration
            history.completion_percentage = completion_percentage
            history.is_completed = completion_percentage >= 70
            history.completed = completion_percentage >= 95
            history.last_watched = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                'success': True, 
                'completion_percentage': round(completion_percentage, 2),
                'is_completed': history.is_completed
            })
        
        return jsonify({'success': False, 'error': 'History not found'}), 404
        
    except Exception as e:
        logger.error(f"Progress update error: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/my-courses')
@login_required
def my_courses():
    """View enrolled courses"""
    try:
        user = User.query.get(session['user_id'])
        enrollments = Enrollment.query.filter_by(student_id=user.id).all()
        
        courses_data = []
        for enrollment in enrollments:
            course = enrollment.course
            total_videos = course.videos.count()
            completed_videos = StudyHistory.query.join(Video).filter(
                StudyHistory.student_id == user.id,
                Video.course_id == course.id,
                StudyHistory.is_completed == True
            ).count()
            
            progress = (completed_videos / total_videos * 100) if total_videos > 0 else 0
            enrollment.completion_percentage = progress
            
            courses_data.append({
                'enrollment': enrollment,
                'course': course,
                'total_videos': total_videos,
                'completed_videos': completed_videos,
                'progress': round(progress, 1)
            })
        
        return render_template('shared/my_courses.html', courses_data=courses_data)
    except Exception as e:
        logger.error(f"My courses error: {str(e)}", exc_info=True)
        flash('An error occurred loading your courses.', 'danger')
        return redirect(url_for('student.dashboard'))

@bp.route('/certificates')
@login_required
def certificates():
    """View earned certificates"""
    try:
        user = User.query.get(session['user_id'])
        certificates = Certificate.query.filter_by(student_id=user.id).all()
        eligible_courses = []
        
        return render_template('shared/certificates.html', certificates=certificates, eligible_courses=eligible_courses)
    except Exception as e:
        logger.error(f"Certificates error: {str(e)}", exc_info=True)
        flash('An error occurred loading certificates.', 'danger')
        return redirect(url_for('student.dashboard'))

@bp.route('/todo')
@login_required
def todo():
    """View todo list"""
    try:
        user = User.query.get(session['user_id'])
        pending_todos = TodoItem.query.filter_by(
            student_id=user.id, 
            is_completed=False
        ).order_by(TodoItem.due_date.asc()).all()
        
        completed_todos = TodoItem.query.filter_by(
            student_id=user.id, 
            is_completed=True
        ).order_by(TodoItem.completed_at.desc()).limit(20).all()
        
        return render_template('shared/todo.html', 
                             pending_todos=pending_todos, 
                             completed_todos=completed_todos)
    except Exception as e:
        logger.error(f"Todo list error: {str(e)}", exc_info=True)
        flash('An error occurred loading your tasks.', 'danger')
        return redirect(url_for('student.dashboard'))

@bp.route('/todo/add', methods=['POST'])
@login_required
def add_todo():
    """Add new todo item"""
    try:
        user = User.query.get(session['user_id'])
        
        title = request.form.get('title', '').strip()
        if not title:
            flash('Task title is required.', 'danger')
            return redirect(url_for('student.todo'))
        
        due_date = None
        due_date_str = request.form.get('due_date')
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                pass
        
        todo = TodoItem(
            student_id=user.id,
            title=title,
            description=request.form.get('description', ''),
            priority=request.form.get('priority', 'medium'),
            due_date=due_date
        )
        
        db.session.add(todo)
        db.session.commit()
        
        flash('✅ Task added successfully!', 'success')
        return redirect(url_for('student.todo'))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Add todo error: {str(e)}", exc_info=True)
        flash('An error occurred adding the task.', 'danger')
        return redirect(url_for('student.todo'))

@bp.route('/todo/<int:todo_id>/toggle', methods=['POST'])
@login_required
def toggle_todo(todo_id):
    """Toggle todo completion status"""
    try:
        user = User.query.get(session['user_id'])
        todo = TodoItem.query.get_or_404(todo_id)
        
        if todo.student_id != user.id:
            abort(403)
        
        todo.is_completed = not todo.is_completed
        todo.completed_at = datetime.utcnow() if todo.is_completed else None
        db.session.commit()
        
        return redirect(url_for('student.todo'))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Toggle todo error: {str(e)}", exc_info=True)
        flash('An error occurred updating the task.', 'danger')
        return redirect(url_for('student.todo'))

@bp.route('/todo/<int:todo_id>/delete', methods=['POST'])
@login_required
def delete_todo(todo_id):
    """Delete todo item"""
    try:
        user = User.query.get(session['user_id'])
        todo = TodoItem.query.get_or_404(todo_id)
        
        if todo.student_id != user.id:
            abort(403)
        
        db.session.delete(todo)
        db.session.commit()
        
        flash('🗑️ Task deleted successfully!', 'success')
        return redirect(url_for('student.todo'))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Delete todo error: {str(e)}", exc_info=True)
        flash('An error occurred deleting the task.', 'danger')
        return redirect(url_for('student.todo'))

@bp.route('/online-classes')
@login_required
def online_classes():
    """View scheduled online classes"""
    try:
        user = User.query.get(session['user_id'])
        enrolled_course_ids = [e.course_id for e in user.enrollments]
        
        now = datetime.utcnow()
        
        if enrolled_course_ids:
            upcoming_classes = OnlineClass.query.filter(
                OnlineClass.course_id.in_(enrolled_course_ids),
                OnlineClass.scheduled_at >= now
            ).order_by(OnlineClass.scheduled_at).all()
            
            past_classes = OnlineClass.query.filter(
                OnlineClass.course_id.in_(enrolled_course_ids),
                OnlineClass.scheduled_at < now
            ).order_by(OnlineClass.scheduled_at.desc()).limit(10).all()
        else:
            upcoming_classes = []
            past_classes = []
        
        return render_template('shared/online_classes.html', 
                             upcoming_classes=upcoming_classes, 
                             past_classes=past_classes)
    except Exception as e:
        logger.error(f"Online classes error: {str(e)}", exc_info=True)
        flash('An error occurred loading online classes.', 'danger')
        return redirect(url_for('student.dashboard'))
