<!--
[작성 방법] 이 회색 주석은 GitHub 화면에 보이지 않는 안내문입니다.
1. 위에서 아래로 순서대로 명령을 실행합니다.
2. 연필 이모지가 있는 자리를 내 실제 출력, 설명, 스크린샷으로 바꿉니다.
3. 토큰, 비밀번호, 인증 코드, 개인 이메일 등은 마스킹합니다.
특별한 안내가 없으면 모든 명령은 Ubuntu(WSL) 터미널에서 실행합니다.

[학습 및 수행 순서] 각 단계의 확인 질문에 답할 수 있으면 다음으로 넘어갑니다.
STEP 1. 환경 준비(2장): WSL 2, Docker Desktop, VSCode, Git이 각각 어떤 역할을 하는가?
STEP 2. 리눅스 기초(5~6장, 15장): 절대/상대 경로의 차이는? 755와 644는 어떻게 해석하는가?
STEP 3. Docker 기초(7~9장): 이미지와 컨테이너의 차이는? exec와 attach 후 exit하면 어떻게 다른가?
STEP 4. 이미지 제작(10장): Dockerfile의 각 줄은 어떤 목적인가?
STEP 5. 네트워크(11장): -p 8080:80에서 앞뒤 숫자는 각각 무엇인가?
STEP 6. 스토리지(12~13장): 바인드 마운트와 볼륨은 언제 각각 사용하는가?
STEP 7. Git/GitHub(14장): 로컬 커밋과 원격 푸시는 어떻게 다른가?
STEP 8. 문서 마감(3~4장, 15~17장): 체크리스트, 개념 설명, 트러블슈팅, 마스킹을 완료했는가?
STEP 9. 선택 과제(18장): Compose와 SSH 인증을 추가로 수행합니다.
-->

# 개발 워크스테이션 구축

## 1. 프로젝트 개요

터미널, Docker, Git/GitHub을 직접 구성해 누가 실행해도 같은 결과를 얻는 개발 환경을 만들고, 그 결과를 로그와 접속 화면으로 검증합니다.

- 터미널로 파일과 권한 관리
- Docker 설치 점검 및 컨테이너 운영
- Dockerfile로 커스텀 웹 서버 이미지 제작
- 포트 매핑, 바인드 마운트, 볼륨 동작 검증
- Git 설정 및 GitHub/VSCode 연동

## 2. 실행 환경

<!--
[작업 폴더: 아래 2.2 준비를 마친 뒤 Ubuntu 터미널에서 실행]
  mkdir -p ~/workstation-mission/site ~/workstation-mission/docs/images
  cd ~/workstation-mission
  내려받은 README.md 복사:
  cp "/mnt/c/Users/<윈도우사용자명>/Downloads/README.md" .

[정보 확인 명령]
  cat /etc/os-release | head -n 2
  echo $SHELL
  docker --version
  git --version
-->

### 2.1 환경 정보

| 항목 | 내용 |
| --- | --- |
| Host OS | Windows 11 (Version 10.0.26300.9711) |
| Linux 환경 | WSL 2 / Ubuntu 26.04.1 LTS |
| Shell / Terminal | bash 5.3.9  / Windows Terminal |
| Docker | Docker Desktop(WSL 2 연동), Docker version 29.9.2, build a82e528 |
| Git | git version 2.53.0 |

### 2.2 환경 구성

1. PowerShell을 관리자 권한으로 열어 `wsl --install -d Ubuntu`를 실행하고, 필요하면 재부팅합니다. Ubuntu를 처음 열 때 Linux 사용자를 만듭니다.
2. `wsl -l -v`로 Ubuntu의 VERSION이 2인지 확인합니다.
3. Docker Desktop for Windows를 설치한 뒤 **Settings > General > Use WSL 2 based engine**을 켭니다.
4. **Settings > Resources > WSL Integration**에서 Ubuntu를 켜고 적용합니다.
5. Windows에 VSCode와 WSL 확장을 설치합니다. Ubuntu에 Git이 없으면 `sudo apt update && sudo apt install -y git`으로 설치합니다.

