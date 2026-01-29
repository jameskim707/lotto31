import streamlit as st
from datetime import datetime
import pandas as pd
from collections import Counter
import random
import requests
import time
import urllib3

# 보안 설정
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- [정밀 계산] 이번 주 정보 자동 추출 ---
def get_this_week_info():
    # 기준: 1208회 (2026년 1월 24일 토요일)
    base_date = datetime(2026, 1, 24)
    base_round = 1208
    
    today = datetime.now()
    weeks_diff = (today - base_date).days // 7
    
    this_round = base_round + weeks_diff + 1
    this_date = base_date + timedelta(weeks=(weeks_diff + 1))
    return this_round, this_date.strftime("%Y년 %m월 %d일")

from datetime import timedelta
auto_round, target_date = get_this_week_info()

st.set_page_config(page_title="제이미 로또 31 - 분석 엔진", layout="wide")

# 로또 API 수집 함수
def get_lotto_data(drw_no):
    url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drw_no}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url, headers=headers, timeout=5, verify=False).json()
        if res.get('returnValue') == 'success':
            return [res[f'drwtNo{i}'] for i in range(1, 7)]
    except:
        return None
    return None

# 전략 번호 (내부 고정)
core_7 = [5, 26, 27, 29, 30, 34, 45]
support_12 = [1, 2, 10, 11, 12, 15, 16, 17, 18, 20, 21, 44]

# --- 상단 타이틀 및 중앙 날짜 표시 ---
st.markdown("<h1 style='text-align: center;'>🎰 제이미 로또 31 분석 엔진</h1>", unsafe_allow_html=True)

# 화면 중앙에 당첨 예정일과 회차를 크게 배치
st.markdown(f"""
    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border: 2px solid #ff4b4b; text-align: center; margin: 20px 0;">
        <h3 style="margin: 0; color: #31333F;">📅 이번 주 추첨일: <span style="color: #ff4b4b;">{target_date}</span></h3>
        <h2 style="margin: 10px 0; color: #31333F;">제 <span style="color: #ff4b4b;">{auto_round}</span> 회</h2>
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ 전략 가동 상태")
    st.success("💎 핵심 7구 필터링 ON")
    st.info("🌿 소외 12구 필터링 ON")
    st.divider()
    st.write(f"현재 분석 기준: {auto_round}회")

# 분석 설정 구간
col1, col2 = st.columns(2)
with col1:
    start_rd = st.number_input("분석 시작 회차 (자동 입력됨)", value=auto_round)
with col2:
    num_steps = st.slider("분석 구간(Step) 수", 1, 10, 10)

if st.button("🚀 계단식 분석 및 조합 생성 시작", type="primary", use_container_width=True):
    for i in range(num_steps):
        curr_start = (start_rd - 1) - (i * 10)
        curr_end = curr_start - 9
        
        segment_nums = []
        status = st.empty()
        
        for r_no in range(curr_start, curr_end - 1, -1):
            status.text(f"⏳ {r_no}회 수집 중...")
            nums = get_lotto_data(r_no)
            if nums:
                segment_nums.extend(nums)
                time.sleep(0.3)
        
        status.empty()

        if len(segment_nums) >= 30:
            freq = Counter(segment_nums)
            solid = [n for n, c in freq.items() if 1 <= c <= 2]
            cold = [n for n in range(1, 46) if n not in freq]

            with st.expander(f"📊 {curr_start}회 ~ {curr_end}회 분석 리포트"):
                c1, c2 = st.columns(2)
                with c1: st.write(f"✅ **실속수:** {sorted(solid)}")
                with c2: st.write(f"❄️ **콜드수:** {sorted(cold)} ({len(cold)}개)")
                
                is_cold_low = len(cold) < 10
                available = [n for n in range(1, 46) if n not in (cold if is_cold_low else [])]
                
                try:
                    c_picks = random.sample([n for n in available if n in core_7], 3)
                    s_picks = random.sample([n for n in available if n in support_12], 2)
                    others = [n for n in available if n not in c_picks + s_picks]
                    o_pick = random.sample(others, 1)
                    
                    st.success(f"✨ 추천 조합: {sorted(c_picks + s_picks + o_pick)}")
                    if is_cold_low: st.caption("💡 콜드수 10개 미만 전략으로 자동 필터링됨")
                except:
                    st.warning("⚠️ 해당 구간 분석 조건에 맞는 번호 부족")
