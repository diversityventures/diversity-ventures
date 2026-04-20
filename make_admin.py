from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = User.query.filter_by(email="denniskiriaku254@gmail.com").first()
    if admin:
        admin.is_admin = True
        db.session.commit()
        print("Existing user promoted to admin.")
    else:
        admin = User(
            full_name="Admin",
            email="denniskiriaku254@gmail.com",
            password=generate_password_hash("Nancywanjikukiriaku@7020050"),
            is_admin=True,
            is_verified=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin account created successfully.")
