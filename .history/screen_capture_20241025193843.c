#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wayland-client.h>
#include <SDL2/SDL.h>
#include "wlr-screencopy-unstable-v1-client-protocol.h"

struct ScreenBuffer {
    unsigned char* data;
    int width;
    int height;
    int bytes_per_pixel;
    SDL_Window* window;
    SDL_Renderer* renderer;
    SDL_Texture* texture;
    struct wl_display* display;
    struct wl_registry* registry;
    struct zwlr_screencopy_manager_v1* screencopy_manager;
    struct wl_output* output;
    struct zwlr_screencopy_frame_v1* frame;
    int frame_ready;
};

static void output_handle_geometry(void *data, struct wl_output *wl_output,
        int32_t x, int32_t y, int32_t physical_width, int32_t physical_height,
        int32_t subpixel, const char *make, const char *model, int32_t transform) {
    // Handle output geometry
}

static void output_handle_mode(void *data, struct wl_output *wl_output,
        uint32_t flags, int32_t width, int32_t height, int32_t refresh) {
    struct ScreenBuffer *screen = data;
    if (flags & WL_OUTPUT_MODE_CURRENT) {
        screen->width = width;
        screen->height = height;
    }
}

static void output_handle_done(void *data, struct wl_output *wl_output) {
    // Handle output done
}

static void output_handle_scale(void *data, struct wl_output *wl_output,
        int32_t factor) {
    // Handle output scale
}

static const struct wl_output_listener output_listener = {
    .geometry = output_handle_geometry,
    .mode = output_handle_mode,
    .done = output_handle_done,
    .scale = output_handle_scale,
};

static void registry_handle_global(void *data, struct wl_registry *registry,
        uint32_t name, const char *interface, uint32_t version) {
    struct ScreenBuffer *screen = data;
    
    if (strcmp(interface, wl_output_interface.name) == 0) {
        screen->output = wl_registry_bind(registry, name,
            &wl_output_interface, 1);
        wl_output_add_listener(screen->output, &output_listener, screen);
    } else if (strcmp(interface, zwlr_screencopy_manager_v1_interface.name) == 0) {
        screen->screencopy_manager = wl_registry_bind(registry, name,
            &zwlr_screencopy_manager_v1_interface, 1);
    }
}

static void registry_handle_global_remove(void *data,
        struct wl_registry *registry, uint32_t name) {
    // Handle removal of global objects
}

static const struct wl_registry_listener registry_listener = {
    .global = registry_handle_global,
    .global_remove = registry_handle_global_remove,
};

static void handle_frame_buffer(void *data,
        struct zwlr_screencopy_frame_v1 *frame,
        enum wl_shm_format format, uint32_t width, uint32_t height,
        uint32_t stride) {
    struct ScreenBuffer *screen = data;
    // Allocate buffer for frame data
    screen->data = realloc(screen->data, stride * height);
}

static void handle_frame_flags(void *data,
        struct zwlr_screencopy_frame_v1 *frame, uint32_t flags) {
    // Handle frame flags
}

static void handle_frame_ready(void *data,
        struct zwlr_screencopy_frame_v1 *frame,
        uint32_t tv_sec_hi, uint32_t tv_sec_lo, uint32_t tv_nsec) {
    struct ScreenBuffer *screen = data;
    screen->frame_ready = 1;
}

static const struct zwlr_screencopy_frame_v1_listener frame_listener = {
    .buffer = handle_frame_buffer,
    .flags = handle_frame_flags,
    .ready = handle_frame_ready,
};

struct ScreenBuffer* init_screen_capture() {
    struct ScreenBuffer* screen = calloc(1, sizeof(struct ScreenBuffer));
    if (!screen) {
        return NULL;
    }

    screen->bytes_per_pixel = 4;  // RGBA format
    screen->frame_ready = 0;

    // Connect to Wayland display
    screen->display = wl_display_connect(NULL);
    if (!screen->display) {
        printf("Cannot connect to Wayland display\n");
        free(screen);
        return NULL;
    }

    // Get registry
    screen->registry = wl_display_get_registry(screen->display);
    wl_registry_add_listener(screen->registry, &registry_listener, screen);
    wl_display_roundtrip(screen->display);
    wl_display_roundtrip(screen->display); // Second roundtrip for output modes

    if (!screen->screencopy_manager || !screen->output) {
        printf("Compositor doesn't support screen capture\n");
        wl_display_disconnect(screen->display);
        free(screen);
        return NULL;
    }

    // Initialize SDL
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL initialization failed: %s\n", SDL_GetError());
        wl_display_disconnect(screen->display);
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
        SDL_Quit();
        wl_display_disconnect(screen->display);
        free(screen);
        return NULL;
    }

    screen->renderer = SDL_CreateRenderer(screen->window, -1,
                                        SDL_RENDERER_ACCELERATED |
                                        SDL_RENDERER_PRESENTVSYNC);
    if (!screen->renderer) {
        printf("Renderer creation failed: %s\n", SDL_GetError());
        SDL_DestroyWindow(screen->window);
        SDL_Quit();
        wl_display_disconnect(screen->display);
        free(screen);
        return NULL;
    }

    screen->texture = SDL_CreateTexture(screen->renderer,
                                      SDL_PIXELFORMAT_RGBA32,
                                      SDL_TEXTUREACCESS_STREAMING,
                                      screen->width,
                                      screen->height);
    if (!screen->texture) {
        printf("Texture creation failed: %s\n", SDL_GetError());
        SDL_DestroyRenderer(screen->renderer);
        SDL_DestroyWindow(screen->window);
        SDL_Quit();
        wl_display_disconnect(screen->display);
        free(screen);
        return NULL;
    }

    return screen;
}

int capture_frame(struct ScreenBuffer* screen) {
    if (!screen || !screen->screencopy_manager || !screen->output) {
        return 0;
    }

    screen->frame_ready = 0;
    screen->frame = zwlr_screencopy_manager_v1_capture_output(
        screen->screencopy_manager, 0, screen->output);
    
    zwlr_screencopy_frame_v1_add_listener(screen->frame, &frame_listener, screen);

    while (!screen->frame_ready) {
        wl_display_dispatch(screen->display);
    }

    zwlr_screencopy_frame_v1_destroy(screen->frame);
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
        if (screen->output) {
            wl_output_destroy(screen->output);
        }
        if (screen->screencopy_manager) {
            zwlr_screencopy_manager_v1_destroy(screen->screencopy_manager);
        }
        if (screen->registry) {
            wl_registry_destroy(screen->registry);
        }
        if (screen->display) {
            wl_display_disconnect(screen->display);
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
