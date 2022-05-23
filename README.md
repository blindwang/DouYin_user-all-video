## 抖音用户信息及视频信息爬取

### Have A Try
选择是否下载视频、是否下载视频信息、是否下载视频封面

```shell
python .\user_video_test.py --download-video --save-video-info --download-video-cover
```
```txt
optional arguments:
  -h, --help            show this help message and exit
  --download-video      download video
  --save-video-info     save video info
  --download-video-cover
                        download video cover
```

## Structure

```text
│  README.md
│  user_url.txt  # 保存要下载的抖音号首页链接
│  user_video_test.py  
│  
├─.idea
│          
├─covers  # 保存抖音号下所有视频的封面
│  ├─105321342275大表哥Vlog
│  │      6923496299199204611cover.jpeg
│          
├─user_info  # 保存抖音号所有信息
│      潘姥姥_user_info.xlsx
│      
├─videos    # 保存抖音号所有视频
│  ├─1099110682212840潘姥姥
│  │      7091480112012594445赶在初夏竹笋还没长大，做个零食尝尝!#夏天的正确打开方式 #乡村守护人#新农人计划2022#跟着抖音学做菜 .mp4
│  │      avatar_larger.jpeg
│  │      avatar_medium.jpeg
│  │      avatar_thumb.jpeg
│          
└─video_info  # 保存抖音号所有视频信息
        潘姥姥_video_info.xlsx
```

## Detail
### user_info

`用户id`
`和用户首页url有关的标识`
`唯一标识id`
`用户昵称`
`关注量`
`粉丝量`
`总点赞数`
`个性签名`
`是否政府媒体`
```text
uid                                                       73178298651
sec_uid             MS4wLjABAAAAzmy07L155965JtgkO8pFyqAxcNiDxtm1WG...
unique_id                                                    qiao2099
nickname                                                         乡村小乔
custom_verify
following_count                                                   435
follower_count                                                7944004
total_favorited                                             149485701
aweme_count                                                      1062
favoriting_count                                                    0
signature           ❤️用视频记录平凡而又美好的小日子～\n�大名：王晨晨    小名：王小乔\n�生日：199...
is_gov_media_vip                                                False
avatar_larger       https://p3.douyinpic.com/aweme/1080x1080/aweme...
avatar_medium       https://p3.douyinpic.com/aweme/720x720/aweme-a...
avatar_thumb        https://p3.douyinpic.com/aweme/100x100/aweme-a...
```

### video_info

`视频id`
`描述`
`评论量`
`点赞量`
`转发量`
`分享量`
```text
aweme_id                                       7100498278642371870
desc             花5000块估下叔叔养了多年的鱼塘，抽干水看看到底值不值......#户外 #农村生活 #我...
comment_count                                                 1407
digg_count                                                   67000
forward_count                                                    0
share_count                                                   1196
cover            [https://p3-sign.douyinpic.com/tos-cn-i-dy/8db...
video            [https://v5-e.douyinvod.com/1e6446a058da86f185...
```
## Tips
不能开梯子！！
