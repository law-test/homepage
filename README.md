# 법학경시대회 홈페이지 v6 (응시자 중심 개편)

## 업로드 방법

ZIP을 풀면 `index.html` 등 HTML 파일들과 `site.css`, `site.js`, `assets/images/` 폴더가 보입니다.
GitHub 저장소 루트에 그대로 올리시면 됩니다.

기존 `assets/images/` 폴더의 다른 이미지 파일(로고, 시상식 사진, favicon 등)은 그대로 두시고,
새로 들어간 `r8_poster_hero.jpg`, `r8_poster_og.jpg`, `r8_poster_full.jpg` 세 파일만 추가로 업로드하시면 됩니다.

## v6에서 바뀐 것

### 1. 일정 통일 — 사이트 전역
- 모든 페이지에서 **2026년 8월 1일 (토) 오후 2시**로 통일 (이전: 8월 중순/일요일 표기 혼재)
- **접수 마감 2026년 7월 31일 (금) 자정** 명시 (notice-bar, 메인 INFO CARDS, schedule)
- JSON-LD startDate/endDate `2026-08-01`로 정정

### 2. 카피 톤 — 위원회 중심 → 응시자 중심
- Hero: "결과는 정직하게 변별됩니다" → "이미 일곱 번의 무대를 지나갔습니다. 여덟 번째 자리, 당신의 100분으로 채워 보세요."
- PILLARS 3개 모두 응시자가 받는 것 중심으로 재작성
- "본 대회는..." 어조 전면 정리 → "이 대회는...", "100분의 시험..." 등
- about/voices/samples/universities 페이지 헤더 모두 응시자 중심 카피로 교체

### 3. 응시 규모 역산 차단
- "약 300명 수상자" 같은 절대 수치 사이트 전역 삭제
- meta description, og:description, twitter:description 모두 정리
- 회차 수치(7회)는 유지, 응시 규모는 정성 표현(스펙트럼·다양성)으로 대체

### 4. HTML 주석 전면 제거
- 14개 파일 약 185개의 주석 제거 (작업 메모성 포함)
- 소스 코드를 응시자가 봐도 깔끔하게

### 5. 제7회 수상자 25명 수상소감 신설
- voices.html 하단에 새 섹션 추가
- 성+이니셜 마스킹 (예: 김O름) · 설문 동의 범위 내 공개
- 응시자 입장에서 "내가 응시하면 어떤 사람이 옆에 있을까"에 답하는 콘텐츠

### 6. 제8회 포스터 — 새 hero 이미지
- 8회 포스터를 JPG로 변환 + 3가지 사이즈로 최적화
  - `r8_poster_hero.jpg` (720×1012, hero 영역용)
  - `r8_poster_og.jpg` (1200×1687, og·twitter 카드용)
  - `r8_poster_full.jpg` (896×1260, lightbox·아카이브용)
- 원본 PNG는 별도 보존

### 7. 메인 SCHEDULE 영역 재편
- 제7회 결과 + 제8회 일정 6단계 (접수 마감 → 시험 → 시상)로 재구성
- 제8회 접수 마감일(7/31)이 메인에서 즉시 보이도록

### 8. media.html 인용 보강
- 17건 → 29건으로 확대 (법률신문 제3·4·5회 추가, ContestKorea 등)
- 통계 카드 갱신 (법조·종합 매체 8개, 대학 공식 4개, 변협·해외·플랫폼 5개)

## 손대지 않은 것

- 디자인·레이아웃·CSS 구조 (`recipient-card` 관련 CSS만 site.css 끝에 추가)
- 접수 URL (`smartstore.naver.com/lawtest` 유지 — `mylawtest.com`이 여기로 포워딩)
- 시상식 사진·로고·favicon 등 기존 이미지 자산
- site.js 동작
