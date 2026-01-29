
import streamlit as st
import random

# 1. 페이지 설정
st.set_page_config(page_title="제이미 로또 31 - 5게임 최적화", layout="wide")

# 헤더 디자인
st.markdown("""
    <div style="text-align: center; border-bottom: 5px solid #ff4b4b; padding-bottom: 20px; margin-bottom: 30px; background-color: #fff5f5; border-radius: 15px;">
        <h1 style="margin: 0; color: #ff4b4b; font-size: 2.5rem; font-weight: 900;">🎰 제이미 로또 31 분석기</h1>
        <p style="color: #333; font-size: 1.2rem; font-weight: bold;">[ 1209회 대비 - 자동 5게임 최적화 모드 ]</p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

# --- [Step 1] 왼쪽: 자동 5게임 입력 (A~E) ---
with col1:
    st.markdown("### 📥 <span style='font-size: 1.4rem;'>Step 1. **자동 5게임** 입력</span>", unsafe_allow_html=True)
    st.write("---")
    
    auto_all = []
    # 사용자님의 요청대로 딱 5개(A~E)만 배치했습니다.
    labels = ['A', 'B', 'C', 'D', 'E']
    
    for label in labels:
        # 입력 시 값이 유지되도록 key를 설정하고 빈칸으로 시작합니다.
        val = st.text_input(f"**🎮 자동 게임 {label}**", placeholder="예: 2, 8, 17, 27, 30, 35", key=f"fixed_5_auto_{label}")
        if val:
            auto_all.extend([int(n.strip()) for n in val.split(',') if n.strip().isdigit()])
    
    unique_auto = sorted(list(set(auto_all)))
    if unique_auto:
        st.success(f"**📋 추출 번호 ({len(unique_auto)}개):** {unique_auto}")

# --- [Step 2] 오른쪽: 전략 번호 대입 ---
with col2:
    st.markdown("### 🎯 <span style='font-size: 1.4rem;'>Step 2. **전략 번호** 대입</span>", unsafe_allow_html=True)
    st.write("---")
    
    user_core = st.text_input("💎 **핵심 전략 (7구+)**", placeholder="내일 고수 추천 상위 번호", key="fixed_core")
    user_support = st.text_input("🌿 **보조 소외 (10구+)**", placeholder="보험용 번호 입력", key="fixed_support")
    
    core_list = [int(n.strip()) for n in user_core.split(',') if n.strip().isdigit()]
    support_list = [int(n.strip()) for n in user_support.split(',') if n.strip().isdigit()]
    
    # 10회귀 흐름 데이터
    reg_data = {6, 27, 30, 36, 38, 42, 25, 16, 24, 32, 9, 19, 29, 35, 37, 3, 18, 40, 44, 5, 12, 26, 39, 15, 21, 10, 11, 17, 34, 1, 13, 20, 45, 33}
    
    matched_c = [n for n in core_list if n in unique_auto and n in reg_data]
    matched_s = [n for n in support_list if n in unique_auto and n in reg_data]
    other_pool = [n for n in unique_auto if n in reg_data if n not in core_list + support_list]

    if matched_c: st.markdown(f"#### ✅ **매칭 핵심수**: <span style='color:#ff4b4b; font-size:1.3rem;'>{matched_c}</span>", unsafe_allow_html=True)
    if matched_s: st.markdown(f"#### ✅ **매칭 소외수**: <span style='color:#007bff; font-size:1.3rem;'>{matched_s}</span>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 1209회 황금 조합 생성", type="primary", use_container_width=True):
        if unique_auto and (core_list or support_list):
            final_combos = []
            for _ in range(5):
                try:
                    c_pick = random.sample(matched_c, min(3, len(matched_c)))
                    s_pick = random.sample(matched_s, min(2, len(matched_s)))
                    o_req = 6 - (len(c_pick) + len(s_pick))
                    combined_pool = list(set(other_pool + unique_auto))
                    o_pick = random.sample([n for n in combined_pool if n not in c_pick + s_pick], min(o_req, len(combined_pool)))
                    res = sorted(c_pick + s_pick + o_pick)
                    if len(res) == 6: final_combos.append(res)
                except: continue
            
            if final_combos:
                st.markdown("### ✨ **최종 추천 조합**")
                for i, combo in enumerate(final_combos, 1):
                    st.info(f"**조합 {i:02d} :** {', '.join(map(str, combo))}")
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


