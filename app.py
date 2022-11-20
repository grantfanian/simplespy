from flask import Flask
import flask
import json
import datetime
app = Flask("vkspy")

template = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><code>{}</code></body></html>'


def reparse(contents: dict):
    d = contents
    #print(d)
    out = []  # output lines array
    a = (lambda a, b=None: out.append(
        (f'<font color="{b}">' if b else '')+'&nbsp;'*l+str(a)+(f'</font>' if b else '')))
    l = 0
    a('<ul class="tree">')
    for i in enumerate(d.keys()):
        l = 0
        a(f"<li><details><summary>")
        a("."+i[1]+"\\n", "brown")
        a("</summary><ul>")

        for ii in d[i[1]]:
            l = 2
            sign = [["-", "/"][ii[0] == "change"], "+"][ii[0] == "add"]
            color = {"-": "red", "+": "green", "/": "blue"}
            if True:
                l = 2
                if len(ii[2]) > 1:
                    a(f"/{sign*2}\\n", color[sign])
                    l += 1
                for iii in ii[2]:
                    if sign in "+-":
                        name = iii[0]
                        val = iii[1]
                    else:
                        name = ii[1]
                        val = ii[2]
                    if name == "last_seen.time":
                        val = [str(datetime.datetime.utcfromtimestamp(
                            _)+datetime.timedelta(hours=3)) for _ in val]
                        
                    a("<li>")
                    a(f"{sign*2} "+str('"'+'": "'.join(map(str, (name,val)))) +
                      '" '+(f"{''}"), color[sign])
                if sign=="/":
                    out.pop(-1)
                    if len(ii[2]) > 2:
                        a(f"{sign*2}/\\n", color[sign])
        a("</ul></details></li>")
    l = 0
    a("</ul>}")
    return "\n".join(out)
# the whole thing is kind of wrong
# and generates HTML with errors


@app.route("/")
def hello_world():
    with open("r.json", "rb") as file:
        j = file.read().decode("utf-8")
    d = json.loads(j)
    cont = template.format(reparse(d).replace("\\n", "<br>    "))
    return cont
    


@app.route("/robots.txt")
def robots():
    return flask.Response("""User-agent: *
Disallow: /""".encode("ascii"), mimetype='text/plain')
    return 
