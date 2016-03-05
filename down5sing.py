import urllib.request
from urllib.request import urlopen
import urllib.parse
import os, shutil, sys
import re
import json
from time import time

def read(sFile=None) -> '2-tuple of lists':
    if sFile == None:
        sInfo = input('请输入要下载的歌曲信息，以回车键结束：');
    else:
        try:
            with open(sFile, 'r', encoding='utf-8') as file:
                sInfo = file.read();
        except UnicodeDecodeError:
            with open(sFile, 'r') as file:
                sInfo = file.read();
    result = re.search(r'^\s*((fc|yc|bz)\$\d+(\$(fc|yc|bz)\$\d+)*)\s*$', sInfo);
    if result:
        values = {
            'songinfo': result.group(1),
            '_': str(int(time()*1000))
        };
        sQuery = urllib.parse.urlencode(values);
        # sUrl = r'http://service.5sing.kugou.com/song/find?songinfo=' + result.group(1) + '&_=' + str(int(time()*1000));
        sUrl = r'http://service.5sing.kugou.com/song/find';
        request = urllib.request.Request(sUrl + '?' + sQuery);
        with urlopen(request) as file:
            aSongs = json.loads(file.read().decode('utf-8'));
        aNames = []
        aUrls = [];
        for x in aSongs:
            aNames.append(x['songname']);
            aUrls.append(x['sign']);
    else:
        delimiter = sInfo.find('http://');
        r1 = re.compile(r'^\s*(\S.*?)\s*$', re.M);
        aNames = r1.findall(sInfo[:delimiter]);
        r2 = re.compile(r'^\s*(https?://.+\.(mp3|wma))\s*$', re.M);
        aUrls = r2.findall(sInfo[delimiter:]);
    return (aNames, aUrls);

def download(sName, sUrl, target):
    filepath = os.path.join(target, sName + sUrl[-4:]);
    mp3 = urllib.request.urlretrieve(sUrl, filename=filepath);
    print('已下载：' + os.path.abspath(mp3[0]))

def main():
    print('程序运行开始');
    target = sys.argv[0] if sys.argv[0] else os.getcwd();
    target = target if os.path.isdir(target) else os.path.split(target)[0];
    # target is current directory then
    sFile = os.path.join(target, 'input.txt')
    if os.path.isfile(sFile):
        aNames, aUrls = read(sFile);
    else:
        print('找不到歌曲信息文件，请将存有歌曲信息的文件以文件名 input.txt 保存到脚本的同目录下。');
        print('转为手动信息输入模式。')
        aNames, aUrls = read();
    print('歌曲信息读取完成。');
    print('将要下载：');
    print(*aNames, sep=' , ');
    target = os.path.join(target, '歌曲下载目录');
    if not os.path.isdir(target):
        os.mkdir(target);
    print('正在下载……');
    for x in zip(aNames, aUrls):
        download(*x, target);
    print('下载已完成。');
    input('按回车键退出。');
    
try:
    main();
except Exception as e:
    print('出现错误：\n', e);
    input('输入回车退出……');