from database import SessionLocal, engine, Base

from auth.models import (
    User,
    Role,
    Permission
)


# =========================================================
# SEED DATABASE
# =========================================================

def seed_database():

    db = SessionLocal()

    # -----------------------------------------------------
    # CREATE PERMISSIONS
    # -----------------------------------------------------

    permission_names = [
        "read_own",
        "read_all",
        "create",
        "update",
        "delete",
        "manage_admin"
    ]

    permissions = {}

    for permission_name in permission_names:

        permission = db.query(Permission).filter(
            Permission.name == permission_name
        ).first()

        if permission is None:

            permission = Permission(
                name=permission_name
            )

            db.add(permission)

            db.flush()

        permissions[permission_name] = permission

    # -----------------------------------------------------
    # CREATE SUPER ADMIN ROLE
    # -----------------------------------------------------

    super_admin = db.query(Role).filter(
        Role.name == "super_admin"
    ).first()

    if super_admin is None:

        super_admin = Role(
            name="super_admin"
        )

        db.add(super_admin)

    # -----------------------------------------------------
    # CREATE ADMIN ROLE
    # -----------------------------------------------------

    admin = db.query(Role).filter(
        Role.name == "admin"
    ).first()

    if admin is None:

        admin = Role(
            name="admin"
        )

        db.add(admin)

    # -----------------------------------------------------
    # CREATE STUDENT ROLE
    # -----------------------------------------------------

    student = db.query(Role).filter(
        Role.name == "student"
    ).first()

    if student is None:

        student = Role(
            name="student"
        )

        db.add(student)

    db.flush()

    # -----------------------------------------------------
    # SUPER ADMIN PERMISSIONS
    # -----------------------------------------------------

    super_admin.permissions = list(
        permissions.values()
    )

    # -----------------------------------------------------
    # ADMIN PERMISSIONS
    # -----------------------------------------------------

    admin.permissions = [

        permissions["read_own"],

        permissions["read_all"],

        permissions["create"],

        permissions["update"],

        permissions["delete"]
    ]

    # -----------------------------------------------------
    # STUDENT PERMISSIONS
    # -----------------------------------------------------

    student.permissions = [

        permissions["read_own"]
    ]

    db.commit()

    db.close()


# =========================================================
# RUN FILE
# =========================================================

if __name__ == "__main__":

    Base.metadata.create_all(
        bind=engine
    )

    seed_database()

    print(
        "Roles and permissions created successfully."
    )