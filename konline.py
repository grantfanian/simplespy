from time import sleep
from util import VkSession


def online(session:VkSession):
    try:
        session.exec("account.setOnline")
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(e)
        sleep(30)
        online(session)


if __name__ == "__main__":
    import os
    token=os.environ["KONLINE_TOKEN"]
    session = VkSession("5.95", token)
    while True:
        online(session)
        sleep(290)
