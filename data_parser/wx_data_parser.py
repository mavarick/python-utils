#encoding:utf8

import json
import time
import xmltodict
import xml.etree.ElementTree as ET


def parse_wx_data(web_data):
    if len(web_data) == 0:
        return None
    # logging, TODO
    # xmlData = ET.fromstring(web_data)
    wx_json_data = xmltodict.parse(web_data)['xml']
    print(json.dumps(wx_json_data))
    msg_type = wx_json_data.get('MsgType', "")
    if not msg_type:
        return None
    if msg_type == 'text':
        return TextMsg(wx_json_data).processing().reply()
    elif msg_type == 'image':
        return ImageMsg(wx_json_data)


class Msg(object):
    def __init__(self, wx_json_data):
        self.ToUserName = wx_json_data['ToUserName']
        self.FromUserName = wx_json_data['FromUserName']
        self.CreateTime = wx_json_data['CreateTime']
        self.MsgType = wx_json_data['MsgType']
        self.MsgId = wx_json_data['MsgId']


class TextMsg(Msg):
    def __init__(self, wx_json_data):
        Msg.__init__(self, wx_json_data)
        self.Content = wx_json_data['Content'].encode("utf-8")
        self.res_data = {
            "ToUserName": self.FromUserName,
            "FromUserName": self.ToUserName,
            "CreateTime": int(time.time()),
            "Content:": "感谢您的回复！"
        }

    def processing(self):
        self.res_data["Content"] = "收到信息，处理中"
        return self

    def reply(self):
        XmlForm = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{Content}]]></Content>
            </xml>
            """
        return XmlForm.format(**self.res_data)

class ImageMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.PicUrl = xmlData.find('PicUrl').text
        self.MediaId = xmlData.find('MediaId').text

class LinkMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        # TODO


def json_to_xml(json_data):
    xml_data = xmltodict.unparse(json_data)
    return xml_data


