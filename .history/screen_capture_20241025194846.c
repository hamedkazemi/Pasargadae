#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <gio/gio.h>
#include <pipewire/pipewire.h>
#include <spa/param/video/format-utils.h>
#include <spa/debug/types.h>
#include <SDL2/SDL.h>

#define PORTAL_BUS_NAME "org.freedesktop.portal.Desktop"
#define PORTAL_OBJECT_PATH "/org/freedesktop/portal/desktop"
#define PORTAL_INTERFACE "org.freedesktop.portal.ScreenCast"

struct ScreenBuffer {
    unsigned char* data;
    int width;
    int height;
    int bytes_per_pixel;
    SDL_Window* window;
    SDL_Renderer* renderer;
    SDL_Texture* texture;
    struct pw_loop* loop;
    struct pw_stream* stream;
    struct pw_context* context;
    struct spa_hook stream_listener;
    GDBusConnection* dbus_connection;
    char* session_handle;
    uint32_t node_id;
};

static void handle_stream_param_changed(void* data, uint32_t id, const struct spa_pod* param)
{
    struct ScreenBuffer* screen = data;
    if (param == NULL || id != SPA_PARAM_Format)
        return;

    uint32_t media_type;
    uint32_t media_subtype;
    
    if (spa_format_parse(param, &media_type, &media_subtype) < 0)
        return;

    if (media_type != SPA_MEDIA_TYPE_video || 
        media_subtype != SPA_MEDIA_SUBTYPE_raw)
        return;

    struct spa_video_info_raw video_info = { 0 };
    if (spa_format_video_raw_parse(param, &video_info) < 0)
        return;

    screen->width = video_info.size.width;
    screen->height = video_info.size.height;
}

static void capture_process(void* userdata)
{
    struct ScreenBuffer* screen = userdata;
    struct pw_buffer* buf;
    struct spa_buffer* spa_buf;

    if ((buf = pw_stream_dequeue_buffer(screen->stream)) == NULL) {
        printf("Out of buffers\n");
        return;
    }

    spa_buf = buf->buffer;
    if (spa_buf->datas[0].data == NULL)
        return;

    // Copy frame data
    void* src = spa_buf->datas[0].data;
    if (src) {
        memcpy(screen->data, src, screen->width * screen->height * screen->bytes_per_pixel);
    }

    pw_stream_queue_buffer(screen->stream, buf);
}

static const struct pw_stream_events stream_events = {
    PW_VERSION_STREAM_EVENTS,
    .param_changed = handle_stream_param_changed,
    .process = capture_process,
};

static gboolean request_session(struct ScreenBuffer* screen, GError** error)
{
    GVariantBuilder builder;
    g_variant_builder_init(&builder, G_VARIANT_TYPE_VARDICT);
    
    // Add session options
    g_variant_builder_add(&builder, "{sv}", "handle_token",
                         g_variant_new_string("screen_capture_token"));
    g_variant_builder_add(&builder, "{sv}", "session_handle_token",
                         g_variant_new_string("screen_capture_session"));

    GVariant* options = g_variant_builder_end(&builder);
    
    // Call CreateSession
    GVariant* result = g_dbus_connection_call_sync(
        screen->dbus_connection,
        PORTAL_BUS_NAME,
        PORTAL_OBJECT_PATH,
        PORTAL_INTERFACE,
        "CreateSession",
        g_variant_new("(a{sv})", options),
        G_VARIANT_TYPE("(o)"),
        G_DBUS_CALL_FLAGS_NONE,
        -1,
        NULL,
        error
    );

    if (!result)
        return FALSE;

    gchar* session_handle;
    g_variant_get(result, "(&o)", &session_handle);
    screen->session_handle = g_strdup(session_handle);
    g_variant_unref(result);

    return TRUE;
}

