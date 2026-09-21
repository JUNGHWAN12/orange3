# Orange 한국어 번역 용어집

Orange 3.40.0(orange-canvas-core 0.2.7, orange-widget-base 4.27.0)을 한국어로 번역할 때 쓰는 용어와 규칙입니다.
세 저장소(`orange3`, `orange-canvas-core`, `orange-widget-base`)의 `i18n/ko/msgs.jaml`에 모두 적용합니다.

- **★** 표시는 수업에서 쓰는 교과서에 맞춰 확정해야 하는 용어입니다. 번역을 시작하기 전에 확정하고 ★를 지웁니다.
- 용어를 바꾸면 이미 번역한 문자열도 함께 고쳐야 합니다. 번역 파일에서 검색해 한꺼번에 수정합니다.

## 1. 결정 사항

| 항목 | 결정 | 근거·주의 |
|---|---|---|
| 위젯 이름 | 번역한다 | 학생의 이해를 우선합니다. 온라인 자료는 영어 이름을 쓰므로 학습지에 6장의 대응표를 넣습니다. |
| 위젯 검색 키워드 | 영어를 그대로 두고 한국어를 덧붙인다 | 예: `file, load, read, open` → `file, load, read, open, 파일, 불러오기, 읽기, 열기`. 영어 이름으로도 검색됩니다. |
| 카테고리 이름 | 번역한다 | 데이터 / 변환 / 시각화 / 모델 / 평가 / 비지도 학습 |
| 신호(채널) 이름 | 번역한다 | 워크플로 파일은 언어와 무관한 신호 ID(`data` 등)로 연결되므로 영어 워크플로도 열립니다. 신호 ID가 없는 아주 오래된 워크플로는 연결이 빠질 수 있습니다. |
| F1 도움말 | **후속 과제** | 도움말은 위젯 이름으로 영어 문서를 찾으므로, 이름을 번역하면 찾지 못합니다. canvas-core를 수정해야 합니다([README](README.md) 참고). |
| 알고리즘 약어 | 그대로 둔다 | PCA, SVM, kNN, t-SNE, MDS, DBSCAN, CN2, PLS, ROC, AUC, SQL, CSV 등 |

## 2. 문체와 표기

| 대상 | 규칙 | 예 |
|---|---|---|
| 메뉴·버튼·탭 | 짧은 명사형 | Open → 열기, Save As... → 다른 이름으로 저장..., Apply → 적용 |
| 체크박스·옵션 | 명사형 또는 "~하기" | Show legend → 범례 표시, Open on double click → 두 번 클릭하여 열기 |
| 위젯 설명·도구 설명(툴팁) | "~합니다" | Read data from an input file… → 파일이나 네트워크에서 데이터를 읽어 출력으로 보냅니다. |
| 오류·경고·정보 메시지 | "~합니다/~습니다", 요청은 "~하세요" | No data on input → 입력 데이터가 없습니다. / Choose another location. → 다른 위치를 선택하세요. |
| 확인 질문 | "~할까요?" | Save Changes? → 변경 사항을 저장할까요? |

- **외래어 표기:** 국립국어원 외래어 표기법을 따릅니다. 예: 워크플로, 메타데이터, 레이블. 다만 널리 굳어진 표기는 그대로 씁니다. 예: 그래디언트(표준 표기는 그레이디언트)
- **띄어쓰기:** 표준 띄어쓰기를 따르되, 한 단어로 굳은 용어는 붙여 씁니다. 예: 막대그래프, 꺾은선그래프
- **줄임표·콜론:** 원문의 `...`, `:`는 그대로 둡니다. 예: `Filter...` → `필터...`, `Name:` → `이름:`
- **단축키 표시(`&`):** 한국어 뒤 괄호 안에 붙입니다. 예: `&File` → `파일(&F)`, `Cu&t` → `잘라내기(&T)`
- **숫자:** 단위 명사를 붙입니다. 한국어는 복수형 처리(`pl()`)가 필요 없으므로 빼도 됩니다.
  - `{n} {pl(n, 'instance')}` → `행 {n}개`
  - `{nerrors} {pl(nerrors, 'error')}` → `오류 {nerrors}개`
