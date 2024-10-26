#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <SDL2/SDL.h>

struct ScreenBuffer {
    unsigned char* data;
    int width;
    int height;
    int bytes_per_pixel;
    SDL_Window* window;
    SDL_Renderer* renderer;
    SDL_Texture* texture;
};

struct ScreenBuffer* init_screen_capture() {
    struct ScreenBuffer* screen = malloc(sizeof(struct ScreenBuffer));
    if (!screen) {
        return NULL;
    }

    // Initialize SDL
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL initialization failed: %s\n", SDL_GetError());
        free(screen);
        return NULL;
    }

    // Get current display mode
    SDL_DisplayMode dm;
    if (SDL_GetCurrentDisplayMode(0, &dm) != 0) {
        printf("SDL_GetCurrentDisplayMode failed: %s\n", SDL_GetError());
        free(screen);
        return NULL;
    }

    screen->width = dm.w;
    screen->height = dm.h;
    screen->bytes_per_pixel = 4;  // RGBA format

    // Create window at half the screen size
    screen->window = SDL_CreateWindow("Screen Capture",
                                    SDL_WINDOWPOS_CENTERED,
                                    SDL_WINDOWPOS_CENTERED,
                                    screen->width / 2,
                                    screen->height / 2,
                                    SDL_WINDOW_SHOWN);
    if (!screen->window) {
        printf("Window creation failed: %s\n", SDL_GetError());
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
        free(screen);
        return NULL;
    }

    return screen;
}

int capture_frame(struct ScreenBuffer* screen) {
    if (!screen || !screen->data) {
        return 0;
    }

    SDL_Surface* screenshot = SDL_CreateRGBSurface(0, screen->width, screen->height, 32,
                                                 0x00FF0000,
                                                 0x0000FF00,
                                                 0x000000FF,
                                                 0xFF000000);
    if (!screenshot) {
        return 0;
    }

    if (SDL_RenderReadPixels(screen->renderer, NULL, SDL_PIXELFORMAT_RGBA32,
                            screen->data, screen->width * 4) != 0) {
        SDL_FreeSurface(screenshot);
        return 0;
    }

    SDL_FreeSurface(screenshot);
    return 1;
}

void render_frame(struct ScreenBuffer* screen) {
    SDL_UpdateTexture(screen->texture, NULL, screen->data,
                     screen->width * screen->bytes_per_pixel);
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
