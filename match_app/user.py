from app import app, db, User

# Pushing the application context
with app.app_context():
    # Query to find if the email already exists
    existing_user = User.query.filter_by(email='c@gmail.com').first()

    if existing_user:
        print(f"User with email 'c@gmail.com' already exists: {existing_user}")
    else:
        print("No user with email 'c@gmail.com' found.")
