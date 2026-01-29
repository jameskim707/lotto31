import streamlit as st
import pandas as pd
from collections import Counter
import random
import requests
import time
import urllib3

# 보안 설정 및 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.set_page_config(page_title="제이미 로또 31 - 7/12 전략", layout="wide")

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

# --- 사용자 확정 전략 번호 (7구 / 12구) ---
core_7 = [5, 26, 27, 29, 30, 34, 45]
support_12 = [1, 2, 10, 11, 12, 15, 16, 17, 18, 20, 21, 44]

with st.sidebar:
    st.header("⚙️ 확정 전략")
    st.success(f"💎 핵심 7구: {core_7}")
    st.info(f"🌿 소외 12구: {support_12}")
    st.divider()
    st.write("31개 그물망 전략 중 19개 핵심 선정 완료")

st.title("🎰 제이미 로또 31 - 계단식 분석 엔진")
st.caption("1199회부터 10회차 단위로 끊어서 흐름 분석")

# 분석 설정
col1, col2 = st.columns(2)
with col1:
    start_rd = st.number_input("분석 시작 회차", value=1199)
with col2:
    num_steps = st.slider("분석 구간 개수", 1, 10, 10)

if st.button("🚀 계단식 분석 및 조합 생성 시작", type="primary"):
    # 계단식 반복 (1199, 1189, 1179...)
    for i in range(num_steps):
        curr_start = start_rd - (i * 10)
        curr_end = curr_start - 9
        
        segment_nums = []
        status_text = st.empty()
        
        for r_no in range(curr_start, curr_end - 1, -1):
            status_text.text(f"⏳ {r_no}회 수집 중...")
            nums = get_lotto_data(r_no)
            if nums:
                segment_nums.extend(nums)
                time.sleep(0.3) # 차단 방지 딜레이
        
        status_text.empty()

        if len(segment_nums) >= 30:
            freq = Counter(segment_nums)
            solid = [n for n, c in freq.items() if 1 <= c <= 2]
            cold = [n for n in range(1, 46) if n not in freq]

            # 구간별 리포트
            with st.expander(f"📊 {curr_start}회 ~ {curr_end}회 리포트 (콜드수: {len(cold)}개)"):
                st.write(f"**💎 실속수:** {sorted(solid)}")
                st.write(f"**❄️ 콜드수:** {sorted(cold)}")
                
                # 사용자님 전략 적용: 콜드수 10개 미만 시 제거
                is_cold_low = len(cold) < 10
                available = [n for n in range(1, 46) if n not in (cold if is_cold_low else [])]
                
                # 조합 생성 (핵심 3개, 소외 2개, 나머지 1개)
                try:
                    c_avail = [n for n in available if n in core_7]
                    s_avail = [n for n in available if n in support_12]
                    
                    c_picks = random.sample(c_avail, 3)
                    s_picks = random.sample(s_avail, 2)
                    others = [n for n in available if n not in c_picks + s_picks]
                    o_pick = random.sample(others, 1)
                    
                    st.success(f"✨ 해당 구간 추천 조합: {sorted(c_picks + s_picks + o_pick)}")
                    if is_cold_low:
                        st.caption("⚠️ 이 구간은 콜드수를 제외하고 번호를 추출했습니다.")
                except:
                    st.warning("⚠️ 해당 구간 조건에 맞는 번호가 부족합니다.")
