import os
import subprocess
import threading
from queue import Queue, Empty
import time

class SATDDetector:
    def __init__(self, jar_path=None):
        if jar_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            jar_path = os.path.join(base_dir, 'satd_detector.jar')

        self.process = subprocess.Popen(
            ['java', '--add-opens', 'java.base/java.lang=ALL-UNNAMED', '-jar', jar_path, 'test'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            bufsize=1  # line-buffered
        )
        self.output_queue = Queue()
        self._start_reader_thread()
        self.lock = threading.Lock()

    def _start_reader_thread(self):
        def stdout_reader():
            for line in self.process.stdout:
                self.output_queue.put(line.strip())

        def stderr_reader():
            for line in self.process.stderr:
                print(f"[java stderr] {line.strip()}")

        self.reader_thread = threading.Thread(target=stdout_reader, daemon=True)
        self.reader_thread.start()

        self.stderr_thread = threading.Thread(target=stderr_reader, daemon=True)
        self.stderr_thread.start()

    def _is_process_alive(self):
        return self.process.poll() is None

    def classify(self, comment: str) -> str:
        with self.lock:
            try:
                self.process.stdin.write(comment + '\n')
                self.process.stdin.flush()
            except Exception as e:
                print(f"Error writing to subprocess: {e}")
                print("Java stderr output:")
                print(self.process.stderr.read())
                raise
            try:
                return self.output_queue.get(timeout=5)
            except Empty:
                print(f"Timeout waiting for output: {self.process.stderr.read()}")
                return "Timeout or Error"

    def close(self):
        try:
            if self._is_process_alive():
                self.process.stdin.write("/exit\n")
                self.process.stdin.flush()
                time.sleep(0.2)
        except Exception:
            pass
        finally:
            if self._is_process_alive():
                self.process.terminate()
            self.reader_thread.join(timeout=1)
            self.stderr_thread.join(timeout=1)
