def is_manager(user):
    if not user.client_set.count():
        return False
    return user.client_set.first().type == "manager"


def is_staff(user):
    return user.is_staff()
def is_manager_or_contributor(user):
    return is_contributor(user) or is_manager(user)

def is_reader(user):
    if not user.client_set.count():
        return False
    return user.client_set.first().type =="reader"


def is_contributor(user):
    if not user.client_set.count():
        return False
    return user.client_set.first().type == "contributor"