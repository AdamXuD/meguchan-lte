# meguchan

> 惠酱的长期维护版本（目前正处于开发阶段）

## 如何部署

1. 安装docker与docker-compose。
2. `docker-compose up`（开摆

## 功能

### 国内新冠疫情信息查询

#### 查询地方疫情信息（风险等级 新增 目前确诊）

指令: 城市名 + 疫情

示例: 天津疫情

#### 查询地方出入政策

指令: 城市名 + 疫情政策

示例: 广州疫情政策

#### 查询城市风险地区

只限查询大陆地级市或直辖市

指令: 城市名 + 风险地区

#### 疫情信息更新推送

指令: 关注疫情 + 城市名

示例: 关注疫情 北京

#### 取消推送
指令: 取消疫情 + 城市名 / 取消关注疫情 + 城市名 / 取消推送疫情 + 城市名

### 获取 Epic 限免游戏资讯

指令: ((E|e)(P|p)(I|i)(C|c))?喜(加一|\+1)

示例: Epic喜加一

### emoji表情包缝合

发送两个连续的emoji表情即可。

### 来点猫猫或狗狗

指令: 来点猫猫 或 来点狗狗

### 枝网查重

#### 查重

指令: /枝网查重 + 要查重的小作文

其他使用方式: 回复需要查重的内容，回复“查重”

#### 随机小作文

指令: /随机小作文

### 天气查询

指令: 天气+地区 或 地区+天气

### 按Pixiv ID 搜索p站图片

指令: 搜(p|P)站(\s+)?(?P<pid>\d+)

示例: 搜p站 12345678

## 特别鸣谢

[@Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

[@nonebot/nonebot2](https://github.com/nonebot/nonebot2)

[@monsterxcn/Nonebot_Plugin_EpicFree](https://github.com/monsterxcn/nonebot_plugin_epicfree)

[@MeetWq/nonebot-plugin-emojimix](https://github.com/MeetWq/nonebot-plugin-emojimix)

[@NoneBot2-Ae/nonebot_plugin_random_cat](https://github.com/NoneBot2-Ae/nonebot-plugin-random-cat)

[@MeetWq/nonebot-plugin-asoulcnki以及枝网项目组](https://github.com/MeetWq/nonebot-plugin-asoulcnki)

[@Zeta-qixi/nonebot-plugin-covid19-news](https://github.com/Zeta-qixi/nonebot-plugin-covid19-news)

[@mnixry/nonebot-plugin-gocqhttp](https://github.com/mnixry/nonebot-plugin-gocqhttp)

[@kexue-z/nonebot-plugin-heweather](https://github.com/kexue-z/nonebot-plugin-heweather)

本项目是站在各位巨人的肩膀上才得以完成的。
