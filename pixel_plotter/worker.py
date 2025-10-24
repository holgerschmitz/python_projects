from typing import Tuple
from dataclasses import dataclass
from math import sqrt

from base import DisplayWorker, ThreadSafeImage

from PyQt6.QtCore import pyqtSlot

@dataclass(frozen=True)
class DisplayParams:
    width: int = 1024
    height: int = 800
    max_iter: int = 100
    xmin: float = -2.1
    xmax: float = 0.9
    ymin: float = -1.2
    ymax: float = 1.2

class MyDisplayWorker(DisplayWorker):
    def __init__(self, shared_image: ThreadSafeImage):
        super().__init__(shared_image)
        self.params = DisplayParams()

    @pyqtSlot()
    def run(self) -> None:
        p = self.params
        for y in range(p.height):
            if self._abort:
                break
            
            for x in range(p.width):
                cx, cy = self.coord_from_pixel(x, y)
                # do some calculation
                color = self._colorize(10)
                self.shared_image.set_pixel_rgb(x, y, color)
        self.finished.emit()
    
    def coord_from_pixel(self, x: int, y: int) -> Tuple[float, float]:
        p = self.params
        cx = p.xmin + (x / (p.width - 1)) * (p.xmax - p.xmin)
        cy = p.ymin + (y / (p.height - 1)) * (p.ymax - p.ymin)
        return cx, cy

    def _colorize(self, n: int) -> Tuple[int, int, int]:
        if n >= self.params.max_iter:
            return 0, 0, 0
        t = n / self.params.max_iter
        r = int(10*n) % 256
        g = int(sqrt(20*n)) % 256
        b = 255 - r
        return r, g, b
