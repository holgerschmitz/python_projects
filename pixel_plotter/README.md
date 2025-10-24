# Pixel Plotter - Dynamic Fractal Renderer

This project demonstrates a flexible, thread-safe architecture for rendering fractals in PyQt6. This system supports pixel-based drawing, making it suitable for various fractal types including the Mandelbrot set, fractal ferns, hopalong attractors, and other algorithms that plot pixels at arbitrary locations.

The application uses a worker thread that draws individual pixels into a thread-safe shared image buffer, while the GUI thread periodically copies and displays the current state. This approach provides smooth real-time visualization without freezing the interface.

## Prerequisites

- Python 3.10 or newer (PyQt6 wheels are easiest on recent Python versions)
- A virtual environment is recommended

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the demo

```bash
python main.py
```

When the window opens you can watch the Mandelbrot fractal emerge pixel by pixel as the worker thread computes each point. The rendering progresses smoothly without blocking the user interface.

## Architecture Overview

### Core Components

- **`ThreadSafeImage`:** A thread-safe wrapper around NumPy image data with mutex protection. Provides methods like `set_pixel()` and `set_pixel_rgb()` for safe concurrent pixel access, plus `copy_to_qimage()` for GUI display.

- **`DisplayWorker` (Abstract Base):** Base class for all fractal workers. Manages the shared image reference, provides common lifecycle methods (`stop()`, `finished` signal), and defines the interface that specific fractal implementations must follow.

- **`MandelbrotWorker` (DisplayWorker implementation):** Computes the Mandelbrot set by iterating through each pixel coordinate, calculating the fractal value, and drawing directly into the shared image using `set_pixel_rgb()`.

- **`DynamicCanvas` (QWidget):** Generic display widget that works with any `ThreadSafeImage`. A `QTimer` periodically calls `copy_to_qimage()` to get the current state and triggers repaints. The `paintEvent` simply blits the copied image to the screen.

- **`DynamicRenderWindow` (QMainWindow):** Main application window that coordinates the shared image, canvas, worker thread, and cleanup logic.

### Threading Model

The heavy computation runs entirely on a background thread and never touches Qt painting APIs. The worker draws pixels into the thread-safe shared buffer using mutex-protected operations. The GUI thread periodically copies this data and handles all painting, keeping the interface responsive.

## Extending for Other Fractals

This architecture is designed to support any fractal that can be rendered by setting individual pixels. To add a new fractal type:

```python
class MyFractalWorker(DisplayWorker):
    def __init__(self, shared_image: ThreadSafeImage, my_params):
        super().__init__(shared_image)
        self.my_params = my_params

    @pyqtSlot()
    def run(self) -> None:
        while not self._abort:
            x, y = self.calculate_next_point()  # Your fractal algorithm
            r, g, b = self.calculate_color()    # Your coloring logic
            self.shared_image.set_pixel(x, y, r, g, b)
        self.finished.emit()
```

Examples of fractals that work well with this approach:
- **Fractal Ferns:** Plot points using iterative function systems
- **Hopalong Attractors:** Generate chaotic point sequences
- **Julia Sets:** Similar to Mandelbrot but with different parameters
- **Strange Attractors:** Lorenz, Rössler, and other dynamical systems

## Configuration

You can adjust rendering parameters in `MandelbrotParams` (resolution, iterations, viewport) or modify the timer interval in `DynamicCanvas` to control update frequency and visual responsiveness.

