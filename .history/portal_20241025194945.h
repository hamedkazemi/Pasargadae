#ifndef PORTAL_H
#define PORTAL_H

#include <gio/gio.h>
#include <stdint.h>

// Initialize portal connection and request screen capture
uint32_t portal_request_screen_capture(GDBusConnection** connection, char** session_handle);

// Cleanup portal resources
void portal_cleanup(GDBusConnection* connection, char* session_handle);

#endif // PORTAL_H
