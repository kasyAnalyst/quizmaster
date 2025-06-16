# 🧠 QuizMaster - Role-Based Quiz Management Platform

<div align="center">
  
  **Interactive Quiz System with Admin Controls & User Management**
  
  [![Live Demo](https://img.shields.io/badge/🌐%20Live%20Demo-Visit%20Site-blue?style=for-the-badge)](https://quizmaster-kasy.vercel.app/)
  [![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/kasyAnalyst/quizmaster/)
  
</div>

---

## 📖 About The Project

QuizMaster is a comprehensive, full-stack quiz management platform that provides role-based access control for both administrators and users. Built with Flask and modern web technologies, it offers a complete solution for creating, managing, and taking interactive quizzes with real-time analytics and secure user authentication.

### ✨ Key Features

#### 👨‍💼 Admin Capabilities
- **Quiz Management** - Create, edit, and delete custom quizzes
- **Question Builder** - Add multiple-choice questions with detailed answers
- **User Management** - View and manage user accounts and permissions
- **Analytics Dashboard** - Comprehensive statistics and user performance metrics
- **Content Control** - Full CRUD operations on quiz content

#### 👤 User Experience
- **Interactive Quizzing** - Take admin-created and API-powered quizzes
- **Real-time Scoring** - Instant feedback and performance tracking
- **Progress Analytics** - Personal dashboard with detailed results and charts
- **Multiple Categories** - Science, History, Geography, Sports, General Knowledge
- **Difficulty Levels** - Easy, Medium, and Hard quiz options

#### 🔐 Security & Authentication
- **Role-Based Access Control (RBAC)** - Distinct Admin and User permissions
- **Secure Authentication** - Password hashing with bcrypt
- **Session Management** - Flask-Login integration with timeout protection
- **CSRF Protection** - WTF-Forms security on all form submissions
- **Browser Security** - Back-button protection and cache control
- **Password Recovery** - Secure email-based password reset system

#### 🌐 Technical Features
- **API Integration** - External trivia questions from The Trivia API
- **Real-time Charts** - Interactive data visualization with Chart.js
- **Responsive Design** - Mobile-first approach with Tailwind CSS
- **Smooth Animations** - Modern UI with CSS transitions and micro-interactions
- **Session Persistence** - Reliable data storage and retrieval

---

## 🛠️ Built With

### Backend Technologies
- ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) **Python 3.8+** - Core programming language
- ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) **Flask** - Lightweight web framework
- ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat&logo=sqlalchemy&logoColor=white) **SQLAlchemy** - Database ORM and management
- ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white) **SQLite** - Embedded database system
- ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white) **Neon PostgreSQL** - Cloud-native serverless PostgreSQL database

### Frontend Technologies
- ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) **HTML5** - Semantic markup structure
- ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white) **CSS3** - Modern styling and animations
- ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) **JavaScript (ES6+)** - Interactive functionality
- ![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white) **Tailwind CSS** - Utility-first CSS framework
- ![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=flat&logo=chart.js&logoColor=white) **Chart.js** - Data visualization and analytics

### Libraries & Extensions
- **Flask-Login** - User session management and authentication
- **Flask-WTF** - Form handling, validation, and CSRF protection
- **Flask-Mail** - Email functionality for password reset
- **Flask-Bcrypt** - Password hashing and security
- **WTForms** - Form validation and rendering
- **Requests** - HTTP library for external API integration
- **Jinja2** - Template engine for dynamic content

### Deployment & Tools
- ![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat&logo=vercel&logoColor=white) **Vercel** - Cloud hosting platform
- ![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white) **Git** - Version control system
- ![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white) **GitHub** - Repository hosting and collaboration

---

## 🚀 Live Demo

