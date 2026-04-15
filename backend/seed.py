import random
import faker
from database import Base, engine, SessionLocal
from models import User, Member, Category
from enumutils import RolesEnum
from auth import gen_pwd_hash

fake = faker.Faker()


def run():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def seedCategory(db):
    category_tags = ['youth', 'children', 'adult']  # fixed typo: chidren -> children
    categories = []

    for name in category_tags:
        cate = Category(name=name)
        db.add(cate)
        categories.append(cate)

    db.commit()
    return categories       # return so seedMembers can use them


def seedUser(db):
    users = []

    admin = User(
        email='admin@bapt.com',
        password = gen_pwd_hash('password123'),
        role=RolesEnum.admin        
    )
    db.add(admin)
    users.append(admin)

    moderator = User(
        email='mod@bapt.com',
        password = gen_pwd_hash('password123'),
        role=RolesEnum.moderator
    )
    db.add(moderator)
    users.append(moderator)

    pastor = User(
        email='pastor@bapt.com',
        password = gen_pwd_hash('password123'),
        role=RolesEnum.pastor       # fixed: was RolesEnum.admin
    )
    db.add(pastor)
    users.append(pastor)

    db.commit()
    return users


def seedMembers(db, categories: list, count: int = 50):
    #              ↑ receive the seeded category objects
    members_array = []

    for _ in range(count):
        assigned_category = random.choice(categories)  # randomly assign one category

        member = Member(
            fullname=fake.name(),
            email=fake.unique.email(),
            phone_no=fake.random_int(min=1000000, max=9999999999),
            category_id=assigned_category.id    # ← the fix: assign the FK
        )
        db.add(member)
        members_array.append(member)

    db.commit()
    return members_array


def execute():
    run()
    db = SessionLocal()

    try:
        categories = seedCategory(db)   # step 1: seed categories, capture the list
        seedMembers(db, categories)     # step 2: pass list into seedMembers
        seedUser(db)                    # step 3: users last, no dependencies
    finally:
        db.close()

    print('Seeding complete.')


if __name__ == '__main__':
    execute()