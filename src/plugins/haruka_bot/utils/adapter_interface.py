from nonebot.adapters.mirai2 import Bot
from nonebot.adapters.mirai2.message import MessageChain as Message
from .compatible import MessageSegment
from .compatible import MessageEvent, GroupMessageEvent, PrivateMessageEvent
from nonebot.adapters.mirai2.event import NewFriendRequestEvent
from nonebot.adapters.mirai2.exception import ActionFailed, NetworkError
from nonebot.adapters.mirai2 import GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER
