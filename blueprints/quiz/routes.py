from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
# FIXED: Import db from models, not from app
from models.models import db, Quiz, Question, Result
from flask_login import login_required, current_user
import requests
import random
import json
from datetime import datetime

quiz = Blueprint('quiz', __name__, template_folder='templates')

def get_option_text(question, option_letter):
    """Get the full text for an option letter"""
    if not option_letter:
        return "Not answered"
    
    # Handle API questions (dict) vs DB questions (object)
    if isinstance(question, dict):
        option_map = {
            'a': question.get('option_a', ''),
            'b': question.get('option_b', ''),
            'c': question.get('option_c', ''),
            'd': question.get('option_d', ''),
        }
    else:
        option_map = {
            'a': question.option_a,
            'b': question.option_b,
            'c': question.option_c,
            'd': question.option_d,
        }
    
    return option_map.get(option_letter.lower(), "Unknown option")

@quiz.route('/quiz_home')
def quiz_home():
    return render_template('quiz_home.html')

@quiz.route('/list_quizzes', methods=['GET'])
def list_quizzes():
    quiz_source = request.args.get('quiz_source', 'admin')

    if quiz_source == 'admin':
        quizzes = Quiz.query.all()
    elif quiz_source == 'api':
        try:
            quiz_options = [
                {
                    'id': 'api_quiz_general',
                    'title': 'General Knowledge Quiz',
                    'category': 'Mixed Topics',
                    'description': '10 random questions from all categories'
                },
                {
                    'id': 'api_quiz_science',
                    'title': 'Science & Nature Quiz', 
                    'category': 'Science',
                    'description': '10 science and nature questions'
                },
                {
                    'id': 'api_quiz_history',
                    'title': 'History Quiz',
                    'category': 'History', 
                    'description': '10 historical questions'
                },
                {
                    'id': 'api_quiz_geography',
                    'title': 'Geography Quiz',
                    'category': 'Geography',
                    'description': '10 geography questions'
                },
                {
                    'id': 'api_quiz_sports',
                    'title': 'Sports & Leisure Quiz',
                    'category': 'Sports',
                    'description': '10 sports and leisure questions'
                },
                {
                    'id': 'api_quiz_easy',
                    'title': 'Easy Trivia Quiz',
                    'category': 'Easy Level',
                    'description': '10 easy difficulty questions'
                },
                {
                    'id': 'api_quiz_hard',
                    'title': 'Challenge Quiz',
                    'category': 'Hard Level', 
                    'description': '10 hard difficulty questions'
                }
            ]
            quizzes = quiz_options
        except Exception as e:
            current_app.logger.error(f"Error creating API quiz options: {str(e)}")
            quizzes = []
            flash(f"Error creating API quiz options: {str(e)}", 'danger')

    return render_template('quiz_home.html', quizzes=quizzes, quiz_source=quiz_source)

