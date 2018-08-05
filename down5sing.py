#! /usr/bin/python3
import urllib.request
from urllib.request import urlopen
from urllib.error import HTTPError
import urllib.parse
import os, sys
import re
import json
from time import time
import base64

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

count = 0;

def fix(aIndex):
    sType, sId = aIndex
    sApiSongSrc = 'http://service.5sing.kugou.com/song/getsongurl?songid={}&songtype={}&from=web&version=6.6.72' #  song.nId, song.sType
    sUrl = sApiSongSrc.format(sId, sType)
    sUrl += '&_={}'.format(str(int(time()*1000)));
    with urlopen(sUrl) as res:
        sData = res.read().decode('utf-8');
        mData = json.loads(sData.strip('()'));
        sUrl = mData['data']['squrl'];
    assert sUrl;
    return sUrl
    # sUrl = 'http://5sing.kugou.com/' + aIndex[0] + '/' + aIndex[1] + '.html'
    # with urlopen(sUrl) as page:
    #     while (1):
    #         line = page.readline()
    #         if (not line or b'ticket' in line): break
    # data = re.search(rb'ticket.+?:.*?[\'"](.+)[\'"]', line).group(1)
    # data = json.loads(base64.b64decode(data).decode('utf-8'))
    # return data['file'];

def download(sName, sUrl, aIndex, target):
    global count;
    filepath = os.path.join(target, re.sub(r'[\\/:*?<>"|\t]', ' ', sName));
    while (os.path.exists(filepath)):
        filepath = re.sub(r'(\.\w+)?$', r'_\1', filepath);
    try:
        mp3 = urllib.request.urlretrieve(sUrl, filename=filepath);
        print('已下载：' + os.path.abspath(mp3[0]))
        count += 1;
    except HTTPError as e:
        print('找不到歌曲地址： ' + sName)
        global aErrorFile;
        aErrorFile.append((aIndex, sName));

def read(sFile=None) -> '2-tuple of lists':
    if sFile == None:
        sInfo = input('请输入要下载的歌曲信息，以回车键结束：');
    else:
        try:
            with open(sFile, 'r', encoding='utf-8-sig') as file:
                sInfo = file.read();
        except UnicodeDecodeError:
            with open(sFile, 'r') as file:
                sInfo = file.read();
    result = re.search(r'^\s*((fc|yc|bz)\$\d+(\$(fc|yc|bz)\$\d+)*)\s*$', sInfo);
    if result:
        # utilise 5sing api to query with ordinal number
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
        aIndices = re.findall(r'(fc|yc|vz)\$(\d+)', result.group(1));
        # [('fc', '123434'), ...]
        mIndices = {}
        for x in aSongs:
            sIndex = '{}${}'.format(x['songtype'], x['id']);
            sName = x['songname'] + x['sign'][-4:];
            sUrl = x['sign'];
            mIndices[sIndex] = [sName, sUrl];
        for sType, sId in aIndices:
            sIndex = '{}${}'.format(sType, sId);
            aNames.append(mIndices[sIndex][0]);
            aUrls.append(mIndices[sIndex][1]);
    else:
        # download from url directly
        delimiter = sInfo.find('http://');
        r1 = re.compile(r'^\s*(\S.*?)\s*$', re.M);
        aNames = r1.findall(sInfo[:delimiter]);
        r2 = re.compile(r'^\s*(https?://.+/([^/]+?(\.mp3|wma)))\s*$', re.M);
        aUrls = r2.findall(sInfo[delimiter:]);
        n1, n2, i = len(aNames), len(aUrls), 0;
        while i < n2:
            if (i < n1): aNames[i] += aUrls[i][2];
            else: aNames[i:] = [aUrls[i][1]];
            aUrls[i] = aUrls[i][0];
            i += 1;
        aIndices = [None for x in range(n2)];
    return (aNames, aUrls, aIndices);

def main():
    global count;
    print('程序运行开始');
    global aErrorFile;
    aErrorFile = [];
    target = sys.argv[0] if sys.argv[0] else os.getcwd();
    target = target if os.path.isdir(target) else os.path.split(target)[0];
    # target is current directory then
    sFile = os.path.join(target, 'input.txt')
    if os.path.isfile(sFile):
        aNames, aUrls, aIndices = read(sFile);
    else:
        print('找不到歌曲信息文件，请将存有歌曲信息的文件以文件名 input.txt 保存到脚本的同目录下。');
        print(doc);
        print('转为手动信息输入模式。')
        aNames, aUrls, aIndices = read();
    assert(len(aNames) == len(aUrls) == len(aIndices));
    print('歌曲信息读取完成。');
    print('将要下载：');
    print(*aNames, sep=' , ');
    target = os.path.join(target, '歌曲下载目录');
    if not os.path.isdir(target):
        os.mkdir(target);
    print('正在下载……');
    for x in zip(aNames, aUrls, aIndices):
        download(*x, target);
    print('\n下载已完成。');
    if (aErrorFile):
        print('\n以下歌曲下载失败： ', *aErrorFile, sep='\n'); 
        print('\n尝试通过网页搜索下载地址……');
        aError = aErrorFile;
        aErrorFile = [];
        for x in aError:
            if (x[0]):
                sUrl = fix(x[0]);
                download(x[1], sUrl, x[0], target);
            else:
                aErrorFile.append(x);
        if (aErrorFile):
            print('\n搜索结束，最终下载失败歌曲如下：', *aErrorFile, sep='\n'); 
        else:
            print('\n搜索结束，所有歌曲下载成功。');
    input('总共下载歌曲 ' + str(count) + ' 首，按回车键退出。');
    
if __name__ == '__main__':
    main();
