# meguchan

> 惠酱的长期维护版本（目前正处于开发阶段）

## 如何部署

1. 安装 docker 与 docker-compose。
2. `docker-compose up`（开摆

## 功能

### emoji 表情包缝合

发送两个连续的 emoji 表情即可。

### 按 Pixiv ID 搜索 p 站图片

指令: 惠酱[p|P]站(\s)?(?P `<pid>`\d+)

示例: 惠酱 p 站 12345678

### 以图搜图

指令：惠酱搜图

然后按照引导继续即可。

### mc 监测

惠酱可以检测 mc 服务器的情况。

使用方法：

1. 发送 "/mc template" 获取设置模板。
2. 发送 "/mc adds <设置>" 可向惠酱添加服务器（仅指定的惠酱管理员可使用）。
3. 发送 "/mc dels <服务器名称>" 可向惠酱删除服务器（仅指定的服务器管理员可使用）。
4. 发送 "/mc check <服务器名称>" 可检测服务器状态。
5. 发送 "/mc list" 可查看本群或由您管理的服务器列表。

## 特别鸣谢

[@Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

[@nonebot/nonebot2](https://github.com/nonebot/nonebot2)

[@MeetWq/nonebot-plugin-emojimix](https://github.com/MeetWq/nonebot-plugin-emojimix)

[@mnixry/nonebot-plugin-gocqhttp](https://github.com/mnixry/nonebot-plugin-gocqhttp)

本项目是站在各位巨人的肩膀上才得以完成的。
