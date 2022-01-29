@echo off
set app="docker.test"
SET CURRENTDIR="%cd%"

docker image prune -a -f
docker build -t %app% .
docker run -it --rm -d -p 56733:80 ^
  --name=%app% ^
  -v %CURRENTDIR%:/app %app%