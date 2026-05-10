"""
queue_manager.py
----------------
Provides a single, shared Python Queue instance that is imported by both
the API and the Worker.  Because both modules run in the same Python process
(or are started from the same process), they share the exact same object in
memory — no IPC, no sockets, just a thread-safe stdlib queue.

If you later scale out to multiple processes or machines, this module is the
only file you need to swap out (e.g., replace with Redis, RabbitMQ, etc.).

Usage:
    from shared.queue_manager import get_queue

    q = get_queue()
    q.put(item)
    item = q.get()
"""

import queue
from typing import Optional

# ---------------------------------------------------------------------------
# Singleton
# ---------------------------------------------------------------------------

_queue: Optional[queue.Queue] = None


def get_queue(maxsize: int = 0) -> queue.Queue:
    """
    Return the application-wide vote queue (creates it on first call).

    Args:
        maxsize: Maximum number of items the queue can hold.
                 0 (default) means unlimited — the queue can grow
                 indefinitely while the worker is disabled.

    Returns:
        The singleton Queue instance.
    """
    global _queue
    if _queue is None:
        _queue = queue.Queue(maxsize=maxsize)
    return _queue


def reset_queue() -> None:
    """
    Discard the current queue and create a fresh one.

    Intended for use in unit tests only — do not call in production.
    """
    global _queue
    _queue = None
