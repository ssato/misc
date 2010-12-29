INCLUDES = -I/usr/include/X11
LIBS = -L/usr/lib -lX11 -lXext -lXtst

CC = gcc
CFLAGS = -Wall -g -O2 $(INCLUDES)

all: xsendevent.so

xsendevent.so: xsendevent.so.1.0
	ln -sf $^ $@

xsendevent.so.1.0: xsendevent.o
	$(CC) $(CFLAGS) $(LIBS) -shared -o $@ $< /usr/lib/libX11.so

xsendevent.o: xsendevent.c
	$(CC) $(CFLAGS) -fPIC -c $<

xfakeevent.so: xfakeevent.so.1.0
	ln -sf $^ $@

xfakeevent.so.1.0: xfakeevent.o
	$(CC) $(CFLAGS) $(LIBS) -shared -o $@ $< /usr/lib/libX11.so

xfakeevent.o: xfakeevent.c
	$(CC) $(CFLAGS) -fPIC -c $<

clean: 
	-rm -f *.o *.so *.so.*

.PHONY: all clean
