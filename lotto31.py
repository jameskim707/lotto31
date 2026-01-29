import streamlit as st
from datetime import datetime
from collections import Counter
import random

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="제이미 로또 31 - 입력형 분석", layout="wide")

# 2. 이번 주 정보 자동 계산
def get_this_week():
    base_round = 1209
    base_date = datetime(2026, 1, 31)
    return base_round, base_date.strftime("%Y년 %m월 %d일")

auto_round, target_date = get_this_week()

# 3. 전략 번호 설정
core_7 = [5, 26, 27, 29, 30, 34, 45]
support_12 = [1, 2, 10, 11, 12, 15, 16, 17, 18, 20, 21, 44]

# --- 좌측 사이드바: 10개 계단 입력란 ---
with st.sidebar:
    st.header("📥 계단 데이터 입력")
    st.caption("10회차 단위 번호를 입력하세요 (쉼표로 구분)")
    
    input_data = {}
    # 1199부터 1109까지 10씩 줄어들며 입력란 생성
    default_vals = [
        "16, 24, 25, 30, 31, 32", "9, 19, 29, 35, 37, 38", "3, 16, 18, 24, 40, 44",
        "5, 12, 24, 26, 39, 42", "3, 9, 27, 28, 38, 39", "8, 15, 19, 21, 32, 36",
        "5, 12, 15, 30, 37, 40", "5, 10, 11, 17, 28, 34", "1, 9, 12, 13, 20, 45",
        "10, 12, 13, 19, 33, 40"
    ]
    
    for i, r_num in enumerate(range(1199, 1100, -10)):
        val = st.text_input(f"{r_num}회 번호", value=default_vals[i])
        if val:
            input_data[r_num] = [int(n.strip()) for n in val.split(",") if n.strip().isdigit()]

    st.divider()
    st.success("💎 핵심 7구/12구 전략 가동")

# --- 메인 상단: 중앙 날짜 및 회차 표시 ---
st.markdown(f"""
    <div style="text-align: center; border: 2px solid #ff4b4b; padding: 20px; border-radius: 15px; background-color: #f9f9f9; margin-bottom: 30px;">
        <h2 style="margin: 0; color: #333;">📅 이번 주 당첨일: <span style="color: #ff4b4b;">{target_date}</span></h2>
        <h1 style="margin: 10px 0; font-size: 3.5rem;">제 {auto_round} 회</h1>
        <p style="color: #666; font-size: 1.1rem;">제이미 로또 31 - 사용자 입력형 계단식 분석</p>
    </div>
""", unsafe_allow_html=True)

# --- 분석 실행 ---
if st.button("🚀 입력 데이터 기반 분석 시작", type="primary", use_container_width=True):
    if input_data:
        # 모든 입력 번호 통합 분석
        all_numbers = [n for nums in input_data.values() for n in nums]
        freq = Counter(all_numbers)
        
        hot = [n for n, c in freq.items() if c >= 3]
        solid = [n for n, c in freq.items() if 1 <= c <= 2]
        cold = [n for n in range(1, 46) if n not in freq]

        st.subheader("📊 계단 구간 통합 요약")
        c1, c2, c3 = st.columns(3)
        c1.metric("🔥 과열수", f"{len(hot)}개")
        c2.metric("💎 실속수", f"{len(solid)}개")
        c3.metric("❄️ 콜드수", f"{len(cold)}개")
        
        st.divider()

        # 각 계단별 세부 결과
        for r_no in sorted(input_data.keys(), reverse=True):
            with st.expander(f"📍 {r_no}회차 기준 분석 및 추출"):
                st.write(f"✅ 입력번호: **{input_data[r_no]}**")
                
                # 콜드수 10개 미만 필터링 전략
                is_cold_low = len(cold) < 10
                available = [n for n in range(1, 46) if n not in (cold if is_cold_low else [])]
                
                try:
                    c_picks = random.sample([n for n in available if n in core_7], 3)
                    s_picks = random.sample([n for n in available if n in support_12], 2)
                    o_pick = random.sample([n for n in available if n not in c_picks+s_picks], 1)
                    st.success(f"✨ 추출 조합: {sorted(c_picks + s_picks + o_pick)}")
                    if is_cold_low: st.caption("💡 콜드수 10개 미만: 콜드수 완전 제외 모드 작동")
                except:
                    st.warning("⚠️ 선택 가능한 번호 부족")
