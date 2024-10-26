#ifndef DISPLAY_H
#define DISPLAY_H

#include <SDL2/SDL.h>

struct Display {
    SDL_Window* window;
    SDL_Renderer* renderer;
    SDL_Texture* texture;
    int width;
    int height;
};

// Initialize SDL display
struct Display* display_init(int width, int height);

// Update display with new frame data
void display_update(struct Display* display, const void* pixels);

// Process SDL events, returns 0 if should quit
int display_handle_events(struct Display* display);

// Cleanup display resources
void display_cleanup(struct Display* display);

#endif // DISPLAY_H
