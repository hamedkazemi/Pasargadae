#include <windows.h>
#include <iostream>
#include <chrono>
#include <thread>
#include <vector>

class ScreenCapture {
private:
    HDC hdcScreen;
    HDC hdcMemory;
    HBITMAP hbmScreen;
    int width;
    int height;
    std::vector<BYTE> buffer;

public:
    ScreenCapture() {
        // Get screen dimensions
        width = GetSystemMetrics(SM_CXSCREEN);
        height = GetSystemMetrics(SM_CYSCREEN);
        
        // Initialize GDI objects
        hdcScreen = GetDC(NULL);
        hdcMemory = CreateCompatibleDC(hdcScreen);
        
        if (!hdcScreen || !hdcMemory) {
            throw std::runtime_error("Failed to initialize screen capture");
        }

        // Create compatible bitmap
        hbmScreen = CreateCompatibleBitmap(hdcScreen, width, height);
        if (!hbmScreen) {
            throw std::runtime_error("Failed to create compatible bitmap");
        }

        SelectObject(hdcMemory, hbmScreen);
        
        // Initialize buffer for pixel data
        buffer.resize(width * height * 4); // 4 bytes per pixel (RGBA)
    }

    ~ScreenCapture() {
        if (hbmScreen) DeleteObject(hbmScreen);
        if (hdcMemory) DeleteDC(hdcMemory);
        if (hdcScreen) ReleaseDC(NULL, hdcScreen);
    }

    void captureFrame() {
        // Copy screen to memory DC
        if (!BitBlt(hdcMemory, 0, 0, width, height, hdcScreen, 0, 0, SRCCOPY)) {
            throw std::runtime_error("Failed to capture screen");
        }

        BITMAPINFOHEADER bi = {0};
        bi.biSize = sizeof(BITMAPINFOHEADER);
        bi.biWidth = width;
        bi.biHeight = -height;  // Top-down image
        bi.biPlanes = 1;
        bi.biBitCount = 32;
        bi.biCompression = BI_RGB;

        // Get the actual bits
        if (!GetDIBits(hdcMemory, hbmScreen, 0, height, buffer.data(), 
                      (BITMAPINFO*)&bi, DIB_RGB_COLORS)) {
            throw std::runtime_error("Failed to get pixel data");
        }

        // At this point, buffer contains the pixel data
        // Each pixel is 4 bytes (RGBA format)
        // You can process the pixels here
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

    // Getter methods for dimensions
    int getWidth() const { return width; }
    int getHeight() const { return height; }
    const std::vector<BYTE>& getBuffer() const { return buffer; }
};

int main() {
    try {
        ScreenCapture capture;
        std::cout << "Starting screen capture at " 
                  << capture.getWidth() << "x" << capture.getHeight() 
                  << " @ 30fps\n";
        capture.run();
    } catch (const std::exception& e) {
        std::cerr << "Fatal error: " << e.what() << std::endl;
        return 1;
    }
    return 0;
}
