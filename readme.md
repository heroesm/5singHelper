# 5sing助手
一个用于改善5sing听歌体验的脚本（插件）。

## 安装
### firefox浏览器：
* 需先安装用户脚本管理插件，如[greasemonkey](https://addons.mozilla.org/en-US/firefox/addon/greasemonkey/)。
* 在脚本的[GreasyFork页面](https://greasyfork.org/en/scripts/17648-5sing%E5%8A%A9%E6%89%8B)中点击 Install this script 或 安装此脚本 以安装。

### Chrome及类似浏览器：
* 需先安装用户脚本管理插件，如[tampermonkey](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo)。
* 在脚本的[GreasyFork页面](https://greasyfork.org/en/scripts/17648-5sing%E5%8A%A9%E6%89%8B)中点击 Install this script 或 安装此脚本 以安装。

## 功能
* 将flash播放替换为html5播放。
* 可选择禁止5sing页面的自动播放。
* 读取当前5sing页面中可能包含的歌曲列表信息，在独立的插件面板中进行播放控制；支持继续载入当前页面中未列出的相关歌曲、选择歌曲显示下载链接等，各种我想要的功能；支持大部分5sing页面。
* 与5sing的独立播放页整合，插件与5sing独立播放页相配合可实现对歌曲列表的编辑操作。

## 备注
* 脚本由纯js写成，未用到第三方库，未用到greasemonkey特权函数。
* 该插件所能播放的歌曲格式取决于浏览器对歌曲格式的支持，即，5sing中偶尔出现的wma文件通常无法播放；当5sing网络出现问题或歌曲链接配置错误时，也可能导致无法播放。
* Github项目主页中存有可批量下载歌曲的配套python脚本。
* 问题反馈与建议可以提交于[GreasyFork](https://greasyfork.org/zh-CN/scripts/17648-5sing%E5%8A%A9%E6%89%8B/feedback)或Github。

## 参见
* [插件截图](https://github.com/heroesm/5singHelper/wiki/%E6%8F%92%E4%BB%B6%E6%88%AA%E5%9B%BE)（截取于早期版本中，界面与目前版本有细微不同）
* [github地址](https://github.com/heroesm/5singHelper)
* [greasyfork地址](https://greasyfork.org/zh-CN/scripts/17648-5sing%E5%8A%A9%E6%89%8B)
