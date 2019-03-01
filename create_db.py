from turnover import app, db
from turnover.models import Role, User

def main():
    """
    This Creates the Database.
    If using for the first time
    run the following command
    'python create_db.py'
    Be sure to properly
    set the Database configurations
    in config.py before running. 
    """
    db.create_all()
    db.session.add(Role(id=0,name='admin'))
    db.session.add(Role(id=1,name='user'))
    db.session.commit()
    print(Role.query.all())
    db.session.add(
        User(
            username='admin',
            password='123456',
            email='user@email.com',
            active=True,
            role_id=0,
        )
    )
    db.session.commit()

if __name__ == '__main__':
    main()
