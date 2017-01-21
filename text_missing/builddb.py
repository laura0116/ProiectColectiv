import datetime
import os
import random
import django


os.environ['DJANGO_SETTINGS_MODULE'] = "text_missing.settings"

django.setup()

from LoginApp.models import Client, UserGroup, Contributor, Manager, GroupType
from TextMissing.models import Document

from django.contrib.auth.models import User
firstNames = ["Emil", "Ion", "Cornel", "Maria", "Vasile", "Bogdan", "Ana", "Laura", "Melisa", "Sergiu", "Ionut", "Dan", "George"]
lastNames = ["Mihalache", "Tomescu", "Miclea", "Ciobanu", "Rusu", "Cosma", "Centea", "Pop", "Popa", "Rus", "Dan",
                 "Pan", "Cornea", "Lazar", "Matei"]
emailStart = ["bla", "abba", "clem", "blllla", "bla2", "bla4"]
emailEnd = ["a", "b", "c", "gmail", "yahoo", "cleeem", "blaa"]
emailFinal = ["ro", "co.uk", "com", "au", "jp"]

def generate_user(user_class):
    nu = user_class()
    nu.first_name = random.choice(firstNames)
    nu.last_name = random.choice(lastNames)
    nu.email = random.choice(emailStart) + "@" + random.choice(emailEnd) + "." + random.choice(emailFinal)
    nu.save()
    nu.user.set_password("parolaparola")
    nu.is_activated = True
    nu.save()
    return nu


def create_group(group_name, user_count=random.choice(range(2, 5))):
    print("Creating group: " + group_name + " with: " + str(user_count) + " users")
    ug = UserGroup(name=group_name)
    ug.leader = generate_user(Manager)
    ug.save()
    ug.users.add(ug.leader)
    for i in range(user_count):
        ug.users.add(generate_user(Contributor))
    return ug

if __name__ == "__main__":
    print("Cleaning db...")
    Client.objects.all().delete()
    Document.objects.all().delete()
    UserGroup.objects.all().delete()
    GroupType.objects.all().delete()

    print("Creating group types...")
    groupTypes = []
    g = GroupType(name="student department")
    g.save()
    g.groups.add(create_group("Mate Info"))
    g.groups.add(create_group("Drept"))
    g.save()
    g = GroupType(name="teaching department")
    g.save()
    g.groups.add(create_group("Mate Info"))
    g.groups.add(create_group("Drept"))
    groupTypes.append(g)
    g = GroupType(name="project")
    g.save()
    g.groups.add(create_group("Project A"))
    g.groups.add(create_group("Project B"))
    g.groups.add(create_group("Project C"))
    groupTypes.append(g)
    g = GroupType(name="doctoral school")
    g.save()
    g.groups.add(create_group("Doctoral school A"))
    g.groups.add(create_group("Doctoral school B"))
    g.groups.add(create_group("Doctoral school C"))
    groupTypes.append(g)
    g = GroupType(name="administrative department")
    g.save()
    g.groups.add(create_group("Department A"))
    g.groups.add(create_group("Department B"))
    g.groups.add(create_group("Department C"))
    groupTypes.append(g)
    g = GroupType(name="grant")
    g.save()
    g.groups.add(create_group("Grant A"))
    g.groups.add(create_group("Grant B"))
    g.groups.add(create_group("Grant C"))
    groupTypes.append(g)
    g = GroupType(name="councils")
    g.save()
    g.groups.add(create_group("DFC"))
    g.groups.add(create_group("CMCS"))
    groupTypes.append(g)
    g = GroupType(name="rector")
    g.save()
    g.groups.add(create_group("rector"))
    g = GroupType(name="dean")
    g.save()
    g.groups.add(create_group("dean", 1))
    groupTypes.append(g)