@quiz.route('/take_quiz/<quiz_id>', methods=['GET', 'POST'])
@login_required
def take_quiz(quiz_id):
    try:
        current_app.logger.info(f"Starting quiz: {quiz_id}, Method: {request.method}")
        quiz_source = request.args.get('source', 'db')
        
        if quiz_source == 'api':
            try:
                current_app.logger.info(f"Processing API quiz: {quiz_id}")
                
                # Map quiz_id to API parameters
                quiz_params_map = {
                    'api_quiz_general': '',
                    'api_quiz_science': '&categories=science',
                    'api_quiz_history': '&categories=history',
                    'api_quiz_geography': '&categories=geography',
                    'api_quiz_sports': '&categories=sport_and_leisure',
                    'api_quiz_easy': '&difficulties=easy',
                    'api_quiz_hard': '&difficulties=hard'
                }
                
                api_params = quiz_params_map.get(quiz_id, '')
                api_url = f"https://the-trivia-api.com/v2/questions?limit=10{api_params}"
                current_app.logger.info(f"API URL: {api_url}")
                
                response = requests.get(api_url, timeout=10)
                current_app.logger.info(f"API Response status: {response.status_code}")
                
                if response.status_code == 200:
                    api_questions = response.json()
                    current_app.logger.info(f"Got {len(api_questions)} questions from API")
                    
                    questions = []
                    for i, q in enumerate(api_questions):
                        try:
                            all_answers = q['incorrectAnswers'] + [q['correctAnswer']]
                            random.shuffle(all_answers)
                            
                            while len(all_answers) < 4:
                                all_answers.append("N/A")
                            
                            formatted_question = {
                                'question_text': q['question']['text'],
                                'option_a': all_answers[0],
                                'option_b': all_answers[1], 
                                'option_c': all_answers[2],
                                'option_d': all_answers[3],
                                'correct_answer': q['correctAnswer'],
                                'category': q.get('category', 'General'),
                                'difficulty': q.get('difficulty', 'medium'),
                                'api_id': q.get('id', f'api_{i}')
                            }
                            
                            # Find which option is correct
                            for option, text in [('a', all_answers[0]), ('b', all_answers[1]), 
                                               ('c', all_answers[2]), ('d', all_answers[3])]:
                                if text == q['correctAnswer']:
                                    formatted_question['correct_option'] = option
                                    break
                            
                            # Ensure correct_option is set
                            if 'correct_option' not in formatted_question:
                                formatted_question['correct_option'] = 'a'
                                formatted_question['option_a'] = q['correctAnswer']
                            
                            questions.append(formatted_question)
                            
                        except Exception as q_error:
                            current_app.logger.error(f"Error processing question {i}: {str(q_error)}")
                            continue
                    
                    quiz_titles = {
                        'api_quiz_general': 'General Knowledge Quiz',
                        'api_quiz_science': 'Science & Nature Quiz',
                        'api_quiz_history': 'History Quiz',
                        'api_quiz_geography': 'Geography Quiz',
                        'api_quiz_sports': 'Sports & Leisure Quiz',
                        'api_quiz_easy': 'Easy Trivia Quiz',
                        'api_quiz_hard': 'Challenge Quiz'
                    }
                    
                    quiz_categories = {
                        'api_quiz_general': 'Mixed Topics',
                        'api_quiz_science': 'Science & Nature',
                        'api_quiz_history': 'History',
                        'api_quiz_geography': 'Geography', 
                        'api_quiz_sports': 'Sports & Leisure',
                        'api_quiz_easy': 'Easy Level',
                        'api_quiz_hard': 'Hard Level'
                    }
                    
                    quiz = {
                        'id': quiz_id,
                        'title': quiz_titles.get(quiz_id, 'Trivia Quiz'),
                        'category': quiz_categories.get(quiz_id, 'Mixed Topics')
                    }
                    
                else:
                    current_app.logger.error(f"API request failed with status: {response.status_code}")
                    flash("Error fetching quiz from API", 'danger')
                    return redirect(url_for('quiz.quiz_home'))
                    
            except requests.RequestException as e:
                current_app.logger.error(f"Request error: {str(e)}")
                flash(f"Error connecting to API: {str(e)}", 'danger')
                return redirect(url_for('quiz.quiz_home'))
            except Exception as e:
                current_app.logger.error(f"API quiz error: {str(e)}")
                flash(f"Error processing API quiz: {str(e)}", 'danger')
                return redirect(url_for('quiz.quiz_home'))
        else:
            try:
                quiz_id_int = int(quiz_id)
                quiz = Quiz.query.get_or_404(quiz_id_int)
                questions = Question.query.filter_by(quiz_id=quiz.id).all()
                current_app.logger.info(f"Loaded DB quiz: {quiz.title} with {len(questions)} questions")
            except ValueError:
                current_app.logger.error(f"Invalid quiz ID: {quiz_id}")
                flash("Invalid quiz ID", 'danger')
                return redirect(url_for('quiz.quiz_home'))

        # Handle form submission
        if request.method == 'POST':
            try:
                current_app.logger.info("Processing quiz submission")
                current_app.logger.info(f"Form keys: {list(request.form.keys())}")
                
                score = 0
                user_answers = []
                
                time_taken = int(request.form.get('time_taken', 0))
                start_time = request.form.get('start_time')
                
                current_app.logger.info(f"Time taken: {time_taken}, Start time: {start_time}")
                
                for i, question in enumerate(questions):
                    user_answer = request.form.get(f'answers_{i + 1}', '')
                    user_answers.append(user_answer)
                    
                    if quiz_source == 'api':
                        correct_option = question.get('correct_option', '')
                    else:
                        correct_option = question.correct_option
                    
                    if user_answer == correct_option:
                        score += 1
                
                current_app.logger.info(f"Calculated score: {score}/{len(questions)}")

                # Store quiz data in session for API quizzes
                if quiz_source == 'api':
                    try:
                        # Clean up old session data first
                        old_keys = [k for k in session.keys() if k.startswith('api_quiz_data_')]
                        for key in old_keys:
                            session.pop(key, None)
                        
                        # Store minimal data in session
                        session[f'api_quiz_data_{current_user.id}'] = {
                            'quiz_title': quiz['title'],
                            'quiz_category': quiz['category'], 
                            'total_questions': len(questions),
                            'quiz_source': quiz_source
                        }
                        
                        # ENHANCED: Store complete question data in the answers JSON
                        enhanced_answers = []
                        for i, question in enumerate(questions):
                            user_answer = user_answers[i] if i < len(user_answers) else ''
                            
                            # Ensure all data is JSON serializable
                            answer_data = {
                                'user_answer': user_answer,
                                'correct_answer': question.get('correct_option', 'a'),
                                'question_text': str(question.get('question_text', f'Question {i+1}')),
                                'options': {
                                    'a': str(question.get('option_a', 'Option A')),
                                    'b': str(question.get('option_b', 'Option B')), 
                                    'c': str(question.get('option_c', 'Option C')),
                                    'd': str(question.get('option_d', 'Option D'))
                                }
                            }
                            enhanced_answers.append(answer_data)
                        
                        # Test JSON serialization before saving
                        user_answers_json = json.dumps(enhanced_answers)
                        current_app.logger.info(f"JSON serialization successful, length: {len(user_answers_json)}")
                        
                        # Parse start_time safely
                        started_at = datetime.now()
                        if start_time:
                            try:
                                started_at = datetime.fromisoformat(start_time)
                            except ValueError:
                                current_app.logger.warning(f"Invalid start_time format: {start_time}")
                        
                        result = Result(
                            user_id=current_user.id,
                            quiz_id=0,  # Use 0 for API quizzes
                            score=score,
                            answers=user_answers_json,
                            time_taken=time_taken,
                            started_at=started_at,
                            completed_at=datetime.now()
                        )
                        
                    except Exception as api_error:
                        current_app.logger.error(f"Error processing API quiz submission: {str(api_error)}")
                        flash('Error processing quiz submission. Please try again.', 'danger')
                        return redirect(url_for('quiz.quiz_home'))
                        
                else:
                    try:
                        # For database quizzes, use simple user_answers
                        user_answers_json = json.dumps(user_answers)
                        
                        # Parse start_time safely
                        started_at = datetime.now()
                        if start_time:
                            try:
                                started_at = datetime.fromisoformat(start_time)
                            except ValueError:
                                current_app.logger.warning(f"Invalid start_time format: {start_time}")
                        
                        result = Result(
                            user_id=current_user.id,
                            quiz_id=quiz.id,
                            score=score,
                            answers=user_answers_json,
                            time_taken=time_taken,
                            started_at=started_at,
                            completed_at=datetime.now()
                        )
                        
                    except Exception as db_error:
                        current_app.logger.error(f"Error processing DB quiz submission: {str(db_error)}")
                        flash('Error processing quiz submission. Please try again.', 'danger')
                        return redirect(url_for('quiz.quiz_home'))
                
                # Save to database
                try:
                    current_app.logger.info("Saving result to database")
                    db.session.add(result)
                    db.session.commit()
                    current_app.logger.info(f"Result saved with ID: {result.id}")
                    
                    flash(f'Quiz submitted successfully! Your score is: {score}', 'success')
                    return redirect(url_for('quiz.quiz_result', result_id=result.id))
                    
                except Exception as save_error:
                    current_app.logger.error(f"Database save error: {str(save_error)}")
                    db.session.rollback()
                    flash('Error saving quiz results. Please try again.', 'danger')
                    return redirect(url_for('quiz.quiz_home'))
                    
            except Exception as submission_error:
                current_app.logger.error(f"Quiz submission error: {str(submission_error)}")
                import traceback
                current_app.logger.error(f"Full traceback: {traceback.format_exc()}")
                db.session.rollback()
                flash('An error occurred while submitting your quiz. Please try again.', 'danger')
                return redirect(url_for('quiz.quiz_home'))

        quiz_duration = 10
        total_questions = len(questions)
        
        return render_template('take_quiz.html', 
                             quiz=quiz, 
                             questions=questions, 
                             quiz_source=quiz_source,
                             quiz_duration=quiz_duration,
                             total_questions=total_questions)
                             
    except Exception as e:
        current_app.logger.error(f"General quiz error: {str(e)}")
        import traceback
        current_app.logger.error(f"Full traceback: {traceback.format_exc()}")
        flash('An error occurred while loading the quiz. Please try again.', 'danger')
        return redirect(url_for('quiz.quiz_home'))

