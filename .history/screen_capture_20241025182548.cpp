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
