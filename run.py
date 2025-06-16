from app import create_app

# Create the app instance - Vercel will find this
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
