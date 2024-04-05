import tkinter as tk
from tkinter import messagebox
import threading

class ThreadController:
    def __init__(self):
        self.thread = None
        self.control_event = threading.Event()

    def run(self, target, args=()):
        if not self.is_running():
            self.control_event.clear()
            self.thread = threading.Thread(target=target, args=args)
            self.thread.start()
        else:
            messagebox.showwarning("Внимание", "Задача уже запущена!")

    def stop(self):
        if self.thread is not None:
            self.control_event.set()
            self.thread.join()  # Дождаться завершения потока
            self.thread = None
        else:
            messagebox.showwarning("Внимание", "Нет запущенной задачи для остановки.")

    def is_running(self):
        return self.thread is not None and self.thread.is_alive()