- **조사:** `{name}` 같은 자리표시자 바로 뒤에는 조사를 붙이지 않습니다. 들어갈 값에 받침이 있는지 알 수 없기 때문입니다.
  - 나쁜 예: `'{name}'을 찾을 수 없습니다`
  - 좋은 예: `변수 '{name}'을(를) 찾을 수 없습니다`, `찾을 수 없는 변수: '{name}'`
- **HTML·자리표시자:** `<b>`, `<br/>`, `{}`, `{0}`, `%s`, `%(path)s`, `\n`은 그대로 둡니다. `{0}`처럼 번호나 이름이 있는 자리표시자는 순서를 바꿔도 됩니다. `%s`, `{}`처럼 번호가 없는 자리표시자가 두 개 이상이면 순서를 바꾸면 안 됩니다.

## 3. 번역 파일(jaml) 값 규칙

| 값 | 의미 | 사용 예 |
|---|---|---|
| `null` | 아직 번역하지 않음(실행하면 영어로 표시) | — |
| 번역문 | 한국어로 표시 | `Open: 열기` |
| `true` | 원문을 그대로 사용 | `PCA`, `SVM`, `,`, `-`, `%`, `N/A`, `hh:mm:ss`, `yyyy-MM-dd hh:mm:ss`, `Ctrl+Backspace`, `utf-8` |
| `false` | 번역하면 안 되는 문자열(식별자, 경로, 정규식) | 슬로베니아어 판정을 그대로 가져왔으므로 원칙적으로 고치지 않습니다. |
| `""` | 여러 줄로 나뉜 문자열의 뒷조각 | 첫 조각에 전체 번역을 넣고, 나머지 조각은 `""`로 둡니다. |

f-string 예시:

```yaml
'{label.title()} Automatically': 자동 {label}
```

`label`에는 "적용", "전송"처럼 이미 번역된 값이 들어갑니다.

## 4. 용어표

### 4.1 일반 화면

| 영어 | 한국어 | 비고 |
|---|---|---|
| widget | 위젯 | |
| workflow (scheme) | 워크플로 | |
| canvas | 캔버스 | |
| toolbox / tool dock | 도구 상자 / 도구 패널 | |
| link | 연결 | |
| channel / signal | 채널 / 신호 | |
| input / output | 입력 / 출력 | |
| add-on | 추가 기능 | |
| settings / preferences | 설정 / 환경 설정 | |
| report | 보고서 | |
| log | 로그 | |
| apply / Apply Automatically | 적용 / 자동 적용 | |
| send / Send Automatically | 전송 / 자동 전송 | |
| commit | 적용 | |
| reset / restore | 초기화 / 복원 | |
| freeze | 일시 정지 | 신호 전달을 멈추는 기능 |
| quick menu | 빠른 메뉴 | |
| annotation (text / arrow) | 주석 (텍스트 주석 / 화살표 주석) | |
| window group | 창 그룹 | |
| example workflows | 예제 워크플로 | |
| video tutorials | 동영상 강좌 | |
| documentation / FAQ | 문서 / 자주 묻는 질문 | |
| feedback / bug report / donate | 의견 보내기 / 버그 신고 / 후원하기 | |
| untitled | 제목 없음 | |
| filter / search | 필터 / 검색 | |
| selection / selected data | 선택 / 선택된 데이터 | 신호 이름 `Selected Data`도 포함 |
| annotated data | 선택 표시 데이터 ★ | 선택 여부를 열로 표시한 데이터 |
| zoom in / zoom out / reset zoom | 확대 / 축소 / 원래 크기 | |
| save image / copy to clipboard | 이미지 저장 / 클립보드에 복사 | |
| error / warning / information | 오류 / 경고 / 정보 | |
| OK / Cancel / Yes / No / Close | 확인 / 취소 / 예 / 아니요 / 닫기 | |

메뉴: `&File` 파일(&F) · `&Edit` 편집(&E) · `&View` 보기(&V) · `&Widget` 위젯(&W) · `Window`(캔버스) 창 · `&Window`(위젯 창) 창(&W) · `&Options` 옵션(&O) · `&Help` 도움말(&H)

### 4.2 데이터

