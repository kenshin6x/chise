export DISPLAY=:99 &
Xvfb :99 -screen 0 1024x768x16 &
x11vnc -forever -display :99 -bg -nopw -listen localhost -xkb -rfbport 5906
