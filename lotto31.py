import streamlit as st
import pandas as pd
from collections import Counter
import random
import requests # 자동 수집을 위해 추가

# 1. 로또 API 수집 함수
def get_lotto_data(drw_no):
    url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drw_no}"
    try:
        res = requests.get(url).json()
        return [res[f'drwtNo{i}'] for i in range(1, 7)] if res.get('returnValue') == 'success' else None
    except:
        return None

# 페이지 설정
st.set_page_config(page_title="제이미 로또 31 분석 엔진", page_icon="🎰", layout="wide")

# 사이드바 설정 (사용자님 원본 유지)
with st.sidebar:
    st.header("⚙️ 전략 구간 설정")
    core_11 = [3, 5, 24, 26, 27, 29, 30, 31, 34, 45, 25]
    support_16 = [1, 2, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 42, 44]
    st.success(f"핵심 11구: {len(core_11)}개")
    st.info(f"소외 16구: {len(support_16)}개")

st.title("🎰 제이미 로또 31 - 계단식 회귀 분석")
st.caption("10회차 단위로 끊어서 내려가는 정밀 흐름 추적")

# 분석 설정 영역
col_set1, col_set2 = st.columns(2)
with col_set1:
    start_rd = st.number_input("시작 회차 입력", value=1199)
with col_set2:
    num_steps = st.slider("분석할 계단(Step) 수", 1, 10, 5)

if st.button("🚀 계단식 분석 및 조합 생성 시작", type="primary"):
    all_summary = []
    
    # 1199 -> 1189 -> 1179 순으로 반복 분석
    for i in range(num_steps):
        curr_start = start_rd - (i * 10)
        curr_end = curr_start - 9
        
        # 구간 데이터 수집
        segment_nums = []
        for r_no in range(curr_start, curr_end - 1, -1):
            nums = get_lotto_data(r_no)
            if nums: segment_nums.extend(nums)
        
        if not segment_nums: continue
        
        # 빈도 분석 및 분류
        freq = Counter(segment_nums)
        hot = [n for n, c in freq.items() if c >= 3]
        solid = [n for n, c in freq.items() if 1 <= c <= 2]
        cold = [n for n in range(1, 46) if n not in freq]
        
        # UI 출력 (Expandable로 깔끔하게)
        with st.expander(f"📊 구간: {curr_start}회 ~ {curr_end}회 (콜드수: {len(cold)}개)"):
            c1, c2, c3 = st.columns(3)
            c1.write(f"**🔥 과열수:** {sorted(hot)}")
            c2.write(f"**💎 실속수:** {sorted(solid)}")
            c3.write(f"**❄️ 콜드수:** {sorted(cold)}")
            
            # 콜드수 10개 미만 시 제거 로직 적용 조합 생성
            available = [n for n in range(1, 46) if n not in (cold if len(cold) < 10 else [])]
            
            # 샘플 조합 1개 생성 (사용자님 3:2:1 비율 적용)
            c_picks = random.sample([n for n in available if n in core_11], 3)
            s_picks = random.sample([n for n in available if n in support_16], 2)
            o_picks = random.sample([n for n in available if n not in (c_picks + s_picks)], 1)
            final_combo = sorted(c_picks + s_picks + o_picks)
            st.code(f"✨ 해당 구간 분석 기반 추천: {final_combo}")

st.divider()
st.info("💡 10회차씩 내려가며 콜드수의 개수가 어떻게 변하는지 확인하세요. 10개 미만인 구간이 '기회'입니다!")
