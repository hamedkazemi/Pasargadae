#include "pipewire_capture.h"
#include <spa/param/video/format-utils.h>
#include <stdio.h>
#include <stdlib.h>

static void capture_process(void* userdata)
{
    struct PwCapture* capture = userdata;
    struct pw_buffer* buf;
    struct spa_buffer* spa_buf;

    if ((buf = pw_stream_dequeue_buffer(capture->stream)) == NULL) {
        printf("Out of buffers\n");
        return;
    }

    spa_buf = buf->buffer;
    if (spa_buf->datas[0].data == NULL)
        return;

    // Call the frame callback
    if (capture->on_frame) {
        capture->on_frame(capture->user_data, spa_buf->datas[0].data,
                         spa_buf->datas[0].maxsize);
    }

    pw_stream_queue_buffer(capture->stream, buf);
}

static const struct pw_stream_events stream_events = {
    PW_VERSION_STREAM_EVENTS,
    .process = capture_process,
};

struct PwCapture* pw_capture_init(uint32_t node_id, int width, int height,
                                void* user_data,
                                void (*on_frame)(void* user_data, const void* buffer, size_t size))
{
    struct PwCapture* capture = calloc(1, sizeof(struct PwCapture));
    if (!capture)
        return NULL;

    capture->user_data = user_data;
    capture->on_frame = on_frame;

    pw_init(NULL, NULL);
    
    capture->loop = pw_loop_new(NULL);
    if (!capture->loop) {
        free(capture);
        return NULL;
    }

    capture->context = pw_context_new(capture->loop, NULL, 0);
    if (!capture->context) {
        pw_loop_destroy(capture->loop);
        free(capture);
        return NULL;
    }

    struct pw_properties* props = pw_properties_new(
        PW_KEY_MEDIA_TYPE, "Video",
        PW_KEY_MEDIA_CATEGORY, "Capture",
        PW_KEY_MEDIA_ROLE, "Screen",
        NULL);

    capture->stream = pw_stream_new_simple(
        capture->loop,
        "screen-capture",
        props,
        &stream_events,
        capture);

    if (!capture->stream) {
        pw_context_destroy(capture->context);
        pw_loop_destroy(capture->loop);
        free(capture);
        return NULL;
    }

    uint8_t buffer[1024];
    struct spa_pod_builder b = SPA_POD_BUILDER_INIT(buffer, sizeof(buffer));
    const struct spa_pod* params[1];
    params[0] = spa_pod_builder_add_object(&b,
        SPA_TYPE_OBJECT_Format, SPA_PARAM_EnumFormat,
        SPA_FORMAT_mediaType, SPA_POD_Id(SPA_MEDIA_TYPE_video),
        SPA_FORMAT_mediaSubtype, SPA_POD_Id(SPA_MEDIA_SUBTYPE_raw),
        SPA_FORMAT_VIDEO_format, SPA_POD_Id(SPA_VIDEO_FORMAT_RGBA),
        SPA_FORMAT_VIDEO_size, SPA_POD_Rectangle(&SPA_RECTANGLE(width, height)),
        SPA_FORMAT_VIDEO_framerate, SPA_POD_Fraction(&SPA_FRACTION(30, 1)));

    pw_stream_connect(capture->stream,
        PW_DIRECTION_INPUT,
        node_id,
        PW_STREAM_FLAG_AUTOCONNECT |
        PW_STREAM_FLAG_MAP_BUFFERS,
        params, 1);

    return capture;
}

void pw_capture_iterate(struct PwCapture* capture)
{
    pw_loop_iterate(capture->loop, 0);
}

void pw_capture_cleanup(struct PwCapture* capture)
{
    if (capture) {
        if (capture->stream) {
            pw_stream_destroy(capture->stream);
        }
        if (capture->context) {
            pw_context_destroy(capture->context);
        }
        if (capture->loop) {
            pw_loop_destroy(capture->loop);
        }
        pw_deinit();
        free(capture);
    }
}
