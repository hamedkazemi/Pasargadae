#include <X11/Xlib.h>
#include <X11/X.h>
#include <chrono>
#include <thread>
#include <iostream>

class ScreenCapture {
private:
    Display* display;
    Window root;
    XImage* image;
    int width;
    int height;

public:
    ScreenCapture() {
        display = XOpenDisplay(nullptr);
        if (!display) {
            throw std::runtime_error("Failed to open X display");
        }
        
        root = DefaultRootWindow(display);
        XWindowAttributes attributes;
        XGetWindowAttributes(display, root, &attributes);
        
        width = attributes.width;
        height = attributes.height;
    }

    ~ScreenCapture() {
        if (display) {
            XCloseDisplay(display);
        }
    }

    void captureFrame() {
        image = XGetImage(display, root, 0, 0, width, height, AllPlanes, ZPixmap);
        if (!image) {
            throw std::runtime_error("Failed to capture screen");
        }

        // Here you can process the pixels
        // image->data contains the raw pixel data
        // Each pixel is 4 bytes (BGRA format)
        
        XDestroyImage(image);
    }

    void run() {
        const auto frame_duration = std::chrono::milliseconds(1000 / 30); // 30 FPS
        auto next_frame = std::chrono::steady_clock::now();

        while (true) {
            try {
                captureFrame();
                
                // Wait until next frame
                next_frame += frame_duration;
                std::this_thread::sleep_until(next_frame);
                
            } catch (const std::exception& e) {
                std::cerr << "Error: " << e.what() << std::endl;
                break;
            }
        }
    }
};

int main() {
    try {
        ScreenCapture capture;
        capture.run();
    } catch (const std::exception& e) {
        std::cerr << "Fatal error: " << e.what() << std::endl;
        return 1;
    }
    return 0;
}
