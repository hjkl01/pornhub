# 介绍
python版本是python 3。
此分支能够找到pornhub中视频的真实地址，并写入文本文档，之后需要通过下载工具idm下载。

基于@killmymates（https://github.com/killmymates/Pornhub） 主要变化是抓取页面内所有视频而不是自己选择，通过idm多线程下载而不是自建下载。
# 使用方法：
cd pornhub 

pip install -r requirements.txt

python crawler.py

idm->任务->导入->从文本文件导入 （选择download_link.txt)

还有，crawler.py中的pornhub地址可任意添加，找注释就能找到。
