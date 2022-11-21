from flask import Flask, url_for, render_template
import flask
import json
import datetime
from jinja2 import Environment, FileSystemLoader

app = Flask("vkspy")


def timefromutc(ls, tz=3):  # would be great to remove this
    if type(ls) == int:
        return str(
            datetime.datetime.utcfromtimestamp(ls) + datetime.timedelta(hours=tz)
        )

    ls.update(
        {
            "time": str(
                datetime.datetime.utcfromtimestamp(ls["time"])
                + datetime.timedelta(hours=tz)
            )
        }
    )
    return ls


app.jinja_env.globals.update(timefromutc=timefromutc)


@app.route("/")
def hello_world():
    with open("r.json", "rb") as file:
        j = file.read().decode("utf-8")
    d = json.loads(j)
    cont = render_template(
        "index.html", events=d, signs={"add": "+", "remove": "-", "change": "/"}
    )
    return cont


@app.route("/robots.txt")
def robots():
    return flask.Response(
        """User-agent: *
Disallow: /""".encode(
            "ascii"
        ),
        mimetype="text/plain",
    )
