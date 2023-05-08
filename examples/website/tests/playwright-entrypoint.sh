#!/bin/sh
set -e                                                                             
if [ "$VNC" == "yes" ]; then                                                       
  USER=root Xvnc -geometry 1280x800 -depth 24 :1 &                                   
  DISPLAY=:1 PWDEBUG=console ./node_modules/.bin/playwright run-server --port 3605   
else                                                                               
  ./node_modules/.bin/playwright run-server --port 3605
fi                                  
