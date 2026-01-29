import streamlit as st
import random

# 1. 페이지 설정
st.set_page_config(page_title="제이미 로또 31 - 공식 엔진", layout="wide")

# 2. [디자인] 1208회 당첨 결과 및 1209회 추첨일 안내
st.markdown("""
    <div style="text-align: center; border-bottom: 3px solid #ff4b4b; padding-bottom: 20px; margin-bottom: 30px;">
        <h1 style="margin: 0; color: #333; font-size: 3rem;">🎰 제이미 로또 31 분석 엔진</h1>
        <div style="margin-top: 15px;">
            <div style="display: inline-block; background-color: #f8f9fa; padding: 10px 20px; border-radius: 10px; border: 1px solid #dee2e6; margin-right: 10px;">
                <span style="color: #666; font-weight: bold;">최근 1208회 당첨번호:</span><br>
                <span style="font-size: 1.2rem; color: #007bff; font-weight: bold;">6, 27, 30, 36, 38, 42 + <span style="color: #ff4b4b;">25</span></span>
            </div>
            <div style="display: inline-block; background-color: #fff5f5; padding: 10px 20px; border-radius: 10px; border: 1px solid #ff4b4b;">
                <span style="color: #ff4b4b; font-weight: bold;">차주 1209회 추첨일:</span><br>
                <span style="font-size: 1.2rem; color: #333; font-weight: bold;">2026년 1월 31일 (토요일)</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

# --- [Step 1] 왼쪽: 자동 번호 통합 입력 ---
with col1:
    st.header("📥 Step 1. 자동 번호 통합 입력")
    st.caption("영수증의 A~E 게임을 입력하세요.")
    
    # 이미지 image_345297.jpg의 실제 번호를 기본값으로 세팅
    auto_receipt = {
        'A': "2, 8, 17, 27, 30, 35", 'B': "8, 20, 30, 31, 36, 38",
        'C': "24, 25, 33, 39, 41, 42", 'D': "4, 19, 20, 25, 28, 29",
        'E': "6, 22, 24, 25, 41, 43"
    }
    
    auto_all = []
    for label in ['A', 'B', 'C', 'D', 'E']:
        val = st.text_input(f"🎮 자동 게임 {label}", value=auto_receipt[label], key=f"auto_in_{label}")
        if val:
            auto_all.extend([int(n.strip()) for n in val.split(',') if n.strip().isdigit()])
    
    unique_auto = sorted(list(set(auto_all)))
    if unique_auto:
        st.success(f"📋 추출된 유니크 번호 ({len(unique_auto)}개): {unique_auto}")

# --- [Step 2] 오른쪽: 전략 대입 및 매칭 ---
with col2:
    st.header("🎯 Step 2. 전략 번호 대입")
    user_core = st.text_input("💎 핵심 7구 대입", value="5, 26, 27, 29, 30, 34, 45")
    user_support = st.text_input("🌿 소외 10구 대입", value="1, 2, 10, 12, 15, 16, 17, 20, 21, 44")
    
    core_list = [int(n.strip()) for n in user_core.split(',') if n.strip().isdigit()]
    support_list = [int(n.strip()) for n in user_support.split(',') if n.strip().isdigit()]
    
    # 최신 회귀 데이터셋
    reg_data = {6, 27, 30, 36, 38, 42, 25, 16, 24, 32, 9, 19, 29, 35, 37, 3, 18, 40, 44, 5, 12, 26, 39, 15, 21, 10, 11, 17, 34, 1, 13, 20, 45, 33}

    # 핵심 매칭 로직
    matched_c = [n for n in core_list if n in unique_auto and n in reg_data]
    matched_s = [n for n in support_list if n in unique_auto and n in reg_data]
    other_pool = [n for n in unique_auto if n in reg_data and n not in core_list and n not in support_list]

    st.write(f"✅ 매칭 핵심수: {matched_c}")
    st.write(f"✅ 매칭 소외수: {matched_s}")

    st.divider()

    if st.button("🚀 1209회 황금 조합 생성", type="primary", use_container_width=True):
        if not unique_auto:
            st.error("먼저 왼쪽 Step 1에 자동 번호를 입력해주세요.")
        elif not matched_c and not matched_s:
            st.warning("전략 번호와 매칭되는 번호가 없습니다. 수동으로 보충합니다.")
            # 번호 부족 시 전체 unique_auto에서 보충
            matched_c = matched_c if matched_c else random.sample(unique_auto, min(3, len(unique_auto)))
            
        final_combos = []
        for _ in range(5):
            try:
                # 3:2:1 황금 비율 추출 알고리즘
                c_pick = random.sample(matched_c, min(3, len(matched_c)))
                s_pick = random.sample(matched_s, min(2, len(matched_s)))
                o_req = 6 - (len(c_pick) + len(s_pick))
                o_pick = random.sample(other_pool, min(o_req, len(other_pool)))
                
                res = sorted(c_pick + s_pick + o_pick)
                # 6개가 부족할 경우 자동 번호에서 랜덤 보충
                while len(res) < 6:
                    add = random.choice([n for n in unique_auto if n not in res])
                    res.append(add)
                    res.sort()
                final_combos.append(res)
            except: continue
        
        st.session_state.results = final_combos

    # 결과 출력
    if 'results' in st.session_state:
        st.subheader("✨ 1209회 추천 조합 (핵심:굵게 / 소외:이탤릭)")
        for i, combo in enumerate(st.session_state.results, 1):
            disp = []
            for n in combo:
                if n in core_list: disp.append(f"**{n}**")
                elif n in support_list: disp.append(f"*{n}*")
                else: disp.append(str(n))
            st.markdown(f"**조합 {i:02d}:** {' , '.join(disp)}")



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
