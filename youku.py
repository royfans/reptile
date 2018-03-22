
import requests
from bs4 import BeautifulSoup
import re
import json
from chapter04.pycharm_sduty import get_body
from chapter04.aria2rpc import rpc_addUri
import time
def send_response(url):

    header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    }
    response = requests.get(url, headers=header)

    return response

# 保存每一集电视剧的 url 到列表中
def save_episodes_list(url):
    # start_url = "http://list.youku.com/show/module?id=310169&tab=showInfo&cname=%E7%94%B5%E8%A7%86%E5%89%A7&callback=jQuery1112035945015645891387_1521182252150&_=1521182252151"
    # res = send_response(url).text
    episodes_list = []
    response = get_body(url)
    if response:
        # 正则提取每一集电视剧的id
        body = response[0]['body']
        all_url_id = re.findall('show\\\\(.*?)\.html\?', body)
        # 列表去重
        all_url_id = set(all_url_id)
        # 判断列表是否为空
        if all_url_id:
            print('every_chapter: ', all_url_id)
            for url in all_url_id:
                episodes_list.append('http://v.youku.com/v_show{}.html\n'.format(url))
                with open('episodes_list.txt', 'a') as el:
                    el.write('http://v.youku.com/v_show{}.html\n'.format(url))
    else:
        print("----------")
        print("获取每一集电视剧的 id 失败！！！")
    return episodes_list

# 获取每一集电视剧的下载列表
def episoder_download(url):
    episoder_download_list = []
    response_body = get_body(url)
    if response_body:
        j = json.loads(response_body[0]['body'][12:-1])
        if '调用成功' in j['ret'][0]:
            flag = False
            stream = j['data']['data']['stream']
            # 清晰度判断
            for i in stream:
                if i['stream_type'] == 'mp4hd2':
                    for seg in i['segs']:
                        episoder_download_list.append(seg['cdn_url'])
                        print('下载列表： ',seg['cdn_url'])
    else:
        print('body is none,retrieving...')
    return episoder_download_list


def _add_aria2_task(url, name):
    """
    :param url:download url
    :param name:dowmload tv name
    :return:
    """
    try:
        result = rpc_addUri(url, {'out': name})
        return result
    except Exception as e:
        print(e)
        return None


def main():
    # teleplay_name_url = input("请输入要下载的电视剧的 url\n(example:http://list.youku.com/show/***):\n")
    # 要下载的电视剧主页 url 格式为 "http://list.youku.com/show/***"
    teleplay_name_url = 'http://list.youku.com/show/id_z19546068702011e69e06.html'
    episodes_list = save_episodes_list(teleplay_name_url)
    print("episodes_url: ",episodes_list)
    print("本电视剧共有{}集".format(len(episodes_list)))
    num = input("请选择要下载的集数(1-{})：\n".format(len(episodes_list)))
    time.sleep(3)
    dl = episodes_list[int(num)-1]
    print("download url:", dl)
    download_list = episoder_download(dl)
    # print(download_list)
    if download_list:
        for i, dl in enumerate(download_list):
            # 添加下载 url 到下载工具中
            # _add_aria2_task(dl, "{0}_{1}.mp4".format(num,i))
            # 把下载的每个单独的视频 name 放到一个文件夹下，以备视频合并时用
            with open('filelist' + str(num) + '.txt' ,'a') as f:
                f.write('file ' + 'D:/Downloads/aria2/' + '{0}_{1}.mp4'.format(num,i) +'\n')
    else:
        main()



if __name__ == "__main__":
    # url_list = get_url('http://list.youku.com/show/id_zefbfbdefbfbdefbfbd1d.html', wait=10)
    # for url in url_list:
    #     # print('url = ', url)
    #     if "list.youku.com/show/module" in url:
    #         save_episodes_list(url)
    # episoder_download('http://v.youku.com/v_show/id_XMzQwMjgyNjQ2MA==.html')
    # save_episodes_list('http://list.youku.com/show/id_zefbfbdefbfbdefbfbd1d.html')
    main()