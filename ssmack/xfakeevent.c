/**
* A tiny wrapper library for XTestFakeKeyEvent / XTestFakeButtonEvent
*/

#include <stdio.h>
#include <X11/X.h>
#include <X11/Xlib.h>
#include <X11/keysym.h>
#include <X11/extensions/XTest.h>

inline unsigned int
XStringToToKeycode (Display * display, const char * const string) {
  return XKeysymToKeycode(display, XStringToKeysym(string) );
}

int
KeyEvent (const char* const keyname)
{
  Display * display = XOpenDisplay(NULL); /* localhost:0.0 */
  if (display == NULL) {
    fprintf(stderr, "Could not open display: localhost:0.0\n");
    return 1;
  }

  unsigned int keycode = XStringToToKeycode(display, keyname);
  XTestFakeKeyEvent(display, keycode, True, CurrentTime);
  XTestFakeKeyEvent(display, keycode, False, CurrentTime);

  XCloseDisplay(display);
  return 0;
}

/**
* @param button Button1, Button2, ... (X11/x.h)
*/
int
MouseEvent (unsigned int button)
{
  Display * display = XOpenDisplay(NULL);
  if (display == NULL) {
    fprintf(stderr, "Could not open display: localhost:0.0\n");
    return 1;
  }

  XTestFakeButtonEvent(display, button, True, CurrentTime);
  XTestFakeButtonEvent(display, button, False, CurrentTime);

  XCloseDisplay(display);
  return 0;
}

/**
* vim: set ts=2 sw=2 expandtab:
*/
