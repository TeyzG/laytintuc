import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import schedule
from datetime import datetime

danhSachMuc = [
    {"name": "Ngôi sao", "url": "https://kenh14.vn/star.chn"},
    {"name": "Phim", "url": "https://kenh14.vn/cine.chn"},
    {"name": "Ca nhạc", "url": "https://kenh14.vn/musik.chn"},
    {"name": "Thời trang", "url": "https://kenh14.vn/beauty-fashion.chn"},
    {"name": "Đời sống", "url": "https://kenh14.vn/doi-song.chn"},
    {"name": "Kinh tế", "url": "https://kenh14.vn/money-z.chn"},
    {"name": "Ăn chơi", "url": "https://kenh14.vn/an-quay-di.chn"},
    {"name": "Sức khỏe", "url": "https://kenh14.vn/suc-khoe.chn"},
    {"name": "Công nghệ", "url": "https://kenh14.vn/tek-life.chn"},
    {"name": "Học đường", "url": "https://kenh14.vn/hoc-duong.chn"},
    {"name": "Xem Mua Luôn", "url": "https://kenh14.vn/xem-mua-luon.chn"},
    {"name": "Video", "url": "https://video.kenh14.vn/"}
]

def layTin():
    tatCa = []

    for muc in danhSachMuc:
        url_muc = muc["url"]
        ten_muc = muc["name"]

        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': '*/*',
            'Referer': 'https://kenh14.vn/'
        }

        thu = 0
        ok = False

        while thu < 3:
            try:
                r = requests.get(url_muc, headers=headers, timeout=15)
                if r.status_code != 200:
                    raise Exception("Trang lỗi")

                soup = BeautifulSoup(r.text, "html.parser")

                cac_bai = soup.find_all("li", class_=lambda c: c and ("news" in c or "item" in c or "knswli" in c))
                if len(cac_bai) < 4:
                    cac_bai = soup.find_all("div", class_=lambda x: x and "news" in x)

                print(">>>", ten_muc, ":", len(cac_bai), "bài")

                for bai in cac_bai:
                    try:
                        td = bai.find("h3")
                        if td:
                            tieu_de = td.get_text().strip()
                        else:
                            a = bai.find("a")
                            if a:
                                tieu_de = a.get("title", "Không rõ").strip()
                            else:
                                tieu_de = "Không biết tiêu đề"

                        mo_ta = ""
                        mota_tag = bai.find("div", class_=lambda x: x and ("sapo" in x or "desc" in x))
                        if mota_tag:
                            mo_ta = mota_tag.get_text().strip()
                        if len(mo_ta) < 15:
                            a2 = bai.find("a")
                            if a2 and a2.get("title"):
                                mo_ta = a2["title"]

                        link = ""
                        the_a = bai.find("a")
                        if the_a:
                            link = the_a.get("href", "")
                            if not link.startswith("http"):
                                link = "https://kenh14.vn" + link

                        hinh = ""
                        img = bai.find("img")
                        if img and img.has_attr("src"):
                            hinh = img["src"]
                        else:
                            hinh = "Không có hình"

                        tatCa.append({
                            "Mục": ten_muc,
                            "Tiêu đề": tieu_de,
                            "Mô tả": mo_ta,
                            "Link": link,
                            "Hình": hinh
                        })

                    except:
                        pass

                ok = True
                break

            except Exception as loi:
                print(f"Lỗi khi lấy {ten_muc}, lần {thu+1}: {loi}")
                cho = random.randint(5, 10)
                print(f"Đợi {cho} giây...")
                time.sleep(cho)
                thu += 1

        time.sleep(random.randint(2, 4))

    if len(tatCa) > 0:
        df = pd.DataFrame(tatCa)
        ten_file = "["+datetime.now().strftime("%Y%m%d_%H%M") + "] tin_kenh14" + ".xlsx"
        df.to_excel(ten_file, index=False)
        print("Đã lưu file:", ten_file)
    else:
        print("Không có bài nào hết.")

#test thử
layTin()
# Chạy lúc 06:00 mỗi ngày
schedule.every().day.at("06:00").do(layTin)

print("Chương trình sẽ báo kết quả sau 6h sáng mỗi ngày...")

while True:
    schedule.run_pending()
    time.sleep(60)
