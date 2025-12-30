"""
Faculty Routes Blueprint
Handles instructor/teacher functionality
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from werkzeug.utils import secure_filename
from app import db
from app.models import User, Course, Video, Enrollment, OnlineClass
from app.utils.decorators import login_required, faculty_required
from app.utils.helpers import allowed_file, generate_unique_filename
import logging
import os

bp = Blueprint('faculty', __name__, url_prefix='/faculty')
logger = logging.getLogger(__name__)

@bp.route('/profile')
@faculty_required
def profile():
    """Faculty profile page"""
    try:
        user = User.query.get(session['user_id'])
        my_courses = Course.query.filter_by(instructor_id=user.id).all()
        total_students = sum(course.enrollment_count for course in my_courses)
        total_videos = sum(course.video_count for course in my_courses)
        stats = {
            'my_courses': len(my_courses),
            'total_students': total_students,
            'total_videos': total_videos
        }
        return render_template('shared/profile.html', user=user, courses=my_courses, stats=stats)
    except Exception as e:
        logger.error(f"Profile error: {str(e)}", exc_info=True)
        flash('An error occurred loading your profile.', 'danger')
        return redirect(url_for('faculty.dashboard'))

@bp.route('/support')
@faculty_required
def support():
    """Faculty support tickets"""
    from app.models import SupportTicket
    user = User.query.get(session['user_id'])
    tickets = SupportTicket.query.filter_by(user_id=user.id).order_by(SupportTicket.created_at.desc()).all()
    return render_template('shared/support.html', tickets=tickets)

@bp.route('/support/<int:ticket_id>')
@faculty_required
def support_detail(ticket_id):
    """View support ticket detail"""
    from app.models import SupportTicket
    ticket = SupportTicket.query.get_or_404(ticket_id)
    return render_template('shared/support_detail.html', ticket=ticket)

@bp.route('/support/<int:ticket_id>/respond', methods=['POST'])
@faculty_required
def support_respond(ticket_id):
    """Respond to support ticket"""
    from app.models import SupportTicket, TicketResponse
    ticket = SupportTicket.query.get_or_404(ticket_id)
    response = TicketResponse(
        ticket_id=ticket.id,
        user_id=session['user_id'],
        message=request.form.get('message')
    )
    db.session.add(response)
    db.session.commit()
    flash('Response added!', 'success')
    return redirect(url_for('faculty.support_detail', ticket_id=ticket_id))

@bp.route('/add-course', methods=['GET', 'POST'])
@faculty_required
def add_course():
    """Create a new course - alias for create_course"""
    return create_course()

@bp.route('/dashboard')
@faculty_required
def dashboard():
    """Faculty dashboard"""
    try:
        user = User.query.get(session['user_id'])
        my_courses = Course.query.filter_by(instructor_id=user.id).all()
        
        # Calculate stats
        total_courses = len(my_courses)
        total_students = sum(course.enrollment_count for course in my_courses)
        total_videos = sum(course.video_count for course in my_courses)
        
        return render_template('shared/dashboard.html',
                             user=user,
                             my_courses=my_courses,
                             total_courses=total_courses,
                             total_students=total_students,
                             total_videos=total_videos)
    except Exception as e:
        logger.error(f"Faculty dashboard error: {str(e)}", exc_info=True)
        flash('An error occurred loading the dashboard.', 'danger')
        return redirect(url_for('auth.index'))

@bp.route('/courses')
@faculty_required
def courses():
    """View my courses"""
    try:
        user = User.query.get(session['user_id'])
        my_courses = Course.query.filter_by(instructor_id=user.id).all()
        
        return render_template('shared/courses.html', courses=my_courses)
    except Exception as e:
        logger.error(f"Faculty courses error: {str(e)}", exc_info=True)
        flash('An error occurred loading courses.', 'danger')
        return redirect(url_for('faculty.dashboard'))

@bp.route('/course/create', methods=['GET', 'POST'])
@faculty_required
def create_course():
    """Create new course"""
    if request.method == 'POST':
        try:
            user = User.query.get(session['user_id'])
            
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            price_npr = float(request.form.get('price_npr', 0))
            duration_hours = int(request.form.get('duration_hours', 0))
            category = request.form.get('category', '').strip()
            level = request.form.get('level', 'beginner')
            
            if not title or not description:
                flash('Title and description are required.', 'danger')
                return render_template('shared/add_course.html')
            
            course = Course(
                title=title,
                description=description,
                price_npr=price_npr,
                duration_hours=duration_hours,
                category=category,
                level=level,
                instructor_id=user.id
            )
            
            db.session.add(course)
            db.session.commit()
            
            logger.info(f"Faculty {user.username} created course: {title}")
            flash('✅ Course created successfully!', 'success')
            return redirect(url_for('faculty.course_detail', course_id=course.id))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Create course error: {str(e)}", exc_info=True)
            flash('An error occurred creating the course.', 'danger')
    
    return render_template('shared/add_course.html')

@bp.route('/course/<int:course_id>')
@faculty_required
def course_detail(course_id):
    """View course details and manage content"""
    try:
        course = Course.query.get_or_404(course_id)
        user = User.query.get(session['user_id'])
        
        # Check ownership
        if course.instructor_id != user.id and user.role != 'admin':
            flash('You do not have permission to view this course.', 'danger')
            return redirect(url_for('faculty.courses'))
        
        videos = Video.query.filter_by(course_id=course_id).order_by(Video.order).all()
        enrollments = Enrollment.query.filter_by(course_id=course_id).all()
        
        return render_template('shared/course_detail.html',
                             course=course,
                             videos=videos,
                             enrollments=enrollments)
    except Exception as e:
        logger.error(f"Faculty course detail error: {str(e)}", exc_info=True)
        flash('An error occurred loading the course.', 'danger')
        return redirect(url_for('faculty.courses'))

@bp.route('/course/<int:course_id>/add-video', methods=['GET', 'POST'])
@faculty_required
def add_video(course_id):
    """Add video to course"""
    course = Course.query.get_or_404(course_id)
    user = User.query.get(session['user_id'])
    
    # Check ownership
    if course.instructor_id != user.id and user.role != 'admin':
        flash('You do not have permission to modify this course.', 'danger')
        return redirect(url_for('faculty.courses'))
    
    if request.method == 'POST':
        try:
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            video_url = request.form.get('video_url', '').strip()
            duration_minutes = int(request.form.get('duration_minutes', 0))
            order = int(request.form.get('order', 0))
            is_free = request.form.get('is_free') == 'on'
            
            if not title or not video_url:
                flash('Title and video URL are required.', 'danger')
                return render_template('shared/add_video.html', course=course)
            
            video = Video(
                title=title,
                description=description,
                video_url=video_url,
                duration_minutes=duration_minutes,
                course_id=course_id,
                order=order,
                is_free=is_free
            )
            
            db.session.add(video)
            db.session.commit()
            
            logger.info(f"Faculty {user.username} added video to course {course.title}")
            flash('🎥 Video added successfully!', 'success')
            return redirect(url_for('faculty.course_detail', course_id=course_id))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Add video error: {str(e)}", exc_info=True)
            flash('An error occurred adding the video.', 'danger')
    
    return render_template('shared/add_video.html', course=course)

@bp.route('/course/<int:course_id>/edit', methods=['GET', 'POST'])
@faculty_required
def edit_course(course_id):
    """Edit course details"""
    course = Course.query.get_or_404(course_id)
    user = User.query.get(session['user_id'])
    
    # Check ownership
    if course.instructor_id != user.id and user.role != 'admin':
        flash('You do not have permission to edit this course.', 'danger')
        return redirect(url_for('faculty.courses'))
    
    if request.method == 'POST':
        try:
            course.title = request.form.get('title', '').strip()
            course.description = request.form.get('description', '').strip()
            course.price_npr = float(request.form.get('price_npr', 0))
            course.duration_hours = int(request.form.get('duration_hours', 0))
            course.category = request.form.get('category', '').strip()
            course.level = request.form.get('level', 'beginner')
            course.is_published = request.form.get('is_published') == 'on'
            course.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            flash('✅ Course updated successfully!', 'success')
            return redirect(url_for('faculty.course_detail', course_id=course_id))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Edit course error: {str(e)}", exc_info=True)
            flash('An error occurred updating the course.', 'danger')
    
    return render_template('shared/edit_course.html', course=course)

@bp.route('/video/<int:video_id>/delete', methods=['POST'])
@faculty_required
def delete_video(video_id):
    """Delete a video"""
    try:
        video = Video.query.get_or_404(video_id)
        user = User.query.get(session['user_id'])
        
        # Check ownership
        if video.course.instructor_id != user.id and user.role != 'admin':
            flash('You do not have permission to delete this video.', 'danger')
            return redirect(url_for('faculty.courses'))
        
        course_id = video.course_id
        db.session.delete(video)
        db.session.commit()
        
        flash('🗑️ Video deleted successfully!', 'success')
        return redirect(url_for('faculty.course_detail', course_id=course_id))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Delete video error: {str(e)}", exc_info=True)
        flash('An error occurred deleting the video.', 'danger')
        return redirect(url_for('faculty.courses'))

@bp.route('/students')
@faculty_required
def students():
    """View all enrolled students"""
    try:
        user = User.query.get(session['user_id'])
        my_courses = Course.query.filter_by(instructor_id=user.id).all()
        
        students_data = {}
        for course in my_courses:
            enrollments = Enrollment.query.filter_by(course_id=course.id).all()
            for enrollment in enrollments:
                student = enrollment.student
                if student.id not in students_data:
                    students_data[student.id] = {
                        'student': student,
                        'courses': []
                    }
                students_data[student.id]['courses'].append(course.title)
        
        return render_template('shared/faculty_students.html', students_data=students_data.values())
    except Exception as e:
        logger.error(f"Faculty students error: {str(e)}", exc_info=True)
        flash('An error occurred loading students.', 'danger')
        return redirect(url_for('faculty.dashboard'))

@bp.route('/schedule-class', methods=['GET', 'POST'])
@faculty_required
def schedule_class():
    """Schedule an online class"""
    user = User.query.get(session['user_id'])
    my_courses = Course.query.filter_by(instructor_id=user.id).all()
    
    if request.method == 'POST':
        try:
            course_id = int(request.form.get('course_id'))
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            meeting_link = request.form.get('meeting_link', '').strip()
            scheduled_at_str = request.form.get('scheduled_at')
            duration_minutes = int(request.form.get('duration_minutes', 60))
            
            if not all([course_id, title, scheduled_at_str]):
                flash('Course, title, and schedule time are required.', 'danger')
                return render_template('shared/schedule_class.html', courses=my_courses)
            
            scheduled_at = datetime.strptime(scheduled_at_str, '%Y-%m-%dT%H:%M')
            
            online_class = OnlineClass(
                course_id=course_id,
                title=title,
                description=description,
                meeting_link=meeting_link,
                scheduled_at=scheduled_at,
                duration_minutes=duration_minutes,
                created_by=user.id
            )
            
            db.session.add(online_class)
            db.session.commit()
            
            logger.info(f"Faculty {user.username} scheduled class: {title}")
            flash('📅 Online class scheduled successfully!', 'success')
            return redirect(url_for('faculty.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Schedule class error: {str(e)}", exc_info=True)
            flash('An error occurred scheduling the class.', 'danger')
    
    return render_template('shared/schedule_class.html', courses=my_courses)
