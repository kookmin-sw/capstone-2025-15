## 🛠 작업 개요
어떤 설정이나 구성을 하려는지 간단히 설명해주세요.

예:
- GitHub 라벨 구성
- .gitignore 파일 작성
- 이슈 템플릿 추가
- 디렉토리 구조 초기화

## 📂 작업 위치
(예: .github/, .gitignore, .vscode/, requirements.txt 등)

## ✅ 체크리스트
- [ ] 설정 작업 계획 확인
- [ ] 관련 파일 작성 또는 수정
- [ ] 커밋 및 PR 생성
- [ ] PR 머지 완료 후 적용 확인
"""

# 파일 저장
infra_file_path = os.path.join(issue_template_path, "infra.md")
with open(infra_file_path, "w") as f:
    f.write(infra_template)

infra_file_path
