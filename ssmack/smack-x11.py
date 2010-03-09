#! /usr/bin/python
# (c) 2006 Michele Campeotto <micampe@micampe.it>, GPLv2
# Hacked to support X11 Key Event; 2006 Satoru SATOH <ssato@redhat.com>
# Hacked to support Compiz; 2006 Andrew Barr <andrew.james.barr@gmail.com>
# inspired from: http://blog.medallia.com/2006/05/smacbook_pro.html

import sys, re, time, os
import errno
try:
  import ctypes
except:
  print >> sys.stderr, """\
%s requires ctypes module to call XSendKeyEvent (X11 API).
Please install ctypes first.
"""
  sys.exit(errno.ENOENT)

INTERVAL = 0.005
POS_FILE = '/sys/devices/platform/hdaps/position'
CAL_FILE = '/sys/devices/platform/hdaps/calibrate'
POS_RX = re.compile('^\((-?\d+),(-?\d+)\)$')
SENS = 8
BASEDIR = os.path.dirname(sys.argv[0])

def load_wrapper_cmodule (prefix=BASEDIR):
  try:
    sys.stderr.write("Loading module %s ... " % (prefix + "/xsendevent.so",))
    xsendevent = ctypes.cdll.LoadLibrary(prefix + "/xsendevent.so")
    sys.stderr.write("Sucess\n")
  except:
    pass
  return xsendevent

def x11_send_key_event(xsendevent, keyname='Right'):
    print >> sys.stdout, "Keyname = %s" % (keyname,)
    xsendevent.KeyEvent(keyname)

def action_1(xsendevent):
    x11_send_key_event(xsendevent, 'Right')

def action_2(xsendevent):
    x11_send_key_event(xsendevent, 'Left')

def get_pos():
    pos = open(POS_FILE).read()
    match = POS_RX.match(pos)
    ret = (int(match.groups()[0]), int(match.groups()[1]))
    #sys.stderr.write("Pos: %d, %d" % ret)
    return ret

def get_calibration():
    pos = open(CAL_FILE).read()
    match = POS_RX.match(pos)
    ret = (int(match.groups()[0]), int(match.groups()[1]))
    #sys.stderr.write("Calibration: %d, %d" % ret)
    return ret

def loop():
  calx, caly = get_calibration()
  stable = 0
  xsendevent = load_wrapper_cmodule()
  while True:
    x, y = get_pos()
    if x == 0: continue
    delta = x - calx
    adelta = abs(delta)
    if adelta < 5:
      stable += 1
    if adelta > SENS and stable > 30:
      stable = 0
      if delta < 0:
        action_1(xsendevent)
      else:
        # FIXME: It seems hard to distinguish two actions actually.
        # More sophiscated implementation should be needed.
        action_1(xsendevent)
        #action_2(xsendevent)
    time.sleep(INTERVAL)

def main():
  try:
    loop()
  except KeyboardInterrupt:
    pass

if __name__ == '__main__':
  main()

# vim: set ts=2 sw=2 expandtab:
