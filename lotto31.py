import streamlit as st
import pandas as pd
from collections import Counter
import random
import requests
import time # 서버 부하 방지를 위해 추가

# 페이지 설정
st.set_page_config(page_title="제이미 로또 31 분석 엔진", page_icon="🎰", layout="wide")

# 1. 로또 API 수집 함수 (안정성 강화)
def get_lotto_data(drw_no):
    url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drw_no}"
    try:
        # User-Agent를 추가하여 브라우저인 척 속여서 차단을 방지합니다.
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=5).json()
        if res.get('returnValue') == 'success':
            return [res[f'drwtNo{i}'] for i in range(1, 7)]
    except Exception as e:
        return None
    return None

# 2. 전략 구간 설정 (사용자님 원본)
core_7 = [ 5, 26, 27, 29, 30,34, 45,]
support_12= [1, 2, 10, 11, 12,15, 16, 17, 18,20,21,44]

with st.sidebar:
    st.header("⚙️ 전략 설정")
    st.success(f"핵심 7구: {len(core_07)}개")
    st.info(f"소외 12구: {len(support_12)}개")

st.title("🎰 제이미 로또 31 - 계단식 분석기")
st.caption("1199회~1109회 구간 10회차 단위 자동 수집")

# 3. 계단식 분석 설정
col_in1, col_in2 = st.columns(2)
with col_in1:
    start_rd = st.number_input("시작 회차 (예: 1199)", value=1199, step=1)
with col_in2:
    num_steps = st.slider("분석할 계단 수 (10개 선택 시 1109회까지)", 1, 10, 5)

# 4. 분석 실행
if st.button("🚀 계단식 분석 및 조합 생성 시작", type="primary"):
    for i in range(num_steps):
        curr_start = start_rd - (i * 10)
        curr_end = curr_start - 9
        
        segment_nums = []
        progress_text = f"⏳ {curr_start}회 구간(10회차) 수집 중..."
        my_bar = st.progress(0, text=progress_text)
        
        for idx, r_no in enumerate(range(curr_start, curr_end - 1, -1)):
            nums = get_lotto_data(r_no)
            if nums:
                segment_nums.extend(nums)
            time.sleep(0.2) # 서버 차단 방지를 위한 짧은 휴식
            my_bar.progress((idx + 1) * 10)
        
        my_bar.empty() # 진행바 제거

        if len(segment_nums) < 30: # 최소 데이터 확인
            st.error(f"❌ {curr_start}회 구간 데이터를 가져오지 못했습니다. 잠시 후 다시 시도하세요.")
            continue

        # 빈도 분석 및 전략 적용
        freq = Counter(segment_nums)
        hot = [n for n, c in freq.items() if c >= 3]
        solid = [n for n, c in freq.items() if 1 <= c <= 2]
        cold = [n for n in range(1, 46) if n not in freq]

        # 결과 출력 UI
        with st.expander(f"📊 {curr_start}회 ~ {curr_end}회 분석 결과 (콜드수: {len(cold)}개)"):
            c1, c2, c3 = st.columns(3)
            with c1: st.write(f"🔥 과열수: {sorted(hot)}")
            with c2: st.write(f"💎 실속수: {sorted(solid)}")
            with c3: st.write(f"❄️ 콜드수: {sorted(cold)}")

            # 콜드수 10개 미만 시 제거 로직
            is_cold_low = len(cold) < 10
            available = [n for n in range(1, 46) if n not in (cold if is_cold_low else [])]
            
            # 추천 조합 (사용자님 3:2:1 로직)
            c_picks = random.sample([n for n in available if n in core_11], min(3, len([n for n in available if n in core_11])))
            s_picks = random.sample([n for n in available if n in support_16], min(2, len([n for n in available if n in support_16])))
            others = [n for n in available if n not in (c_picks + s_picks)]
            o_picks = random.sample(others, 1) if others else []
            
            st.info(f"✨ 추천 조합: {sorted(c_picks + s_picks + o_picks)}")
            if is_cold_low: st.warning("⚠️ 이 구간은 콜드수가 10개 미만입니다. 콜드수를 제외하고 조합했습니다.")



