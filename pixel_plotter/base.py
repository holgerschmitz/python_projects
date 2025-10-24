from typing import Tuple
import numpy as np

from PyQt6.QtCore import QObject, QMutex, QMutexLocker, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QImage

class ThreadSafeImage:
    """Thread-safe wrapper around QImage for pixel-based drawing."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._buffer = np.zeros((height, width, 3), dtype=np.uint8)
        self._mutex = QMutex()
        
    def set_pixel(self, x: int, y: int, r: int, g: int, b: int) -> None:
        """Set a single pixel. Thread-safe."""
        if 0 <= x < self.width and 0 <= y < self.height:
            with QMutexLocker(self._mutex):
                self._buffer[y, x] = [r, g, b]
    
    def set_pixel_rgb(self, x: int, y: int, rgb: Tuple[int, int, int]) -> None:
        """Set a single pixel with RGB tuple. Thread-safe."""
        self.set_pixel(x, y, rgb[0], rgb[1], rgb[2])
    
    def copy_to_qimage(self) -> QImage:
        """Create a copy of the current image data as QImage. Thread-safe."""
        with QMutexLocker(self._mutex):
            buffer_copy = self._buffer.copy()
        
        return QImage(
            buffer_copy.data,
            self.width,
            self.height,
            self.width * 3,
            QImage.Format.Format_RGB888,
        )
    
    def clear(self, r: int = 0, g: int = 0, b: int = 0) -> None:
        """Clear the image with the specified color. Thread-safe."""
        with QMutexLocker(self._mutex):
            self._buffer[:, :] = [r, g, b]


class DisplayWorker(QObject):
    """Base class for workers that draw into a ThreadSafeImage."""
    
    finished = pyqtSignal()
    
    def __init__(self, shared_image: ThreadSafeImage):
        super().__init__()
        self.shared_image = shared_image
        self._abort = False
    
    def stop(self) -> None:
        """Request the worker to stop."""
        self._abort = True
    
    @pyqtSlot()
    def run(self) -> None:
        """Override this method to implement image generation."""
        raise NotImplementedError("Subclasses must implement run()")

