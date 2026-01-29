# 제이미 로또 31 - 최종 통합 및 자동화 버전
import streamlit as st
import pandas as pd
from collections import Counter
import random
import requests

# 페이지 설정
st.set_page_config(page_title="제이미 로또 31 분석 엔진", page_icon="🎰", layout="wide")

# 로또 API 수집 함수
def get_lotto_data(drw_no):
    url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drw_no}"
    try:
        res = requests.get(url, timeout=5).json()
        if res.get('returnValue') == 'success':
            return [res[f'drwtNo{i}'] for i in range(1, 7)]
    except:
        return None
    return None

# 사이드바 전략 설정
with st.sidebar:
    st.header("⚙️ 전략 구간 설정")
    core_11 = [3, 5, 24, 26, 27, 29, 30, 31, 34, 45, 25] # 핵심 11구
    support_16 = [1, 2, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 42, 44] # 소외 16구
    st.success(f"핵심 11구: {len(core_11)}개")
    st.info(f"소외 16구: {len(support_16)}개")

st.title("🎰 제이미 로또 31 - 계단식 회귀 분석")
st.caption("1199회부터 1109회까지 10회차 단위 자동 추적")

# 분석 설정
col_input1, col_input2 = st.columns(2)
with col_input1:
    start_rd = st.number_input("분석 시작 회차", value=1199, step=1)
with col_input2:
    num_steps = st.slider("분석 구간(Step) 개수", 1, 10, 10) # 10개 선택 시 1109회까지 분석

if st.button("🚀 계단식 분석 시작", type="primary"):
    for i in range(num_steps):
        curr_start = start_rd - (i * 10)
        curr_end = curr_start - 9
        
        # 10회차 데이터 수집
        segment_nums = []
        with st.spinner(f'{curr_start}회 구간 수집 중...'):
            for r_no in range(curr_start, curr_end - 1, -1):
                nums = get_lotto_data(r_no)
                if nums: segment_nums.extend(nums)
        
        if not segment_nums:
            st.warning(f"{curr_start}회 구간 데이터가 없습니다.")
            continue
            
        # 빈도 분석
        freq = Counter(segment_nums)
        hot = [n for n, c in freq.items() if c >= 3]
        solid = [n for n, c in freq.items() if 1 <= c <= 2]
        cold = [n for n in range(1, 46) if n not in freq]
        
        # 결과 표시
        with st.expander(f"📊 {curr_start}회 ~ {curr_end}회 분석 (콜드수: {len(cold)}개)"):
            c1, c2, c3 = st.columns(3)
            c1.write(f"**🔥 과열수:** {sorted(hot)}")
            c2.write(f"**💎 실속수:** {sorted(solid)}")
            c3.write(f"**❄️ 콜드수:** {sorted(cold)}")
            
            # 콜드수 10개 미만 시 제거 로직 적용
            available = [n for n in range(1, 46) if n not in (cold if len(cold) < 10 else [])]
            
            # 조합 생성 (3:2:1 비율)
            try:
                c_avail = [n for n in available if n in core_11]
                s_avail = [n for n in available if n in support_16]
                o_avail = [n for n in available if n not in c_avail + s_avail]
                
                combo = sorted(random.sample(c_avail, 3) + random.sample(s_avail, 2) + random.sample(o_avail, 1))
                st.code(f"✨ 추천 조합: {combo}")
            except:
                st.write("⚠️ 선택 가능한 번호가 부족하여 조합을 생성할 수 없습니다.")
