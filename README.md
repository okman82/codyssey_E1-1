# Docker 개발 워크스테이션 구축 미션

## 1) 프로젝트 개요
WSL2(Ubuntu) 환경에서 Docker 기반 개발 워크스테이션을 구축하고,
터미널 조작 · 파일 권한 · Docker 운영 · Dockerfile 커스텀 이미지 ·
포트 매핑 · 바인드 마운트 · 볼륨 영속성 · Git/GitHub 연동까지
전 과정을 수행·검증한 기록이다.

---

## 2) 실행 환경
| 항목 | 내용 |
|------|------|
| OS | Ubuntu (WSL2 / kernel 6.18.54.1-microsoft-standard-WSL2) |
| Shell | bash |
| Terminal | Windows Terminal + WSL2 |
| Docker | 29.9.2 (Docker Desktop, WSL2 연동) |
| Git | 2.53.0 |

---

## 3) 수행 체크리스트
- [x] 터미널 기본 조작 및 폴더 구성
- [x] 파일/디렉토리 권한 변경 실습
- [x] Docker 설치/점검 (version, info)
- [x] Docker 기본 운영 (images, ps -a, logs, stats)
- [x] hello-world 실행
- [x] ubuntu 컨테이너 진입 (attach/exec 차이 관찰)
- [x] Dockerfile 커스텀 이미지 빌드/실행
- [x] 포트 매핑 접속 (8080, 8081 — 2회)
- [x] 바인드 마운트 반영 (전/후 비교)
- [x] 볼륨 영속성 (삭제 전/후 비교)
- [x] Git 설정 + GitHub/VSCode 연동

---

## 4) 터미널 기본 조작 로그
$ pwd
/home/ogasa9995/workspace/docker-mission

$ ls -la
total 24
drwxr-xr-x 3 ogasa9995 ogasa9995 4096 Nov  3 22:07 .
drwxr-xr-x 3 ogasa9995 ogasa9995 4096 Nov  2 21:11 ..
drwxr-xr-x 7 ogasa9995 ogasa9995 4096 Nov  2 22:13 .git
-rw-r--r-- 1 ogasa9995 ogasa9995  409 Nov  2 21:59 Dockerfile
-rw-r--r-- 1 ogasa9995 ogasa9995   54 Nov  2 21:56 hello.txt

$ mkdir testdir
$ touch testfile.txt
$ echo "연습용 파일" > testfile.txt
$ cat testfile.txt
연습용 파일
$ cp testfile.txt testdir/
$ mv testfile.txt renamed.txt
$ ls -la testdir
-rw-r--r-- 1 ogasa9995 ogasa9995   17 Nov  3 22:08 testfile.txt
#절대경로 vs 상대경로: /home/ogasa9995/workspace/docker-mission(루트 /부터 시작)은 절대경로,
#testdir/(현재 위치 기준)은 상대경로다.

---

## 5) 파일 권한 실습 (변경 전/후 비교)

# 파일 권한 변경
$ ls -l renamed.txt
-rw-r--r-- 1 ogasa9995 ogasa9995 17 Nov  3 22:08 renamed.txt   # 변경 전 (644)
$ chmod 600 renamed.txt
$ ls -l renamed.txt
-rw------- 1 ogasa9995 ogasa9995 17 Nov  3 22:08 renamed.txt   # 변경 후 (600)

# 디렉토리 권한 변경
$ ls -ld testdir
drwxr-xr-x 2 ogasa9995 ogasa9995 4096 Nov  3 22:08 testdir     # 변경 전 (755)
$ chmod 700 testdir
$ ls -ld testdir
drwx------ 2 ogasa9995 ogasa9995 4096 Nov  3 22:08 testdir     # 변경 후 (700)



## 6) Docker 설치 및 점검
$ docker --version
Docker version 29.9.2, ...
(docker --version / docker info 실제 출력 붙여넣기)

## 7) Docker 기본 운영
$ docker images
IMAGE                ID             DISK USAGE   CONTENT SIZE
hello-world:latest   c567b231f656   25.9kB       9.49kB
myimage:latest       e2105412e1ea   159MB        42.1MB
nginx:latest         5ab5b0b01097   243MB        66.8MB
ubuntu:latest        6a06111c3b0a   163MB        45.9MB

