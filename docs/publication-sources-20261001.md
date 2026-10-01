# 2026-10-01 학생 공동연구 논문 반영 근거

사용자가 제공한 KCI 논문 3편을 `data/publications.json`에 추가했다. 제목, 저자 순서, 학술지, 권호, 수록 면, DOI와 KCI 등재 여부는 KCI 상세 페이지에서 확인했다. 발행 월은 아래 권호 정보와 공식 발간 기록으로 확인했다. 원문 초록의 법률 해석을 홈페이지 설명으로 재가공하지 않고 서지정보를 제공한다.

| 논문 | 저자 순서 | 학술지·권호 | 발행 | 수록 면 | DOI |
| --- | --- | --- | --- | --- | --- |
| 민간 AI ‘헌법’의 행동 구현에 대한 공법적 통제 — 범용모델 공급자의 규범번역권력을 중심으로 | 김민규·남한결·박상영 | 중앙법학 28권 3호 | 2026.09 | 53–97 | 10.21759/caulaw.2026.28.3.53 |
| 개인파산에서 파산선고 후 성립한 납부지연가산세의 절차상 지위와 면책 — 기간경과형 조세 부대채권의 분류와 입법적 조정을 중심으로 | 김민규·박병재 | 법학논총(숭실대학교 법학연구소) 66호 | 2026.09 | 41–78 | 10.35867/ssulri.2026.66..002 |
| 재량적 과징금 산정지원의 자동화와 행정법적 통제 — 「행정기본법」 제20조의 적용경계와 인간･시스템의 역할분배를 중심으로 | 김민규·박상영 | 법제 714호 | 2026.09 | 43–91 | 10.23028/moleg.2026.714..001 |

## 공식 출처

1. 민간 AI 헌법 논문
   - [KCI 상세·인용정보](https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART003388860)
   - [KCI 중앙법학 28권 3호](https://www.kci.go.kr/kciportal/po/search/poSereArtiList.kci?sereId=001297&volIsseId=VOL000201054): 2026년 9월 발행, 저자 및 53–97면 대조.
2. 개인파산·납부지연가산세 논문
   - [KCI 상세·인용정보](https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART003384878)
   - [KCI 숭실대학교 법학논총 66호](https://www.kci.go.kr/kciportal/po/search/poSereArtiList.kci?sereId=SER000014369&volIsseId=VOL000200778): 2026년 9월 발행, 저자 및 41–78면 대조.
3. 재량적 과징금 산정지원 논문
   - [KCI 상세·인용정보](https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART003380714)
   - [국가기록원 법제 제714호 발간등록](https://archives.go.kr/next/newmanager/publishmentSubscriptionDetail.do?gubun_flg=&keyword=&page=58&prt_seq=198801): 법제 2026년 9월호, 발간일자 2026-09-15.
   - [법제처 학술지 공식 홈페이지](https://moleg.jams.or.kr/co/main/jmMain.kci): 제714호를 2026년 9월호로 명시.

## 분류와 표현

- 세 편은 사용자의 “학생들이랑 논문썼어”라는 설명에 따라 `student_collaboration`으로 분류했다.
- KCI 저자 이름과 순서를 그대로 반영했다. 박병재와 남한결을 수상자로 단정하는 별도 소개는 추가하지 않았다.
- 기존 `recipient` 6편은 유지하고, 홈페이지에서는 “학생 공동연구·수상자 학술 논문”이라는 제목으로 총 9편을 함께 제공한다.
- 같은 달의 신규 논문은 KCI 번호 역순으로 배치했으며, 확인되지 않은 일별 발행 순서를 주장하지 않는다.
- KCI 상세 페이지 두 건은 검색 도구에서 일시적으로 열리지 않아 같은 공식 URL에 대한 직접 HTTP 요청으로 HTML을 읽고 메타태그와 본문 서지정보를 대조했다. 권호 정보도 같은 공식 사이트에서 직접 확인했다.

## 공모전 종료 표시

`content/achievements.html`의 제2회 자기주도 학습법 공모전 안내를 “접수 마감” 및 “지난 공고 및 양식 보기”로 변경했다. 접수 종료일은 기존 공고의 2026-09-26과 사용자의 마감 확인을 근거로 한다.
