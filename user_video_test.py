import requests
import os, re
import argparse
import pandas as pd
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]

class DouYin(object):
    def __init__(self):

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        }
        self.user_video_url = r"https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid="
        self.user_info_url = r"https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid="

    def hello(self, share_link):
        # 传入抖音分享链接
        home = requests.get(url=share_link, headers=self.headers)
        # print(home.url)

        sec_uid = home.url.split("?")[0].split("user/")[1]
        # print(sec_uid)

        return sec_uid

    def get_user_info(self, sec_uid):
        # 传入抖音分享链接，获取博主基本信息
        data_dict = {}
        url = self.user_info_url + sec_uid
        # print(url)
        user_info_json = requests.get(url=url, headers=self.headers).json()

        print(user_info_json)

        # 将json数据保存到字典中
        data_dict["uid"] = user_info_json["user_info"]["uid"]
        # data_dict["iid"]=iid
        data_dict["sec_uid"] = sec_uid
        # data_dict["did"]=did
        data_dict["unique_id"] = user_info_json["user_info"]["unique_id"]
        data_dict["nickname"] = user_info_json["user_info"]["nickname"]
        # data_dict["region"] = user_info_json["user_info"]["region"]
        data_dict["custom_verify"] = user_info_json["user_info"]["custom_verify"]
        data_dict["following_count"] = user_info_json["user_info"]["following_count"]
        data_dict["follower_count"] = user_info_json["user_info"]["follower_count"]
        data_dict["total_favorited"] = user_info_json["user_info"]["total_favorited"]
        data_dict["aweme_count"] = user_info_json["user_info"]["aweme_count"]
        data_dict["favoriting_count"] = user_info_json["user_info"]["favoriting_count"]
        data_dict["signature"] = user_info_json["user_info"]["signature"]
        data_dict["is_gov_media_vip"] = user_info_json["user_info"]["is_gov_media_vip"]
        data_dict["avatar_larger"] = user_info_json["user_info"]["avatar_larger"]["url_list"]
        data_dict["avatar_medium"] = user_info_json["user_info"]["avatar_medium"]["url_list"]
        data_dict["avatar_thumb"] = user_info_json["user_info"]["avatar_thumb"]["url_list"]

        # print(data_dict)

        return data_dict

    def get_user_video(self, sec_uid):
        video_list = []
        max_cursor = 0
        signature = ''  # 不要signature都能获取视频json数据
        # requests.get('http://localhost:3000/sign').text #"u1KJbAAA3AlCqWFj3Z0ZXLtSiX" #小透明"5BEIowAAgIQZKuCsQX4LqOCRCL"
        # print(signature)
        has_more = True
        while has_more:
            url = self.user_video_url + sec_uid + "&count=21&max_cursor=" + str(
                max_cursor) + "&aid=1128&_signature=" + signature + "&dytk="
            # print(url)
            user_video_json = requests.get(url=url, headers=self.headers).json()
            # max_cursor = user_video_json["max_cursor"]
            has_more = user_video_json["has_more"]
            # print(max_cursor)

            for i in range(len(user_video_json["aweme_list"])):
                video_dict = {}
                video_dict["aweme_id"] = user_video_json["aweme_list"][i]["aweme_id"]
                video_dict["desc"] = user_video_json["aweme_list"][i]["desc"]
                video_dict["comment_count"] = user_video_json["aweme_list"][i]["statistics"]["comment_count"]
                video_dict["digg_count"] = user_video_json["aweme_list"][i]["statistics"]["digg_count"]
                video_dict["forward_count"] = user_video_json["aweme_list"][i]["statistics"]["forward_count"]
                video_dict["share_count"] = user_video_json["aweme_list"][i]["statistics"]["share_count"]
                video_dict["cover"] = user_video_json["aweme_list"][i]["video"]["cover"]["url_list"]
                video_dict["video"] = user_video_json["aweme_list"][i]["video"]["play_addr"]["url_list"]

                video_list.append(video_dict)
                # print(video_dict)
        # print(len(video_list))
        return video_list

    def download(self, path, data_dict, video_list):
        # 下载大中小三张头像图片，传入路径，并在该路径下创建一个uid+ickname格式的文件夹保存头像和视频
        uid = data_dict["uid"]
        nickname = data_dict["nickname"]
        folder = os.path.join(path, uid+nickname)
        # 创建储存目录
        try:
            os.makedirs(folder, 777)
        except FileExistsError:
            pass
        os.chdir(folder)  # 进入创建的目录
        # 下载头像并保存
        avatar_larger = requests.get(data_dict["avatar_larger"][0], self.headers).content
        with open("avatar_larger.jpeg", "wb") as f:
            f.write(avatar_larger)
            f.close()
        avatar_medium = requests.get(data_dict["avatar_medium"][0], self.headers).content
        with open("avatar_medium.jpeg", "wb") as f:
            f.write(avatar_medium)
            f.close()
        avatar_thumb = requests.get(data_dict["avatar_thumb"][0], self.headers).content
        with open("avatar_thumb.jpeg", "wb") as f:
            f.write(avatar_thumb)
            f.close()
        n = 0
        video_mun = len(video_list)
        for i in video_list:
            video = requests.get(i["video"][0], self.headers).content
            # 检测名字合法性
            video_name = i["aweme_id"] + i["desc"]
            reg = re.compile(r'[\\/:*?"<>|\r\n]+')
            valid_name = reg.findall(video_name)
            if valid_name:
                for nv in valid_name:
                    video_name = video_name.replace(nv, "_")
            n = n + 1
            print("正在下载", n, "/", video_mun)
            with open(video_name + ".mp4", "wb") as f:
                f.write(video)
                f.close()

    def download_video_cover(self, path, data_dict, video_list):
        uid = data_dict["uid"]
        nickname = data_dict["nickname"]
        folder = os.path.join(path, uid + nickname)
        # 创建储存目录
        try:
            os.makedirs(folder, 777)
        except FileExistsError:
            pass
        os.chdir(folder)  # 进入创建的目录
        cover_num = len(video_list)
        n = 0
        for video in video_list:
            video_code = video["aweme_id"]
            cover = requests.get(video["cover"][0], self.headers).content
            n = n + 1
            print("正在下载", n, "/", cover_num)
            with open(f"{video_code}cover.jpeg", "wb") as f:
                f.write(cover)
                f.close()

    def run(self,share_link, download, info, cover):
        # path为文件保存路径必须以/结尾，share_link为分享链接
        sec_uid = self.hello(share_link)
        # print(sec_uid)
        data_dict = self.get_user_info(sec_uid)
        # print(data_dict)
        video_list = self.get_user_video(sec_uid)
        if info:
            # print(video_list[0])
            user_result_excel = pd.DataFrame(data_dict).iloc[0, :]
            video_result_excel = pd.DataFrame(video_list)
            # 写入excel
            user_result_excel.to_excel(os.path.join("user_info", data_dict["nickname"]+"_user_info.xlsx"))
            video_result_excel.to_excel(os.path.join("video_info", data_dict["nickname"]+"_video_info.xlsx"))
        if download:
            self.download("videos", data_dict, video_list)
        if cover:
            self.download_video_cover("covers", data_dict, video_list)

def get_url_list():
    with open("user_url.txt", "r") as f:
        url_list = [line.strip() for line in f if line.startswith("https://www.douyin.com/user/")]
    return url_list

if __name__ == "__main__":
    os.makedirs("user_info", exist_ok=True)
    os.makedirs("video_info", exist_ok=True)
    # 潘姥姥
    # https://www.douyin.com/user/MS4wLjABAAAAJk22pApYXsM0UGSlYmpBXwOnzZfv1I5b3tJun5Og0_MdCI3Ka9zmY2Xkc4BSkDYh
    # user_share_url = r"https://v.douyin.com/eaJtdAb/"
    parser = argparse.ArgumentParser()
    parser.add_argument('--download-video', action='store_true', help='download video')
    parser.add_argument('--save-video-info', action='store_true', help='save video info')
    parser.add_argument('--download-video-cover', action='store_true', help='download video cover')
    args = parser.parse_args()
    download = args.download_video
    info = args.save_video_info
    cover = args.download_video_cover
    douyin = DouYin()
    # path为文件保存路径必须以/结尾，share_link为分享链接
    url_list = get_url_list()
    for url in url_list:
        os.chdir(ROOT)
        douyin.run(url, download, info, cover)