/**
* xsendevent.c - A simple wrapper library for XSendEvent (X11 API).
* Copyright (c) 2006 Satoru SATOH <ssato@redhat.com>, BSD.
*
* Compile it like the following:
*
*  $ gcc -Wall -g -O2 -fPIC -c xsendevent.c
*  $
*  $ # Ugly, but this works.
*  $ gcc -Wall -g -O2 -shared -o xsendevent.so.1.0 xsendevent.o /usr/lib/libX11.so
*  $ ln -sf xsendevent.so.1.0 xsendevent.so
*/

#include <stdio.h>
#include <X11/X.h>
#include <X11/Xlib.h>
#include <X11/keysym.h>

inline unsigned int
XStringToToKeycode (Display * display, const char * const string) {
  return XKeysymToKeycode(display, XStringToKeysym(string) );
}

int
KeyEvent (const char* const keyname) {
  Display * display = NULL;
  Window window = 0;
  int revert_to_ret = 0;
  XKeyEvent event;
  Status status;

  display = XOpenDisplay(NULL); /* localhost:0.0 */
  if (display == NULL) {
    fprintf(stderr, "Could not open display: localhost:0.0\n");
    return 1;
  }

  /**
  * Target window is the window currently focused.
  */
  XGetInputFocus(display, &window, &revert_to_ret);
  if (window == 0) {
    fprintf(stderr, "Could not detect the window which has gotten input focus.\n");
    return 1;
  }

  event.display = display;
  event.window = window;
  event.root = RootWindow(display, DefaultScreen(display));
  event.subwindow = None;
  event.time = CurrentTime;
  event.x = event.y = 1;
  event.x_root = event.y_root = 1;
  event.same_screen = 1;
  event.keycode = XStringToToKeycode(display, keyname);
  /* event.state = modifiers; */
  
  event.type = KeyPress;
  status = XSendEvent(display, window, 1, KeyPressMask, (XEvent *)&event);
  if (status == 0) {
    fprintf(stderr, "Failed to send evnet: type=KeyPress\n");
    return 1; /* error */
  }

  event.type = KeyRelease;
  status = XSendEvent(display, window, 1, KeyReleaseMask, (XEvent *)&event);

  XSync(display, 1);
  XCloseDisplay(display);

  return status;
}

/**
* vim: set ts=2 sw=2 expandtab:
*/
