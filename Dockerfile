# ubuntu 이미지를 베이스로 사용
FROM ubuntu:latest


# 작업 디렉토리 설정 (컨테이너 안의 기본 폴더)
WORKDIR /app

# 호스트의 hello.txt 를 컨테이너 /app 안으로 복사
COPY hello.txt .

# 빌드 시점에 명령 실행 (패키지 목록 갱신)
RUN apt-get update && apt-get install -y figlet


# 컨테이너가 실행되면 메시지를 출력
CMD ["cat", "hello.txt"]