| 영어 | 한국어 | 비고 |
|---|---|---|
| data / dataset | 데이터 / 데이터 세트 | |
| data table | 데이터 테이블 | |
| row / column | 행 / 열 | |
| instance / data instance | 행 / 데이터 행 | row와 같은 말로 옮깁니다. `sample`을 "표본"으로 옮기므로 "샘플"은 쓰지 않습니다. |
| variable | 변수 | |
| feature | 특성 | |
| attribute | 속성 | |
| meta attribute / metas | 메타 속성 / 메타 | |
| target / target variable | 타깃 / 타깃 변수 | |
| class / class variable / class value | 클래스 / 클래스 변수 / 클래스 값 | |
| target class | 타깃 클래스 | |
| label | 레이블 | |
| categorical / numeric | 범주형 / 수치형 | |
| discrete / continuous | 이산형 / 연속형 | |
| text / string | 텍스트 / 문자열 | |
| time / datetime | 시간 / 날짜·시간 | |
| value | 값 | |
| missing value | 결측치 | |
| domain | 도메인 | 변수 구성(데이터 구조) |
| subset / data subset | 부분집합 / 데이터 부분집합 | |
| sample / sampling | 표본 / 표본 추출 | |
| random / replicable | 무작위 / 재현 가능 | Replicable training → 재현 가능한 훈련 |
| weight | 가중치 | |
| index | 인덱스 | |
| sparse | 희소 | |
| duplicate / unique | 중복 / 고유 | |
| outlier | 이상치 | |
| distribution / frequency / density | 분포 / 빈도 / 밀도 | |
| mean / median / mode | 평균 / 중앙값 / 최빈값 | |
| minimum / maximum | 최솟값 / 최댓값 | |
| standard deviation / variance / dispersion | 표준편차 / 분산 / 산포 | |
| correlation | 상관관계 | 계수를 뜻하면 상관계수 |
| bin | 구간 | |

### 4.3 변환·전처리

| 영어 | 한국어 | 비고 |
|---|---|---|
| preprocess / preprocessor | 전처리 / 전처리기 | |
| transform / transformation | 변환 | |
| normalize / standardize | 정규화 / 표준화 | |
| impute | 결측치 대체 | |
| discretize | 이산화 | |
| continuize | 연속화 | |
| feature selection / rank / score | 특성 선택 / 순위 / 점수 | |
| purge | 정리 | |
| randomize / shuffle | 무작위 섞기 / 섞기 | |
| merge / concatenate / split | 병합 / 이어 붙이기 / 분할 | |
| aggregate / group by | 집계 / 그룹별 | |
| pivot table | 피벗 테이블 | |
| melt | 긴 형식 변환 ★ | 넓은 형식 → 긴 형식 |
| formula / expression | 수식 / 식 | |
| encode / one-hot encoding | 인코딩 / 원-핫 인코딩 | |

### 4.4 모델·학습

| 영어 | 한국어 | 비고 |
|---|---|---|
| model / learner | 모델 / 학습기 | |
| classifier / regressor | 분류기 / 회귀 모델 | |
| classification / regression | 분류 / 회귀 | |
| train / training data / test data | 훈련 / 훈련 데이터 / 테스트 데이터 | |
| fit | 훈련 | 곡선에서는 적합 |
| predict / prediction / probability | 예측 / 예측값 / 확률 | |
| parameter / hyperparameter | 매개변수 / 하이퍼파라미터 | |
| regularization | 규제 ★ | "정규화"로 옮기면 normalize와 혼동됩니다. |
| learning rate / iteration | 학습률 / 반복 | |
| loss / overfitting | 손실 / 과대적합 | |
| decision tree / tree | 결정 트리 / 트리 | |
| random forest | 랜덤 포레스트 | |
| gradient boosting | 그래디언트 부스팅 | |
| neural network / hidden layer / activation | 신경망 / 은닉층 / 활성화 함수 | |
| support vector machine | 서포트 벡터 머신 | 위젯 이름은 SVM |
| kernel | 커널 | |
| k-nearest neighbors / neighbor | k-최근접 이웃 / 이웃 | |
| naive Bayes | 나이브 베이즈 | |
| linear / logistic regression | 선형 회귀 / 로지스틱 회귀 | |
| ridge / lasso / elastic net | 릿지 / 라쏘 / 엘라스틱넷 | |
| stochastic gradient descent | 확률적 경사 하강법 | |
| ensemble / stacking | 앙상블 / 스태킹 | |
| calibration / threshold | 보정 / 임계값 | |
| rule / rule induction | 규칙 / 규칙 유도 | |
| scoring sheet | 점수표 | |

### 4.5 평가

