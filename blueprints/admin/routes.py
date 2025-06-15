from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app import db
from models.models import Quiz, Question
from flask_login import login_required, current_user
import time

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/dashboard')
@login_required   
def dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('quiz.quiz_home'))
    quizzes = Quiz.query.all()  # Fetch all quizzes
    return render_template('admin_dashboard.html', quizzes=quizzes)

@admin.route('/add_quiz', methods=['GET', 'POST'])
@login_required
def add_quiz():
    if current_user.role != 'admin':
        return redirect(url_for('quiz.quiz_home'))
    
    if request.method == 'POST':
        # Get quiz basic info
        title = request.form['title']
        category = request.form['category']
        
        # Create new quiz
        new_quiz = Quiz(title=title, category=category, created_by=current_user.id)
        db.session.add(new_quiz)
        db.session.flush()  # This gives us the quiz.id without committing
        
        # Process questions
        questions_data = {}
        for key, value in request.form.items():
            if key.startswith('questions['):
                # Parse the key to extract question number and field
                # Format: questions[1][text], questions[1][option_a], etc.
                parts = key.split('[')
                question_num = parts[1].split(']')[0]
                field_name = parts[2].split(']')[0]
                
                if question_num not in questions_data:
                    questions_data[question_num] = {}
                questions_data[question_num][field_name] = value
        
        # Save questions to database
        for question_data in questions_data.values():
            if all(field in question_data for field in ['text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option']):
                new_question = Question(
                    question_text=question_data['text'],
                    option_a=question_data['option_a'],
                    option_b=question_data['option_b'],
                    option_c=question_data['option_c'],
                    option_d=question_data['option_d'],
                    correct_option=question_data['correct_option'],
                    quiz_id=new_quiz.id
                )
                db.session.add(new_question)
        
        try:
            db.session.commit()
            flash(f'Quiz "{title}" created successfully with {len(questions_data)} questions!', 'success')
            return redirect(url_for('admin.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating quiz. Please try again.', 'error')
            return redirect(url_for('admin.add_quiz'))
    
    return render_template('add_quiz.html')

@admin.route('/edit_quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def edit_quiz(quiz_id):
    if current_user.role != 'admin':
        return redirect(url_for('quiz.quiz_home'))
    
     # Clear flash messages when entering edit page
    if request.method == 'GET':
        session.pop('_flashes', None) # Clear flash messages when entering edit page
    if request.method == 'GET':
        session.pop('_flashes', None)

    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()

    if request.method == 'POST':
        try:
            # Update quiz basic info
            quiz.title = request.form['title']
            quiz.category = request.form['category']

            # Handle questions to delete
            questions_to_delete = request.form.get('questions_to_delete', '')
            if questions_to_delete:
                delete_ids = [int(id) for id in questions_to_delete.split(',') if id]
                for question_id in delete_ids:
                    question_to_delete = Question.query.get(question_id)
                    if question_to_delete and question_to_delete.quiz_id == quiz_id:
                        db.session.delete(question_to_delete)

            # Update existing questions
            for key, value in request.form.items():
                if key.startswith('existing_questions[') and not key.endswith('[id]'):
                    # Parse: existing_questions[123][text] -> question_id=123, field=text
                    parts = key.split('[')
                    question_id = int(parts[1].split(']')[0])
                    field_name = parts[2].split(']')[0]
                    
                    # Skip if marked for deletion
                    if f'delete_question_{question_id}' in request.form:
                        continue
                    
                    question = Question.query.get(question_id)
                    if question and question.quiz_id == quiz_id:
                        if field_name == 'text':
                            question.question_text = value
                        elif field_name == 'option_a':
                            question.option_a = value
                        elif field_name == 'option_b':
                            question.option_b = value
                        elif field_name == 'option_c':
                            question.option_c = value
                        elif field_name == 'option_d':
                            question.option_d = value
                        elif field_name == 'correct_option':
                            question.correct_option = value

            # Add new questions
            new_questions_data = {}
            for key, value in request.form.items():
                if key.startswith('new_questions['):
                    # Parse: new_questions[1][text] -> question_num=1, field=text
                    parts = key.split('[')
                    question_num = parts[1].split(']')[0]
                    field_name = parts[2].split(']')[0]
                    
                    if question_num not in new_questions_data:
                        new_questions_data[question_num] = {}
                    new_questions_data[question_num][field_name] = value

            # Save new questions to database
            for question_data in new_questions_data.values():
                if all(field in question_data for field in ['text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option']):
                    new_question = Question(
                        question_text=question_data['text'],
                        option_a=question_data['option_a'],
                        option_b=question_data['option_b'],
                        option_c=question_data['option_c'],
                        option_d=question_data['option_d'],
                        correct_option=question_data['correct_option'],
                        quiz_id=quiz.id
                    )
                    db.session.add(new_question)

            db.session.commit()
            
            # SOLUTION: Return to edit page with success message instead of dashboard
            flash(f'Quiz "{quiz.title}" updated successfully!', 'success')
            return render_template('edit_quiz.html', quiz=quiz, questions=Question.query.filter_by(quiz_id=quiz_id).all())
            
        except Exception as e:
            db.session.rollback()
            flash('Error updating quiz. Please try again.', 'error')
            return render_template('edit_quiz.html', quiz=quiz, questions=questions)

    return render_template('edit_quiz.html', quiz=quiz, questions=questions)

@admin.route('/delete_quiz/<int:quiz_id>')
@login_required
def delete_quiz(quiz_id):
    print(f"Delete function called for quiz_id: {quiz_id}")  # Debug line
    
    if current_user.role != 'admin':
        print("User is not admin")  # Debug line
        return redirect(url_for('quiz.quiz_home'))

    quiz = Quiz.query.get_or_404(quiz_id)
    print(f"Found quiz: {quiz.title}")  # Debug line
    
    quiz_title = quiz.title  # Store title before deletion
    
    try:
        db.session.delete(quiz)
        db.session.commit()
        print("Quiz deleted and committed")  # Debug line
        
        flash(f'Quiz "{quiz_title}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting quiz. Please try again.', 'error')
    
    return redirect(url_for('admin.dashboard'))

# ALTERNATIVE SOLUTION: Add a specific route for showing messages
@admin.route('/show_success/<message>')
@login_required
def show_success(message):
    if current_user.role != 'admin':
        return redirect(url_for('quiz.quiz_home'))
    
    flash(message, 'success')
    return redirect(url_for('admin.dashboard'))