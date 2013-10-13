from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import db

class UserPrefs(db.Model):
    tz_offset = db.IntegerProperty(default=0)
    user = db.UserProperty(auto_current_user_add=True)
    def cache_set(self):
        memcache.set(self.key().name(), self, namespace=self.key().kind())
    def put(self):
        self.cache_set()
        db.Model.put(self)

def get_userprefs(user_id=None):
    if not user_id:
        user = users.get_current_user()
        if not user:
            return None
        user_id = user.user_id()
    key = db.Key.from_path('UserPrefs', user_id)
    userprefs = db.get(key)
    if not userprefs:
        userprefs = UserPrefs(key_name=user_id)
    return userprefs
