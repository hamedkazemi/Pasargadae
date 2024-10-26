#include "portal.h"
#include <stdio.h>

#define PORTAL_BUS_NAME "org.freedesktop.portal.Desktop"
#define PORTAL_OBJECT_PATH "/org/freedesktop/portal/desktop"
#define PORTAL_INTERFACE "org.freedesktop.portal.ScreenCast"
#define REQUEST_PATH "/org/freedesktop/portal/desktop/request"
#define SESSION_PATH "/org/freedesktop/portal/desktop/session"

static void wait_for_response(GDBusConnection* connection, const char* path)
{
    GMainContext* context = g_main_context_new();
    GMainLoop* loop = g_main_loop_new(context, FALSE);
    g_main_context_push_thread_default(context);

    // Wait a bit for the portal to process the request
    g_timeout_add(1000, (GSourceFunc)g_main_loop_quit, loop);
    g_main_loop_run(loop);

    g_main_context_pop_thread_default(context);
    g_main_loop_unref(loop);
    g_main_context_unref(context);
}

static gboolean request_session(GDBusConnection* connection, char** session_handle, GError** error)
{
    GVariantBuilder builder;
    g_variant_builder_init(&builder, G_VARIANT_TYPE_VARDICT);
    
    // Add session options
    g_variant_builder_add(&builder, "{sv}", "session_handle_token",
                         g_variant_new_string("screen_capture_session"));

    GVariant* options = g_variant_builder_end(&builder);
    
    // Call CreateSession
    GVariant* result = g_dbus_connection_call_sync(
        connection,
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

    gchar* handle;
    g_variant_get(result, "(&o)", &handle);
    *session_handle = g_strdup(handle);
    g_variant_unref(result);

    // Wait for the portal to process the session creation
    wait_for_response(connection, *session_handle);

    return TRUE;
}

static gboolean select_sources(GDBusConnection* connection, const char* session_handle, GError** error)
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
        connection,
        PORTAL_BUS_NAME,
        PORTAL_OBJECT_PATH,
        PORTAL_INTERFACE,
        "SelectSources",
        g_variant_new("(oa{sv})", session_handle, options),
        NULL,
        G_DBUS_CALL_FLAGS_NONE,
        -1,
        NULL,
        error
    );

    if (!result)
        return FALSE;

    g_variant_unref(result);

    // Wait for user selection
    wait_for_response(connection, session_handle);

    return TRUE;
}

static uint32_t start_screencast(GDBusConnection* connection, const char* session_handle, GError** error)
{
    GVariantBuilder builder;
    g_variant_builder_init(&builder, G_VARIANT_TYPE_VARDICT);
    
    // Add restore token
    g_variant_builder_add(&builder, "{sv}", "handle_token",
                         g_variant_new_string("screen_capture_start"));

    GVariant* options = g_variant_builder_end(&builder);
    
    // Call Start
    GVariant* result = g_dbus_connection_call_sync(
        connection,
        PORTAL_BUS_NAME,
        PORTAL_OBJECT_PATH,
        PORTAL_INTERFACE,
        "Start",
        g_variant_new("(osa{sv})", session_handle, "", options),
        G_VARIANT_TYPE("(u)"),
        G_DBUS_CALL_FLAGS_NONE,
        -1,
        NULL,
        error
    );

    if (!result)
        return 0;

    guint32 node_id;
    g_variant_get(result, "(u)", &node_id);
    g_variant_unref(result);

    // Wait for the screencast to start
    wait_for_response(connection, session_handle);

    return node_id;
}

uint32_t portal_request_screen_capture(GDBusConnection** connection, char** session_handle)
{
    GError* error = NULL;
    *connection = g_bus_get_sync(G_BUS_TYPE_SESSION, NULL, &error);
    if (!*connection) {
        printf("Failed to connect to D-Bus: %s\n", error->message);
        g_error_free(error);
        return 0;
    }

    if (!request_session(*connection, session_handle, &error)) {
        printf("Failed to create session: %s\n", error->message);
        g_error_free(error);
        g_object_unref(*connection);
        *connection = NULL;
        return 0;
    }

    if (!select_sources(*connection, *session_handle, &error)) {
        printf("Failed to select sources: %s\n", error->message);
        g_error_free(error);
        g_free(*session_handle);
        *session_handle = NULL;
        g_object_unref(*connection);
        *connection = NULL;
        return 0;
    }

    uint32_t node_id = start_screencast(*connection, *session_handle, &error);
    if (node_id == 0) {
        printf("Failed to start screencast: %s\n", error->message);
        g_error_free(error);
        g_free(*session_handle);
        *session_handle = NULL;
        g_object_unref(*connection);
        *connection = NULL;
        return 0;
    }

    return node_id;
}

void portal_cleanup(GDBusConnection* connection, char* session_handle)
{
    if (session_handle) {
        GError* error = NULL;
        // Close the session
        g_dbus_connection_call_sync(
            connection,
            PORTAL_BUS_NAME,
            session_handle,
            "org.freedesktop.portal.Session",
            "Close",
            NULL,
            NULL,
            G_DBUS_CALL_FLAGS_NONE,
            -1,
            NULL,
            &error);

        if (error) {
            g_error_free(error);
        }

        g_free(session_handle);
    }
    
    if (connection) {
        g_object_unref(connection);
    }
}
