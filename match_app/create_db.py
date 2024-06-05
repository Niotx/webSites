from app import app, db

# Set up application context
app.app_context().push()

# Create the database tables
db.create_all()

print("Database tables created.")
