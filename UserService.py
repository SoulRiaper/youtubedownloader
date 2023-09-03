import json

import redis

from ProjectExceptions import *


class UserService:

    def __init__(self, user_cache_store: redis.Redis):
        self.user_cache_store = user_cache_store

    def is_in_download(self, user_id: str) -> bool:
        return self.user_cache_store.get(f"usr:{user_id}") is not None

    def register_user(self, user_id: str, action: str = ""):
        self.user_cache_store.set(f"usr:{user_id}",
                                  json.JSONEncoder().encode({
                                      "action": action,
                                      "url_list": [],

                                  }))

    def update_user(self, user_id: str , user: dict):
        self.user_cache_store.set(f"usr:{user_id}",
                                  json.JSONEncoder().encode(user))

    def get_user(self, user_id):
        return json.JSONDecoder().decode(self.user_cache_store.get(f"usr:{user_id}"))

    def add_url_to_user(self, user_id: str, url: str):
        if self.is_in_download(user_id):
            user = self.get_user(user_id)

            if url not in user["url_list"]:
                user["url_list"].append(url)
                self.update_user(user_id, user)
            else:
                raise UrlAlreadyExcepted
        else:
            raise UserNoneException

    def delete_user_urls(self, user_id: str):
        self.user_cache_store.delete(f"usr:{user_id}")