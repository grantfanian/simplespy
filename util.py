import time
import datetime
import json
import requests
from dictdiffer import diff, patch

# removed crop_photo and photo urls
fields = "photo_id,verified,sex,bdate,city,country,home_town,has_photo,online,domain,has_mobile,contacts,site,education,universities,schools,status,last_seen,followers_count,common_count,occupation,nickname,relatives,relation,personal,connections,exports,activities,interests,music,movies,tv,books,games,about,quotes,can_post,can_see_all_posts,can_see_audio,can_write_private_message,can_send_friend_request,is_favorite,is_hidden_from_feed,timezone,screen_name,maiden_name,is_friend,friend_status,career,military,blacklisted,blacklisted_by_me,can_be_invited_group"


class VkError(Exception):
    pass


class VkSession:
    def __init__(self, version: str, token: str, base:str="https://api.vk.com/method/"):
        self.prop = {"v": version, "access_token": token}
        self.base = base

    def exec(self, method: str, **kwargs):
        kwargs.update(self.prop)
        resp = requests.get(self.base + method, params=kwargs)
        if resp.ok:
            result = resp.json()
            if "response" in result.keys():
                return result["response"]
            else:
                raise VkError(f"  :(  \n{json.dumps(result,indent=1)}")
        else:
            raise ValueError(f"server response: {resp.status_code}")


class Logger:
    def __init__(self, filename="r.json"):
        self.log = {}
        self.filename = filename
        try:
            with open(filename, "rb") as f:
                self.log = json.loads(f.read().decode("utf-8"))
                self.loaded = True
        except FileNotFoundError:
            self.loaded = False

    def rewrite(self, update):
        try:
            with open(self.filename, "rb") as file:
                data = json.loads(file.read().decode("utf-8"))
        except FileNotFoundError:
            data = {}
        data.update(update)
        with open(self.filename, "wb") as file:
            file.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))

    def append(self, last: dict, current: dict):
        if self.loaded:
            result = {}
            for step in self.log.keys():
                # reconstruct last from diffs from the past
                patch(self.log[step], result, in_place=True)
            last = result
            self.loaded = None
        if last != {} and last["online"] == current["online"]:
            # ignore last_seen until online changed
            d = list(diff(last, current, ignore=set(["last_seen"])))
        else:
            d = list(diff(last, current))
        if len(d) > 0:
            now = str(
                datetime.datetime.utcnow() + datetime.timedelta(hours=3)
            )  # force GMT+3
            print(d)
            self.log[now] = d
            self.rewrite(self.log)


class SpyEye:
    def __init__(self, session: VkSession):
        self.last = {}
        self.current = {}
        self.session = session
        self.fields = fields

    def gaze(
        self, user_id, logger: Logger, fields=fields
    ):  # можно и домен и айди вроде
        self.logger = logger
        self.user_id = user_id
        self.fields = fields
        while True:
            self.last = self.current.copy()
            self.current = self.session.exec(
                "users.get", user_id=self.user_id, fields=self.fields
            )[0]
            logger.append(self.last.copy(), self.current.copy())
            time.sleep(20)


if __name__ == "__main__":
    import os

    access_token, uid = os.environ["SIMPLESPY_TOKEN"], os.environ["SIMPLESPY_UID"]
    vk = VkSession("5.89", access_token)
    logger = Logger()
    eye = SpyEye(vk)
    eye.gaze(uid, logger)
