import requests, json, time
from django.utils.text import slugify

OUTPUT_FOLDER = "/Users/benja/code/Videos/"

secrets = 0

with open('secret.json') as json_file:
    secrets = json.load(json_file)
    

p = {"limit":"4"}

user_agent = "lsf-scraper/0.1 by /u/lsf-bot"

### reddit AUTH
client_auth = requests.auth.HTTPBasicAuth(secrets.get("app-id"), secrets.get("reddit-secret"))
post_data = {"grant_type": "password", "username": secrets.get("reddit-user"), "password": secrets.get("reddit-passw")}
headers = {"User-Agent": user_agent}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
token = response.json().get("access_token")


headers = {"Authorization": "bearer " + token, "User-Agent": user_agent}

lsf_req = requests.get("https://reddit.com/r/livestreamfail/new.json",headers=headers, params=p)

response = lsf_req.json()


children = response.get("data").get("children")

# print(json.dumps(children,indent=4))

class Clip:
    def __init__(self, url, title, file_path, download_url):
        self.url = url
        self.title = title
        self.file_path = file_path
        self.download_url = download_url



for post in children:
    post_data = post.get("data")
    title = post_data.get("title")
    post_url = post_data.get("url")
    
    if not "clip" in post_url: 
        print("VOD Detected!: "+ post_url)
        continue


    print("Working on: "+title+"\nURL:     "+post_url)

    download = requests.post("https://clipr.xyz/api/grabclip", data={"clip_url":post_url})
    download_url = "http:"+ download.json().get("download_url")
    print("DL:      "+download_url)
    
    title.replace('"',"")

    clip_request = requests.get(download_url)
    path = OUTPUT_FOLDER+slugify(title)+".mp4"
    print("File Path:   "+path)
    open(path, 'wb').write(clip_request.content)


    





