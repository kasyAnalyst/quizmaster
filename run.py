from app import create_app

app, db, bcrypt = create_app()

if __name__== '__main__':
    app.run(debug=True, use_reloader=True)