import streamlit as st
from collections import Counter
import random

# 페이지 설정
st.set_page_config(page_title="제이미 로또 31 - 3중 매칭", layout="wide")

# --- [비공개] 전략 번호 설정 ---
CORE_7 = [5, 26, 27, 29, 30, 34, 45]
SUPPORT_10 = [1, 2, 10, 12, 15, 16, 17, 20, 21, 44]

# 상단 대시보드
st.markdown("<h1 style='text-align: center;'>🎰 제이미 로또 31 3중 매칭 엔진</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

# --- 왼쪽: 10계단 회귀 데이터 (image_34c392.jpg 근거) ---
with col1:
    st.header("📥 10계단 회귀 데이터")
    default_vals = {
        1199: "16, 24, 25, 30, 31, 32", 1189: "9, 19, 29, 35, 37, 38", 
        1179: "3, 16, 18, 24, 40, 44", 1169: "5, 12, 24, 26, 39, 42",
        1159: "3, 9, 27, 28, 38, 39", 1149: "8, 15, 19, 21, 32, 36",
        1139: "5, 12, 15, 30, 37, 40", 1129: "5, 10, 11, 17, 28, 34",
        1119: "1, 9, 12, 13, 20, 45", 1109: "10, 12, 13, 19, 33, 40"
    }
    regression_pool = []
    for r in range(1199, 1100, -10):
        val = st.text_input(f"📍 {r}회", value=default_vals.get(r, ""), key=f"inp_{r}")
        if val:
            regression_pool.extend([int(n.strip()) for n in val.split(',') if n.strip().isdigit()])
    unique_regression = set(regression_pool)

# --- 오른쪽: 자동 23구 매칭 분석 ---
with col2:
    st.header("📝 자동 23구 전략 대입")
    # 사진(image_345297.jpg)에서 추출된 유니크 23구
    # 2, 4, 6, 8, 17, 19, 20, 22, 24, 25, 27, 28, 29, 30, 31, 33, 35, 36, 38, 39, 41, 42, 43
    auto_23 = [2, 4, 6, 8, 17, 19, 20, 22, 24, 25, 27, 28, 29, 30, 31, 33, 35, 36, 38, 39, 41, 42, 43]
    
    st.info(f"📋 자동 유니크 23구 대입 완료")
    
    # --- 핵심: 3중 매칭 로직 (자동 ∩ 전략 ∩ 회귀) ---
    # 1. 자동 번호에 있으면서 + 회귀 데이터에도 있고 + 핵심 7구인 번호
    final_core = [n for n in CORE_7 if n in auto_23 and n in unique_regression]
    # 2. 자동 번호에 있으면서 + 회귀 데이터에도 있고 + 소외 10구인 번호
    final_support = [n for n in SUPPORT_10 if n in auto_23 and n in unique_regression]
    # 3. 자동 번호 + 회귀 데이터에는 있지만 전략에는 없는 나머지
    final_others = [n for n in auto_23 if n in unique_regression and n not in CORE_7 and n not in SUPPORT_10]

    st.success(f"💎 최종 매칭 핵심 7구: {sorted(final_core)}")
    st.warning(f"🌿 최종 매칭 소외 10구: {sorted(final_support)}")

    if st.button("🚀 3중 매칭 기반 조합 생성", type="primary", use_container_width=True):
        results = []
        for _ in range(5):
            try:
                # 3:2:1 비율로 추출 시도 (번호 부족 시 유연하게 조정)
                c_pick = random.sample(final_core, min(3, len(final_core)))
                s_pick = random.sample(final_support, min(2, len(final_support)))
                o_pick = random.sample(final_others, 6 - (len(c_pick) + len(s_pick)))
                results.append(sorted(c_pick + s_pick + o_pick))
            except: continue
        st.session_state.triple_match = results

    if 'triple_match' in st.session_state:
        for i, res in enumerate(st.session_state.triple_match, 1):
            display = []
            for n in res:
                if n in CORE_7: display.append(f"**{n}**")
                elif n in SUPPORT_10: display.append(f"*{n}*")
                else: display.append(str(n))
            st.markdown(f"**조합 {i:02d}:** {' , '.join(display)}")
