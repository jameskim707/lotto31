
import streamlit as st
import random

# 1. 페이지 설정
st.set_page_config(page_title="제이미 로또 31 - 테스트 모드", layout="wide")

# 헤더 디자인
st.markdown("""
    <div style="text-align: center; border-bottom: 5px solid #ff4b4b; padding-bottom: 20px; margin-bottom: 30px; background-color: #fff5f5; border-radius: 15px;">
        <h1 style="margin: 0; color: #ff4b4b; font-size: 2.5rem; font-weight: 900;">🎰 제이미 로또 31 (테스트용)</h1>
        <p style="color: #333; font-size: 1.2rem; font-weight: bold;">[ 1209회 전략 검증 - 테스트 데이터 입력됨 ]</p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

# --- [Step 1] 왼쪽: 자동 5게임 입력 ---
with col1:
    st.markdown("### 📥 <span style='font-size: 1.4rem;'>Step 1. **자동 5게임** 입력</span>", unsafe_allow_html=True)
    st.write("---")
    
    auto_all = []
    labels = ['A', 'B', 'C', 'D', 'E']
    for label in labels:
        val = st.text_input(f"**🎮 자동 게임 {label}**", placeholder="번호 입력", key=f"test_auto_{label}")
        if val:
            auto_all.extend([int(n.strip()) for n in val.split(',') if n.strip().isdigit()])
    
    unique_auto = sorted(list(set(auto_all)))

# --- [Step 2] 오른쪽: 전략 대입 (테스트 번호 기본 입력) ---
with col2:
    st.markdown("### 🎯 <span style='font-size: 1.4rem;'>Step 2. **전략 번호** 대입 (테스트)</span>", unsafe_allow_html=True)
    st.write("---")
    
    # 요청하신 대로 우리가 만든 번호들을 미리 넣어두었습니다.
    user_core = st.text_input("💎 **핵심 전략 (7구)**", value="5, 26, 27, 29, 30, 34, 45", key="test_core")
    user_support = st.text_input("🌿 **소외 그룹 (10구)**", value="1, 2, 10, 12, 15, 16, 17, 20, 21, 44", key="test_support")
    
    core_list = [int(n.strip()) for n in user_core.split(',') if n.strip().isdigit()]
    support_list = [int(n.strip()) for n in user_support.split(',') if n.strip().isdigit()]
    
    # 10회귀 데이터 기반 매칭 로직
    reg_data = {6, 27, 30, 36, 38, 42, 25, 16, 24, 32, 9, 19, 29, 35, 37, 3, 18, 40, 44, 5, 12, 26, 39, 15, 21, 10, 11, 17, 34, 1, 13, 20, 45, 33}
    matched_c = [n for n in core_list if n in unique_auto and n in reg_data]
    matched_s = [n for n in support_list if n in unique_auto and n in reg_data]

    if matched_c: st.markdown(f"#### ✅ **매칭 핵심수**: <span style='color:#ff4b4b;'>{matched_c}</span>", unsafe_allow_html=True)
    if matched_s: st.markdown(f"#### ✅ **매칭 소외수**: <span style='color:#007bff;'>{matched_s}</span>", unsafe_allow_html=True)

    if st.button("🚀 테스트 조합 생성", type="primary", use_container_width=True):
        st.info("테스트용 조합이 생성되었습니다. (내일 고수 데이터 입력 시 초기화 권장)")



st.markdown("## 📘 설명란")

with st.expander("제이미 로또 31 엔진 사용 설명서", expanded=False):
    st.markdown("""
### 🔹 1단계: 자동 데이터 확보 (Step 1)
**입력 방법**  
새로 구매한 자동 영수증 **10게임의 번호를 A~J 칸에 입력**하세요.

**중요 포인트**  
- 숫자는 반드시 **쉼표(,)** 로 구분해야 엔진이 인식합니다.  
  (예: `2, 8, 17, 27, 30, 35`)

**분석 효과**  
- 입력 즉시 중복이 제거된 **유니크 번호**가 자동 추출됩니다.  
- 이 숫자들이 이후 모든 분석의 **기초 재료**가 됩니다.

---

### 🔹 2단계: 고수 데이터 대입 (Step 2)
**핵심 그룹 (7구 이상)**  
- 고수 추천 번호 중 **가장 많이 언급되거나 확신도가 높은 번호**를 입력하세요.

**보조 그룹 (10구 이상)**  
- 빈도는 낮지만 **보험용으로 가져갈 번호**를 입력합니다.

**유연성**  
- 번호 개수는 **7개, 10개에 고정되지 않습니다.**  
- 더 많이 입력해도 엔진이 자동으로 계산합니다.

---

### 🔹 3단계: 매칭 및 조합 생성
**매칭 확인**  
- ✅ 매칭 핵심수 = **[자동 번호] ∩ [고수 추천]**  
- 가장 강력한 우선 후보입니다.

**조합 생성**  
- 🔴 조합 생성 버튼을 누르면  
  **황금 비율 (핵심 3 : 보조 2 : 기타 1)** 로  
  최적의 **5개 조합**이 자동 완성됩니다.
""")