**🌐 [Visit QuizMaster Live](https://quizmaster-kasy.vercel.app/)**

### Demo Credentials
```
Admin Access:
Email: admin@quizmaster.com
Password: admin123

User Access:  
Email: user@quizmaster.com
Password: user123
```

---

## 🏗️ Project Architecture

```
QuizMaster/
├── 📁 blueprints/           # Modular application components
│   ├── 📁 auth/            # Authentication and user management
│   ├── 📁 admin/           # Admin dashboard and controls
│   └── 📁 quiz/            # Quiz functionality and routes
├── 📁 models/              # Database models and schema
│   └── 📄 models.py        # User, Quiz, Question, Result models
├── 📁 static/              # Static assets
│   ├── 📁 css/            # Custom stylesheets
│   ├── 📁 js/             # JavaScript functionality
│   └── 📁 img/            # Images and icons
├── 📁 templates/           # Jinja2 HTML templates
│   ├── 📄 base.html       # Base template with navigation
│   ├── 📄 home.html       # Landing page
│   ├── 📄 login.html      # Authentication forms
│   ├── 📄 quiz_home.html  # Quiz selection interface
│   ├── 📄 take_quiz.html  # Interactive quiz interface
│   └── 📄 quiz_result.html # Results and analytics
├── 📄 app.py              # Main application factory
├── 📄 requirements.txt    # Python dependencies
├── 📄 vercel.json         # Deployment configuration
└── 📄 README.md           # Project documentation
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git for version control

### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/kasyAnalyst/quizmaster.git
   cd quizmaster
   ```

2. **Create Virtual Environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   # Create .env file
   touch .env
   
   # Add configuration variables
   echo "SECRET_KEY=your-secret-key-here or python -c 'import secrets; print(secrets.token_hex(32))'" >> .env
   echo "DATABASE_URL=sqlite:///online_quiz.db" >> .env
   echo "FLASK_ENV=development" >> .env
   ```

5. **Initialize Database**
   ```bash
   python app.py
   # Database will be created automatically on first run
   ```

6. **Run Application**
   ```bash
   # Using Flask CLI
   flask run
   
   # Or directly with Python
   python app.py
   ```

7. **Access Application**
   ```
   Open browser to: http://localhost:5000
   ```

---

## 🎮 Usage Guide

### For New Users
1. **Registration** - Create an account with username, email, and password
2. **Role Selection** - Choose between User or Admin role during registration
3. **Email Verification** - Complete account setup (if email is configured)
4. **Profile Management** - Update personal information and preferences

### For Users
1. **Browse Quizzes** - Explore available quizzes by category and difficulty
2. **Take Quizzes** - Answer questions with timer and real-time feedback
3. **View Results** - Analyze performance with detailed charts and statistics
4. **Track Progress** - Monitor improvement over time with historical data
5. **Review Answers** - Learn from mistakes with comprehensive explanations

### For Admins
1. **Dashboard Access** - Overview of platform statistics and user activity
2. **Quiz Creation** - Build custom quizzes with multiple-choice questions
3. **Content Management** - Edit, update, or delete existing quizzes
4. **User Management** - View user accounts, activity, and performance metrics
5. **Analytics Review** - Access comprehensive reports and data insights

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Flask secret key for sessions | None | Yes |
| `DATABASE_URL` | Database connection string | `sqlite:///online_quiz.db` | No |
| `FLASK_ENV` | Flask environment mode | `development` | No |
| `MAIL_SERVER` | SMTP server for emails | `smtp.gmail.com` | No |
| `MAIL_PORT` | SMTP port number | `587` | No |
| `MAIL_USERNAME` | Email account username | None | No |
| `MAIL_PASSWORD` | Email account password | None | No |

### API Integration

The application integrates with [The Trivia API](https://the-trivia-api.com/) for dynamic content:

- **Endpoint**: `https://the-trivia-api.com/v2/questions`
- **Categories**: Science, History, Geography, Sports, Entertainment, General Knowledge
- **Difficulties**: Easy, Medium, Hard
- **Question Types**: Multiple choice with 4 options
- **Rate Limiting**: No authentication required, free tier available

---

## 📊 Database Schema

### Core Models

**User Model**
- `id` (Primary Key)
- `username` (Unique, String)
- `email` (Unique, String)
- `password` (Hashed, String)
- `role` (Enum: 'user', 'admin')
- `created_at` (Timestamp)

**Quiz Model**
- `id` (Primary Key)
- `title` (String)
- `category` (String)
- `description` (Text)
- `created_by` (Foreign Key → User)
- `created_at` (Timestamp)

**Question Model**
- `id` (Primary Key)
- `quiz_id` (Foreign Key → Quiz)
- `question_text` (Text)
- `option_a` (String)
- `option_b` (String)
- `option_c` (String)
- `option_d` (String)
- `correct_option` (Enum: 'a', 'b', 'c', 'd')

**Result Model**
- `id` (Primary Key)
- `user_id` (Foreign Key → User)
- `quiz_id` (Foreign Key → Quiz)
- `score` (Integer)
- `answers` (JSON)
- `time_taken` (Integer, seconds)
- `completed_at` (Timestamp)

---

## 🔐 Security Features

### Authentication & Authorization
- **Password Hashing** - Bcrypt with salt for secure password storage
- **Session Management** - Flask-Login with configurable timeout
- **Role-Based Access** - Granular permissions for Admin and User roles
- **CSRF Protection** - Token-based protection on all forms

### Data Protection
- **Input Validation** - Comprehensive server-side validation with WTForms
- **SQL Injection Prevention** - SQLAlchemy ORM with parameterized queries
- **XSS Protection** - Automatic output escaping with Jinja2
- **Secure Headers** - Cache control and security headers

### Session Security
- **HTTP-Only Cookies** - Prevent JavaScript access to session cookies
- **Secure Transmission** - HTTPS enforcement in production
- **Session Expiration** - Automatic logout after inactivity
- **Browser Protection** - Back-button prevention after logout

---

## 🚀 Deployment

### Vercel Deployment (Recommended)

1. **Prepare Configuration**
   ```json
   // vercel.json
   {
     "version": 2,
     "builds": [{"src": "app.py", "use": "@vercel/python"}],
     "routes": [{"src": "/(.*)", "dest": "app.py"}]
   }
   ```

2. **Deploy via GitHub**
   - Connect repository to Vercel
   - Configure environment variables
   - Deploy with automatic builds

3. **Environment Setup**
   - Add production environment variables
   - Configure email settings (if using)
   - Set security configurations

### Alternative Deployment Options
- **Heroku** - Traditional PaaS with database add-ons
- **Railway** - Modern platform with automatic deployments
- **PythonAnywhere** - Python-focused hosting service
- **Digital Ocean** - VPS with manual configuration

---

## 🤝 Contributing

Contributions are welcome and appreciated! Here's how to get involved:

### Development Workflow
1. **Fork the Repository** - Create your own copy of the project
2. **Create Feature Branch** - `git checkout -b feature/AmazingFeature`
3. **Make Changes** - Implement your feature or bug fix
4. **Write Tests** - Ensure your changes are properly tested
5. **Commit Changes** - `git commit -m 'Add some AmazingFeature'`
6. **Push to Branch** - `git push origin feature/AmazingFeature`
7. **Open Pull Request** - Submit your changes for review

### Development Guidelines
- Follow PEP 8 style guidelines for Python code
- Write clear, descriptive commit messages
- Add documentation for new features
- Ensure backward compatibility when possible
- Test thoroughly before submitting

### Code Standards
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and modular
- Handle errors gracefully with proper logging

---

## 🐛 Known Issues & Roadmap

### Current Limitations
- Email functionality requires SMTP configuration
- SQLite database suitable for development/small deployments
- Session storage in server memory (not distributed)

### Planned Enhancements
- [ ] **Advanced Analytics** - Machine learning insights and recommendations
- [ ] **Multiplayer Quizzes** - Real-time competitive quiz sessions
- [ ] **Mobile Application** - Native iOS and Android apps
- [ ] **Advanced Question Types** - True/false, fill-in-the-blank, matching
- [ ] **Quiz Import/Export** - JSON/CSV format support
- [ ] **Social Features** - User profiles, leaderboards, achievements
- [ ] **API Documentation** - REST API for third-party integrations
- [ ] **Performance Optimization** - Caching and database optimization
- [ ] **Internationalization** - Multi-language support
- [ ] **Theme Customization** - User-selectable UI themes

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Educational Practice Project License

Copyright (c) 2025 Prosper .N. Collins

This project is developed for educational and learning purposes. You are free to:
- Use this code for learning and reference
- Modify and adapt it for your own educational projects
- Share it with others for educational purposes
- Use it as a foundation for your own applications

This software is provided "as is" for educational purposes. While you're welcome 
to use and learn from this code, please note that it's a practice project and 
may not be suitable for production use without further development and testing.

## Acknowledgments
- Built as a learning project to demonstrate Flask web development
- Uses The Trivia API for educational quiz content
- Deployed on Vercel with Neon PostgreSQL for learning cloud deployment

Happy coding and learning! 🚀

---

## 👨‍💻 Author

**[Your Name]**
- 🌐 Portfolio: [myportfolio.com](https://github.com/kasyAnalyst/portfolio)
- 💼 LinkedIn: [linkedin.com/in/prosper-n-collins](https://www.linkedin.com/in/prosper-n-collins-919b9a191/)
- 🐙 GitHub: [@kasyanalyst](https://github.com/kasyAnalyst)
- 📧 Email: kasyAnalyst@gmail.com

---

## 🙏 Acknowledgments

- **[The Trivia API](https://the-trivia-api.com/)** - Providing comprehensive trivia questions
- **[Flask Community](https://flask.palletsprojects.com/)** - Excellent documentation and framework
- **[Tailwind CSS](https://tailwindcss.com/)** - Beautiful utility-first CSS framework
- **[Chart.js](https://chartjs.org/)** - Powerful data visualization library
- **[Vercel](https://vercel.com/)** - Seamless deployment platform
- **[SQLAlchemy](https://sqlalchemy.org/)** - Robust Python SQL toolkit

---

<div align="center">
  
  **⭐ Star this repository if you found it helpful! ⭐**
  
  Made with ❤️ and ☕ by [Prosper .N. Collins](https://github.com/kasyAnalyst)
  
  *Building the future of interactive learning, one quiz at a time.*
  
</div>
