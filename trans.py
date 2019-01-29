#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import json
import getopt
import random
import urllib
import hashlib
import requests
import logging


sw_addr = os.environ['HOME'] + "/.trans"
config_addr = sw_addr + "/config.json"
log_addr = sw_addr + "/trans.log"

if not os.path.exists(sw_addr):
    os.mkdir(sw_addr)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

logger2f = logging.getLogger("logger2f")
logger2f.setLevel(logging.INFO)
handler = logging.FileHandler(log_addr)
handler.setLevel(logging.INFO)
formatter2f = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter2f)
logger2f.addHandler(handler)

lan_supported = [
"zh", "ja", "en", "ko", "fr", "ar", "pl", "da", "de", "ru", "fi",
"nl", "cs", "ro", "no", "pt", "sv", "es", "hi", "id", 
"it", "th", "tr", "el", "hu", "auto"
]

lan_supported_arg =  [
"zh-CHS", "ja", "EN", "ko", "fr", "ar", "pl", "da", "de", "ru", "fi",
"nl", "cs", "ro", "no", "pt", "sv", "es", "hi", "id", 
"it", "th", "tr", "el", "hu", "auto"
]


err_msg_en = {
101: 'necessary parameters are missing',
102: 'language type not supported',
103: 'too long to translate',
104: 'API type not supported',
105: 'signature type not supported',
106: 'response type not supported',
107: 'encryption type of transmission not supported',
108: 'invalid appkey',
109: 'incorret format of batchLog',
201: 'failed in decryption',
202: 'failed in checking signature',
301: 'failed in querying dictionary',
302: 'failed in querying small language',
303: 'other errors on server',
401: 'account is in debt'
}

err_msg_ch = {
101: '缺少必填的参数',
102: '不支持的语言类型',
103: '翻译文本过长',
104: '不支持的API类型',
105: '不支持的签名类型',
106: '不支持的响应类型',
107: '不支持的传输加密类型',
108: 'appKey无效',
109: 'batchLog格式不正确',
201: '解密失败',
202: '签名检验失败',
301: '辞典查询失败',
302: '小语种查询失败',
303: '服务端的其他异常',
401: '账户已经欠费'
}

config_options = [
    "default_src",  # 默认源语言
    "default_tar",  # 默认目标语言
    "appkey",       # 应用id
    "secretkey",    # 密钥
    "notice_lan",   # 提示语言
    "use_https",    # 是否使用https
]



default_config = {
'default_src':'auto',
'default_tar':'auto',
'appkey':'',
'secretkey': '',
'notice_lan':'en',
"use_https": False
}   

http_api_address = "http://openapi.youdao.com/api"
https_api_address = "https://openapi.youdao.com/api"

class result:
    def __init__(
            this,
            errCode = 0,
            query = None,
            speakUrl = None,
            tSpeakUrl = None,
            translation = None,
            basic = None,
            web = None,
            l = None,
            dict_ = None,
            webdict = None,
        ):
        this.errCode = errCode
        this.query = query
        this.speakUrl = speakUrl
        this.tSpeakUrl = tSpeakUrl
        this.translation = translation
        this.basic = basic
        this.web = web
        l = l
        dict_ = dict_
        webdict = webdict

def show_help():
    print("Welcome to trans.It is a very simple commandline-based translation software.")
    print("\t-q(--query): show the query text");
    print("\t-w(--web): show the web translation");
    print("\t-l(--lan): show the language between source and target");
    print("\t-f(--from) <language_type>: set the source language type into language_type");
    print("\t-t(--to) <language_type>: set the target language type into langugae_type");
    print("\n")
    print("Here're language types supported:");
    print(lan_supported)

def read_config():
    try:
        fp = open(config_addr, "r+")
    except FileNotFoundError:
        fp = open(config_addr, "w+")
        # write into default configuration
        fp.write(json.dumps(default_config))
        logger2f.info('config.json not found and new one created.')
    except:
        logger.error("an error has occured")
        logger2f.error("an error has occured with open()")
        fp.close()
        raise
    fp.close()
    
    fp = open(config_addr, "r+")
    config = None
    try:
        config = json.loads(fp.read())
    except json.decoder.JSONDecodeError:
        logger.error("there's sth wrong with the config.json file.")
    except:
        logger.error("an error has occured")
        logger2f.error("an error has occured with json.loads()")
        fp.close()
        raise

    fp.close()
    return config

def trans(url, text, src, tar, appKey, secretKey):
    global lan_supported
    global lan_supported_arg

    logger2f.info("query: %s" % text)

    index1 = lan_supported.index(src)
    index2 = lan_supported.index(tar)
    if index1 == -1 or index2 == -1:
        logger.error("language you pass is not supported")
    if text == None or len(text) == 0:
        logger.error("the text shouldn't be empty")
    
    salt = random.randint(1, 65536)
    sign = hashlib.md5(str(appKey + text + str(salt) + secretKey).encode("utf-8")).hexdigest()    

    params = {
        'q':text,
        'from': lan_supported_arg[index1],
        'to': lan_supported_arg[index2],
        'appKey':appKey,
        'salt':salt,
        'sign':sign
    }
    try:
        res = requests.get(url, params=params)
    except:
        return None

    jsonres = json.loads(res.text)

    res = result()
    
    for key in jsonres:
        res.__dict__[key] = jsonres[key]

    return res



if __name__ == "__main__":
    current_config = read_config()
    
    url = http_api_address
    if current_config != None and 'use_https' in current_config and current_config['use_https']:
        url = https_api_address

    src = current_config['default_src']
    tar = current_config['default_tar']
    appkey = current_config['appkey']
    secretkey = current_config['secretkey']

    '''
    options:
    -q(--query): 显示查询的内容
    -w(--web): 显示网络释义
    -l(--lan): 显示语言转换内容
    -f(--from) 语言: 源语言类型
    -t(--to) 语言: 目标语言类型
    '''
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'qwlhf:t:', ['query','web','lan', 'from=','to=',"help"])
    except getopt.GetoptError as err:
        logger.error(str(err))
        sys.exit(2)
    
    query = False
    web = False
    lan = False
    for o,a in optlist:
        if o in ("-q", "--query"):
            query = True
        elif o in ("-w", "--web"):
            web = True
        elif o in ("-l", "--lan"):
            lan = True
        elif o in ("-f", "--from"):
            src = str(a).lower()
        elif o in ("-t", "--to"):
            tar = str(a).lower()
        elif o in("-h", "--help"):
            show_help()

    for arg in args:
        res = trans(url, arg, src, tar, appkey, secretkey)
        # 如果有错误， 打印错误代码（双语是最骚的）
        if int(res.errCode) in err_msg_en:
            if str.upper(current_config['notice_lan']) == "CH":
                logger.error(err_msg_ch[errCode])
            else:
                logger.error(err_msg_en[errCode])
        # 输出翻译内容
        if lan:
            print("%s -> %s:" % (src, tar))
        if query:
            print("query: %s" % arg)
        print(res.translation)
        if web:
            print("web translation:")
            webtrans = res.web
            print(webtrans)                

