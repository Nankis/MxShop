# -*- coding: utf-8 -*-
__author__ = 'Ginseng'
import requests
import json


class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):  # 发送短信
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": '【龙仁深测试】您的验证码是{code}。如非本人操作，请忽略本短信'.format(code=code)
        }

        response = requests.post(self.single_send_url, data=parmas)  # 向云片网发送验证请求
        re_dict = json.loads(response.text)  # 发送之后会返回json,  将其反序列成dict 可以查看请求状态码
        return re_dict

# if __name__ == "__main__":
#     yun_pian = YunPian("")
#     yun_pian.send_sms("7777", "")
