#include "display.h"
#include <stdlib.h>

struct Display* display_init(int width, int height)
{
    struct Display* display = calloc(1, sizeof(struct Display));
    if (!display)
        return NULL;

    display->width = width;
    display->height = height;

    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        free(display);
        return NULL;
    }

    display->window = SDL_CreateWindow("Screen Capture",
                                     SDL_WINDOWPOS_CENTERED,
                                     SDL_WINDOWPOS_CENTERED,
                                     width / 2,
                                     height / 2,
                                     SDL_WINDOW_SHOWN);
    if (!display->window) {
        SDL_Quit();
        free(display);
        return NULL;
    }

    display->renderer = SDL_CreateRenderer(display->window, -1,
                                         SDL_RENDERER_ACCELERATED |
                                         SDL_RENDERER_PRESENTVSYNC);
    if (!display->renderer) {
        SDL_DestroyWindow(display->window);
        SDL_Quit();
        free(display);
        return NULL;
    }

    display->texture = SDL_CreateTexture(display->renderer,
                                       SDL_PIXELFORMAT_RGBA32,
                                       SDL_TEXTUREACCESS_STREAMING,
                                       width,
                                       height);
    if (!display->texture) {
        SDL_DestroyRenderer(display->renderer);
        SDL_DestroyWindow(display->window);
        SDL_Quit();
        free(display);
        return NULL;
    }

    return display;
}

void display_update(struct Display* display, const void* pixels)
{
    SDL_UpdateTexture(display->texture, NULL, pixels,
                     display->width * 4);  // 4 bytes per pixel
    SDL_RenderClear(display->renderer);
    SDL_RenderCopy(display->renderer, display->texture, NULL, NULL);
    SDL_RenderPresent(display->renderer);
}

int display_handle_events(struct Display* display)
{
    SDL_Event event;
    while (SDL_PollEvent(&event)) {
        if (event.type == SDL_QUIT) {
            return 0;
        }
        if (event.type == SDL_KEYDOWN) {
            if (event.key.keysym.sym == SDLK_ESCAPE) {
                return 0;
            }
        }
    }
    return 1;
}

void display_cleanup(struct Display* display)
{
    if (display) {
        if (display->texture) {
            SDL_DestroyTexture(display->texture);
        }
        if (display->renderer) {
            SDL_DestroyRenderer(display->renderer);
        }
        if (display->window) {
            SDL_DestroyWindow(display->window);
        }
        SDL_Quit();
        free(display);
    }
}
