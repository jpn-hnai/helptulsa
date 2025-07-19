from pathlib import Path
from datetime import datetime
import yaml
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import schedule
import time


def diff_resources(path: Path):
    now = datetime.utcnow().isoformat()
    diff_file = path.with_suffix(f".{now}.diff")
    diff_file.write_text(f"Diff at {now}\n")


def start_scheduler(path: Path):
    schedule.every().day.at("00:00").do(diff_resources, path=path)

    class ReloadHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.src_path == str(path):
                diff_resources(path)

    observer = Observer()
    observer.schedule(ReloadHandler(), path=str(path.parent))
    observer.start()
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
