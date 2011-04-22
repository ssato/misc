#! /bin/bash
set -e

if test $# -lt 1; then
    echo "Usage: $0 RHEL_CD_ISO_0 RHEL_CD_ISO_1 [RHEL_CD_ISO_2 ...]"
    exit 1
fi


firstiso=$1

dvddir=${firstiso/disc1.iso/dvd}
dvdnam=${dvddir##*/}

mntdir=$(mktemp -d --suffix="-rhel-iso")

for iso in $@; do
    trap INT TERM "umount $mntdir"
    sudo mount -o loop,ro $iso $mntdir
    cp -af $mntdir/.* $dvddir/
    cp -af $mntdir/ $dvddir/
    sudo umount $mntdir 
done
rm -rf $mntdir
 

#export PYTHONPATH="/usr/lib/anaconda"
#export PATH="/usr/lib/anaconda-runtime:$PATH"
#pkgorder $TARGET i386 > $TARGET/RedHat/base/pkgorder
#genhdlist --withnumbers --fileorder $TARGET/RedHat/base/pkgorder --hdlist $TARGET/RedHat/base/hdlist $TARGET/
 
mkisofs -r -T -J \
-V "RHEL Custom DVD" \
-b isolinux/isolinux.bin \
-c isolinux/boot.cat \
-no-emul-boot \
-boot-load-size 4 \
-boot-info-table \
-v \
-o "${dvddir}/../${dvdnam}.iso" $dvddir/
