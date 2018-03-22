# reptile
Crawling Youku
## 爬取优酷视频
- 第一步：获取电视剧每一集的 url
> pychrom_sdudy 用来抓取请求数据，返回请求的 response
- 第二步：获取每一集 url 的下载地址
> youku.py 解析 response，获取每一集的url和下载地址
- 第三步：下载视频
> aria2rpc.py 用来下载视频，需要用到 aria 这个下载工具
- 第四步：拼接视频
> stitching_video.py 拼接视频，用到的工具为 ffmpeg