static gboolean select_sources(struct ScreenBuffer* screen, GError** error)
{
    GVariantBuilder builder;
    g_variant_builder_init(&builder, G_VARIANT_TYPE_VARDICT);
    
    // Add source type (monitor for screen capture)
    g_variant_builder_add(&builder, "{sv}", "types",
                         g_variant_new_uint32(1)); // 1 = monitor
    g_variant_builder_add(&builder, "{sv}", "multiple",
                         g_variant_new_boolean(FALSE));
    g_variant_builder_add(&builder, "{sv}", "cursor_mode",
                         g_variant_new_uint32(1)); // 1 = embedded

    GVariant* options = g_variant_builder_end(&builder);
    
    // Call SelectSources
    GVariant* result = g_dbus_connection_call_sync(
        screen->dbus_connection,
        PORTAL_BUS_NAME,
        PORTAL_OBJECT_PATH,
        PORTAL_INTERFACE,
        "SelectSources",
        g_variant_new("(oa{sv})", screen->session_handle, options),
        NULL,
        G_DBUS_CALL_FLAGS_NONE,
        -1,
        NULL,
        error
    );

    if (!result)
        return FALSE;

    g_variant_unref(result);
    return TRUE;
}

static gboolean start_screencast(struct ScreenBuffer* screen, GError** error)
{
    GVariantBuilder builder;
    g_variant_builder_init(&builder, G_VARIANT_TYPE_VARDICT);
    
    // Add restore token
    g_variant_builder_add(&builder, "{sv}", "restore_token",
                         g_variant_new_string("screen_capture_restore"));

    GVariant* options = g_variant_builder_end(&builder);
    
    // Call Start
    GVariant* result = g_dbus_connection_call_sync(
        screen->dbus_connection,
        PORTAL_BUS_NAME,
        PORTAL_OBJECT_PATH,
        PORTAL_INTERFACE,
        "Start",
        g_variant_new("(osa{sv})", screen->session_handle, "", options),
        G_VARIANT_TYPE("(u)"),
        G_DBUS_CALL_FLAGS_NONE,
        -1,
        NULL,
        error
    );

    if (!result)
        return FALSE;

    guint32 node_id;
    g_variant_get(result, "(u)", &node_id);
    screen->node_id = node_id;
    g_variant_unref(result);

    return TRUE;
}

struct ScreenBuffer* init_screen_capture() {
    struct ScreenBuffer* screen = calloc(1, sizeof(struct ScreenBuffer));
    if (!screen) {
        return NULL;
    }

    screen->width = 1920;  // Default resolution
    screen->height = 1080;
    screen->bytes_per_pixel = 4;  // RGBA format

    // Initialize GIO
    GError* error = NULL;
    screen->dbus_connection = g_bus_get_sync(G_BUS_TYPE_SESSION, NULL, &error);
    if (!screen->dbus_connection) {
        printf("Failed to connect to D-Bus: %s\n", error->message);
        g_error_free(error);
        free(screen);
        return NULL;
    }

    // Request screen capture permission through portal
    if (!request_session(screen, &error) ||
        !select_sources(screen, &error) ||
        !start_screencast(screen, &error)) {
        printf("Failed to get screen capture permission: %s\n", error->message);
        g_error_free(error);
        g_object_unref(screen->dbus_connection);
        free(screen);
        return NULL;
    }

    // Initialize PipeWire
    pw_init(NULL, NULL);
    
    screen->loop = pw_loop_new(NULL);
    if (!screen->loop) {
        g_object_unref(screen->dbus_connection);
        free(screen);
        return NULL;
    }

    screen->context = pw_context_new(screen->loop, NULL, 0);
    if (!screen->context) {
        pw_loop_destroy(screen->loop);
        g_object_unref(screen->dbus_connection);
        free(screen);
        return NULL;
    }

    struct pw_properties* props = pw_properties_new(
        PW_KEY_MEDIA_TYPE, "Video",
        PW_KEY_MEDIA_CATEGORY, "Capture",
        PW_KEY_MEDIA_ROLE, "Screen",
        NULL);

    screen->stream = pw_stream_new_simple(
        screen->loop,
        "screen-capture",
        props,
        &stream_events,
        screen);

