import multiprocessing
import thread
"""
! UNTESTED
"""
class ThreadQueue:

    """
    Constructor, lol
    """
    def __init__(self):
        self._queue = Queue.Queue(0)
        self._max_threads = multiprocessing.cpu_count()
        self._active_threads_count = 0

    """
    Adds task to queue.
    """
    def addTask(self, func, args, kwargs):
        self._queue.put((func, args, kwargs))
        self._start_next()

    """
    Starts next function with arguments from queue.
    """
    def _start_next(self):
        if self._queue.empty():
            return

        if self._active_threads_count >= self._max_threads:
            return

        func, args, kwargs = self._queue.get()
        
        thread.start_new_thread(self._run, (func, args, kwars))

    """
    Callback for finishing thread
    """
    def _callback(self):
        self._active_threads_count--
        self._start_next()

    """
    Internal run function
    """
    def _run(self, func, args, kwargs):
        func(args, kwargs)
        self._callback()