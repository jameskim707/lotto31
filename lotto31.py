import streamlit as st
from datetime import datetime, timedelta
from collections import Counter
import random

# 1. 사용자 제공 데이터 내장 (1199회 ~ 1109회)
# 이 데이터는 분석 로직에 즉시 반영됩니다.
STEP_DATA = {
    1199: [16, 24, 25, 30, 31, 32],
    1189: [9, 19, 29, 35, 37, 38],
    1179: [3, 16, 18, 24, 40, 44],
    1169: [5, 12, 24, 26, 39, 42],
    1159: [3, 9, 27, 28, 38, 39],
    1149: [8, 15, 19, 21, 32, 36],
    1139: [5, 12, 15, 30, 37, 40],
    1129: [5, 10, 11, 17, 28, 34],
    1119: [1, 9, 12, 13, 20, 45],
    1109: [10, 12, 13, 19, 33, 40]
}

# 2. 이번 주 회차 정보 자동 계산
def get_this_week():
    base_round = 1209
    base_date = datetime(2026, 1, 31)
    return base_round, base_date.strftime("%Y년 %m월 %d일")

auto_round, target_date = get_this_week()

# 3. 전략 번호 (7구 / 12구)
core_7 = [5, 26, 27, 29, 30, 34, 45]
support_12 = [1, 2, 10, 11, 12, 15, 16, 17, 18, 20, 21, 44]

st.set_page_config(page_title="제이미 로또 31 - 초고속 분석", layout="wide")

# --- 좌측 사이드바: 카피용 데이터 리스트 ---
with st.sidebar:
    st.header("📋 데이터 카피존")
    st.write("블로그 포스팅용 텍스트")
    copy_text = ""
    for r in sorted(STEP_DATA.keys(), reverse=True):
        copy_text += f"{r} 회\t" + "\t".join(map(str, STEP_DATA[r])) + "\n"
    st.text_area("Ctrl+C로 복사하세요", copy_text, height=400)
    st.divider()
    st.success("💎 핵심 7구/12구 전략 가동")

# --- 메인 상단: 이번 주 정보 (가운데 정렬) ---
st.markdown(f"""
    <div style="text-align: center; border: 2px solid #ff4b4b; padding: 20px; border-radius: 15px; background-color: #f9f9f9; margin-bottom: 30px;">
        <h2 style="margin: 0; color: #333;">📅 이번 주 당첨일: <span style="color: #ff4b4b;">{target_date}</span></h2>
        <h1 style="margin: 10px 0; font-size: 3.5rem;">제 {auto_round} 회</h1>
        <p style="color: #666; font-size: 1.1rem;">제이미 로또 31 - 계단식 회귀 분석 시스템</p>
    </div>
""", unsafe_allow_html=True)

# 분석 실행 버튼
if st.button("🚀 초고속 계단식 분석 실행", type="primary", use_container_width=True):
    # 제공된 10개 데이터를 기반으로 분석 수행
    all_numbers = [n for nums in STEP_DATA.values() for n in nums]
    freq = Counter(all_numbers)
    
    # 전체 요약 리포트
    st.subheader("📊 10개 계단 구간 통합 분석")
    col_a, col_b, col_c = st.columns(3)
    
    hot = [n for n, c in freq.items() if c >= 3]
    solid = [n for n, c in freq.items() if 1 <= c <= 2]
    cold = [n for n in range(1, 46) if n not in freq]
    
    col_a.metric("🔥 과열수", f"{len(hot)}개")
    col_b.metric("💎 실속수", f"{len(solid)}개")
    col_c.metric("❄️ 콜드수", f"{len(cold)}개")
    
    st.divider()

    # 각 계단별 세부 분석 및 조합
    for r in sorted(STEP_DATA.keys(), reverse=True):
        with st.expander(f"📍 {r}회차 기준 분석 및 추천 조합"):
            current_nums = STEP_DATA[r]
            st.write(f"✅ 당첨번호: **{current_nums}**")
            
            # 전략 적용 (콜드수 10개 미만 시 제거 등)
            # 여기서는 전체 10개 계단 통합 콜드수 기준으로 시뮬레이션
            available = [n for n in range(1, 46) if n not in (cold if len(cold) < 10 else [])]
            
            try:
                c_picks = random.sample([n for n in available if n in core_7], 3)
                s_picks = random.sample([n for n in available if n in support_12], 2)
                o_pick = random.sample([n for n in available if n not in c_picks+s_picks], 1)
                st.success(f"✨ 추천: {sorted(c_picks + s_picks + o_pick)}")
            except:
                st.warning("조합 조건 부족")
