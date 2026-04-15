import argparse
import random
from os import getenv

from dotenv import load_dotenv
from faker import Faker
from sqlalchemy.orm import Session

from auth import gen_pwd_hash
from database import Base, SessionLocal, engine
from enumutils import RolesEnum
from models import Category, Member, User

load_dotenv()
fake = Faker()

DEFAULT_CATEGORIES = ['youth', 'children', 'adult']
DEFAULT_USERS = [
    ('admin@bapt.com', 'password123', RolesEnum.admin),
    ('mod@bapt.com', 'password123', RolesEnum.moderator),
    ('pastor@bapt.com', 'password123', RolesEnum.pastor),
]


def create_tables():
    Base.metadata.create_all(bind=engine)


def seed_categories(db: Session):
    existing = {c.name for c in db.query(Category).filter(Category.name.in_(DEFAULT_CATEGORIES)).all()}
    created = []

    for name in DEFAULT_CATEGORIES:
        if name not in existing:
            category = Category(name=name)
            db.add(category)
            created.append(name)

    if created:
        db.commit()
        print(f'Created categories: {created}')
    else:
        print('Categories already exist, skipping category seeding.')

    return db.query(Category).filter(Category.name.in_(DEFAULT_CATEGORIES)).all()


def seed_users(db: Session):
    created = []
    emails = []

    for email, password, role in DEFAULT_USERS:
        emails.append(email)
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            continue

        user = User(email=email, password=gen_pwd_hash(password), role=role)
        db.add(user)
        created.append(email)

    if created:
        db.commit()
        print(f'Created users: {created}')
    else:
        print('Default users already exist, skipping user seeding.')

    return db.query(User).filter(User.email.in_(emails)).all()


def seed_members(db: Session, categories, count: int = 20, force: bool = False):
    if not force and db.query(Member).count() > 0:
        print('Members already exist, skipping member seeding.')
        return

    if not categories:
        categories = seed_categories(db)

    members = []
    for _ in range(count):
        category = random.choice(categories)
        member = Member(
            fullname=fake.name(),
            email=fake.unique.email(),
            phone_no=fake.random_int(min=1_000_000, max=9_999_999_999),
            category_id=category.id,
        )
        db.add(member)
        members.append(member)

    db.commit()
    print(f'Created {len(members)} members.')


def execute(count: int = 20, force: bool = False):
    create_tables()
    db = SessionLocal()
    try:
        seed_categories(db)
        seed_users(db)
        seed_members(db, categories=None, count=count, force=force)
    finally:
        db.close()

    print('Safe seeding complete.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Seed the database safely without dropping existing data.')
    parser.add_argument('--members', type=int, default=20, help='Number of members to generate')
    parser.add_argument('--force', action='store_true', help='Force seeding members even if members already exist')
    args = parser.parse_args()

    execute(count=args.members, force=args.force)
