import pychrome
import time

# 所有请求的 url 列表
# url_list = []
# 请求的 body
response_body = []
# 筛选需要的url,filter_url[0] 为获取全部电视剧集数的url,filter[1]位获取每一集电视剧的下载url
filter_url = ['list.youku.com/show/module', 'acs.youku.com/h5']


class GetBody(object):


    def __init__(self, url):
        self.browser = pychrome.Browser(url="http://127.0.0.1:9222")
        self.tab = self.browser.new_tab()
        self.url = url

    def request_will_be_sent(self, **kwargs):
        loading_url = kwargs.get('request').get('url')
        # print("loading: %s" % loading_url)
        # print("loading_id: %s" % kwargs.get('requestId'))
        for i in filter_url:
            if i in loading_url:
                print(loading_url)
                requestId = kwargs.get('requestId')
                print(requestId)
                # time.sleep(5)
                try:
                    time.sleep(4)
                    body = self.tab.Network.getResponseBody(requestId=requestId)
                    print('body = ', body)
                    print(type(body))
                except:
                    print("第一次获取body失败，正在重新请求...")
                    time.sleep(4)
                    body = self.tab.Network.getResponseBody(requestId=requestId)
                    print('body = ', body)
                    # tab.Page.reload()
                    # request_will_be_sent()
                finally:
                    del response_body[:]
                    response_body.append(body)

    def start_url(self):
        # start the tab
        self.tab.Network.requestWillBeSent = self.request_will_be_sent

        self.tab.start()

        # call method
        self.tab.Network.enable()
        # call method with timeout
        self.tab.Page.navigate(url=self.url, _timeout=8)

        # wait for loading
        self.tab.wait(8)

        # stop the tab (stop handle events and stop recv message from chrome)
        self.tab.stop()

        # close tab
        self.browser.close_tab(self.tab)

def get_body(url):
     g = GetBody(url)
     g.start_url()
     return response_body

if __name__ == "__main__":
    # m = get_url("http://v.youku.com/v_show/id_XMzQwMjgyNjQ2MA==.html", wait=10)
    # if m is None:
    #     m
    # else:
    # m = main()
    # print(m)