import typing
import requests,json,uuid,time,os,colorama

class APIs:
    login_attempt_count: int = 0
    csrftoken: str = None
    headers: dict = None
    session_id: str = None
    cookies:dict = None
    uid:str = None
    def __init__(self,username,password) -> None:
        self.username: str = username
        self.password: str = password
        self.phone_id: str = str(uuid.uuid4())
        self.adid:     str = str(uuid.uuid4())
        self.guid:     str = str(uuid.uuid4())
        self.uuid:     str = str(uuid.uuid4())
        self.device_id = f'android-{uuid.uuid4()}'
        
    def make_headers(self) -> dict:
        headers:dict = {}
        headers['User-Agent'] = 'Instagram 155.0.0.27.107 Android (20/5.6; 320dpi; 1080x1260; HUAWEI; VIVO-Z9QXB; zqjk; mm3693; en_US)'
        headers['Connection'] = 'close'
        security = requests.get('https://i.instagram.com/api/v1/si/fetch_headers/',headers=headers, verify=True)
        headers['csrftoken'] = security.cookies.get_dict()['csrftoken']
        self.csrftoken = security.cookies.get_dict()['csrftoken']
        headers['x-mid'] = security.cookies.get_dict()['mid']
        headers['Accept'] = '*/*'
        headers['X-Ig-Connection-Type'] = 'WIFI'
        headers['X-Ig-Capabilities'] = '3brTvx0='
        headers['X-Fb-Http-Engine'] = 'Liger'
        headers['X-Fb-Client-Ip'] = 'True'
        headers['X-Fb-Server-Cluster'] = 'True'
        headers['Connection'] = 'close'
        return headers
    
    def login(self) -> bool:
        
        data: dict = {
        };self.headers = self.make_headers()
        data['username'] = self.username
        data['enc_password'] = '#PWD_INSTAGRAM:0:{0}:{1}'.format(int(time.time()),self.password)
        data['adid'] = self.adid
        data['guid'] = self.guid
        data['device_id'] = self.device_id
        data['login_attempt_count'] = f'{self.login_attempt_count}';self.login_attempt_count += 1
        data['_csrftoken'] = self.csrftoken
        payload = {}
        payload['signed_body'] = f'SIGNATURE.{json.dumps(data)}'
        login_res = requests.post('https://i.instagram.com/api/v1/accounts/login/', headers=self.headers, data=payload)
        if login_res.text.__contains__('logged_in_user'):
            self.cookies = login_res.cookies.get_dict()
            self.session_id = self.cookies['sessionid']
            return True
        elif login_res.text.__contains__("challenge_required"):  
            challenge_context = login_res.json()['challenge']['challenge_context']  
            challenge_res = requests.get(f"https://i.instagram.com{login_res.json()['challenge']['api_path']}?guid={self.guid}device_id={self.device_id}challenge_context={challenge_context}", headers=self.headers, cookies=login_res.cookies.get_dict(),allow_redirects=True)
            
        else:
            return False
                
    def get_feed_liked(self) -> requests.Response: return requests.get("https://i.instagram.com/api/v1/feed/liked/", cookies=self.cookies, headers=self.headers)

    def unlike(self,id) -> bool:
        data: dict = {}
        data["delivery_class"] = "organic"
        data["media_id"] = f"{id}"
        data["radio_type"] = "wifi-none"
        data["_uid"] = f"{self.uid}"
        data["_uuid"] = f"{self.uuid}"
        data["is_carousel_bumped_post"] = "false"
        data["container_module"] = "video_view_other"
        payload = {}
        payload["signed_body"] = f"SIGNATURE.{json.dumps(data)}"
        payload["d"] = "0"
        unlike_res = requests.post(f"https://i.instagram.com/api/v1/media/{id}/unlike/",cookies=self.cookies,headers=self.headers,data=payload) 
        if '"status":"ok"' in unlike_res.text:
            return True
        else:
            return False

def clear() -> None: os.system('cls') if os.name == 'nt' else os.system('clear')

def banner() -> None:
    clear()
    print(colorama.Fore.RED+'''

██████╗ ███████╗██╗   ██╗██╗██╗     
██╔══██╗██╔════╝██║   ██║██║██║     
██║  ██║█████╗  ██║   ██║██║██║     
██║  ██║██╔══╝  ╚██╗ ██╔╝██║██║     
██████╔╝███████╗ ╚████╔╝ ██║███████╗
╚═════╝ ╚══════╝  ╚═══╝  ╚═╝╚══════╝
                                    
                                [ Unlike-Bot v0.1 ]
'''+colorama.Fore.RESET)


def main() -> typing.Any:
        try:
            os.system('title DEVIL HERE ^| insta @0xdevil')
            banner()
            print('['+colorama.Fore.LIGHTRED_EX+'@'+colorama.Fore.RESET+'] This tool by | insta: 0xdevil\n\n')
            username = input('['+colorama.Fore.MAGENTA+'+'+colorama.Fore.RESET+'] Username: ')
            password = input('['+colorama.Fore.MAGENTA+'+'+colorama.Fore.RESET+'] Password: ')
            API = APIs(username,password)
            if API.login():
                while True:
                    try:
                        feed_liked = API.get_feed_liked()
                        items = feed_liked.json()["items"]
                        for item in items:
                            media_id = item["id"]
                            media_code = item["code"]
                            if(API.unlike(media_id)):
                                print("["+colorama.Fore.GREEN+"+"+colorama.Fore.RESET+f"] Done unlike -> https://www.instagram.com/p/{media_code}/")
                            else:
                                print("["+colorama.Fore.RED+"-"+colorama.Fore.RESET+f"] Error while unlike -> https://www.instagram.com/p/{media_code}/")
                    except Exception:
                        print("["+colorama.Fore.RED+"-"+colorama.Fore.RESET+f"] Error while unlike")
                        exit(0)
            else:
                print("["+colorama.Fore.RED+"-"+colorama.Fore.RESET+f"] Error while Login")
                exit(0)
        except KeyboardInterrupt:
            print('\n['+colorama.Fore.RED+'CTRL+C'+colorama.Fore.RESET+'] \nExit [ KeyboardInterrupt ]')
            print('['+colorama.Fore.MAGENTA+'^'+colorama.Fore.RESET+'] Follow me\ninstagram @0xdevil')
            exit(0) 

if __name__ == '__main__':
    main() 