import streamlit as st
import pandas as pd
from collections import Counter
import random

# 페이지 설정
st.set_page_config(page_title="제이미 로또 31 - 전략 강화", layout="wide")

# --- [확정] 핵심 7구 및 소외 12구 (이 번호 내에서만 추출) ---
core_7 = [5, 26, 27, 29, 30, 34, 45]
support_12 = [1, 2, 10, 11, 12, 15, 16, 17, 18, 20, 21, 44]

# 상단 레이아웃
st.markdown("<h1 style='text-align: center;'>🎰 제이미 로또 31 분석 엔진</h1>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="text-align: center; border: 2px solid #ff4b4b; padding: 15px; border-radius: 15px; background-color: #f9f9f9; margin-bottom: 25px;">
        <h3 style="margin: 0; color: #333;">📅 이번 주 추첨일: <span style="color: #ff4b4b;">2026년 01월 31일</span></h3>
        <h2 style="margin: 5px 0;">제 1209 회</h2>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.header("📊 계단식 데이터 입력")
    # 사용자님이 제공하신 10개 계단 데이터 기본값
    default_vals = {
        1199: "16, 24, 25, 30, 31, 32", 1189: "9, 19, 29, 35, 37, 38", 
        1179: "3, 16, 18, 24, 40, 44", 1169: "5, 12, 24, 26, 39, 42",
        1159: "3, 9, 27, 28, 38, 39", 1149: "8, 15, 19, 21, 32, 36",
        1139: "5, 12, 15, 30, 37, 40", 1129: "5, 10, 11, 17, 28, 34",
        1119: "1, 9, 12, 13, 20, 45", 1109: "10, 12, 13, 19, 33, 40"
    }
    
    rounds_data = []
    for r_num in range(1199, 1100, -10):
        numbers = st.text_input(f"📍 {r_num} 회차", value=default_vals.get(r_num, ""), key=f"r_{r_num}")
        if numbers:
            rounds_data.append([int(n.strip()) for n in numbers.split(',') if n.strip().isdigit()])
    
    if st.button("🔍 분석 및 필터 적용", type="primary", use_container_width=True):
        all_nums = [n for r in rounds_data for n in r]
        freq = Counter(all_nums)
        st.session_state.analysis = {
            'cold': [n for n in range(1, 46) if n not in all_nums],
            'freq': freq
        }

with col2:
    st.header("🎯 전략 조합 생성")
    if 'analysis' in st.session_state:
        cold_nums = st.session_state.analysis['cold']
        st.write(f"❄️ 현재 구간 콜드수: {len(cold_nums)}개")
        
        num_combos = st.slider("생성 조합 수", 1, 20, 5)
        
        if st.button("✨ 7구/12구 우선 조합 생성", type="primary", use_container_width=True):
            # 필터 로직: 콜드수가 10개 미만이면 제외수로 간주
            exclude_target = cold_nums if len(cold_nums) < 10 else []
            
            # 최종 후보군 (전체 45개 중 제외수 뺀 것)
            final_pool = [n for n in range(1, 46) if n not in exclude_target]
            
            # 전략 번호 내 가용 번호 재확인
            valid_core = [n for n in core_7 if n in final_pool]
            valid_support = [n for n in support_12 if n in final_pool]
            
            results = []
            for _ in range(num_combos):
                try:
                    # 1. 핵심 7구에서 무조건 3개 추출
                    picks = random.sample(valid_core, 3)
                    # 2. 소외 12구에서 무조건 2개 추출
                    picks += random.sample(valid_support, 2)
                    # 3. 나머지 1개는 7구/12구 제외한 후보군에서 추출
                    remaining_pool = [n for n in final_pool if n not in core_7 and n not in support_12]
                    picks += random.sample(remaining_pool, 1)
                    
                    results.append(sorted(picks))
                except ValueError:
                    continue
            st.session_state.final_combos = results

        if 'final_combos' in st.session_state:
            for i, res in enumerate(st.session_state.final_combos, 1):
                # 가이드: 굵게(7구), 기울임(12구)
                display = []
                for n in res:
                    if n in core_7: display.append(f"**{n}**")
                    elif n in support_12: display.append(f"*{n}*")
                    else: display.append(str(n))
                st.markdown(f"**조합 {i:02d}:** {' , '.join(display)}")
    else:
        st.info("👈 왼쪽에서 데이터를 먼저 분석해주세요.")
