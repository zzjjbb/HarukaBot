from typing import Union, Optional, Literal
from nonebot.adapters import Event as BaseEvent
from nonebot.adapters import mirai2


# class _WrapEvent:
#     def __init__(self, event: mirai2.Event):
#         assert isinstance(event, mirai2.Event)
#         self._mirai_event = event
#
#     def __getattr__(self, item):
#         return getattr(self._mirai_event, item)


class MessageEvent:
    message_type: Literal['private', 'group']
    self_id: int
    group_id: Optional[int]
    user_id: Optional[int]
    sub_type: str

    def __init__(self, event: mirai2.MessageEvent):
        self.self_id = event.self_id


class GroupMessageEvent(MessageEvent):
    __slots__ = ('self_id', 'group_id')
    message_type = 'group'

    def __init__(self, event: mirai2.GroupMessage):
        super().__init__(event)
        self.group_id = event.sender.group.id


class PrivateMessageEvent(MessageEvent):
    __slots__ = ('self_id', 'user_id', 'sub_type')
    message_type = 'private'

    def __init__(self, event: Union[mirai2.FriendMessage, mirai2.TempMessage]):
        super().__init__(event)
        self.user_id = event.sender.id
        if isinstance(event, mirai2.FriendMessage):
            self.sub_type = 'friend'
        elif isinstance(event, mirai2.TempMessage):
            self.sub_type = 'group'


class MessageSegment:
    @staticmethod
    def image(src: str):
        """only process the base64 (dynamic) or url (live) cases used in this project"""
        if src[:9] == "base64://":
            return mirai2.MessageSegment.image(base64=src[9:])
        elif src[:4] == "http":
            return mirai2.MessageSegment.image(url=src)
        else:
            return mirai2.MessageSegment.plain("[unsupported image]\n" + src)

    @staticmethod
    def at(user_id: Union[int, str]):
        if user_id == 'all':
            return mirai2.MessageSegment.at_all()
        else:
            return mirai2.MessageSegment.at(int(user_id))


def event_converter(func):
    def func_compat(*args, **kwargs):
        event = args[0]
        if isinstance(event, mirai2.GroupMessage):
            event = GroupMessageEvent(event)
        elif isinstance(event, (mirai2.FriendMessage, mirai2.TempMessage)):
            event = PrivateMessageEvent(event)
        func(event, *args[1:], **kwargs)

    return func_compat()


from functools import wraps
