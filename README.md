# 表盘激活插件 (Watchface Activation Plugin)

一个用于AstrBot的小米手表表盘激活插件，支持通过API接口激活各种表盘。

## 功能特性

- **表盘激活**: 通过指定的API接口激活小米手表表盘
- **批量管理**: 支持配置多个表盘，方便批量激活
- **用户友好**: 简单的命令格式，清晰的结果展示
- **错误处理**: 完善的错误处理机制，提供详细的错误信息

## 安装要求

- AstrBot 框架
- Python 3.7+
- 依赖包：`aiohttp`, `PyYAML`

## 安装方法

1. 将插件文件夹放置在AstrBot的plugins目录下
2. 确保已安装所需依赖：
   ```bash
   pip install aiohttp PyYAML
   ```
3. 重启AstrBot即可使用

## 使用方法

### 可用命令

- `/激活表盘 <表盘名称> <设备码> <激活码>` - 激活指定表盘
- `/表盘列表` - 查看所有可用的表盘列表
- `/激活帮助` - 查看使用帮助

### 示例

```
/激活表盘 花束系列-星野 123456 789012
/表盘列表
/激活帮助
```

## 配置说明

插件的表盘配置保存在 `config.yaml` 文件中。初始状态下该文件只包含示例配置，开发者需要根据实际需求添加表盘信息。

### 配置格式
```yaml
watchfaces:
  "表盘名称":
    watchId: 表盘ID
    page: 页面编号
    character: 角色标识
```

### 配置字段说明
- `watchId`: 表盘的唯一标识ID
- `page`: 表盘所在的页面编号  
- `character`: 表盘的角色标识符

## 支持的表盘

本插件支持任意表盘的激活，开发者需要在`config.yaml`文件中配置具体的表盘信息。

## API接口

插件使用以下API接口进行表盘激活：
- **URL**: `https://azumachiaki.com/api/voucher-unlock-lua`
- **方法**: POST
- **参数**: `watchId`, `page`, `character`, `deviceId`, `voucherCode`

## 错误代码说明

- **code: 0**: 激活成功，返回解锁密码
- **code: -1**: 激活失败，返回错误信息

## 开发者使用指南

### 添加新表盘
1. 在`config.yaml`文件中的`watchfaces`部分添加新表盘配置
2. 重启AstrBot使配置生效
3. 使用`/表盘列表`命令验证配置是否正确
4. 使用`/激活表盘 表盘名称 设备码 激活码`进行激活

### 获取表盘参数
开发者需要通过其他方式获取表盘的`watchId`、`page`和`character`参数，这些参数通常可以从表盘的官方文档或相关资源中获得。

## 开发信息

- **版本**: v1.0.0
- **作者**: BakaCookie520
- **仓库**: https://github.com/BakaCookie520/BiaoPanJiHuo

## 支持

如有问题或建议，请参考 [AstrBot帮助文档](https://astrbot.app)

## 许可证

本项目采用开源许可证，欢迎开发者贡献代码和反馈问题。
