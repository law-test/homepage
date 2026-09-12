# 법학경시대회 홈페이지

[lawtest.or.kr](https://lawtest.or.kr/)에서 서비스하는 정적 홈페이지입니다. 공통 메뉴·회차 정보·논문 목록을 한 곳에서 관리하고 HTML을 생성합니다. 빌드는 Python 3 표준 라이브러리만 사용합니다.

## 내용 수정

- `data/site.json`: 제8회 시상식·수상자·점수, 제1~7회 기록, 소속 학교와 미확정 항목.
- `data/publications.json`: 논문 서지, KCI·DOI, 수상자 논문과 관련 연구 분류.
- `content/*.html`: 각 페이지 본문. 생성된 루트 HTML을 직접 수정하지 않습니다.
- `templates/layout.html`: 공통 메뉴·배너·푸터·검색 및 공유 정보.
- `assets/css/updates.css`, `assets/js/site.js`: 공통 화면과 메뉴·사진 확대 동작.
- `docs/content-sources.md`: 확인 자료와 미확정 항목.

## 빌드와 확인

저장소 루트에서 실행합니다.

```sh
python -X utf8 scripts/build_site.py
python -X utf8 scripts/check_site.py
node --check assets/js/site.js
python -m http.server 8765 --bind 127.0.0.1
```

마지막 명령은 로컬 확인용 서버입니다. `http://127.0.0.1:8765/`에서 데스크톱·모바일 메뉴, 공지·FAQ 바로가기, 정답 펼치기와 사진 확대를 확인합니다. 정적 검사는 내부 링크·앵커·공통 메뉴·제목·구조화 데이터·핵심 수상 결과를 검사합니다. 실제 시험 시스템이나 외부 결제는 검사하지 않습니다.

생성된 루트 HTML 15개와 `sitemap.xml`도 함께 커밋합니다. 기존 GitHub Pages 배포 경로와 `CNAME`을 유지합니다. `.nojekyll`은 생성된 파일을 그대로 배포하도록 합니다.

## 제8회 사진 추가

확정 사진을 `assets/images/`에 저장하고 `data/site.json`의 `round8.photo`에 `/assets/images/파일명.jpg` 형식으로 경로를 입력한 뒤 다시 빌드합니다. 사진이 없는 동안에는 빈 사진 영역과 안내가 표시됩니다. 다른 회차의 사진으로 대신하지 않습니다.

## 확인이 필요한 정보

제9회 일정·요강은 미정입니다. 운영 기준이 확정되면 응시 안내·공지·FAQ·약관을 함께 갱신합니다. 새 접수 배너의 회차와 일정도 공통 레이아웃에서 변경합니다. 점수는 공개 허락된 값만 사용하며 원본 신청서·채점표·연락처는 저장소에 올리지 않습니다.
