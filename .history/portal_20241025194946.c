#include "portal.h"
#include <stdio.h>

#define PORTAL_BUS_NAME "org.freedesktop.portal.Desktop"
#define PORTAL_OBJECT_PATH "/org/freedesktop/portal/desktop"
#define PORTAL_INTERFACE "org.freedesktop.portal.ScreenCast"

static gboolean request_session(GDBusConnection* connection, char** session_handle, GError** error)
{
    GVariantBuilder builder;
    g_variant_builder_init(&builder, G_VARIANT_TYPE_VARDICT);
    
    g_variant_builder_add(&builder, "{sv}", "handle_token",