| 영어 | 한국어 | 비고 |
|---|---|---|
| evaluate / evaluation results | 평가 / 평가 결과 | |
| cross-validation / fold | 교차 검증 / 폴드 | |
| leave-one-out | 하나씩 빼기 교차 검증 ★ | LOO |
| test on train data / test on test data | 훈련 데이터로 테스트 / 테스트 데이터로 테스트 | |
| accuracy / classification accuracy (CA) | 정확도 / 분류 정확도(CA) | |
| precision / recall / F1 | 정밀도 / 재현율 / F1 | |
| sensitivity / specificity | 민감도 / 특이도 | |
| true/false positive/negative | 참 양성 / 거짓 양성 / 참 음성 / 거짓 음성 | TP, FP, TN, FN |
| MSE / RMSE / MAE / R2 | 평균 제곱 오차 / 평균 제곱근 오차 / 평균 절대 오차 / 결정 계수 | 표 머리글은 약어 유지 |
| log loss | 로그 손실 | |
| confusion matrix | 혼동 행렬 | |
| ROC curve / AUC | ROC 곡선 / AUC | |
| lift curve / performance curve | 향상도 곡선 / 성능 곡선 | |
| calibration plot | 보정 그래프 | |
| permutation | 순열 | |

### 4.6 비지도 학습

| 영어 | 한국어 | 비고 |
|---|---|---|
| unsupervised learning | 비지도 학습 | |
| clustering / cluster | 클러스터링 / 클러스터 | |
| hierarchical clustering / linkage / dendrogram | 계층적 클러스터링 / 연결 방식 / 덴드로그램 | |
| k-means | k-평균 | |
| silhouette | 실루엣 | |
| distance / distance matrix / metric | 거리 / 거리 행렬 / 거리 척도 | |
| Euclidean / Manhattan / cosine | 유클리드 / 맨해튼 / 코사인 | |
| Jaccard / Pearson / Spearman / Hamming | 자카드 / 피어슨 / 스피어만 / 해밍 | |
| PCA / principal component / explained variance | 주성분 분석(PCA) / 주성분 / 설명된 분산 | |
| component | 성분 | |
| projection / dimensionality reduction | 투영 / 차원 축소 | |
| MDS | 다차원 척도법(MDS) | |
| manifold learning | 매니폴드 학습 | |
| self-organizing map | 자기 조직화 지도 | |
| correspondence analysis | 대응 분석 | |
| community (Louvain) | 커뮤니티 | |

### 4.7 시각화

| 영어 | 한국어 | 비고 |
|---|---|---|
| plot / graph / chart | 그래프 | "그림"은 위젯 이름에만 씁니다. |
| visualize / visualization | 시각화 | |
| axis / legend / grid | 축 / 범례 / 격자 | |
| color / size / shape / opacity | 색 / 크기 / 모양 / 불투명도 | |
| jitter | 지터 | |
| regression line / confidence interval | 회귀선 / 신뢰 구간 | |
| tooltip | 도구 설명 | |

## 5. 카테고리 이름

| 영어 | 한국어 |
|---|---|
| Data | 데이터 |
| Transform | 변환 |
| Visualize | 시각화 |
| Model | 모델 |
| Evaluate | 평가 |
| Unsupervised | 비지도 학습 |

## 6. 위젯 이름 대응표 (104개)

### 데이터 (Data)

| 영어 | 한국어 |
|---|---|
| File | 파일 |
| CSV File Import | CSV 파일 가져오기 |
| Datasets | 데이터 세트 |
| SQL Table | SQL 테이블 |
| Data Table | 데이터 테이블 |
| Paint Data | 데이터 그리기 |
| Data Info | 데이터 정보 |
| Rank | 특성 순위 |
| Edit Domain | 도메인 편집 |
| Color | 색상 |
| Column Statistics | 열 통계 |
| Save Data | 데이터 저장 |

### 변환 (Transform)

