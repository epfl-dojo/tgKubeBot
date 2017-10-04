# projet de Kube Bot
# chercher quel last version de KuberNet S sur le web
# import
import urllib.request, json, pprint
import pickle

STATE_FILE = "./k8s.state"

def get_last_ver():
    releases_json = urllib.request.urlopen("https://api.github.com/repos/kubernetes/kubernetes/releases").read()
    releases = json.loads(releases_json.decode())
    for r in sorted(releases, key=lambda r:r["tag_name"], reverse=True):
        if "-" not in r["tag_name"]:
            return r


if __name__ == '__main__':
    try:
        state = pickle.load(STATE_FILE)
    except:
        state = {
            latest : None,
        }
    latest = get_last_ver()
    print("Latest version is : %s" % latest['tag_name'])
    print(latest['body'])
