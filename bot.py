import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

SITES = [
    {
        "name": "경기도 문화예술의전당",
        "url": "https://www.ggac.or.kr/ggac/M0000121/board/list.do",
        "selector": "td.num"
    },
    {
        "name": "용인문화재단",
        "url": "https://www.yicf.or.kr/cop/bbs/selectBoardList.do?bbsId=notice_main",
        "selector": "tbody tr"  # 표의 첫 번째 줄을 통째로 낚아채는 명령입니다
    }
]

def send_message(text):
    if not TOKEN or not CHAT_ID:
        print("토큰이나 채팅 ID 설정이 누락되었습니다.")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": text}
    requests.get(url, params=params)

def check():
    for site in SITES:
        try:
            # 브라우저인 척 속이기 위해 헤더 추가 (매우 중요!)
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(site["url"], headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            target = soup.select_one(site["selector"])
            
            if target:
                latest = target.get_text().strip()
                file_path = f"{site['name']}.txt"
                
                old_data = ""
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding='utf-8') as f:
                        old_data = f.read().strip()
                
                if old_data != latest:
                    send_message(f"🔔 [신규 공고!] {site['name']}\n내용: {latest}\n바로가기: {site['url']}")
                    with open(file_path, "w", encoding='utf-8') as f:
                        f.write(latest)
                print(f"{site['name']} 확인 완료: {latest}")
            else:
                print(f"{site['name']}에서 데이터를 찾지 못했습니다.")
                
        except Exception as e:
            print(f"{site['name']} 에러 발생: {e}")

if __name__ == "__main__":
    check()