| 영어 | 한국어 |
|---|---|
| Data Sampler | 데이터 표본 추출 |
| Select Columns | 열 선택 |
| Select Rows | 행 선택 |
| Transpose | 행/열 바꾸기 ★ |
| Split | 분할 |
| Merge Data | 데이터 병합 |
| Concatenate | 데이터 이어 붙이기 |
| Select by Data Index | 인덱스로 선택 |
| Unique | 중복 제거 |
| Aggregate Columns | 열 집계 |
| Group by | 그룹별 집계 |
| Pivot Table | 피벗 테이블 |
| Apply Domain | 도메인 적용 |
| Preprocess | 전처리 |
| Impute | 결측치 대체 |
| Continuize | 연속화 |
| Discretize | 이산화 |
| Randomize | 무작위 섞기 |
| Purge Domain | 도메인 정리 |
| Melt | 긴 형식 변환 ★ |
| Formula | 수식 |
| Create Class | 클래스 만들기 |
| Create Instance | 행 만들기 |
| Python Script | 파이썬 스크립트 |

### 시각화 (Visualize)

| 영어 | 한국어 |
|---|---|
| Tree Viewer | 트리 뷰어 |
| Box Plot | 상자 그림 |
| Violin Plot | 바이올린 그림 |
| Distributions | 분포 |
| Scatter Plot | 산점도 |
| Line Plot | 꺾은선그래프 |
| Bar Plot | 막대그래프 |
| Sieve Diagram | 체 다이어그램 ★ |
| Mosaic Display | 모자이크 그림 |
| FreeViz | FreeViz |
| Linear Projection | 선형 투영 |
| Radviz | Radviz |
| Heat Map | 히트맵 |
| Venn Diagram | 벤 다이어그램 |
| Silhouette Plot | 실루엣 그림 |
| Pythagorean Tree | 피타고라스 트리 |
| Pythagorean Forest | 피타고라스 포레스트 |
| CN2 Rule Viewer | CN2 규칙 뷰어 |
| Nomogram | 노모그램 |
| Scoring Sheet Viewer | 점수표 뷰어 |

### 모델 (Model)

| 영어 | 한국어 |
|---|---|
| Constant | 상수 모델 |
| CN2 Rule Induction | CN2 규칙 유도 |
| Calibrated Learner | 보정된 학습기 |
| kNN | kNN |
| Tree | 결정 트리 |
| Random Forest | 랜덤 포레스트 |
| Gradient Boosting | 그래디언트 부스팅 |
| SVM | SVM |
| Linear Regression | 선형 회귀 |
| Logistic Regression | 로지스틱 회귀 |
| Naive Bayes | 나이브 베이즈 |
| Scoring Sheet | 점수표 |
| AdaBoost | AdaBoost |
| PLS | PLS |
| Curve Fit | 곡선 적합 |
| Neural Network | 신경망 |
| Stochastic Gradient Descent | 확률적 경사 하강법 |
| Stacking | 스태킹 |
| Save Model | 모델 저장 |
| Load Model | 모델 불러오기 |

### 평가 (Evaluate)

| 영어 | 한국어 |
|---|---|
| Test and Score | 테스트 및 평가 ★ |
| Predictions | 예측 |
| Feature as Predictor | 특성을 예측값으로 |
| Confusion Matrix | 혼동 행렬 |
| ROC Analysis | ROC 분석 |
| Performance Curve | 성능 곡선 |
| Calibration Plot | 보정 그래프 |
| Permutation Plot | 순열 그래프 |
| Parameter Fitter | 매개변수 탐색 |

### 비지도 학습 (Unsupervised)

| 영어 | 한국어 |
|---|---|
| Distance File | 거리 파일 |
| Distance Matrix | 거리 행렬 |
| t-SNE | t-SNE |
| Correlations | 상관관계 |
| Distance Map | 거리 맵 |
| Hierarchical Clustering | 계층적 클러스터링 |
| k-Means | k-평균 클러스터링 |
| Louvain Clustering | 루뱅 클러스터링 |
| DBSCAN | DBSCAN |
| Manifold Learning | 매니폴드 학습 |
| Outliers | 이상치 탐지 |
| PCA | PCA |
| Correspondence Analysis | 대응 분석 |
| Distance Transformation | 거리 변환 |
| Distances | 거리 계산 |
| MDS | MDS |
| Neighbors | 이웃 찾기 |
| Save Distance Matrix | 거리 행렬 저장 |
| Self-Organizing Map | 자기 조직화 지도 |

## 7. 확정이 필요한 용어(★) 모음

선택 표시 데이터 · 규제 · 하나씩 빼기 교차 검증 · 긴 형식 변환 · 행/열 바꾸기 · 체 다이어그램 · 테스트 및 평가
