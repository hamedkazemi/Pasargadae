#include "portal.h"
#include "pipewire_capture.h"
#include "display.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define WIDTH 1920
#define HEIGHT 1080

struct Context {
    struct Display* display;
    unsigned char* buffer;
};

static void on_frame(void* user_data, const void* buffer, size_t size)
{
    struct Context* ctx = user_data;
    memcpy(ctx->buffer, buffer, size);
    display_update(ctx->display, ctx->buffer);
}

int main()
{
    GDBusConnection* connection = NULL;
    char* session_handle = NULL;
    struct Context ctx = {0};
    struct PwCapture* capture = NULL;
    int ret = 1;

    // Request screen capture through portal
    uint32_t node_id = portal_request_screen_capture(&connection, &session_handle);
    if (node_id == 0) {
        printf("Failed to get screen capture permission\n");
        goto cleanup;
    }

    // Initialize display
    ctx.display = display_init(WIDTH, HEIGHT);
    if (!ctx.display) {
        printf("Failed to initialize display\n");
        goto cleanup;
    }

    // Allocate frame buffer
    ctx.buffer = malloc(WIDTH * HEIGHT * 4);
    if (!ctx.buffer) {
        printf("Failed to allocate buffer\n");
        goto cleanup;
    }

    // Initialize PipeWire capture
    capture = pw_capture_init(node_id, WIDTH, HEIGHT, &ctx, on_frame);
    if (!capture) {
        printf("Failed to initialize capture\n");
        goto cleanup;
    }

    printf("Starting capture at %dx%d @ 30 fps\n", WIDTH, HEIGHT);

    // Main loop
    while (display_handle_events(ctx.display)) {
        pw_capture_iterate(capture);
        SDL_Delay(1000/30);  // Cap at 30fps
    }

    ret = 0;

cleanup:
    if (capture) {
        pw_capture_cleanup(capture);
    }
    if (ctx.buffer) {
        free(ctx.buffer);
    }
    if (ctx.display) {
        display_cleanup(ctx.display);
    }
    portal_cleanup(connection, session_handle);

    return ret;
}
