import urllib.request
from urllib.request import urlopen
import urllib.parse
import os, shutil, sys
import re
import json
from time import time

doc = '''\
input.txt中接受两种形式的输入文本：一种为点击插件的“查看下载地址”按钮后显现的 歌曲名 歌曲地址 列表组成的多行字符串（一般来说即为直接将该窗格内所有内容复制得到的内容，只复制地址行也可以下载，这时文件名会从地址中获取）；第二种为点击插件的导出歌曲按钮后显现的由歌曲ID和类型组成的单行字符串。
前者形如：
    第一首歌
    第二首歌
    
    http://data.5sing.kgimg.com/xxx
    http://data.5sing.kgimg.com/xxxx
    http://data.5sing.kgimg.com/xxxxx
    
后者形如：
    yc$1234567$fc$9998765$bz$1111111
''';

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
            aNames.append(x['songname'] + x['sign'][-4:]);
            aUrls.append(x['sign']);
    else:
        delimiter = sInfo.find('http://');
        r1 = re.compile(r'^\s*(\S.*?)\s*$', re.M);
        aNames = r1.findall(sInfo[:delimiter]);
        r2 = re.compile(r'^\s*(https?://.+/([^/.]+(\.mp3|wma)))\s*$', re.M);
        aUrls = r2.findall(sInfo[delimiter:]);
        n1, n2, i = len(aNames), len(aUrls), 0;
        while i < n2:
            if (i < n1): aNames[i] += aUrls[i][2];
            else: aNames[i:] = [aUrls[i][1]];
            aUrls[i] = aUrls[i][0];
            i += 1;
    return (aNames, aUrls);

def download(sName, sUrl, target):
    filepath = os.path.join(target, re.sub(r'[\\\/]', ' ', sName));
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
        print(doc);
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
    
main();
