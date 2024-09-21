import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # Name of the project, typically derived from the APK filename
    package_name = Column(String, nullable=False)  # The package name of the analyzed APK
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp of when the project was created

    # Relationships to other tables
    endpoints = relationship("Endpoint", back_populates="project")  # One-to-many relationship with Endpoint table
    firebase_keys = relationship("FirebaseKey",
                                 back_populates="project")  # One-to-many relationship with FirebaseKey table


class Endpoint(Base):
    __tablename__ = 'endpoints'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))  # Foreign key linking to the Project table
    url = Column(String, nullable=False)  # The URL or endpoint found during analysis
    method = Column(String)  # The HTTP method associated with the endpoint (GET, POST, etc.), if available
    source = Column(String, nullable=False)  # The source of this endpoint (e.g., 'regex' for regex analysis)
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp of when the endpoint was discovered

    # Relationship back to the Project table
    project = relationship("Project", back_populates="endpoints")


class FirebaseKey(Base):
    __tablename__ = 'firebase_keys'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))  # Foreign key linking to the Project table
    key = Column(String, nullable=False)  # The Firebase key found during analysis
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp of when the Firebase key was discovered

    # Relationship back to the Project table
    project = relationship("Project", back_populates="firebase_keys")


# Use an environment variable for the database path, with a default value
db_path = os.environ.get('SQLITE_DB_PATH', 'sqlite:///api_discovery.db')
engine = create_engine(db_path)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def get_db_session():
    """Create and return a new database session."""
    return Session()


def add_project(name, package_name):
    """
    Add a new project to the database.

    :param name: Name of the project
    :param package_name: Package name of the APK
    :return: ID of the newly created project
    """
    session = get_db_session()
    project = Project(name=name, package_name=package_name)
    session.add(project)
    session.commit()
    project_id = project.id
    session.close()
    return project_id


def add_endpoint(project_id, url, method, source):
    """
    Add a new endpoint to the database.

    :param project_id: ID of the associated project
    :param url: URL or endpoint string
    :param method: HTTP method (if known)
    :param source: Source of the endpoint discovery (e.g., 'regex')
    """
    session = get_db_session()
    endpoint = Endpoint(project_id=project_id, url=url, method=method, source=source)
    session.add(endpoint)
    session.commit()
    session.close()


def add_firebase_key(project_id, key):
    """
    Add a new Firebase key to the database.

    :param project_id: ID of the associated project
    :param key: Firebase key string
    """
    session = get_db_session()
    firebase_key = FirebaseKey(project_id=project_id, key=key)
    session.add(firebase_key)
    session.commit()
    session.close()


def get_project_endpoints(project_id):
    """
    Retrieve all endpoints associated with a specific project.

    :param project_id: ID of the project
    :return: List of dictionaries containing endpoint information
    """
    session = get_db_session()
    endpoints = session.query(Endpoint).filter_by(project_id=project_id).all()
    result = [{"url": e.url, "method": e.method, "source": e.source} for e in endpoints]
    session.close()
    return result


def get_project_firebase_keys(project_id):
    """
    Retrieve all Firebase keys associated with a specific project.

    :param project_id: ID of the project
    :return: List of dictionaries containing Firebase key information
    """
    session = get_db_session()
    firebase_keys = session.query(FirebaseKey).filter_by(project_id=project_id).all()
    result = [{"key": k.key} for k in firebase_keys]
    session.close()
    return result
