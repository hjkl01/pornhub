
## 用法

```sh
git clone https://github.com/lesssound/pornhub
cd pornhub && pip install -r requirements.txt
# 编辑 settings.toml, 配置proxy_url 和 喜欢的列表页面
python crawler.py webm
# 待程序运行完毕， 会在webm文件夹下download两页的webm缩略图，对应名称为详细页面的URL后缀
python crawler.py mp4
# 在MP4文件夹可看到下载好的MP4文件
```

## tips
- 可以在 [vultr](https://www.vultr.com/?ref=7378179) 上申请1小时的机器,下载完成后用scp download到本地
- 使用Trojan: [shadowsocks邀请码](https://portal.shadowsocks.nl/aff.php?aff=24252)
- 项目中用到了[youtube-dl](https://github.com/ytdl-org/youtube-dl)