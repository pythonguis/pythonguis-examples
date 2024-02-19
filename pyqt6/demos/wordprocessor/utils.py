import os
import uuid


def hexuuid():
    return uuid.uuid4().hex


def splitext(p):
    return os.path.splitext(p)[1].lower()
