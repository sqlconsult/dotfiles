#!/usr/bin/env bash
#
# from http://www.javahelps.com/2017/09/install-oracle-jdk-9-on-linux.html
#
# get tar file in Downloads directory
#
mkdir ~/Downloads/
cd ~/Downloads
wget -c --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/9.0.4+11/c2514751926b4512b076cc82f959763f/jdk-9.0.4_linux-x64_bin.tar.gz
#
# decompress into /usr/lib/jvm
#
sudo mkdir /usr/lib/jvm
cd /usr/lib/jvm
sudo tar -xvzf ~/Downloads/jdk-9.0.4_linux-x64_bin.tar.gz
#
# update environment variables file
#
#    append to path [;/usr/lib/jvm/jdk-9/bin]
sudo sed '/PATH/ s/$/;\/usr\/lib\/jvm\/jdk-9\/bin/' /etc/environment
#    add to end of file [JAVA_HOME="/usr/lib/jvm/jdk-9"]
sudo echo JAVA_HOME="/usr/lib/jvm/jdk-9" >> /etc/environment
#
# inform Ubuntu about Java's location
#
sudo update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/jdk-9/bin/java"
sudo update-alternatives --install "/usr/bin/javac" "javac" "/usr/lib/jvm/jdk-9/bin/javac"
sudo update-alternatives --set java /usr/lib/jvm/jdk-9/bin/java
sudo update-alternatives --set javac /usr/lib/jvm/jdk-9/bin/javac
#
# verify setup
#
update-alternatives --list java
update-alternatives --list javac
java -version