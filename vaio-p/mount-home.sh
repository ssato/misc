#! /bin/bash
set -e

cryptsetup luksOpen /dev/vg/lv_home luks-e34853ce-be78-4a19-8cf1-2172ee28b736
mount /dev/mapper/luks-e34853ce-be78-4a19-8cf1-2172ee28b736 /home
