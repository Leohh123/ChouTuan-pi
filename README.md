# 丑团外卖柜

## 启动

进入项目目录，然后

```bash
python main.py
```

首先会进行设备登录，输出以下内容表示登录成功

```
{"code": 1, "message": "\u60a8\u5c1a\u672a\u767b\u5f55", "data": null}
{"code": 0, "message": "\u767b\u5f55\u6210\u529f", "data": null}
{"code": 0, "message": "ok", "data": "device_001"}
```

屏幕上会显示二维码及当前剩余柜数

每隔一秒输出当前需要开门的信息，以及每个外卖柜的占用状态，例如：

```
{"code": 0, "message": "ok", "data": [{"id": 3, "deposit_username": "hyf", "pickup_username": "hyf", "device_id": "device_001", "cabinet_no": 0, "state": 0, "moment": "2022-11-25T17:45:46.544"}]} [False, False, False] // 表示当前有一个订单需要开0号柜门，三个外卖柜都没有被占用
```

```
{"code": 0, "message": "ok", "data": []} [True, False, False] // 表示没有开门的动作，只有0号外卖柜被占用
```

外卖柜开门后会输出 `open_cabinet` 加开门的柜子编号，然后屏幕输出等待柜门关闭（关门对应GPIO接高电平，开门为低电平），关门后输出 `close_cabinet` 加柜子编号

## 配置

配置文件为 `config.json` ，示例：

```json
{
    "device_id": "device_001", // 设备名称，需以该名称注册账号
    "passwd": "123", // 账号密码
    "host": "http://xxx.xxx.xxx.xxx:yyyy", // 主机
    "cabinet_num": 3, // 外卖柜数量
    "servo_pin": [ // 分别对应三个外卖柜舵机信号线连接的GPIO编号
        17,
        27,
        22
    ],
    "btn_pin": [ // 分别对应三个外卖柜开关连接的GPIO编号
        10,
        9,
        11
    ]
}
```

## 其它

字体文件 `SourceHanSans-Regular.ttc`