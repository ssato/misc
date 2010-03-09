#! /usr/bin/python
# (c) 2006 Michele Campeotto <micampe@micampe.it>, GPLv2
# Hacked to support Beryl; 2006 Satoru SATOH <ssato@redhat.com>
# Hacked to support Compiz; 2006 Andrew Barr <andrew.james.barr@gmail.com>
# inspired from: http://blog.medallia.com/2006/05/smacbook_pro.html

import sys, re, time, os

INTERVAL = 0.01
POS_FILE = '/sys/devices/platform/hdaps/position'
CAL_FILE = '/sys/devices/platform/hdaps/calibrate'
POS_RX = re.compile('^\((-?\d+),(-?\d+)\)$')
SENS = 8
BASEDIR = os.path.dirname(sys.argv[0])

# FIXME: This does not work. Maybe I'm missing something...
def dbus_swicth_to_workspace_at_side(side='left'):
  import dbus
  service = "org.freedesktop.beryl"
  path = "/org/freedesktop/beryl/rotate/allscreens/rotate_" + side
  interface = service + ".activate"
  iface = dbus.Interface(
    dbus.SessionBus().get_object(service, path),
    interface
  )
  (stat, rid) = commands.getstatusoutput("xwininfo -root | grep 'Window id' | cut -d' ' -f 4")
  if stat == 0:
    root_id = int(eval(rid))
    iface.activate("root", dbus.Int32(root_id))

def swicth_to_workspace_at_side(side='left'):
    os.system(BASEDIR + "/dsend.sh rotate rotate_" + side)

def swicth_to_workspace_at_right():
    swicth_to_workspace_at_side('right')

def swicth_to_workspace_at_left():
    swicth_to_workspace_at_side('left')

def get_pos():
    pos = open(POS_FILE).read()
    match = POS_RX.match(pos)
    return (int(match.groups()[0]), int(match.groups()[1]))

def get_calibration():
    pos = open(CAL_FILE).read()
    match = POS_RX.match(pos)
    return (int(match.groups()[0]), int(match.groups()[1]))

def loop():
  calx, caly = get_calibration()
  stable = 0
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
        swicth_to_workspace_at_right()
#        print '->', adelta
      else:
        swicth_to_workspace_at_left()
#        print '<-', adelta
    time.sleep(INTERVAL)

def main():
  try:
    loop()
  except KeyboardInterrupt:
    pass

if __name__ == '__main__':
  main()
