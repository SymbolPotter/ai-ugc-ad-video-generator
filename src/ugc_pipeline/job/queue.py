"""In-process job queue with a bounded worker pool."""
from __future__ import annotations

import queue
import threading
from collections.abc import Callable

from ugc_pipeline.job.spec import JobSpec
from ugc_pipeline.logging import get_logger

log = get_logger("job.queue")


class JobQueue:
    def __init__(self, max_parallel: int = 4) -> None:
        self._q: queue.Queue[JobSpec | None] = queue.Queue()
        self._max = max_parallel
        self._threads: list[threading.Thread] = []
        self._stop = threading.Event()

    def submit(self, spec: JobSpec) -> None:
        self._q.put(spec)

    def start(self, handler: Callable[[JobSpec], None]) -> None:
        for i in range(self._max):
            t = threading.Thread(target=self._worker, args=(handler,), name=f"ugc-w{i}", daemon=True)
            t.start()
            self._threads.append(t)

    def _worker(self, handler: Callable[[JobSpec], None]) -> None:
        while not self._stop.is_set():
            item = self._q.get()
            if item is None:
                self._q.task_done()
                return
            try:
                handler(item)
            except Exception:  # noqa: BLE001 — worker must survive any job error
                log.exception("job crashed job=%s", item.job_id)
            finally:
                self._q.task_done()

    def shutdown(self, wait: bool = True) -> None:
        self._stop.set()
        for _ in self._threads:
            self._q.put(None)
        if wait:
            for t in self._threads:
                t.join(timeout=5)