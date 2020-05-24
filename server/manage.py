import os
from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app import models

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)

@manager.command
def create_db():
    os.system('createdb flask_api')
    os.system('createdb test_db')
    print('Databases created')

@manager.command
def drop_db():
    os.system(
        'psql -c "DROP DATABASE IF EXISTS test_db"')
    os.system(
        'psql -c "DROP DATABASE IF EXISTS flask_api"')
    print('Databases dropped')

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()