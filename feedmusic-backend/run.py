from app import create_app, db

app = create_app()

@app.cli.command("init-db")
def init_db():
    """Clear the existing data and create new tables."""
    db.drop_all()
    db.create_all()
    print("Initialized the database.")

@app.cli.command("create-admin")
def create_admin():
    """Create an admin user."""
    from app.models import User
    
    if User.query.filter_by(username='admin').first():
        print("Admin user already exists.")
        return
        
    admin = User(username='admin', role='admin')
    admin.set_password('123456')
    
    db.session.add(admin)
    db.session.commit()
    print("Admin user created successfully.")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
