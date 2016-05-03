功能简介：

告别flash。将5sing播放器替换为html5播放，可禁止5sing的自动播放。
可读取各5sing页面中的歌曲列表到独立面板中，支持页面包括个人中心、歌手空间、独立播放页面等，并支持在个人中心和个人空间中远程载入当前列表中没有列出的歌曲。统一样式，独立播放，支持多种播放控制，可选取歌曲以显示下载链接或在5sing独立播放页中播放。
支持使用谷歌、百度进行5sing站内搜索的功能，支持导入、导出列表中的歌曲（配合5sing原生的独立播放页可实现对歌曲列表的任意编辑操作），提供可配置的参数及热键，使用localStorage方式将所选参数存在本地。

代码由纯原生javascript写成，没有用到greasemonkey的特权。脚本在firefox的greasemonkey上编写并经过长期使用测试，在chrome下通过tampermonkey实测也可使用该脚本，就是界面要难看一点……
需要注明的一点是，该插件所能播放的歌曲格式取决于html5播放器对歌曲格式的支持，一般来说，mp3文件播放都没有问题，但在遇到5sing中偶然出现的wma格式歌曲时则无法播放（此时仍然可以显示歌曲地址等信息），5sing网络出现问题（在5sing很常见）或本身歌曲链接有问题时（5sing有时候会莫名出现这种链接不对的情况）也无法播放（从1.0.4版本开始插件会自动尝试修复该问题）。

[插件截图见此：
https://github.com/heroesm/5singHelper/wiki/%E6%8F%92%E4%BB%B6%E6%88%AA%E5%9B%BE](https://github.com/heroesm/5singHelper/wiki/%E6%8F%92%E4%BB%B6%E6%88%AA%E5%9B%BE)。

[github地址：https://github.com/heroesm/5singHelper](https://github.com/heroesm/5singHelper)

[greasyfork地址：https://greasyfork.org/zh-CN/scripts/17648-5sing%E5%8A%A9%E6%89%8B](https://greasyfork.org/zh-CN/scripts/17648-5sing%E5%8A%A9%E6%89%8B)