$ docker ps -a
CONTAINER ID   IMAGE   STATUS                      PORTS                    NAMES
8c14fe1a875c   nginx   Up 50 minutes               0.0.0.0:8080->80/tcp     mycompose-web-1
f22afff1bc88   nginx   Exited (0) 53 minutes ago                            mynginx

$ docker stats --no-stream
CONTAINER ID   NAME              CPU %   MEM USAGE / LIMIT    MEM %   NET I/O           PIDS
8c14fe1a875c   mycompose-web-1   0.00%   18.7MiB / 15.25GiB   0.12%   9.74kB / 5.95kB   25
docker logs (발췌)
$ docker logs mynginx
/docker-entrypoint.sh: Configuration complete; ready for start up
2026/11/03 12:08:32 [notice] 1#1: nginx/1.31.8 start worker processes
172.17.0.1 - - [03/Nov/2026:12:08:36 +0000] "GET /index.html HTTP/1.1" 200 29
...
2026/11/03 12:15:27 [notice] 1#1: signal 3 (SIGQUIT) received, shutting down
2026/11/03 12:15:27 [notice] 1#1: exit
접속 로그(GET /index.html 200)로 브라우저 접속 성공을,
SIGQUIT ... exit로 정상 종료(graceful shutdown)를 확인했다.

## 8) 컨테이너 실행 실습
hello-world: 실행 성공 (설치 정상 동작 확인)
ubuntu: docker run -it ubuntu bash로 진입, 내부에서 ls, echo 수행
attach vs exec 관찰

attach: 실행 중인 컨테이너의 메인 프로세스에 연결 → 나가면 컨테이너도 종료될 수 있음
exec: 컨테이너 안에서 새 프로세스(예: bash)를 실행 → 나가도 컨테이너는 계속 동작
일회용 특성: --rm 없이도 컨테이너 종료 시 내부 변경사항은 이미지에 반영되지 않음


## 9) Dockerfile 커스텀 이미지
선택한 베이스: (실제 Dockerfile 내용에 맞게 수정)

dockerfile

# Dockerfile 실제 내용 붙여넣기
커스텀 포인트 & 목적

(예) COPY : 정적 콘텐츠 교체 → 기본 페이지 대신 내 콘텐츠 제공
(예) RUN : 패키지 설치 → 필요한 기능 추가
빌드/실행

$ docker build -t myimage .
$ docker run -d -p 8080:80 myimage


## 10) 포트 매핑 접속 증거 (2회)

# 1회차 (Compose, 8080)
$ docker ps -a   # 0.0.0.0:8080->80/tcp 확인

# 2회차 (8081)
$ docker run -d -p 8081:80 --name web-8081 nginx
8b5dae0ef195...
$ curl http://localhost:8081
<!DOCTYPE html>
...
<h1>Welcome to nginx!</h1>
...
#포트 매핑이 필요한 이유: 컨테이너는 격리된 네트워크를 가지므로,
#호스트의 포트(8080/8081)를 컨테이너 포트(80)에 연결해야 외부(브라우저)에서 접근할 수 있다.

브라우저 접속 화면 (주소창 포함)
port-8080
port-8081

## 11) 바인드 마운트 반영 (전/후 비교)

$ docker run -d -p 8082:80 -v $(pwd)/site:/usr/share/nginx/html nginx
# 호스트에서 index.html 수정 → 새로고침 시 즉시 반영
(변경 전/후 화면 또는 curl 결과 붙여넣기)

## 12) 볼륨 영속성 검증 (삭제 전/후 비교)
$ docker volume create myvolume
$ docker run -d --name vol-test -v myvolume:/data ubuntu sleep infinity
$ docker exec vol-test bash -c "echo hi > /data/hello.txt && cat /data/hello.txt"
hi
$ docker rm -f vol-test                      # 컨테이너 삭제

$ docker run -d --name vol-test2 -v myvolume:/data ubuntu sleep infinity
$