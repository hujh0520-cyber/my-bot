import requests
from bs4 import BeautifulSoup
import os

# 텔레그램 설정 (나중에 깃허브 설정에서 넣을 거예요)
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# 감시할 사이트 정보
SITES = [
    {
        "name": "경기도 문화예술의전당",
        "url": "https://www.ggac.or.kr/ggac/M0000121/board/list.do",
        "selector": "td.num" # 게시판 번호 위치
    },
    {
        "name": "용인문화재단",
        "url": "https://www.yicf.or.kr/cop/bbs/selectBoardList.do?bbsId=notice_main",
        "selector": "td.subject a" # 게시판 제목 위치
    }
]

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": text}
    requests.get(url, params=params)

def check():
    for site in SITES:
        try:
            res = requests.get(site["url"])
            soup = BeautifulSoup(res.text, 'html.parser')
            # 가장 최신글의 내용을 가져옴
            latest = soup.select_one(site["selector"]).text.strip()
            
            # 이전 데이터와 비교 (파일 저장 방식)
            file_path = f"{site['name']}.txt"
            old_data = ""
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    old_data = f.read().strip()
            
            if old_data != latest:
                send_message(f"🔔 [신규 공고!] {site['name']}\n내용: {latest}\n바로가기: {site['url']}")
                with open(file_path, "w") as f:
                    f.write(latest)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    check()
