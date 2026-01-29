import streamlit as st
import pandas as pd
from collections import Counter
import random
import requests # API 호출을 위해 추가

# 1. 로또 API 데이터 수집 함수 (추가)
def get_lotto_numbers(drw_no):
    url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drw_no}"
    try:
        res = requests.get(url).json()
        if res.get('returnValue') == 'success':
            return [res[f'drwtNo{i}'] for i in range(1, 7)]
    except:
        return None
    return None

# 페이지 설정
st.set_page_config(
    page_title="제이미 로또 31 분석 엔진",
    page_icon="🎰",
    layout="wide"
)

# 타이틀
st.title("🎰 제이미 로또 31 분석 엔진")
st.caption("31개 그물로 당첨 번호 6개 중 5~6개 포획")

# 사이드바 (설정)
with st.sidebar:
    st.header("⚙️ 설정")
    core_11 = [3, 5, 24, 26, 27, 29, 30, 31, 34, 45, 25] #
    support_16 = [1, 2, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 42, 44] #
    
    st.success(f"핵심 11구: {len(core_11)}개")
    st.info(f"소외 16구: {len(support_16)}개")

# 메인 영역
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📊 10회차 데이터 수집")
    
    # --- 핵심 수정 부분: 자동 입력 기능 ---
    target_drw = st.number_input("최신 회차 입력 (예: 1208)", min_value=1, value=1208)
    
    if st.button("🚀 데이터 자동 불러오기", type="primary"):
        with st.spinner('최근 10회차 데이터를 수집 중입니다...'):
            auto_rounds = []
            for i in range(10):
                nums = get_lotto_numbers(target_drw - i)
                if nums:
                    auto_rounds.append(nums)
            st.session_state.rounds_data = auto_rounds
            st.success(f"✅ {target_drw}회부터 10회분 수집 완료!")

    # 수집된 데이터 표시
    if 'rounds_data' in st.session_state:
        st.subheader("📋 수집된 당첨 번호")
        df = pd.DataFrame(st.session_state.rounds_data, columns=[f"n{i}" for i in range(1,7)])
        st.table(df)
        
        # 분석 실행
        all_numbers = [n for r in st.session_state.rounds_data for n in r]
        frequency = Counter(all_numbers)
        hot = [n for n, c in frequency.items() if c >= 3]
        solid = [n for n, c in frequency.items() if 1 <= c <= 2]
        cold = [n for n in range(1, 46) if n not in frequency]
        
        st.session_state.analysis = {'hot': hot, 'solid': solid, 'cold': cold, 'frequency': frequency}

# 오른쪽: 분석 결과 + 조합 생성 (사용자님 코드 로직 유지)
with col2:
    st.header("🎯 분석 결과")
    if 'analysis' in st.session_state:
        analysis = st.session_state.analysis
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("🔥 과열수", f"{len(analysis['hot'])}개")
            st.write(sorted(analysis['hot']))
        with col_b:
            st.metric("💎 실속수", f"{len(analysis['solid'])}개")
            st.write(sorted(analysis['solid']))
        with col_c:
            st.metric("❄️ 콜드수", f"{len(analysis['cold'])}개")
            if len(analysis['cold']) < 10: st.write("(제거 대상)") #

        st.divider()
        st.subheader("🎲 황금비율 조합 (3:2:1)")
        num_combos = st.slider("생성할 조합 수", 1, 10, 5)
        
        if st.button("✨ 조합 생성"):
            available = [n for n in range(1, 46) if n not in (analysis['cold'] if len(analysis['cold']) < 10 else [])] #
            # ... (이하 사용자님의 조합 생성 로직과 동일하게 작동)
            combinations = []
            for _ in range(num_combos):
                core_picks = random.sample([n for n in available if n in core_11], 3)
                support_picks = random.sample([n for n in available if n in support_16], 2)
                others = [n for n in available if n not in (core_picks + support_picks)]
                other_pick = random.sample(others, 1)
                combinations.append(sorted(core_picks + support_picks + other_pick))
            
            for i, combo in enumerate(combinations, 1):
                st.markdown(f"**{i}번:** {combo}") # 핵심/소외 강조 표시 가능
