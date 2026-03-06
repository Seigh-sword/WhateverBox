import os

class Keys:
    API_ID = int(os.environ.get("TG_API_ID", 0))
    API_HASH = os.environ.get("TG_API_HASH", "")
    BOX_ID = -1003391436065
    SESSION_STRING = os.environ.get("SESSION_STRING", "")

    @classmethod
    def get_session(cls):
        return cls.SESSION_STRING
