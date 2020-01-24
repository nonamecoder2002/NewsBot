docker image rm noname_coder_bot:latest
docker build . -t noname_coder_bot
docker run -d --restart always --name noname_coder_bot noname_coder_bot