> **재현 시 주의사항:** 작업 폴더는 WSL 내부(`~/workstation-mission`)에 둡니다. `/mnt/c` 아래는 Windows 파일 시스템이어서 기본 설정에서는 `chmod` 결과가 의도대로 반영되지 않을 수 있습니다. Windows 탐색기에서는 `\\wsl$\Ubuntu\home\<사용자명>\workstation-mission` 경로로 접근합니다.

## 3. 수행 체크리스트

<!-- 해당 단계를 끝낼 때마다 [ ]를 [x]로 바꿉니다. -->

- [ ] 터미널 기본 조작 및 폴더 구성
- [ ] 파일/디렉토리 권한 변경 실습
- [ ] Docker 설치 및 데몬 점검
- [ ] Docker 기본 운영 명령 수행
- [ ] hello-world, ubuntu 컨테이너 실행
- [ ] Dockerfile 기반 커스텀 이미지 빌드/실행
- [ ] 포트 매핑 접속 확인(2개 포트)
- [ ] 바인드 마운트 변경 반영 확인
- [ ] Docker 볼륨 영속성 확인
- [ ] Git 설정 및 GitHub/VSCode 연동
- [ ] 민감정보 마스킹 확인

## 4. 검증 방법 요약

| 검증 대상 | 사용한 명령 | 확인 기준 | 결과 위치 |
| --- | --- | --- | --- |
| 터미널 조작 | `pwd`, `ls -la`, `cp`, `mv`, `rm` | 파일 상태가 명령대로 변경됨 | [5장](#5-터미널-조작-로그) |
| 권한 | `ls -l`, `ls -ld`, `chmod` | 변경 전후 권한 값이 다름 | [6장](#6-권한-실습) |
| Docker 동작 | `docker --version`, `docker info` | 버전 및 Server 정보 출력 | [7장](#7-docker-설치-및-기본-점검) |
| 컨테이너 운영 | `docker ps -a`, `docker logs`, `docker stats` | 상태, 로그, 리소스 확인 | [8장](#8-docker-기본-운영-명령), [9장](#9-컨테이너-실행-실습) |
| 커스텀 이미지 | `docker build`, `docker run` | 이미지 생성 및 컨테이너 실행 | [10장](#10-dockerfile-기반-커스텀-이미지) |
| 포트 매핑 | `curl`, 브라우저 | 지정 포트에서 페이지 응답 | [11장](#11-포트-매핑-및-접속-증거) |
| 바인드 마운트 | `docker run -v`, `curl` | 호스트 수정이 즉시 반영됨 | [12장](#12-바인드-마운트-변경-반영) |
| 볼륨 | `docker volume`, `docker rm -f` | 컨테이너 삭제 후 데이터 유지 | [13장](#13-docker-볼륨-영속성) |
| Git/GitHub | `git config --list`, `git push` | 설정 확인 및 원격 저장소 반영 | [14장](#14-git-설정-및-github-연동) |

## 5. 터미널 조작 로그

<!--
[실행 명령] 아래 전체를 실행하고 명령과 출력을 함께 붙여 넣습니다.
pwd
ls -la
mkdir -p ~/practice-lab/docs
cd ~/practice-lab
pwd
touch empty.txt
echo "hello terminal" > note.txt
cat note.txt
ls -la
cp note.txt docs/note-copy.txt
ls -la docs
mv note.txt renamed.txt
mv renamed.txt docs/
ls -la . docs
rm empty.txt
rm -r docs
ls -la

[경로 차이 확인]
cd /tmp && pwd
cd ~/practice-lab && pwd
mkdir -p sub && cd sub && pwd
cd .. && pwd
-->

```bash
ogasa9995@GNIA-C201-B04:~/workstation-mission$ pwd
/home/ogasa9995/workstation-mission
ogasa9995@GNIA-C201-B04:~/workstation-mission$ ls -la
total 40
drwxr-xr-x  5 ogasa9995 ogasa9995  4096 Nov  4 18:24 .
drwxr-x--- 11 ogasa9995 ogasa9995  4096 Nov  4 18:24 ..
drwxr-xr-x  7 ogasa9995 ogasa9995  4096 Nov  4 18:24 .git
-rw-r--r--  1 ogasa9995 ogasa9995 19534 Nov  4 18:24 README.md
drwxr-xr-x  3 ogasa9995 ogasa9995  4096 Nov  4 18:24 docs
drwxr-xr-x  2 ogasa9995 ogasa9995  4096 Nov  4 18:24 site
ogasa9995@GNIA-C201-B04:~/workstation-mission$ mkdir -p ~/practice-lab/docs
ogasa9995@GNIA-C201-B04:~/workstation-mission$ cd ~/practice-lab/
ogasa9995@GNIA-C201-B04:~/practice-lab$ pwd
/home/ogasa9995/practice-lab
ogasa9995@GNIA-C201-B04:~/practice-lab$ touch empty.txt
ogasa9995@GNIA-C201-B04:~/practice-lab$ echo "hello terminal" > note.txt
ogasa9995@GNIA-C201-B04:~/practice-lab$ cat note.txt
hello terminal
ogasa9995@GNIA-C201-B04:~/practice-lab$ ls -la
total 16
drwxr-xr-x  3 ogasa9995 ogasa9995 4096 Nov  4 18:26 .
drwxr-x--- 12 ogasa9995 ogasa9995 4096 Nov  4 18:25 ..
drwxr-xr-x  2 ogasa9995 ogasa9995 4096 Nov  4 18:25 docs
-rw-r--r--  1 ogasa9995 ogasa9995    0 Nov  4 18:26 empty.txt
-rw-r--r--  1 ogasa9995 ogasa9995   15 Nov  4 18:26 note.txt
ogasa9995@GNIA-C201-B04:~/practice-lab$ cp note.txt docs/note-copy.txt
ogasa9995@GNIA-C201-B04:~/practice-lab$ ls -la docs
total 12
drwxr-xr-x 2 ogasa9995 ogasa9995 4096 Nov  4 18:27 .
drwxr-xr-x 3 ogasa9995 ogasa9995 4096 Nov  4 18:26 ..
-rw-r--r-- 1 ogasa9995 ogasa9995   15 Nov  4 18:27 note-copy.txt
ogasa9995@GNIA-C201-B04:~/practice-lab$ ls -la docs
total 12
drwxr-xr-x 2 ogasa9995 ogasa9995 4096 Nov  4 18:27 .
drwxr-xr-x 3 ogasa9995 ogasa9995 4096 Nov  4 18:26 ..
-rw-r--r-- 1 ogasa9995 ogasa9995   15 Nov  4 18:27 note-copy.txt
ogasa9995@GNIA-C201-B04:~/practice-lab$ mv note.txt renamed.txt
ogasa9995@GNIA-C201-B04:~/practice-lab$ mv renamed.txt docs/
ogasa9995@GNIA-C201-B04:~/practice-lab$ ls -la . docs
.:
total 12
drwxr-xr-x  3 ogasa9995 ogasa9995 4096 Nov  4 18:27 .
drwxr-x--- 12 ogasa9995 ogasa9995 4096 Nov  4 18:25 ..
drwxr-xr-x  2 ogasa9995 ogasa9995 4096 Nov  4 18:27 docs
-rw-r--r--  1 ogasa9995 ogasa9995    0 Nov  4 18:26 empty.txt

docs:
total 16
drwxr-xr-x 2 ogasa9995 ogasa9995 4096 Nov  4 18:27 .
drwxr-xr-x 3 ogasa9995 ogasa9995 4096 Nov  4 18:27 ..
-rw-r--r-- 1 ogasa9995 ogasa9995   15 Nov  4 18:27 note-copy.txt
-rw-r--r-- 1 ogasa9995 ogasa9995   15 Nov  4 18:26 renamed.txt
ogasa9995@GNIA-C201-B04:~/practice-lab$ rm empty.txt
ogasa9995@GNIA-C201-B04:~/practice-lab$ rm -r docs
ogasa9995@GNIA-C201-B04:~/practice-lab$ ls -la
total 8
drwxr-xr-x  2 ogasa9995 ogasa9995 4096 Nov  4 18:28 .
drwxr-x--- 12 ogasa9995 ogasa9995 4096 Nov  4 18:25 ..
ogasa9995@GNIA-C201-B04:~/practice-lab$ cd /tmp
ogasa9995@GNIA-C201-B04:/tmp$
ogasa9995@GNIA-C201-B04:/tmp$ pwd
/tmp
ogasa9995@GNIA-C201-B04:/tmp$ cd ~/practice-lab
ogasa9995@GNIA-C201-B04:~/practice-lab$
ogasa9995@GNIA-C201-B04:~/practice-lab$
ogasa9995@GNIA-C201-B04:~/practice-lab$ pwd
/home/ogasa9995/practice-lab
ogasa9995@GNIA-C201-B04:~/practice-lab$ mkdir -p sub
ogasa9995@GNIA-C201-B04:~/practice-lab$ cd sub
ogasa9995@GNIA-C201-B04:~/practice-lab/sub$ pwd
/home/ogasa9995/practice-lab/sub
ogasa9995@GNIA-C201-B04:~/practice-lab/sub$ cd ..
ogasa9995@GNIA-C201-B04:~/practice-lab$ pwd
/home/ogasa9995/practice-lab
```

## 6. 권한 실습

<!--
[파일]
cd ~/practice-lab
printf '#!/bin/sh\necho "script ran"\n' > hello.sh
chmod 644 hello.sh
ls -l hello.sh
./hello.sh               Permission denied가 나오는지 확인
chmod 755 hello.sh
ls -l hello.sh
./hello.sh               실행되는지 확인

[디렉토리]
mkdir -p locked
ls -ld locked
chmod 700 locked
ls -ld locked
chmod 755 locked
ls -ld locked
-->

### 6.1 파일 권한 변경

```bash
printf '#!/bin/sh\necho "script ran"\n' > hello.sh
ogasa9995@GNIA-C201-B04:~/practice-lab$ chmod 644 hello.sh
ogasa9995@GNIA-C201-B04:~/practice-lab$ ls -l hello.sh
-rw-r--r-- 1 ogasa9995 ogasa9995 28 Nov  4 18:45 hello.sh
ogasa9995@GNIA-C201-B04:~/practice-lab$ ./hello.sh
bash: ./hello.sh: Permission denied
ogasa9995@GNIA-C201-B04:~/practice-lab$ chmod 755 hello.sh
ogasa9995@GNIA-C201-B04:~/practice-lab$ ls -l hello.sh
-rwxr-xr-x 1 ogasa9995 ogasa9995 28 Nov  4 18:45 hello.sh
ogasa9995@GNIA-C201-B04:~/practice-lab$ ./hello.sh
script ran
```

### 6.2 디렉토리 권한 변경

```bash
ogasa9995@GNIA-C201-B04:~/practice-lab$ mkdir -p locked
ogasa9995@GNIA-C201-B04:~/practice-lab$ ls -ld locked
drwxr-xr-x 2 ogasa9995 ogasa9995 4096 Nov  4 18:46 locked
ogasa9995@GNIA-C201-B04:~/practice-lab$ chmod 700 locked
ogasa9995@GNIA-C201-B04:~/practice-lab$ ls -ld locked
drwx------ 2 ogasa9995 ogasa9995 4096 Nov  4 18:46 locked
ogasa9995@GNIA-C201-B04:~/practice-lab$ chmod 755 locked
ogasa9995@GNIA-C201-B04:~/practice-lab$ ls -ld locked
drwxr-xr-x 2 ogasa9995 ogasa9995 4096 Nov  4 18:46 locked
```

## 7. Docker 설치 및 기본 점검

<!--
docker --version
docker info
docker info에 사용자명이나 개인 정보가 보이면 마스킹합니다.
-->

```bash
✏️ docker --version, docker info 명령과 출력 붙여넣기
```

## 8. Docker 기본 운영 명령

<!--
docker pull nginx:alpine
docker pull ubuntu
docker images
docker run -d --name ops-web -p 8079:80 nginx:alpine
docker ps
curl -s http://localhost:8079 > /dev/null
docker logs ops-web
docker stats --no-stream
docker stop ops-web
docker ps
docker ps -a
docker rm ops-web
-->

```bash
✏️ 이미지, 컨테이너, 로그, 리소스 확인 명령과 출력 붙여넣기
```

## 9. 컨테이너 실행 실습

<!--
[hello-world]
docker run hello-world

[ubuntu 내부 진입]
docker run -it --name my-ubuntu ubuntu bash
  ls
  echo "inside container"
  exit
docker ps -a             Exited 상태 확인

[exec 관찰]
docker start my-ubuntu
docker exec -it my-ubuntu bash
  echo "via exec"
  exit
docker ps                Up 유지 확인

[attach 관찰]
docker attach my-ubuntu
  프롬프트가 보이지 않으면 Enter를 한 번 누릅니다.
  exit
docker ps -a             Exited 상태 확인
docker rm my-ubuntu
-->

### 9.1 hello-world

```bash
✏️ docker run hello-world 명령과 출력 붙여넣기
```

### 9.2 ubuntu 컨테이너

```bash
✏️ 컨테이너 내부 명령과 출력 붙여넣기
```

### 9.3 attach와 exec 비교

<!-- 아래 내용은 내 관찰 결과와 일치하는지 확인한 뒤 내 말로 고칩니다. -->

| 구분 | 동작 | 내 관찰 결과 |
| --- | --- | --- |
| `docker exec -it` | 실행 중인 컨테이너에서 새 프로세스를 시작합니다. 그 셸을 종료해도 메인 프로세스는 유지됩니다. | ✏️ 관찰 결과 |
| `docker attach` | 메인 프로세스의 입출력에 연결합니다. 여기서 `exit`하면 메인 프로세스가 끝나 컨테이너도 종료됩니다. | ✏️ 관찰 결과 |

```bash
✏️ exec, attach 실습 명령과 출력 붙여넣기
```

## 10. Dockerfile 기반 커스텀 이미지

<!--
[방식 A] 기존 웹 서버 이미지에 정적 콘텐츠를 교체합니다.

1. 터미널에서 nano site/index.html 로 직접 작성합니다. 내용은 자유롭게 바꾸되
   이후 실습을 위해 아래 줄은 그대로 포함합니다.
   <p>version: v1</p>

2. 프로젝트 최상위에서 nano Dockerfile 로 직접 작성합니다. 아래는 구성 예시입니다.
   미션 예시를 그대로 제출하면 안 되므로 라벨 값, 페이지 내용 등을 내 것으로 바꿉니다.

   FROM nginx:alpine
   LABEL org.opencontainers.image.title="<내 이미지 이름>"
   ENV APP_ENV=dev
   COPY site/ /usr/share/nginx/html/
   HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
     CMD wget -q --spider http://127.0.0.1/ || exit 1

3. 빌드 및 확인
   cd ~/workstation-mission
   docker build -t my-web:1.0 .
   docker images my-web
-->

### 10.1 선택한 베이스

- **베이스 이미지:** ✏️ 예: `nginx:alpine`
- **선택 이유:** ✏️ 내 선택 이유
- **소스:** [site/index.html](site/index.html), [Dockerfile](Dockerfile)

### 10.2 커스텀 포인트

| 항목 | 적용 내용 | 목적 |
| --- | --- | --- |
| `LABEL` | ✏️ 적용 값 | ✏️ 이미지 정보 표시 |
| `ENV` | ✏️ 적용 값 | ✏️ 실행 모드 구분 |
| `COPY` | ✏️ 적용 값 | ✏️ 기본 페이지를 내 콘텐츠로 교체 |
| `HEALTHCHECK` | ✏️ 적용 값 | ✏️ 웹 서버 응답 상태 확인 |

### 10.3 Dockerfile

```dockerfile
✏️ 내가 작성한 Dockerfile 전체 붙여넣기
```

### 10.4 빌드 결과

```bash
✏️ docker build, docker images 명령과 핵심 출력 붙여넣기
```

## 11. 포트 매핑 및 접속 증거

<!--
docker run -d -p 8080:80 --name my-web-8080 my-web:1.0
curl -i http://localhost:8080
docker run -d -p 8081:80 --name my-web-8081 my-web:1.0
curl -i http://localhost:8081
docker ps
docker inspect --format '{{.State.Health.Status}}' my-web-8080
docker logs my-web-8080

브라우저에서 두 주소를 열고 주소창이 보이도록 캡처합니다(Win+Shift+S).
파일은 docs/images/port-8080.png, docs/images/port-8081.png로 저장합니다.
-->

```bash
✏️ 컨테이너 실행, curl, docker ps, 상태 확인 명령과 출력 붙여넣기
```

**http://localhost:8080 접속 화면**

![8080 포트 접속 화면](docs/images/port-8080.png)

**http://localhost:8081 접속 화면**

![8081 포트 접속 화면](docs/images/port-8081.png)

## 12. 바인드 마운트 변경 반영

<!--
cd ~/workstation-mission
docker run -d --name my-web-bind -p 8082:80 -v "$(pwd)/site:/usr/share/nginx/html" my-web:1.0

[변경 전]
curl -s http://localhost:8082 | grep "version:"

[호스트 파일 수정]
sed -i 's/version: v1/version: v2/' site/index.html

[변경 후]
curl -s http://localhost:8082 | grep "version:"     v2가 나와야 합니다.
curl -s http://localhost:8080 | grep "version:"     이미지로 실행한 컨테이너는 v1이 유지됩니다.

[정리]
sed -i 's/version: v2/version: v1/' site/index.html
docker rm -f my-web-bind
-->

```bash
✏️ 실행 명령과 변경 전후 출력 붙여넣기
```

**결과 해석:** ✏️ 8082와 8080의 응답이 달랐던 이유를 이미지와 마운트의 차이로 설명

## 13. Docker 볼륨 영속성

<!--
docker volume create web-data
docker volume ls
docker volume inspect web-data
docker run -d --name vol-a -v web-data:/data ubuntu sleep infinity
docker exec vol-a sh -c "echo 'persist-test' > /data/note.txt && cat /data/note.txt"

[컨테이너 삭제]
docker rm -f vol-a
docker ps -a

[새 컨테이너에서 확인]
docker run -d --name vol-b -v web-data:/data ubuntu sleep infinity
docker exec vol-b cat /data/note.txt

[정리]
docker rm -f vol-b
-->

```bash
✏️ 볼륨 생성, 연결, 삭제 전후 검증 명령과 출력 붙여넣기
```

**결과 해석:** ✏️ 컨테이너를 삭제해도 데이터가 남은 이유

## 14. Git 설정 및 GitHub 연동

<!--
[Git 설정]
git config --global user.name "<GitHub 이름>"
git config --global user.email "<GitHub noreply 이메일>"
git config --global init.defaultBranch main
git config --list
개인 이메일이 보이면 마스킹합니다.

[저장소 연결]
1. GitHub에서 비어 있는 Public 저장소를 만듭니다.
   README, .gitignore를 자동 생성하지 않습니다.
2. 프로젝트에서 실행합니다.
   cd ~/workstation-mission
   code .
3. VSCode 왼쪽 아래 계정 메뉴에서 GitHub에 로그인합니다.
4. VSCode 통합 터미널에서 실행합니다.
   git init
   git status
   git add .
   git commit -m "docs: 개발 워크스테이션 미션 결과 정리"
   git remote add origin https://github.com/<내 ID>/<저장소 이름>.git
   git push -u origin main
   git remote -v

[캡처]
VSCode의 GitHub 로그인 상태와 원격 저장소 연결 화면을 캡처합니다.
토큰과 인증 코드가 보이지 않게 하고 docs/images/vscode-github.png로 저장합니다.
-->

### 14.1 Git 설정

```bash
✏️ git config --list 결과 붙여넣기(개인정보 마스킹)
```

### 14.2 GitHub 저장소 연동

```bash
✏️ git status, git remote -v, git log --oneline 결과 붙여넣기
```

![VSCode GitHub 연동 화면](docs/images/vscode-github.png)

## 15. 핵심 개념 정리

<!-- 아래 초안을 이해한 뒤 내 실습 결과를 예로 들어 내 말로 고칩니다. -->

### 절대 경로와 상대 경로

절대 경로는 루트(`/`)에서 시작하므로 현재 위치와 관계없이 같은 대상을 가리킵니다. 예: `/home/user/practice-lab`  
상대 경로는 현재 위치를 기준으로 해석합니다. 예: `../docs`

### 파일 권한과 755, 644

`r`은 읽기(4), `w`는 쓰기(2), `x`는 실행(1)이며, 세 자리 숫자는 차례로 소유자, 그룹, 기타 사용자의 권한 합계입니다.

- `755`: 소유자 `rwx`, 그룹과 기타 사용자 `r-x`
- `644`: 소유자 `rw-`, 그룹과 기타 사용자 `r--`

디렉토리의 `x`는 해당 디렉토리로 들어가거나 그 안의 항목에 접근할 수 있는 권한입니다.

### 이미지와 컨테이너, 커스텀 이미지

이미지는 실행에 필요한 내용을 묶은 읽기 전용 템플릿이고, 컨테이너는 이미지를 실행한 격리된 인스턴스입니다. 커스텀 이미지는 `FROM`으로 기존 이미지를 가져와 필요한 내용만 더해 만들기 때문에 같은 환경을 반복해서 재현할 수 있습니다.

### 포트 매핑이 필요한 이유

컨테이너는 격리된 네트워크에서 실행되므로 내부 포트에 호스트에서 바로 접근할 수 없습니다. `-p <호스트 포트>:<컨테이너 포트>`로 연결하면 호스트 주소로 접속할 수 있고, 내부 포트가 같은 컨테이너도 서로 다른 호스트 포트로 함께 실행할 수 있습니다.

### 바인드 마운트와 Docker 볼륨

| 구분 | 바인드 마운트 | Docker 볼륨 |
| --- | --- | --- |
| 저장 위치 | 내가 지정한 호스트 경로 | Docker가 관리하는 영역 |
| 주요 용도 | 개발 중 코드 변경 즉시 반영 | 데이터베이스 등 영속 데이터 보관 |
| 컨테이너 삭제 시 | 호스트 파일 유지 | 볼륨 데이터 유지 |

### Git과 GitHub

Git은 내 컴퓨터에서 변경 이력을 관리하는 버전 관리 도구입니다. GitHub는 Git 저장소를 원격으로 호스팅하며 코드 리뷰, 이슈 등 협업 기능을 제공하는 플랫폼입니다.

## 16. 트러블슈팅

<!--
실제로 겪은 문제를 2건 이상 기록합니다. 문제가 없었다면 아래 상황을 직접 재현하고
재현했다는 사실을 함께 적습니다.

[포트 충돌] my-web-8080이 실행 중일 때
docker run -d -p 8080:80 --name dup-web my-web:1.0
docker ps -a
docker rm dup-web

[/mnt/c 권한]
cd /mnt/c/Users/<윈도우사용자명>/
touch chmod-test.txt
chmod 600 chmod-test.txt
ls -l chmod-test.txt
rm chmod-test.txt

[그 외 자주 생기는 문제]
- WSL에서 docker 명령을 찾지 못함: WSL Integration 설정 확인
- git push 비밀번호 인증 실패: VSCode 로그인 또는 SSH 키 사용
-->

### 사례 1: ✏️ 문제 제목

- **문제:** ✏️ 발생한 현상과 오류 메시지
- **원인 가설:** ✏️ 처음 예상한 원인
- **확인:** ✏️ 가설을 확인한 명령과 결과
- **해결/대안:** ✏️ 조치 내용과 조치 후 결과

### 사례 2: ✏️ 문제 제목

- **문제:** ✏️ 발생한 현상과 오류 메시지
- **원인 가설:** ✏️ 처음 예상한 원인
- **확인:** ✏️ 가설을 확인한 명령과 결과
- **해결/대안:** ✏️ 조치 내용과 조치 후 결과

## 17. 보안 및 개인정보 점검

- [ ] 문서, 로그, 스크린샷에 토큰, 비밀번호, 개인키, 인증 코드가 없음
- [ ] `git config --list`와 `docker info`의 개인 정보를 확인하고 필요한 부분을 마스킹함
- [ ] 저장소의 커밋 이력에도 민감정보가 없음

<!--
[보너스: 선택 사항] 수행하지 않으면 아래 18장 전체를 삭제합니다.

docker-compose.yml 예시:

services:
  web:
    build: .
    ports:
      - "${WEB_PORT:-8090}:80"
    environment:
      APP_ENV: ${APP_ENV:-dev}
  helper:
    image: nginx:alpine

실행:
docker compose up -d --build
docker compose ps
docker compose logs web
docker compose exec -T web wget -qO- http://helper | head -n 5
docker compose exec web printenv APP_ENV
docker compose down
WEB_PORT=9090 APP_ENV=prod docker compose up -d
curl -I http://localhost:9090
docker compose exec web printenv APP_ENV
docker compose down

GitHub SSH:
ssh-keygen -t ed25519 -C "github-key"
cat ~/.ssh/id_ed25519.pub
공개키(.pub)만 GitHub Settings > SSH and GPG keys에 등록합니다.
ssh -T git@github.com
git remote set-url origin git@github.com:<내 ID>/<저장소 이름>.git
git push
개인키(id_ed25519)는 절대 공유하지 않습니다.
-->

## 18. 보너스 과제

- [ ] Docker Compose 단일 서비스 실행
- [ ] Docker Compose 멀티 컨테이너 및 서비스 이름 통신 확인
- [ ] Compose 운영 명령(`up`, `down`, `ps`, `logs`) 수행
- [ ] 환경 변수로 포트와 모드 변경
- [ ] GitHub SSH 키 등록 및 푸시 확인

```bash
✏️ 수행한 보너스 항목의 명령과 출력 붙여넣기
```

<!--
[제출 전 최종 점검]
1. grep -n "✏️" README.md 를 실행해 채우지 않은 곳을 찾습니다. 이 줄만 나오면 통과입니다.
2. ls docs/images 로 스크린샷 3개가 있는지 확인합니다.
3. 수정 내용을 커밋하고 푸시합니다.
4. GitHub 저장소 화면에서 이미지와 목차 링크를 확인합니다.
5. 저장소 링크를 제출합니다.
-->
