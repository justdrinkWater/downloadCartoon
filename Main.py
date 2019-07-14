from DownloadPage import *

url = "http://www.pufei.net/manhua/20/"
save_path = "F:/dongman"

downloadPage = DownloadPage()
content = downloadPage.get_page_chapter(url, save_path)
