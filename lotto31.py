import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from collections import Counter
import random
import requests
import time
import urllib3

# 보안 설정
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- [추가] 회차 자동 계산 로직 ---
def get_current_round():
    # 기준 날짜: 2026년 1월 31일 (1209회)
    base_date = datetime(2026, 1, 31)
    base_round = 1209
    
    today = datetime.now()
    # 기준일로부터 차이 계산 (주 단위)
    weeks_diff = (today - base_date).days // 7
    return base_round + weeks_diff

auto_round = get_current_round()

st.set_page_config(page_title="제이미 로또 31 - 자동 회차 모드", layout="wide")

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

# 전략 번호 (코드 내부 저장)
core_7 = [5, 26, 27, 29, 30, 34, 45]
support_12 = [1, 2, 10, 11, 12, 15, 16, 17, 18, 20, 21, 44]

# 사이드바 (깔끔하게 정리)
with st.sidebar:
    st.header("🎯 시스템 상태")
    st.success("💎 핵심 7구/12구 전략 가동 중")
    st.info(f"📅 오늘 기준 예상 회차: {auto_round}회")
    st.divider()
    st.caption("좌측 번호 노출을 차단했습니다.")

st.title("🎰 제이미 로또 31 - 자동 회차 분석기")
st.caption(f"현재 {auto_round}회차를 기준으로 10회씩 계단식 분석을 수행합니다.")

# 분석 설정 (자동 계산된 회차가 기본값으로 들어감)
col1, col2 = st.columns(2)
with col1:
    # value=auto_round를 통해 자동으로 1209회가 뜨게 설정함
    start_rd = st.number_input("분석 시작 회차", value=auto_round)
with col2:
    num_steps = st.slider("분석 구간(Step) 수", 1, 10, 10)

if st.button("🚀 자동 분석 및 조합 생성 시작", type="primary"):
    for i in range(num_steps):
        curr_start = start_rd - (i * 10)
        curr_end = curr_start - 9
        
        segment_nums = []
        status = st.empty()
        
        for r_no in range(curr_start, curr_end - 1, -1):
            status.text(f"⏳ {r_no}회 데이터 자동 수집 중...")
            nums = get_lotto_data(r_no)
            if nums:
                segment_nums.extend(nums)
                time.sleep(0.3)
        
        status.empty()

        if len(segment_nums) >= 30:
            freq = Counter(segment_nums)
            solid = [n for n, c in freq.items() if 1 <= c <= 2]
            cold = [n for n in range(1, 46) if n not in freq]

            with st.expander(f"📊 {curr_start}회 ~ {curr_end}회 구간 (콜드수: {len(cold)}개)"):
                st.write(f"✅ **실속수:** {sorted(solid)}")
                st.write(f"❄️ **콜드수:** {sorted(cold)}")
                
                is_cold_low = len(cold) < 10
                available = [n for n in range(1, 46) if n not in (cold if is_cold_low else [])]
                
                try:
                    c_picks = random.sample([n for n in available if n in core_7], 3)
                    s_picks = random.sample([n for n in available if n in support_12], 2)
                    others = [n for n in available if n not in c_picks + s_picks]
                    o_pick = random.sample(others, 1)
                    
                    st.success(f"✨ 추출 조합: {sorted(c_picks + s_picks + o_pick)}")
                except:
                    st.warning("⚠️ 조건 만족 번호 부족")
