# private-urls
Hide URLs and see when they are visited.

### Installation instruction
Create the database <- do in docker
```
cd app
from project import db, create_app
db.create_all(app=create_app()) # pass the create_app result so Flask-SQLAlchemy gets the configuration.
```