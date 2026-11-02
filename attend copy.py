import os

# 출석 데이터를 저장할 파일 이름
DB_FILE = "attendance.txt"

def add_attendance():
    """새로운 출석 기록을 추가합니다."""
    date = input("날짜를 입력하세요 (예: 2023-10-27): ")
    name = input("이름을 입력하세요: ")
    
    # 'a' 모드는 append(추가)를 의미합니다. 파일이 없으면 새로 생성합니다.
    with open(DB_FILE, "a", encoding="utf-8") as f:
        f.write(f"{date},{name}\n")
    
    print(f"\n✅ {name}님의 출석이 기록되었습니다!")

def view_attendance():
    """저장된 모든 출석 기록을 보여줍니다."""
    if not os.path.exists(DB_FILE):
        print("\n아직 출석 기록이 없습니다.")
        return

    print("\n--- [스터디 출석 목록] ---")
    print(f"{'날짜':<15} | {'이름'}")
    print("-" * 25)
    
    # 'r' 모드는 read(읽기)를 의미합니다.
    with open(DB_FILE, "r", encoding="utf-8") as f:
        for line in f:
            # strip()으로 줄바꿈을 제거하고, ','를 기준으로 나눕니다.
            date, name = line.strip().split(",")
            print(f"{date:<15} | {name}")
    print("-" * 25)

def main():
    """프로그램의 메인 메뉴를 실행합니다."""
    while True:
        print("\n[스터디 출석 관리 프로그램]")
        print("1. 출석 체크하기")
        print("2. 출석 명단 보기")
        print("3. 종료하기")
        
        choice = input("원하는 메뉴 번호를 선택하세요: ")
        
        if choice == '1':
            add_attendance()
        elif choice == '2':
            view_attendance()
        elif choice == '3':
            print("프로그램을 종료합니다. 열공하세요!")
            break
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")

if __name__ == "__main__":
    main()