    if (!screen->stream) {
        pw_context_destroy(screen->context);
        pw_loop_destroy(screen->loop);
        g_object_unref(screen->dbus_connection);
        free(screen);
        return NULL;
    }

    // Initialize SDL
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL initialization failed: %s\n", SDL_GetError());
        pw_stream_destroy(screen->stream);
        pw_context_destroy(screen->context);
        pw_loop_destroy(screen->loop);
        g_object_unref(screen->dbus_connection);
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
        pw_stream_destroy(screen->stream);
        pw_context_destroy(screen->context);
        pw_loop_destroy(screen->loop);
        g_object_unref(screen->dbus_connection);
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
        pw_stream_destroy(screen->stream);
        pw_context_destroy(screen->context);
        pw_loop_destroy(screen->loop);
        g_object_unref(screen->dbus_connection);
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
        pw_stream_destroy(screen->stream);
        pw_context_destroy(screen->context);
        pw_loop_destroy(screen->loop);
        g_object_unref(screen->dbus_connection);
        free(screen);
        return NULL;
    }

    // Allocate memory for pixel data
    screen->data = malloc(screen->width * screen->height * screen->bytes_per_pixel);
    if (!screen->data) {
        SDL_DestroyTexture(screen->texture);
        SDL_DestroyRenderer(screen->renderer);
        SDL_DestroyWindow(screen->window);
        SDL_Quit();
        pw_stream_destroy(screen->stream);
        pw_context_destroy(screen->context);
        pw_loop_destroy(screen->loop);
        g_object_unref(screen->dbus_connection);
        free(screen);
        return NULL;
    }

    // Setup stream parameters
    uint8_t buffer[1024];
    struct spa_pod_builder b = SPA_POD_BUILDER_INIT(buffer, sizeof(buffer));
    const struct spa_pod* params[1];
    params[0] = spa_pod_builder_add_object(&b,
        SPA_TYPE_OBJECT_Format, SPA_PARAM_EnumFormat,
        SPA_FORMAT_mediaType, SPA_POD_Id(SPA_MEDIA_TYPE_video),
        SPA_FORMAT_mediaSubtype, SPA_POD_Id(SPA_MEDIA_SUBTYPE_raw),
        SPA_FORMAT_VIDEO_format, SPA_POD_Id(SPA_VIDEO_FORMAT_RGBA),
        SPA_FORMAT_VIDEO_size, SPA_POD_Rectangle(&SPA_RECTANGLE(screen->width, screen->height)),
        SPA_FORMAT_VIDEO_framerate, SPA_POD_Fraction(&SPA_FRACTION(30, 1)));

    pw_stream_connect(screen->stream,
        PW_DIRECTION_INPUT,
        screen->node_id,  // Use the node ID from portal
        PW_STREAM_FLAG_AUTOCONNECT |
        PW_STREAM_FLAG_MAP_BUFFERS,
        params, 1);

    return screen;
}

void render_frame(struct ScreenBuffer* screen) {
    SDL_UpdateTexture(screen->texture, NULL, screen->data,
                     screen->width * screen->bytes_per_pixel);
    SDL_RenderClear(screen->renderer);
    SDL_RenderCopy(screen->renderer, screen->texture, NULL, NULL);
    SDL_RenderPresent(screen->renderer);
}

void capture_loop(struct ScreenBuffer* screen) {
    SDL_Event event;
    int running = 1;

    printf("Starting capture at %dx%d @ 30 fps\n",
           screen->width, screen->height);

    while (running) {
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

        pw_loop_iterate(screen->loop, 0);
        render_frame(screen);
        SDL_Delay(1000/30);  // Cap at 30fps
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
        if (screen->stream) {
            pw_stream_destroy(screen->stream);
        }
        if (screen->context) {
            pw_context_destroy(screen->context);
        }
        if (screen->loop) {
            pw_loop_destroy(screen->loop);
        }
        if (screen->session_handle) {
            g_free(screen->session_handle);
        }
        if (screen->dbus_connection) {
            g_object_unref(screen->dbus_connection);
        }
        SDL_Quit();
        pw_deinit();
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
