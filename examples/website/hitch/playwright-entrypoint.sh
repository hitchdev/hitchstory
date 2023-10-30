#! /bin/bash
if [[ "$VNC" == "yes" ]]; then
  USER=root Xvnc -geometry ${VNCSCREENSIZE:-1024x768} -depth 24 :1 &   
  
  # Wait for port to be ready
  while ! nc -z localhost 5901; do   
    sleep 0.1
  done
  DISPLAY=:1 PWDEBUG=console ./node_modules/.bin/playwright run-server --port 3605   
else                                                                               
  ./node_modules/.bin/playwright run-server --port 3605
fi                                  
