#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <SDL2/SDL.h>
#include <X11/Xlib.h>
#include <X11/X.h>

struct ScreenBuffer {
    unsigned char* data;
    int width;
    int height;
    int bytes_per_pixel;
    SDL_Window* window;
    SDL_Renderer* renderer;
    SDL_Texture* texture;
    Display* display;
    Window root;
    XImage* ximage;
};

struct ScreenBuffer* init_screen_capture() {
    struct ScreenBuffer* screen = malloc(sizeof(struct ScreenBuffer));
    if (!screen) {
        return NULL;
    }

    // Initialize X11
    screen->display = XOpenDisplay(NULL);
    if (!screen->display) {
        printf("Cannot open X display\n");
        free(screen);
        return NULL;
    }

    screen->root = DefaultRootWindow(screen->display);
    XWindowAttributes gwa;
    XGetWindowAttributes(screen->display, screen->root, &gwa);
    screen->width = gwa.width;
    screen->height = gwa.height;
    screen->bytes_per_pixel = 4;  // RGBA format

    // Initialize SDL
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL initialization failed: %s\n", SDL_GetError());
        XCloseDisplay(screen->display);
        free(screen);
        return NULL;
    }

    // Create window at half the screen size
    screen->window = SDL_CreateWindow("Screen Capture",
                                    SDL_WINDOWPOS_CENTERED,
                                    SDL_WINDOWPOS_CENTERED,
                                    screen->width / 2,
                                    screen->height / 2,
                                    SDL_WINDOW_SHOWN);
    if (!screen->window) {
        printf("Window creation failed: %s\n", SDL_GetError());
        XCloseDisplay(screen->display);
        free(screen);
        return NULL;
    }

    // Create renderer
    screen->renderer = SDL_CreateRenderer(screen->window, -1,
                                        SDL_RENDERER_ACCELERATED |
                                        SDL_RENDERER_PRESENTVSYNC);
    if (!screen->renderer) {
        printf("Renderer creation failed: %s\n", SDL_GetError());
        SDL_DestroyWindow(screen->window);
        XCloseDisplay(screen->display);
        free(screen);
        return NULL;
    }

    // Create texture
    screen->texture = SDL_CreateTexture(screen->renderer,
                                      SDL_PIXELFORMAT_RGBA32,
                                      SDL_TEXTUREACCESS_STREAMING,
                                      screen->width,
                                      screen->height);
    if (!screen->texture) {
        printf("Texture creation failed: %s\n", SDL_GetError());
        SDL_DestroyRenderer(screen->renderer);
        SDL_DestroyWindow(screen->window);
        XCloseDisplay(screen->display);
        free(screen);
        return NULL;
    }

    // Allocate memory for pixel data
    size_t buffer_size = screen->width * screen->height * screen->bytes_per_pixel;
    screen->data = malloc(buffer_size);
    if (!screen->data) {
        SDL_DestroyTexture(screen->texture);
        SDL_DestroyRenderer(screen->renderer);
        SDL_DestroyWindow(screen->window);
        XCloseDisplay(screen->display);
        free(screen);
        return NULL;
    }

    return screen;
}

int capture_frame(struct ScreenBuffer* screen) {
    if (!screen || !screen->data) {
        return 0;
    }

    // Capture the screen using X11
    screen->ximage = XGetImage(screen->display, screen->root, 0, 0,
                              screen->width, screen->height,
                              AllPlanes, ZPixmap);
    
    if (!screen->ximage) {
        return 0;
    }

    // Convert BGR to RGBA (X11 uses BGR, SDL uses RGBA)
    unsigned char* src = (unsigned char*)screen->ximage->data;
    unsigned char* dst = screen->data;
    
    for (int i = 0; i < screen->width * screen->height; i++) {
        // BGR to RGBA conversion
        dst[i * 4 + 0] = src[i * 4 + 2]; // R
        dst[i * 4 + 1] = src[i * 4 + 1]; // G
        dst[i * 4 + 2] = src[i * 4 + 0]; // B
        dst[i * 4 + 3] = 255;            // A
    }

    XDestroyImage(screen->ximage);
    return 1;
}

void render_frame(struct ScreenBuffer* screen) {

        // Handle events
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = 0;
            }
            if (event.type == SDL_KEYDOWN) {
                if (event.key.keysym.sym == SDLK_ESCAPE) {
                    running = 0;
                }
            }
        }

        if (!capture_frame(screen)) {
            printf("Failed to capture frame\n");
            break;
        }

        render_frame(screen);

        // Cap frame rate
        frame_time = SDL_GetTicks() - frame_start;
        if (frame_delay > frame_time) {
            SDL_Delay(frame_delay - frame_time);
        }
    }
}

void cleanup_screen_capture(struct ScreenBuffer* screen) {
    if (screen) {
        if (screen->data) {
            free(screen->data);
        }
        if (screen->texture) {
            SDL_DestroyTexture(screen->texture);
        }
        if (screen->renderer) {
            SDL_DestroyRenderer(screen->renderer);
        }
        if (screen->window) {
            SDL_DestroyWindow(screen->window);
        }
        SDL_Quit();
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
