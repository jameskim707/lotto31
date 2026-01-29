import streamlit as st
from collections import Counter
import random

st.set_page_config(page_title="제이미 로또 31 - 7구/10구 매칭", layout="wide")

# 1. [수정] 확정 전략 번호 (7구 / 10구)
core_7 = [5, 26, 27, 29, 30, 34, 45]
support_10 = [1, 2, 10, 12, 15, 16, 17, 20, 21, 44]

# 상단 디자인 (중앙 집중형)
st.markdown("<h1 style='text-align: center;'>🎰 제이미 로또 31 매칭 엔진</h1>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="text-align: center; border: 2px solid #ff4b4b; padding: 15px; border-radius: 15px; background-color: #f9f9f9; margin-bottom: 25px;">
        <h3 style="margin: 0; color: #333;">📅 1209회 추첨 예정일: <span style="color: #ff4b4b;">2026년 01월 31일</span></h3>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

# 왼쪽: 10회귀 입력 (제공해주신 데이터 기본값 세팅)
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
    
    unique_regression = set(regression_pool) # 10회귀 전체 출현 번호

# 오른쪽: 전략 매칭 및 조합 생성
with col2:
    st.header("🎯 전략 매칭 결과")
    
    # --- 핵심 로직: 10회귀 데이터와 전략 번호 매칭 ---
    matched_core = [n for n in core_7 if n in unique_regression]
    matched_support = [n for n in support_10 if n in unique_regression]
    # 10회귀에는 있지만 전략(7+10구)에는 없는 번호 (흐름수)
    matched_others = [n for n in unique_regression if n not in core_7 and n not in support_10]

    # 매칭 현황 대시보드
    st.success(f"💎 매칭 핵심 7구: {sorted(matched_core)} ({len(matched_core)}개)")
    st.info(f"🌿 매칭 소외 10구: {sorted(matched_support)} ({len(matched_support)}개)")
    st.warning(f"🌊 매칭 기타 흐름수: {len(matched_others)}개")
    
    num_combos = st.slider("생성할 조합 수", 1, 20, 5)
    
    if st.button("✨ 매칭 기반 황금 조합 생성", type="primary", use_container_width=True):
        final_results = []
        for _ in range(num_combos):
            try:
                # 3:2:1 황금 비율 추출 (매칭된 번호 내에서만!)
                c_pick = random.sample(matched_core, min(3, len(matched_core)))
                s_pick = random.sample(matched_support, min(2, len(matched_support)))
                # 부족한 칸은 매칭된 기타 번호에서 채움
                o_pick = random.sample(matched_others, 6 - (len(c_pick) + len(s_pick)))
                
                final_results.append(sorted(c_pick + s_pick + o_pick))
            except:
                continue
        st.session_state.matched_combos = final_results

    # 결과 표시
    if 'matched_combos' in st.session_state:
        for i, res in enumerate(st.session_state.matched_combos, 1):
            display = []
            for n in res:
                if n in core_7: display.append(f"**{n}**") # 7구 강조
                elif n in support_10: display.append(f"*{n}*") # 10구 이탤릭
                else: display.append(str(n))
            st.markdown(f"**조합 {i:02d}:** {' , '.join(display)}")
