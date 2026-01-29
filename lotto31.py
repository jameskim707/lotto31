import streamlit as st
import pandas as pd
from collections import Counter
import random
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="제이미 로또 31 분석 엔진",
    page_icon="🎰",
    layout="wide"
)

# --- 전략 번호 설정 (사용자 확정본) ---
core_7 = [5, 26, 27, 29, 30, 34, 45]
support_12 = [1, 2, 10, 11, 12, 15, 16, 17, 18, 20, 21, 44]

# 타이틀 및 중앙 날짜 표시
st.markdown("<h1 style='text-align: center;'>🎰 제이미 로또 31 분석 엔진</h1>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="text-align: center; border: 2px solid #ff4b4b; padding: 15px; border-radius: 15px; background-color: #f9f9f9; margin-bottom: 25px;">
        <h3 style="margin: 0; color: #333;">📅 이번 주 추첨일: <span style="color: #ff4b4b;">2026년 01월 31일</span></h3>
        <h1 style="margin: 5px 0;">제 1209 회</h1>
    </div>
""", unsafe_allow_html=True)

# 사이드바 (설정 정보)
with st.sidebar:
    st.header("⚙️ 전략 필터 상태")
    st.success(f"💎 핵심 7구 가동 중")
    st.info(f"🌿 소외 12구 가동 중")
    st.divider()
    st.caption("비공개 번호 전략이 시스템에 내장되었습니다.")

# 메인 영역
col1, col2 = st.columns([1, 1])

# 왼쪽: 10회차 계단식 데이터 입력
with col1:
    st.header("📊 계단식 데이터 입력")
    st.write("1199회부터 1109회까지 번호를 입력하세요.")
    
    rounds_data = []
    # 사용자님이 주신 데이터를 기본값으로 설정
    default_vals = {
        1199: "16, 24, 25, 30, 31, 32", 1189: "9, 19, 29, 35, 37, 38", 
        1179: "3, 16, 18, 24, 40, 44", 1169: "5, 12, 24, 26, 39, 42",
        1159: "3, 9, 27, 28, 38, 39", 1149: "8, 15, 19, 21, 32, 36",
        1139: "5, 12, 15, 30, 37, 40", 1129: "5, 10, 11, 17, 28, 34",
        1119: "1, 9, 12, 13, 20, 45", 1109: "10, 12, 13, 19, 33, 40"
    }
    
    for r_num in range(1199, 1100, -10):
        numbers = st.text_input(
            f"📍 {r_num} 회차", 
            value=default_vals.get(r_num, ""),
            key=f"round_{r_num}"
        )
        if numbers:
            nums = [int(n.strip()) for n in numbers.split(',') if n.strip().isdigit()]
            rounds_data.append(nums)
    
    if st.button("🔍 즉시 분석 시작", type="primary", use_container_width=True):
        if len(rounds_data) >= 1:
            all_numbers = [n for r in rounds_data for n in r]
            frequency = Counter(all_numbers)
            
            # 분류 로직
            hot = [n for n, c in frequency.items() if c >= 3]
            solid = [n for n, c in frequency.items() if 1 <= c <= 2]
            cold = [n for n in range(1, 46) if n not in all_numbers]
            
            st.session_state.analysis = {
                'hot': hot, 'solid': solid, 'cold': cold, 'freq': frequency
            }
            st.success("✅ 분석 데이터가 생성되었습니다!")

# 오른쪽: 분석 결과 + 조합 생성
with col2:
    st.header("🎯 분석 결과 리포트")
    
    if 'analysis' in st.session_state:
        res = st.session_state.analysis
        
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("🔥 과열수", f"{len(res['hot'])}개")
        col_b.metric("💎 실속수", f"{len(res['solid'])}개")
        col_c.metric("❄️ 콜드수", f"{len(res['cold'])}개")
        
        if len(res['cold']) < 10:
            st.warning("⚠️ 콜드수가 10개 미만입니다. 조합 시 콜드수가 제외됩니다.")
        
        st.divider()
        
        num_combos = st.slider("생성할 조합 수", 1, 20, 5)
        
        if st.button("✨ 황금비율 조합 생성", type="primary", use_container_width=True):
            # 전략 적용 필터
            is_cold_low = len(res['cold']) < 10
            available = [n for n in range(1, 46) if n not in (res['cold'] if is_cold_low else [])]
            
            combos = []
            for _ in range(num_combos):
                try:
                    c_picks = random.sample([n for n in available if n in core_7], 3)
                    s_picks = random.sample([n for n in available if n in support_12], 2)
                    others = [n for n in available if n not in c_picks + s_picks]
                    o_pick = random.sample(others, 1)
                    combos.append(sorted(c_picks + s_picks + o_pick))
                except:
                    continue
            st.session_state.combos = combos

        # 결과 출력
        if 'combos' in st.session_state:
            for i, c in enumerate(st.session_state.combos, 1):
                # 가독성 높은 번호 표시
                c_in = [n for n in c if n in core_7]
                s_in = [n for n in c if n in support_12]
                
                line = " ".join([f"**{n}**" if n in c_in else f"*{n}*" if n in s_in else str(n) for n in c])
                st.markdown(f"**조합 {i:02d}:** {line} (핵심{len(c_in)}/소외{len(s_in)})")
    else:
        st.info("👈 왼쪽에서 데이터를 확인하고 [분석 시작]을 눌러주세요.")
