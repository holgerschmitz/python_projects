from __future__ import annotations

import sys

from PyQt6.QtCore import QObject, QThread, QTimer, QMutex, QMutexLocker, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

from base import ThreadSafeImage
from worker import MyDisplayWorker


class DynamicCanvas(QWidget):
    """Generic canvas that can display any image drawn into a ThreadSafeImage."""
    
    def __init__(self, shared_image: ThreadSafeImage, update_interval_ms: int = 16, scale: int = 1, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.shared_image = shared_image
        self.scale = max(1, scale)
        self.setMinimumSize(shared_image.width * self.scale, shared_image.height * self.scale)
        self.setMaximumSize(shared_image.width * self.scale, shared_image.height * self.scale)

        # Local copy of the image for display
        self._display_image = QImage(
            shared_image.width,
            shared_image.height,
            QImage.Format.Format_RGB888
        )
        self._display_image.fill(0)  # Start with black

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_display)
        self._timer.start(update_interval_ms)

    def _update_display(self) -> None:
        """Copy the current state from shared image and trigger repaint."""
        self._display_image = self.shared_image.copy_to_qimage()
        self.update()

    def paintEvent(self, event):  # type: ignore[override]
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, False)
        target_rect = self.rect()
        source_rect = self._display_image.rect()
        painter.drawImage(target_rect, self._display_image, source_rect)


class DynamicRenderWindow(QMainWindow):
    def __init__(self, width: int = 1024, height: int = 800):
        super().__init__()
        self.setWindowTitle("PyQt dynamic render window")

        # Create shared image that worker will draw into
        self.shared_image = ThreadSafeImage(width, height)
        
        # Create canvas that displays the shared image
        self.canvas = DynamicCanvas(shared_image=self.shared_image, update_interval_ms=20, scale=1)
        self.setCentralWidget(self.canvas)

        # Set up worker thread
        self._worker_thread = QThread(self)
        self._worker = MyDisplayWorker(shared_image=self.shared_image)
        self._worker.moveToThread(self._worker_thread)
        self._worker.finished.connect(self._worker_thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._worker_thread.finished.connect(self._worker_thread.deleteLater)
        self._worker_thread.started.connect(self._worker.run)

        self._worker_thread.start()

    def closeEvent(self, event):  # type: ignore[override]
        self.canvas._timer.stop()
        try:
            self._worker.stop()
            self._worker_thread.quit()
            self._worker_thread.wait(2000)
        except Exception:
            pass

        super().closeEvent(event)


def main() -> int:
    app = QApplication(sys.argv)
    window = DynamicRenderWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
