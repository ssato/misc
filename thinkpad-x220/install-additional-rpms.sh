#! /bin/bash
set -ex


file_server=${file:-FILE_SERVER}

#repo --name="adobe-linux-x86_64" --baseurl=http://linuxdownload.adobe.com/linux/x86_64/
#repo --name="bluejeans" --baseurl=https://swdl.bluejeans.com/repos/bluejeans/x86_64/release/rpm/
#repo --name="rpmfusion-free" --mirrorlist=http://mirrors.rpmfusion.org/mirrorlist?repo=free-fedora-20&arch=x86_64
#repo --name="rpmfusion-free-updates" --mirrorlist=http://mirrors.rpmfusion.org/mirrorlist?repo=free-fedora-updates-released-20&arch=x86_64
## Edit the server name in the url if the server is not resolvable.
#repo --name="fedora-nrt-ssato" --baseurl=http://file/ssato/yum/fedora/20/x86_64/

# groups:
groups="base-x libreoffice rpm-development-tools virtualization"

# repo release rpms:
repo_rpms="
http://linuxdownload.adobe.com/adobe-release/adobe-release-x86_64-1.0-1.noarch.rpm
http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-20.noarch.rpm
http://${file_server}/ssato/yum/fedora/20/x86_64/fedora-nrt-ssato-release-20-1.fc20.noarch.rpm
"

# rpms to install additionally if not installed:
rpms="
apg
audit
autofs
avahi
avahi-autoipd
avahi-ui-gtk3
bridge-utils
cadaver
calibre
check
check-devel
cifs-utils
cmake
conky
control-center
cscope
ctags
cups
cups-filesystem
cups-filters
cups-pk-helper
curl
dnf
docker-io
fakeroot
firefox
firewalld-config
fortune-mod
gcc-c++
gimp-data-extras
git-annex
git-svn
gnome-tweak-tool
golang
golang-godoc
golang-gotype
golang-src
golang-vim
graphviz-python
gstreamer1
gstreamer1-plugins-bad-free
gstreamer1-plugins-base
gstreamer1-plugins-good
gstreamer1-plugins-good-extras
gstreamer-ffmpeg
hardlink
ibus-skk
ibus-wayland
inkscape
iperf
iwl6000-firmware
iwl6000g2a-firmware
iwl6000g2b-firmware
mlocate
mock
mscgen
msmtp
mutt
NetworkManager-openvpn-gnome
NetworkManager-vpnc-gnome
nfs-utils
openssh-askpass
openssh-clients
openssh-server
p7zip
pigz
pinfo
pyflakes
pylint
python-flake8
python-nose
python-pep8
python-pip
python-pygments
python-tablib
samba-client
scratch
screen
strace
tcpdump
thunderbird
vconfig
vim-enhanced
virt-manager
virt-viewer
w3m
wayland
weston
wget
wireless-tools
xz
zenity
zsh
"


# from adobe-linux-x86_64:
rpms="
$rpms
flash-plugin.x86_64
"

# from bluejeans:
rpms="
$rpms
bjnplugin
rbjnplugin
"

# from rpmfusion-free*:
rpms="
$rpms
ffmpeg-compat
"

# from fedora-nrt-ssato:
rpms="
$rpms
miniascape-confsrc-rhui
miniascape-data-default-nrt-overrides
mock-data-nrt
myrepo-data-nrt
packagemaker-core
python-docutils-exts-bootstrap-data-rhui
python-docutils-exts-data-nrt
rhel-soe-assessmentkit
swapi-data-nrt
"

# TODO:
#mplayer-tools

sudo yum install -y dnf
sudo dnf group install -y $groups || :
sudo dnf install -y $rpms
