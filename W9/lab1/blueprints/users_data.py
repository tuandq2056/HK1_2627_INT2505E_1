

USERS_DB = {
    1: {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
    },
    2: {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com",
    },
    3: {
        "first_name": "Bob",
        "last_name": "Johnson",
        "email": "bob.johnson@example.com",
    },
}


def get_user(uid: int):
    """Lấy thông tin người dùng theo uid.
    
    Cung cấp đồng thời cả key mới ('first_name', 'last_name') cho v2
    và key cũ ('f', 'l') cho v1 để đảm bảo tính tương thích ngược.
    """
    user = USERS_DB.get(uid)
    if not user:
        return None

    return {
        **user,
        "f": user.get("first_name", ""),
        "l": user.get("last_name", ""),
    }
