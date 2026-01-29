import streamlit as st
import random

# 1. 페이지 설정
st.set_page_config(page_title="로또네오45 - 1209회 실전", layout="wide")

st.markdown("""
    <div style="text-align: center; border-bottom: 5px solid #ff4b4b; padding-bottom: 20px; margin-bottom: 30px; background-color: #fff5f5; border-radius: 15px;">
        <h1 style="margin: 0; color: #ff4b4b; font-size: 2.5rem; font-weight: 900;">🎰 로또네오45 베타버전 (1209회)</h1>
        <p style="color: #333; font-size: 1.2rem; font-weight: bold;">[ 실시간 자동 매칭 & 데이터 분석 시스템 ]</p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

# --- [Step 1] 왼쪽: 자동 5게임 입력 ---
with col1:
    st.markdown("### 📥 <span style='font-size: 1.4rem;'>Step 1. **자동 5게임** 입력</span>", unsafe_allow_html=True)
    auto_all = []
    labels = ['A', 'B', 'C', 'D', 'E']
    for label in labels:
        val = st.text_input(f"**🎮 자동 게임 {label}**", placeholder="예: 2, 8, 17...", key=f"final_v1_auto_{label}")
        if val:
            auto_all.extend([int(n.strip()) for n in val.split(',') if n.strip().isdigit()])
    unique_auto = sorted(list(set(auto_all)))
    if unique_auto:
        st.success(f"📋 추출된 유니크 번호: {unique_auto}")

# --- [Step 2] 오른쪽: 1209회 전략 번호 대입 (수정 완료) ---
with col2:
    # 사용자님의 요청대로 제목을 수정했습니다.
    st.markdown("### 🎯 <span style='font-size: 1.4rem;'>Step 2. **1209회 전략 번호 대입**</span>", unsafe_allow_html=True)
    
    user_core = st.text_input("💎 **핵심 그룹 (고수 다수 추천)**", value="5, 26, 27, 29, 30, 34, 45", key="final_v1_core")
    user_support = st.text_input("🌿 **보조 그룹 (보험용 추천)**", value="1, 2, 10, 12, 15, 16, 17, 20, 21, 44", key="final_v1_support")
    
    core_list = [int(n.strip()) for n in user_core.split(',') if n.strip().isdigit()]
    support_list = [int(n.strip()) for n in user_support.split(',') if n.strip().isdigit()]
    
    # 10회귀 흐름 데이터
    reg_data = {6, 27, 30, 36, 38, 42, 25, 16, 24, 32, 9, 19, 29, 35, 37, 3, 18, 40, 44, 5, 12, 26, 39, 15, 21, 10, 11, 17, 34, 1, 13, 20, 45, 33}
    
    matched_c = [n for n in core_list if n in unique_auto and n in reg_data]
    matched_s = [n for n in support_list if n in unique_auto and n in reg_data]

    if matched_c: st.markdown(f"#### ✅ 핵심 매칭: <span style='color:#ff4b4b;'>{matched_c}</span>", unsafe_allow_html=True)
    if matched_s: st.markdown(f"#### ✅ 보조 매칭: <span style='color:#007bff;'>{matched_s}</span>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 버튼 로직과 들여쓰기를 완벽하게 정리했습니다.
    if st.button("🚀 1209회 황금 조합 생성", type="primary", use_container_width=True):
        if not unique_auto:
            st.error("먼저 Step 1에 자동 번호를 입력해주세요!")
        else:
            final_combos = []
            for _ in range(5):
                try:
                    c_pick = random.sample(matched_c, min(3, len(matched_c)))
                    s_pick = random.sample(matched_s, min(2, len(matched_s)))
                    needed = 6 - (len(c_pick) + len(s_pick))
                    others = [n for n in unique_auto if n not in c_pick + s_pick]
                    o_pick = random.sample(others, min(needed, len(others)))
                    res = sorted(list(set(c_pick + s_pick + o_pick)))
                    while len(res) < 6:
                        extra = random.randint(1, 45)
                        if extra not in res: res.append(extra)
                    final_combos.append(sorted(res))
                except: continue
            
            st.subheader("✨ 생성된 1209회 조합")
            for i, combo in enumerate(final_combos, 1):
                st.info(f"**조합 {i:02d}:** {combo}")




st.markdown("## 📘 설명란")

with st.expander("로또네오45 엔진 사용 설명서", expanded=False):
    st.markdown("""
#### 🔹 1단계: 자동 데이터 확보
**입력 방법**  
새로 구매한 자동 영수증 **5게임의 번호를 A~J 칸에 입력**하세요.

**중요 포인트**  
- 숫자는 반드시 **쉼표(,)** 로 구분해야 엔진이 인식합니다.  
  (예: `2, 8, 17, 27, 30, 35`)

**분석 효과**  
- 입력 즉시 중복이 제거된 **유니크 번호**가 자동 추출됩니다.  
- 이 숫자들이 이후 모든 분석의 **기초 데이터**가 됩니다.

---

#### 🔹 2단계: 고수 데이터 대입
**핵심 그룹**  
- 고수 추천 번호 중 **확신도가 높거나 가장 많이 언급된 번호**를 입력하세요.

**보조 그룹**  
- 빈도는 낮지만 **보험용으로 가져갈 번호**들을 입력합니다.

**유연성**  
- 번호 개수는 고정되어 있지 않습니다.  
- 더 많이 입력해도 엔진이 자동으로 최적 계산을 수행합니다.

---

#### 🔹 3단계: 매칭 및 조합 생성
**매칭 확인**  
- ✅ 매칭 핵심수 = **[자동 번호] ∩ [고수 추천]**  
- 가장 우선적으로 사용되는 강력한 후보입니다.

**조합 생성 방식**  
- 🔴 조합 생성 버튼을 누르면  
  **황금 비율 (핵심 3 : 보조 2 : 기타 1)** 기준으로  
  **실전 선택에 집중할 수 있도록 5세트 조합만 생성**합니다.

**왜 5세트인가?**  
- 너무 많지 않아 **비교·선택이 쉽고**  
- 집중도가 높아 **실사용에 적합**하기 때문입니다.
""")







