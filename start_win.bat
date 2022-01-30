@echo off
set app="stylize"
SET CURRENTDIR="%cd%"

docker build -t %app% .
docker run -it --rm -d -p 56733:80 ^
  --name=%app% ^
  -v %CURRENTDIR%:/app %app%