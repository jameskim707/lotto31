import streamlit as st
from collections import Counter
import random

st.set_page_config(page_title="제이미 로또 31 - 매칭 엔진", layout="wide")

# 1. 확정 전략 번호
core_7 = [5, 26, 27, 29, 30, 34, 45]
support_12 = [1, 2, 10, 11, 12, 15, 16, 17, 18, 20, 21, 44]

# 상단 디자인
st.markdown("<h1 style='text-align: center;'>🎰 제이미 로또 31 매칭 엔진</h1>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="text-align: center; border: 2px solid #ff4b4b; padding: 15px; border-radius: 15px; background-color: #f9f9f9; margin-bottom: 25px;">
        <h3 style="margin: 0;">📅 1209회 추첨 예정일: <span style="color: #ff4b4b;">2026년 01월 31일</span></h3>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.header("📥 10계단 회귀 데이터")
    # 사용자 제공 10개 데이터
    default_vals = {
        1199: "16, 24, 25, 30, 31, 32", 1189: "9, 19, 29, 35, 37, 38", 
        1179: "3, 16, 18, 24, 40, 44", 1169: "5, 12, 24, 26, 39, 42",
        1159: "3, 9, 27, 28, 38, 39", 1149: "8, 15, 19, 21, 32, 36",
        1139: "5, 12, 15, 30, 37, 40", 1129: "5, 10, 11, 17, 28, 34",
        1119: "1, 9, 12, 13, 20, 45", 1109: "10, 12, 13, 19, 33, 40"
    }
    
    input_nums = []
    for r in range(1199, 1100, -10):
        val = st.text_input(f"📍 {r}회", value=default_vals.get(r, ""), key=f"inp_{r}")
        if val:
            input_nums.extend([int(n.strip()) for n in val.split(',') if n.strip().isdigit()])
    
    # 10회귀 전체 번호 중 중복 제거
    regression_pool = set(input_nums)

with col2:
    st.header("🎯 전략 매칭 결과")
    
    # --- 핵심 로직: 매칭 필터링 ---
    # 10회귀 데이터에 존재하면서 동시에 전략 번호에 있는 것만 추출
    matched_core = [n for n in core_7 if n in regression_pool]
    matched_support = [n for n in support_12 if n in regression_pool]
    # 나머지 흐름수 (10회귀 데이터 중 7구/12구에 없는 것)
    matched_others = [n for n in regression_pool if n not in core_7 and n not in support_12]

    # 매칭 현황 표시
    st.success(f"💎 매칭된 핵심 7구: {sorted(matched_core)}")
    st.info(f"🌿 매칭된 소외 12구: {sorted(matched_support)}")
    
    num_combos = st.slider("생성 조합 수", 1, 20, 5)
    
    if st.button("✨ 매칭 번호 기반 조합 생성", type="primary", use_container_width=True):
        final_combos = []
        for _ in range(num_combos):
            try:
                # 매칭된 번호가 부족할 경우를 대비한 안전 로직
                c_pick = random.sample(matched_core, min(3, len(matched_core)))
                s_pick = random.sample(matched_support, min(2, len(matched_support)))
                o_pick = random.sample(matched_others, 6 - (len(c_pick) + len(s_pick)))
                
                final_combos.append(sorted(c_pick + s_pick + o_pick))
            except:
                continue
        
        st.session_state.matched_results = final_combos

    if 'matched_results' in st.session_state:
        for i, res in enumerate(st.session_state.matched_results, 1):
            display = []
            for n in res:
                if n in core_7: display.append(f"**{n}**") # 핵심7구 볼드
                elif n in support_12: display.append(f"*{n}*") # 소외12구 이탤릭
                else: display.append(str(n))
            st.markdown(f"**조합 {i:02d}:** {' , '.join(display)}")
