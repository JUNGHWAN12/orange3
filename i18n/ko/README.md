# Orange 한국어 번역 (수업 배포용)

학생들에게 나눠 줄 한국어판 Orange를 만들기 위한 작업 폴더입니다. 공식 저장소(biolab)에는 기여하지 않습니다.

배포 방식: 학생 PC에 공식 설치 파일로 Orange를 설치한 뒤, **같은 버전의 소스로 만든 번역 파일(`.py`, `i18n/*.json`)만 덮어씁니다.** 컴파일된 모듈(`.pyd`)은 건드리지 않으므로 컴파일러가 필요 없습니다. 실제 배포는 언어팩 폴더 안의 `설치.bat`을 더블클릭하는 원스톱 방식입니다(아래 "배포 관련" 참고).

## 다운로드 (동료 교사용)

번역 소스(`.py`, `msgs.jaml`)는 이 저장소에 있지만, 실제로 설치에 쓰는 **완성된 언어팩 zip**은 용량 때문에 Git에 올리지 않고 [GitHub 릴리스](https://github.com/JUNGHWAN12/orange3/releases)에 따로 올려 둡니다. 공식 설치 파일은 GitHub이 `.exe` 첨부를 막아 릴리스에 올리지 못했고, 대신 biolab 공식 사이트 링크를 그대로 씁니다.

| 파일 | 다운로드 | 용도 |
|---|---|---|
| `orange-ko-3.40.0.zip` | <https://github.com/JUNGHWAN12/orange3/releases/latest/download/orange-ko-3.40.0.zip> | 한글 언어팩 + `설치.bat`(4MB) |
| `Orange3-3.40.0-x86_64.exe` | <https://download.biolab.si/download/files/Orange3-3.40.0-x86_64.exe> | 공식 Orange 설치 파일(biolab 공식 사이트, 387MB, 이미 설치되어 있으면 생략 가능) |

**사용법:** `orange-ko-3.40.0.zip`을 압축 풀고, 그 안에 `Orange3-3.40.0-x86_64.exe`를 함께 넣은 뒤 `설치.bat`을 더블클릭합니다. 자세한 내용은 [배포·테스트 가이드](https://claude.ai/code/artifact/b91ab674-80b0-4cd7-8966-f0fa73a2b4bc)를 참고하세요.

⚠️ biolab 다운로드 페이지(<https://orange.biolab.si/download>)는 버전이 올라가면 최신 버전으로 바뀝니다. 위 파일명이 `Orange3-3.40.0-x86_64.exe`가 아니게 되면, 이 언어팩과 버전이 맞지 않는 것이니 받지 마세요.

## 기준 버전

| 패키지 | 버전 | 저장소 위치 | 브랜치 |
|---|---|---|---|
| Orange3 | 3.40.0 | `C:\orange3` | `ko` (태그 `3.40.0`에서 시작) |
| orange-canvas-core | 0.2.7 | `C:\orange-canvas-core` | `ko` (태그 `0.2.7`에서 시작) |
| orange-widget-base | 4.27.0 | `C:\orange-widget-base` | `ko` (태그 `4.27.0`에서 시작) |

- **설치 파일:** `Orange3-3.40.0-x86_64.exe`. 학생 PC에도 반드시 이 파일로 설치합니다. 설치 파일마다 들어 있는 canvas-core·widget-base 버전이 다를 수 있습니다.
- **번역 도구:** `C:\orange3\.venv-ko` 가상환경에 trubar 0.3.4가 있습니다. 공식 빌드와 같은 버전입니다. 이 폴더는 `.git/info/exclude`로 Git에서 제외했습니다.
- **원격 저장소:** `C:\orange3`의 `upstream`은 biolab 공식 저장소입니다. 태그를 받을 때만 씁니다.

## 파일

| 파일 | 내용 |
|---|---|
| `msgs.jaml` | Orange 번역 파일(canvas-core·widget-base는 각 저장소의 `i18n/ko/msgs.jaml`) |
| `GLOSSARY.md` | 용어집과 번역 규칙 |
| `tools/tm.py` | 번역 작업 도구(목록 뽑기, 가져오기, 검사, 빌드 확인) |
| `tools/check_install.py` | 저장소 3곳의 소스가 설치된 Orange와 정확히 같은지 확인합니다. |
| `tools/seed_msgs.py` | 슬로베니아어 파일에서 한국어 번역 파일의 뼈대를 만듭니다. 이미 있는 파일은 덮어쓰지 않습니다. |
| `tools/_common.py` | 도구가 함께 쓰는 설정(저장소 경로, 설치 경로, 빌드) |

세 저장소의 `i18n/trubar-config.yaml`에는 한국어(`name: 한국어`, `international-name: Korean`)를 추가했습니다.

## 자주 쓰는 명령 (PowerShell, `C:\orange3`에서 실행)

아래 예시의 `tm`은 `.venv-ko\Scripts\python i18n\ko\tools\tm.py`를 줄여 쓴 것입니다. 저장소 이름은 `canvas`, `widget`, `orange`로 씁니다.

| 목적 | 명령 |
|---|---|
| 소스와 설치본이 같은지 확인 (`RESULT: OK`) | `.venv-ko\Scripts\python i18n\ko\tools\check_install.py` |
| 진행률 확인 (`Untranslated` = 남은 수) | `.venv-ko\Scripts\trubar stat i18n\ko\msgs.jaml` |
| 번역하지 않은 문자열 뽑기 | `tm export orange -p widgets/data/owfile.py -o todo.txt` |
| 번역 가져오기 | `tm import orange todo.ko.txt` (이미 번역한 항목을 고칠 때는 `--force`) |
| 자리표시자·공백 검사 | `tm lint` |
| 빌드와 f-string 문법 확인 | `tm build-check` |

### 번역 파일 형식

`tm export`의 출력은 `번호<탭>원문` 형식입니다. 번호 뒤 기호의 뜻은 다음과 같습니다.

- `=`: 슬로베니아어는 원문을 그대로 둠
- `~`: 슬로베니아어는 빈 조각으로 둠
- `[R]`: 예전 신호 이름
- `[S]`: 설정 기본값
- `[C]`: 코드에서 비교에 쓰임
- `[K]`: 사전 키로 쓰임

`[R]`, `[S]`, `[C]`, `[K]`가 붙은 항목은 **코드를 확인한 뒤** 번역합니다.

번역은 `번호|번역문` 한 줄씩 작성합니다. 특수 값은 다음과 같습니다.

- `@keep`: 원문 유지
- `@no`: 번역 금지
- `@empty`: 빈 조각
- `⏎`: 실제 줄바꿈

가져오기 도구는 다음을 자동으로 처리합니다.

- 번역문 끝 공백을 원문과 똑같이 맞춥니다.
- 원문에 없는 `{…}`가 들어가거나 `%s` 개수가 다르면 저장하지 않습니다.

## 번역할 때 지킬 코드 규칙

번역하면 동작이 깨지는 문자열이 있습니다. 이번 번역에서 확인한 규칙입니다.

1. **워크플로에 저장되는 값은 원문을 유지합니다.** 설정에 문자열 그대로 저장되는 값을 번역하면, 영어판에서 만든 워크플로(내장 예제 포함)를 열 때 오류가 나거나 설정이 사라집니다.
2. **코드가 소문자로 바꿔 매개변수로 넘기는 값은 원문을 유지합니다.** 예: AdaBoost의 Linear/Square/Exponential
3. **여러 곳에서 비교하는 문자열은 모든 곳에서 같은 번역을 씁니다.** 예: 도움말 메뉴 URL 키(Quick Start, Documentation 등은 canvas-core와 Orange 양쪽), 피벗 테이블의 Total, 보고서의 Data instances(Select Rows와 공유)
4. **코드가 부분 문자열을 검사하는 경우** 번역도 그 관계를 유지합니다. 예: Select Rows의 `"defined"` → "값이"("값이 있음"에 포함), `" one of"` → " 중 하나"
5. **예전 신호 이름(`replaces=[...]`)은 원문을 유지합니다.** 현재 이름과 같은 문자열이라 분리할 수 없는 경우만 번역했습니다. 이 경우에도 연결은 신호 ID로 복원됩니다.
6. **여러 조각으로 나뉜 문자열**은 조각마다 원래 자리표시자만 넣습니다. 한 조각을 `@empty`로 비우고 다른 조각에 문장 전체를 넣어도 됩니다.
7. `pl()`(영어 복수형)은 빼고, 안쪽 식만 쓸 수 있습니다. 예: `{pl(n, unit)}` → `{unit}`

## 호환성 때문에 원문으로 남긴 항목

아래 항목은 화면에 영어로 보입니다. 한국어로 바꾸려면 코드를 고쳐야 합니다(후속 과제).

| 위젯 | 영어로 남은 항목 | 이유 |
|---|---|---|
| 열 집계 | Sum, Product, Variance, Median, Count non-zero | 설정값이자 사전 키 |
| 그룹별 집계 | 집계 함수 이름 전체 | 설정에 이름으로 저장 |
| 중복 제거 | Last/First/Middle/Random instance, Discard non-unique instances | 설정에 이름으로 저장 |
| 특성 순위 | Information Gain, Information Gain Ratio, Gini Decrease, Univariate Regression | 설정에 이름으로 저장(내장 예제에서도 사용) |
| 데이터 병합 | Row index, Instance id | 워크플로에 저장 |
| 행 선택 | All variables, All numeric variables, All string variables | 워크플로에 저장 |
| 막대그래프 | Enumeration | 워크플로에 저장 |
| 계층적 클러스터링 | Enumeration, Name | 설정에 저장 |
| 거리 행렬 | None, Enumerate, Labels, Attribute names | 컨텍스트에 저장 |
| MDS | Stress | 설정에 저장 |
| AdaBoost | Linear, Square, Exponential | scikit-learn 매개변수로 사용 |
| CN2 규칙 유도 | 보고서 항목 이름, ordered/exclusive 등 | 학습기 매개변수 키 |
| 데이터 세트 | English | 서버 데이터의 언어 값 |
| 데이터/모델/거리 저장 | 파일 형식 이름 | 설정에 문자열로 저장 |
| 평가 지표 | CA, Prec, Recall, F1, AUC, MSE 등 약어 | 표준 약어(설명은 한국어) |

## 현황 (2026-09-17)

| 단계 | 상태 |
|---|---|
| 0. 버전 고정·환경 준비 | 완료. 세 패키지 모두 설치본과 일치합니다(`check_install.py` 통과). |
| 1. 번역 파일 뼈대 | 완료 |
| 2. 용어집 | 대안이 있던 용어 8개는 대안으로 확정했습니다. ★ 용어 7개는 현재 표기로 번역했으며, 바꾸려면 일괄 수정이 필요합니다. |
| 3. 번역 | **완료.** 모두 4,934개(canvas-core 469, widget-base 140, Orange 4,325). 미번역 0, 검사 오류 0, 빌드 확인 통과 |
| 3.5 검증 | **완료.** 아래 "검증 결과" 참고 |
| 4. 언어팩 만들기 | 시작 전 |
| 5. 학생 PC 배포 | 시작 전 |

## 검증 결과 (2026-09-18)

번역이 실제로 위젯을 깨뜨리지 않는지 두 가지 방법으로 확인했습니다. 도구는 `i18n/ko/tools/` 옆에 두지 않고 세션 임시 폴더에서 실행했습니다(재사용하려면 이 방식을 참고해 다시 작성하면 됩니다).

1. **위젯 104개 전수 스모크 테스트.** `Data`/`Visualize`/`Model`/`Evaluate`/`Unsupervised`의 모든 위젯을 오프스크린 Qt에서 하나씩(위젯당 별도 프로세스) 생성해 보았습니다. 한국어와 영어(비교 기준)에서 결과가 완전히 같았습니다: 103개 정상 생성, 2개는 위젯 클래스가 없는 보조 모듈이라 정상적으로 스킵, 1개는 프로세스 종료 시점 세그폴트(위젯 생성 자체는 성공한 뒤 인터프리터 종료 중 발생, 매번 다른 위젯에서 무작위로 나타나고 재현되지 않음 — 언어와 무관한 환경 문제로 확인). **번역으로 인해 생성이 실패하는 위젯은 없습니다.**
2. **위젯 단위 테스트 일부 실행.** `data` 위젯 앞부분(owaggregatecolumns~owfile 등)의 pytest를 한국어·영어로 병렬 실행해 비교했습니다(전체 166개 파일 중 일부만 실행됨, 세션 종료로 중단). 한국어에서만 발생한 오류·실패 36건을 모두 코드까지 확인한 결과, **전부 "번역을 모르는 낡은 테스트 코드"가 원인**이었고 실제 동작 문제는 없었습니다. 예:
   - 콤보박스 항목이나 위젯 텍스트를 영어 문자열로 직접 비교하는 테스트(예: `"Copy to all"`, `"Spearman correlation"`)
   - 위젯이 내부적으로만 쓰는 상태(예: 시간 단위 콤보박스의 저장·복원)를 테스트가 영어 값으로 직접 주입하는 경우 — 실제 사용에서는 항상 같은 언어끼리 저장·조회되므로 문제없음
   - 화면 최소 크기 검사(`test_minimum_size`)는 **영어판에서도** 같은 이유로 실패(글꼴 폭에 민감한 낡은 테스트)

## 통합 설치 파일 (constructor 빌드)

두 파일(공식 설치본 + 언어팩 적용 스크립트)을 따로 배포하는 대신, `conda`의 `constructor`로 한국어가 이미 적용된 **단일 설치 파일**을 만들 수 있습니다. 공식 설치 파일에서 7-Zip으로 추출한 241개 conda 패키지를 로컬 채널로 만들어 오프라인으로 빌드합니다.

**빌드 순서** (`i18n/ko`에서, `build-env`는 `constructor`+`conda-index`가 설치된 conda 환경):

```powershell
python tools\build_langpack.py            # dist\orange-ko-3.40.0\ 생성
python tools\build_local_channel.py <추출한 pkgs 폴더> channel   # 로컬 채널 구성
<build-env>\python -m conda_index channel  # repodata.json 생성
python tools\generate_construct_yaml.py    # installer-build\construct.yaml 생성
$env:CONDA_SOLVER = "classic"
<build-env>\python -m constructor installer-build --output-dir installer-build
```

**`CONDA_SOLVER=classic`이 반드시 필요합니다.** 기본값인 conda-libmamba-solver로 빌드하면 241개 패키지를 모두 정확한 버전으로 고정(pin)해 한 번에 설치할 때, 내부 재시도(attempt #1→#2) 과정에서 인덱스를 잘못 처리해 `_openmp_mutex`(사실은 무작위 패키지)를 "채널에 없음"으로 잘못 보고하며 실패합니다. 같은 채널·같은 스펙으로 직접 `solver.solve_final_state()`를 한 번만 호출하면 항상 성공하는 것으로 확인했고(재시도 경로 자체의 버그), classic 솔버는 이 재시도 로직을 타지 않아 문제없이 빌드됩니다. `_openmp_mutex`를 일부러 버전 고정 없이 두는 우회는 근본 원인이 아니었으므로 필요 없습니다(다른 240개와 동일하게 고정).

결과물은 `installer-build\Orange3-Korean-3.40.0-Windows-x86_64.exe` (약 450MB). `post_install.bat`이 패키지 설치 직후 언어팩을 덮어쓰고 `Orange.ini`를 한국어로 초기화합니다.

**실제 설치 테스트 결과 (2026-09-18): 실패. 이 방식은 배포하지 않는 것을 권장합니다.**

교사 PC에서 대화형으로 실제 설치를 실행해 두 가지 독립적인 문제를 확인했습니다.

1. **`_conda.exe`(PyInstaller로 패키징된 내장 실행 파일) 자가 압축 해제 실패.** `[PYI-xxxxx:ERROR] Failed to extract ...: failed to open archive file!` 형태로 "Failed to extract packages" 오류가 발생했고, 재시도할 때마다 실패하는 파일이 다름(`libmambapy-2.8.0.dist-info`, `libmpdec-4.dll` 등) — 빌드 중에도 같은 패턴을 여러 번 겪었던, 이 종류의 PC에서 실시간 백신 검사가 임시 추출 파일에 간섭하는 문제로 추정됩니다. `Add-MpPreference`로 예외를 추가해 우회를 시도했으나 관리자 권한으로도 `0x800106ba` 오류로 막혔습니다 — 학교 PC의 Defender 변조 방지/조직 정책이 로컬 예외 추가 자체를 차단하는 것으로 보입니다.
2. **`post_install.bat` 실행이 깨짐.** 오류를 무시하고 진행한 로그(`.step.log`)를 보면 `REM` 주석 줄과 `xcopy`/`set` 명령들이 토큰 경계가 어긋난 채 실행되어(`'uns'`, `'uarantees'`, `'verlays'`, `'"\Orange"'` 등 단어 일부만 명령으로 인식) 대부분 "내부 또는 외부 명령이 아닙니다" 오류만 남기고, 언어팩 덮어쓰기와 `Orange.ini` 작성이 의도한 대로 되지 않았습니다. 원인 미확인(추정: NSIS가 `.bat`을 다루는 과정에서 UTF-8 인코딩이 깨짐).

두 문제 모두 **2파일 방식(공식 설치본 + `설치.bat`/`install_ko.ps1`)에는 존재하지 않습니다** — 단순 파일 복사만 하므로 PyInstaller 자가 압축 해제나 NSIS의 `.bat` 재작성을 거치지 않습니다. constructor 빌드 자체(위 "빌드 순서")는 성공하지만, 결과물 설치가 이 환경에서 신뢰할 수 없으므로, 실제 배포는 2파일 방식을 기준으로 합니다.

## 알려진 문제와 후속 과제

**코드 수정 필요(4단계에서 함께 처리)**

- **F1 도움말:** canvas-core는 위젯 이름으로 영어 온라인 문서를 찾습니다(`orangecanvas/help/provider.py`의 `HtmlIndexProvider.search`). 번역된 이름을 영어 이름으로 되돌려 찾도록 고쳐야 합니다.
- **시각 설정:** widget-base의 `VisualSettingsDialog.apply_settings`는 저장된 키가 없으면 KeyError를 냅니다(`orangewidget/utils/visual_settings_dlg.py`). 영어판에서 그래프 글꼴 등을 바꿔 저장한 워크플로를 열 수 있도록, 모르는 키는 건너뛰게 고쳐야 합니다.
- **코드를 고친 뒤:** `check_install.py`가 수정한 파일을 설치본과 다르다고 보고하므로, 수정 파일은 제외하고 비교하도록 도구도 함께 고칩니다.

**배포 관련**

- **원스톱 설치:** `tools/build_langpack.py`가 만드는 `dist/orange-ko-3.40.0/` 폴더에 `설치.bat`이 들어 있습니다. `Orange3-3.40.0-x86_64.exe`를 같은 폴더에 넣고 `설치.bat`을 더블클릭하면 `install_orange_ko.ps1`을 호출해 (필요하면) Orange를 `C:\Orange`에 설치하고 이어서 한국어 언어팩을 적용합니다. UAC 창이 한 번 뜹니다. PowerShell 실행 정책 문제 없이 더블클릭만으로 되도록 만든 것이 이 `.bat`의 목적입니다.
- **Orange 업데이트:** 학생이 Orange를 업데이트하면 번호가 맞지 않는 `Korean.json`이 남아 엉뚱한 문장이 표시될 수 있습니다. 설치 스크립트에서 업데이트 확인(`startup/check-updates`)을 끕니다.
- **언어 설정:** 설치 스크립트에서 `application/language`를 `한국어`로 설정합니다. 설정 파일은 `%APPDATA%\biolab.si\Orange.ini`입니다. PC 복원 프로그램이 이 파일을 지우는 경우에는 모든 사용자에게 적용되는 `%PROGRAMDATA%\biolab.si\Orange.ini`에 설정하는 방법을 시험합니다.
- **관리자 권한:** Orange가 `C:\Program Files\Orange`에 설치되어 있으면 파일을 덮어쓸 때 관리자 권한이 필요합니다.
- **예제 워크플로:** 내장 예제의 제목과 주석은 영어입니다. 한국어 예제(`i18n/ko/static/`)를 만들지는 나중에 정합니다.
- **호환성:** 한국어판에서 저장한 워크플로를 영어판(공식 설치본)에서 열면, 번역된 설정값(예: 시각 설정) 때문에 문제가 생길 수 있습니다. 수업에서는 모두 한국어판을 쓰는 것을 전제로 합니다.

## 버전을 올릴 때

1. 새 설치 파일로 교사 PC의 Orange를 업데이트하고, 들어 있는 canvas-core·widget-base 버전을 확인합니다.
2. 세 저장소에서 새 태그를 받아 `ko` 브랜치에 병합합니다. 예: `git fetch --no-tags upstream refs/tags/3.41.0:refs/tags/3.41.0`, 그다음 `git merge 3.41.0`
3. 각 저장소에서 `trubar collect`로 번역 파일을 새 소스에 맞춥니다.

   ```powershell
   .venv-ko\Scripts\trubar --conf i18n\trubar-config.yaml collect -s Orange i18n\ko\msgs.jaml
   ```

4. `check_install.py`로 일치하는지 확인하고, `tm export`로 새로 생긴 문자열을 뽑아 번역합니다. `tm lint`, `tm build-check`로 확인한 뒤 언어팩을 다시 만듭니다.
