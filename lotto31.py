import streamlit as st
import pandas as pd
from collections import Counter
import random
import requests
import time
import urllib3

# 보안 설정
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.set_page_config(page_title="제이미 로또 31 - 클린 모드", layout="wide")

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

# --- [전략 번호: 코드 내부에만 존재] ---
core_7 = [5, 26, 27, 29, 30, 34, 45]
support_12 = [1, 2, 10, 11, 12, 15, 16, 17, 18, 20, 21, 44]

# 사이드바: 번호 리스트 숨김 처리
with st.sidebar:
    st.header("⚙️ 전략 시스템")
    st.success("💎 핵심 7구 필터링 활성화")
    st.info("🌿 소외 12구 필터링 활성화")
    st.divider()
    st.caption("사용자님의 비공개 전략 번호가 시스템에 반영되어 있습니다.")

st.title("🎰 제이미 로또 31 - 계단식 분석 엔진 (Clean)")
st.caption("1199회부터 10회차 단위 자동 수집 및 흐름 분석")

# 분석 구간 설정
col1, col2 = st.columns(2)
with col1:
    start_rd = st.number_input("분석 시작 회차", value=1199)
with col2:
    num_steps = st.slider("분석할 계단(Step) 수", 1, 10, 10)

if st.button("🚀 계단식 분석 시작", type="primary"):
    for i in range(num_steps):
        curr_start = start_rd - (i * 10)
        curr_end = curr_start - 9
        
        segment_nums = []
        status_text = st.empty()
        
        for r_no in range(curr_start, curr_end - 1, -1):
            status_text.text(f"⏳ {r_no}회 데이터 가져오는 중...")
            nums = get_lotto_data(r_no)
            if nums:
                segment_nums.extend(nums)
                time.sleep(0.3)
        
        status_text.empty()

        if len(segment_nums) >= 30:
            freq = Counter(segment_nums)
            solid = [n for n, c in freq.items() if 1 <= c <= 2]
            cold = [n for n in range(1, 46) if n not in freq]

            # 결과 리포트
            with st.expander(f"📊 {curr_start}회 ~ {curr_end}회 구간 분석 (상세 보기)"):
                st.write(f"✅ **이 구간 실속수:** {sorted(solid)}")
                st.write(f"❄️ **이 구간 콜드수:** {sorted(cold)} ({len(cold)}개)")
                
                # 콜드수 10개 미만 체크 및 조합
                is_cold_low = len(cold) < 10
                available = [n for n in range(1, 46) if n not in (cold if is_cold_low else [])]
                
                try:
                    c_picks = random.sample([n for n in available if n in core_7], 3)
                    s_picks = random.sample([n for n in available if n in support_12], 2)
                    others = [n for n in available if n not in c_picks + s_picks]
                    o_pick = random.sample(others, 1)
                    
                    st.success(f"✨ 추천 조합: {sorted(c_picks + s_picks + o_pick)}")
                except:
                    st.warning("⚠️ 분석 조건에 맞는 번호 조합이 부족합니다.")
