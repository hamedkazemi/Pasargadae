#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#ifdef _WIN32
#include <windows.h>
#else
#include <unistd.h>
#endif

// Structure to hold screen capture data
struct ScreenBuffer {
    unsigned char* data;
    int width;
    int height;
    int bytes_per_pixel;
};

// Initialize screen capture
struct ScreenBuffer* init_screen_capture() {
    struct ScreenBuffer* screen = malloc(sizeof(struct ScreenBuffer));
    if (!screen) {
        return NULL;
    }

    #ifdef _WIN32
    screen->width = GetSystemMetrics(SM_CXSCREEN);
    screen->height = GetSystemMetrics(SM_CYSCREEN);
    #else
    // For other systems, you might want to implement a different way
    // to get screen dimensions or allow user input
    screen->width = 1920;  // default resolution
    screen->height = 1080;
    #endif

    screen->bytes_per_pixel = 4;  // RGBA format
    
    // Allocate memory for pixel data
    size_t buffer_size = screen->width * screen->height * screen->bytes_per_pixel;
    screen->data = malloc(buffer_size);
    
    if (!screen->data) {
        free(screen);
        return NULL;
    }

    return screen;
}

// Capture single frame
int capture_frame(struct ScreenBuffer* screen) {
    if (!screen || !screen->data) {
        return 0;
    }

    #ifdef _WIN32
    HDC hdc = GetDC(NULL);
    HDC memdc = CreateCompatibleDC(hdc);
    HBITMAP hbmp = CreateCompatibleBitmap(hdc, screen->width, screen->height);
    
    SelectObject(memdc, hbmp);
    BitBlt(memdc, 0, 0, screen->width, screen->height, hdc, 0, 0, SRCCOPY);

    BITMAPINFOHEADER bmi = {0};
    bmi.biSize = sizeof(BITMAPINFOHEADER);
    bmi.biWidth = screen->width;
    bmi.biHeight = -screen->height;  // Top-down
    bmi.biPlanes = 1;
    bmi.biBitCount = 32;
    bmi.biCompression = BI_RGB;

    GetDIBits(memdc, hbmp, 0, screen->height, screen->data, (BITMAPINFO*)&bmi, DIB_RGB_COLORS);

    DeleteObject(hbmp);
    DeleteDC(memdc);
    ReleaseDC(NULL, hdc);
    #else
    // For other systems, implement appropriate screen capture method
    // This is just a placeholder that fills the buffer with a pattern
    for (int i = 0; i < screen->width * screen->height * screen->bytes_per_pixel; i++) {
        screen->data[i] = i % 256;
    }
    #endif

    return 1;
}

// Sleep function for frame timing
void sleep_ms(int milliseconds) {
    #ifdef _WIN32
    Sleep(milliseconds);
    #else
    usleep(milliseconds * 1000);
    #endif
}

// Calculate time difference in milliseconds
double time_diff_ms(struct timespec start, struct timespec end) {
    return (end.tv_sec - start.tv_sec) * 1000.0 + 
           (end.tv_nsec - start.tv_nsec) / 1000000.0;
}

// Main capture loop
void capture_loop(struct ScreenBuffer* screen) {
    const int target_fps = 30;
    const int frame_time = 1000 / target_fps; // time per frame in milliseconds
    struct timespec frame_start, frame_end;
    
    printf("Starting capture at %dx%d @ %d fps\n", 
           screen->width, screen->height, target_fps);

    while (1) {
        clock_gettime(CLOCK_MONOTONIC, &frame_start);
        
        if (!capture_frame(screen)) {
            printf("Failed to capture frame\n");
            break;
        }

        // Here you can process screen->data which contains the pixel data
        // Each pixel is 4 bytes (RGBA format)
        
        clock_gettime(CLOCK_MONOTONIC, &frame_end);
        
        // Calculate sleep time to maintain target FPS
        double elapsed = time_diff_ms(frame_start, frame_end);
        if (elapsed < frame_time) {
            sleep_ms((int)(frame_time - elapsed));
        }
    }
}

// Cleanup
void cleanup_screen_capture(struct ScreenBuffer* screen) {
    if (screen) {
        if (screen->data) {
            free(screen->data);
        }
        free(screen);
    }
}

int main() {
    struct ScreenBuffer* screen = init_screen_capture();
    if (!screen) {
        printf("Failed to initialize screen capture\n");
        return 1;
    }

    capture_loop(screen);
    cleanup_screen_capture(screen);
    return 0;
}
