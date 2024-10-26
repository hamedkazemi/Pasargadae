#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <xcb/xcb.h>
#include <SDL2/SDL.h>

struct ScreenBuffer {
    unsigned char* data;
    int width;
    int height;
    int bytes_per_pixel;
    SDL_Window* window;
    SDL_Renderer* renderer;
    SDL_Texture* texture;
    xcb_connection_t* connection;
    xcb_screen_t* screen;
    xcb_drawable_t root;
};

struct ScreenBuffer* init_screen_capture() {
    struct ScreenBuffer* screen = malloc(sizeof(struct ScreenBuffer));
    if (!screen) {
        return NULL;
    }

    // Initialize XCB connection
    screen->connection = xcb_connect(NULL, NULL);
    if (xcb_connection_has_error(screen->connection)) {
        printf("Cannot open display\n");
        free(screen);
        return NULL;
    }

    // Get the first screen
    screen->screen = xcb_setup_roots_iterator(xcb_get_setup(screen->connection)).data;
    screen->root = screen->screen->root;
    screen->width = screen->screen->width_in_pixels;
    screen->height = screen->screen->height_in_pixels;
    screen->bytes_per_pixel = 4;  // RGBA format

    // Initialize SDL
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL initialization failed: %s\n", SDL_GetError());
        xcb_disconnect(screen->connection);
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
        xcb_disconnect(screen->connection);
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
        xcb_disconnect(screen->connection);
        free(screen);
        return NULL;
    }

    // Create texture
        munmap(screen->fb_data, screen->fb_size);
        close(screen->fb_fd);
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
        munmap(screen->fb_data, screen->fb_size);
        close(screen->fb_fd);
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
        munmap(screen->fb_data, screen->fb_size);
        close(screen->fb_fd);
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
        munmap(screen->fb_data, screen->fb_size);
        close(screen->fb_fd);
        free(screen);
        return NULL;
    }

    // Allocate display buffer
    screen->display_data = malloc(screen->width * screen->height * 4); // RGBA
    if (!screen->display_data) {
        SDL_DestroyTexture(screen->texture);
        SDL_DestroyRenderer(screen->renderer);
        SDL_DestroyWindow(screen->window);
        munmap(screen->fb_data, screen->fb_size);
        close(screen->fb_fd);
        free(screen);
        return NULL;
    }

    return screen;
}

int capture_frame(struct ScreenBuffer* screen) {
    if (!screen || !screen->fb_data || !screen->display_data) {
        return 0;
    }

    // Convert framebuffer format to RGBA
    unsigned char* src = screen->fb_data;
    unsigned char* dst = screen->display_data;
    
    for (int i = 0; i < screen->width * screen->height; i++) {
        // Convert based on framebuffer format
        unsigned short pixel;
        if (screen->vinfo.bits_per_pixel == 16) {
            // RGB565 to RGBA conversion
            pixel = ((unsigned short*)src)[i];
            dst[i * 4 + 0] = ((pixel >> 11) & 0x1F) << 3;  // R
            dst[i * 4 + 1] = ((pixel >> 5) & 0x3F) << 2;   // G
            dst[i * 4 + 2] = (pixel & 0x1F) << 3;          // B
            dst[i * 4 + 3] = 255;                          // A
        } else if (screen->vinfo.bits_per_pixel == 32) {
            // Assuming ARGB or XRGB
            dst[i * 4 + 0] = src[i * 4 + 1];  // R
            dst[i * 4 + 1] = src[i * 4 + 2];  // G
            dst[i * 4 + 2] = src[i * 4 + 3];  // B
            dst[i * 4 + 3] = 255;             // A
        }
    }

    return 1;
}

void render_frame(struct ScreenBuffer* screen) {
    SDL_UpdateTexture(screen->texture, NULL, screen->display_data,
                     screen->width * 4);  // 4 bytes per pixel for RGBA
    SDL_RenderClear(screen->renderer);
    SDL_RenderCopy(screen->renderer, screen->texture, NULL, NULL);
    SDL_RenderPresent(screen->renderer);
}

void capture_loop(struct ScreenBuffer* screen) {
    Uint32 frame_start, frame_time;
    const int target_fps = 30;
    const int frame_delay = 1000 / target_fps;
    SDL_Event event;
    int running = 1;

    printf("Starting capture at %dx%d @ %d fps\n",
           screen->width, screen->height, target_fps);

    while (running) {
        frame_start = SDL_GetTicks();

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
        if (screen->display_data) {
            free(screen->display_data);
        }
        if (screen->fb_data) {
            munmap(screen->fb_data, screen->fb_size);
        }
        if (screen->fb_fd != -1) {
            close(screen->fb_fd);
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
