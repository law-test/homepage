# 법학경시대회 홈페이지 v5

## 업로드 방법

ZIP을 풀면 바로 `index.html`, `samples.html`, `about.html`, `assets/`, `photos/` 등이 보입니다.
GitHub 저장소에는 이 파일들을 루트에 그대로 올려야 합니다.

중요: `index.html`만 교체하면 상단 메뉴의 `문제 샘플`, `대회 소개`, `응시자 정보` 등이 파일 없음으로 나올 수 있습니다.
반드시 `samples.html`을 포함한 모든 HTML 파일과 `assets/`, `photos/` 폴더를 함께 올려 주세요.

## 이번 v5 수정

- 상단 메뉴의 내부 링크를 `./samples.html`처럼 로컬 미리보기와 GitHub Pages에서 모두 안전한 상대경로로 정리했습니다.
- `samples.html` 누락/오타 상황에 대비해 `sample.html`, `problem.html`, `problems.html`, `problem-samples.html`, `question-samples.html`, `samples/index.html` 별칭 페이지를 추가했습니다.
- 404 페이지에 홈, 문제 샘플, 공지사항, 문의하기 바로가기를 추가했습니다.
