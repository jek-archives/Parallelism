import queue
from typing import Optional

_queue: Optional[queue.Queue] = None


def get_queue(maxsize: int = 0) -> queue.Queue:
    global _queue
    if _queue is None:
        _queue = queue.Queue(maxsize=maxsize)
    return _queue


def reset_queue() -> None:
    global _queue
    _queue = None