@quiz.route('/quiz_result/<int:result_id>', methods=['GET'])
@login_required
def quiz_result(result_id):
    try:
        result = Result.query.get_or_404(result_id)
        
        # Check if this is an API quiz result
        if result.quiz_id == 0:  # API quiz
            # Get quiz data from session (for quiz info)
            api_quiz_data = session.get(f'api_quiz_data_{current_user.id}')
            
            if api_quiz_data:
                quiz = {
                    'id': 'api_quiz',
                    'title': api_quiz_data['quiz_title'],
                    'category': api_quiz_data['quiz_category']
                }
                quiz_source = api_quiz_data['quiz_source']
            else:
                # Fallback for quiz info only
                quiz = {
                    'id': 'api_quiz',
                    'title': 'API Trivia Quiz',
                    'category': 'Mixed Topics'
                }
                quiz_source = 'api'
            
            # Load answers (which now contain full question data)
            try:
                user_answers = json.loads(result.answers)
            except json.JSONDecodeError:
                current_app.logger.error("Failed to parse quiz answers JSON")
                user_answers = []
            
            # Check if we have enhanced answer format
            if user_answers and isinstance(user_answers[0], dict) and 'question_text' in user_answers[0]:
                # NEW FORMAT: Full question data stored in database
                questions = []
                failed_answers = []
                correct_count = 0
                
                for i, answer_data in enumerate(user_answers):
                    # Reconstruct question object
                    question = {
                        'question_text': answer_data['question_text'],
                        'option_a': answer_data['options']['a'],
                        'option_b': answer_data['options']['b'],
                        'option_c': answer_data['options']['c'],
                        'option_d': answer_data['options']['d'],
                        'correct_option': answer_data['correct_answer']
                    }
                    questions.append(question)
                    
                    user_answer = answer_data['user_answer']
                    correct_answer = answer_data['correct_answer']
                    
                    if user_answer != correct_answer:
                        question_text = answer_data['question_text']
                        user_answer_text = answer_data['options'].get(user_answer, 'Not answered') if user_answer else 'Not answered'
                        correct_answer_text = answer_data['options'].get(correct_answer, 'Unknown')
                        
                        failed_answers.append((
                            question_text,
                            user_answer,
                            user_answer_text,
                            correct_answer,
                            correct_answer_text
                        ))
                    else:
                        correct_count += 1
            else:
                # OLD FORMAT: Fallback to dummy questions
                flash('Question details unavailable. Showing basic score only.', 'warning')
                questions = [{'question_text': f'Question {i+1}'} for i in range(len(user_answers))]
                failed_answers = []
                correct_count = result.score
                
        else:  # Database quiz - existing logic
            quiz = Quiz.query.get(result.quiz_id)
            questions = Question.query.filter_by(quiz_id=quiz.id).all()
            quiz_source = 'db'
            
            # Existing logic for database quizzes
            try:
                user_answers = json.loads(result.answers)
            except json.JSONDecodeError:
                current_app.logger.error("Failed to parse quiz answers JSON")
                user_answers = []
                
            failed_answers = []
            correct_count = 0
            
            for i, question in enumerate(questions):
                user_answer = user_answers[i] if i < len(user_answers) else ''
                correct_answer = question.correct_option

                if user_answer != correct_answer:
                    user_answer_text = get_option_text(question, user_answer)
                    correct_answer_text = get_option_text(question, correct_answer)
                    question_text = question.question_text
                    
                    failed_answers.append((
                        question_text,
                        user_answer,
                        user_answer_text,
                        correct_answer,
                        correct_answer_text
                    ))
                else:
                    correct_count += 1

        # Calculate metrics
        total_questions = len(questions)
        incorrect_count = total_questions - correct_count
        percentage = (result.score / total_questions) * 100 if total_questions > 0 else 0
        
        if hasattr(result, 'time_taken') and result.time_taken:
            minutes = result.time_taken // 60
            seconds = result.time_taken % 60
            time_formatted = f"{minutes}m {seconds}s"
        else:
            time_formatted = "N/A"

        chart_data = {
            'correct': correct_count,
            'incorrect': incorrect_count,
            'percentage': round(percentage, 1),
            'time_taken': time_formatted
        }

        return render_template('quiz_result.html', 
                             quiz=quiz, 
                             questions=questions, 
                             score=result.score, 
                             failed_answers=failed_answers,
                             chart_data=chart_data,
                             total_questions=total_questions,
                             result=result)
                             
    except Exception as e:
        current_app.logger.error(f"Quiz result error: {str(e)}")
        import traceback
        current_app.logger.error(f"Full traceback: {traceback.format_exc()}")
        flash('Error loading quiz results.', 'danger')
        return redirect(url_for('quiz.quiz_home'))
