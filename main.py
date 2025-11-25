from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import aiohttp
import yaml
import os

@register("watchface_activation", "表盘激活插件", "小米手表表盘激活插件", "1.0.0")
class WatchfaceActivationPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.config = None
        self.api_url = "https://azumachiaki.com/api/voucher-unlock-lua"

    async def initialize(self):
        """插件初始化，加载配置文件"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f)
                logger.info("表盘激活插件配置加载成功")
            else:
                logger.error("配置文件 config.yaml 不存在")
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")

    @filter.command("激活表盘")
    async def activate_watchface(self, event: AstrMessageEvent):
        """激活表盘指令：/激活表盘 表盘名称 设备码 激活码"""
        message_str = event.message_str.strip()
        parts = message_str.split()
        
        # 验证参数数量
        if len(parts) < 4:
            yield event.plain_result("使用方法：/激活表盘 表盘名称 设备码 激活码")
            return
        
        watchface_name = parts[1]
        device_code = parts[2]
        voucher_code = parts[3]
        
        # 验证表盘名称是否存在
        if not self.config or watchface_name not in self.config.get("watchfaces", {}):
            yield event.plain_result(f"错误：表盘 '{watchface_name}' 不存在，请检查表盘名称")
            return
        
        # 获取表盘配置
        watchface_config = self.config["watchfaces"][watchface_name]
        
        # 准备请求数据
        request_data = {
            "deviceCode": device_code,
            "voucherCode": voucher_code,
            "watchId": str(watchface_config["watchId"]),
            "page": str(watchface_config["page"]),
            "character": str(watchface_config["character"])
        }
        
        try:
            # 发送 POST 请求
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, json=request_data) as response:
                    # 无论状态码如何，都尝试解析返回的 JSON 数据
                    try:
                        result = await response.json()
                        
                        # 解析返回结果
                        code = result.get("code", -1)
                        message = result.get("message", "未知错误")
                        
                        # 根据 code 返回不同消息
                        if code == 0:
                            # 获取 unlockPwd 数据
                            data = result.get("data", {})
                            unlock_pwd = data.get("unlockPwd", "未找到解锁密码")
                            yield event.plain_result(f"✅ 激活成功！解锁密码：{unlock_pwd}")
                        elif code == -1:
                            yield event.plain_result(f"⚠️ 系统返回：{message}")
                        elif code == 1:
                            yield event.plain_result(f"❌ 激活失败{message}")
                        else:
                            yield event.plain_result(f"⚠️ 系统返回（状态码：{response.status}）：{message}")
                    except Exception as json_error:
                        # 如果 JSON 解析失败，返回原始错误信息
                        yield event.plain_result(f"❌ 服务器错误，状态码：{response.status}，且无法解析返回数据")
                        
        except aiohttp.ClientError as e:
            yield event.plain_result(f"❌ 网络连接错误：{str(e)}")
        except Exception as e:
            yield event.plain_result(f"❌ 系统错误：{str(e)}")

    @filter.command("表盘列表")
    async def list_watchfaces(self, event: AstrMessageEvent):
        """显示可用的表盘列表"""
        if not self.config or "watchfaces" not in self.config:
            yield event.plain_result("❌ 配置文件加载失败或没有配置表盘")
            return
        
        watchfaces = self.config["watchfaces"]
        if not watchfaces:
            yield event.plain_result("暂无可用表盘")
            return
        
        result = "📱 可用表盘列表：\n"
        for name in watchfaces.keys():
            result += f"• {name}\n"
        
        result += "使用方法：/激活表盘 表盘名称 设备码 激活码"
        yield event.plain_result(result)

    @filter.command("激活帮助")
    async def help_command(self, event: AstrMessageEvent):
        """显示帮助信息"""
        help_text = """📱 表盘激活插件使用说明：

🔹 激活表盘：
/激活表盘 表盘名称 设备码 激活码

🔹 查看表盘列表：
/表盘列表

🔹 获取帮助：
/激活帮助

📋 当前支持您配置的所有表盘，使用 /表盘列表 查看完整列表

💡 提示：设备码和激活码请从官方渠道获取"""
        yield event.plain_result(help_text)

    async def terminate(self):
        """插件卸载"""
        logger.info("表盘激活插件已卸载")
