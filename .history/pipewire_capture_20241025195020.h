#ifndef PIPEWIRE_CAPTURE_H
#define PIPEWIRE_CAPTURE_H

#include <pipewire/pipewire.h>
#include <stdint.h>

struct PwCapture {
    struct pw_loop* loop;
    struct pw_stream* stream;
    struct pw_context* context;
    struct spa_hook stream_listener;
    void* user_data;
    void (*on_frame)(void* user_data, const void* buffer, size_t size);
};

// Initialize PipeWire capture
struct PwCapture* pw_capture_init(uint32_t node_id, int width, int height,
                                void* user_data,
                                void (*on_frame)(void* user_data, const void* buffer, size_t size));

// Process one iteration of the capture loop
void pw_capture_iterate(struct PwCapture* capture);

// Cleanup PipeWire resources
void pw_capture_cleanup(struct PwCapture* capture);

#endif // PIPEWIRE_CAPTURE_H
