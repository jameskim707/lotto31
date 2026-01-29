Python 3.14.2 (tags/v3.14.2:df79316, Dec  5 2025, 17:18:21) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
# 제이미 로또 31 - Streamlit 버전
import streamlit as st
import pandas as pd
from collections import Counter
import random

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
    
    # 핵심 11구
    core_11 = [3, 5, 24, 26, 27, 29, 30, 31, 34, 45, 25]
    
    # 소외 16구
    support_16 = [1, 2, 10, 11, 12, 13, 14, 15, 16, 
                  17, 18, 19, 20, 21, 42, 44]
    
    st.success(f"핵심 11구: {len(core_11)}개")
    st.info(f"소외 16구: {len(support_16)}개")
    st.warning(f"전체 그물: {len(core_11) + len(support_16)}개")

# 메인 영역
col1, col2 = st.columns([1, 1])

# 왼쪽: 데이터 입력 + 분석
with col1:
    st.header("📊 10회차 데이터 분석")
    
    # 데이터 입력
    st.subheader("10회차 당첨번호 입력")
    
    rounds_data = []
    for i in range(10):
        numbers = st.text_input(
            f"{i+1}회차", 
            placeholder="예: 1,4,16,23,31,41",
            key=f"round_{i}"
        )
        if numbers:
            nums = [int(n.strip()) for n in numbers.split(',')]
            rounds_data.append(nums)
    
    # 분석 버튼
    if st.button("🔍 분석 시작", type="primary"):
        if len(rounds_data) >= 5:
            # 빈도 계산
            all_numbers = [n for round in rounds_data for n in round]
            frequency = Counter(all_numbers)
            
            # 분류
            hot = [n for n, c in frequency.items() if c >= 3]
            solid = [n for n, c in frequency.items() if 1 <= c <= 2]
            cold = [n for n in range(1, 46) if n not in frequency]
            
            # 결과 저장
            st.session_state.analysis = {
                'hot': hot,
                'solid': solid,
                'cold': cold,
                'frequency': frequency
            }
            
            st.success("✅ 분석 완료!")
        else:
            st.error("최소 5회차 이상 입력해주세요!")

# 오른쪽: 분석 결과 + 조합 생성
with col2:
    st.header("🎯 분석 결과")
    
    if 'analysis' in st.session_state:
        analysis = st.session_state.analysis
        
        # 빈도 분석 결과
        st.subheader("📈 빈도 분석")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("🔥 과열수", f"{len(analysis['hot'])}개")
            if analysis['hot']:
                st.write(sorted(analysis['hot']))
        
        with col_b:
            st.metric("💎 실속수", f"{len(analysis['solid'])}개")
            if analysis['solid']:
                st.write(sorted(analysis['solid']))
        
        with col_c:
            st.metric("❄️ 콜드수", f"{len(analysis['cold'])}개")
            if len(analysis['cold']) < 10:
                st.write("(제거 대상)")
        
        st.divider()
        
        # 조합 생성
        st.subheader("🎲 황금비율 조합 (3:2:1)")
        
        num_combos = st.slider("생성할 조합 수", 1, 10, 5)
        
        if st.button("✨ 조합 생성", type="primary"):
            # 콜드수 제거
            if len(analysis['cold']) < 10:
                available = [n for n in range(1, 46) 
                           if n not in analysis['cold']]
            else:
                available = list(range(1, 46))
            
            # 조합 생성
            combinations = []
            for _ in range(num_combos):
                # 핵심 11구에서 3개
                core_available = [n for n in available if n in core_11]
                if len(core_available) >= 3:
                    core_picks = random.sample(core_available, 3)
                else:
                    core_picks = core_available
                
                # 소외 16구에서 2개
                support_available = [n for n in available if n in support_16]
                if len(support_available) >= 2:
                    support_picks = random.sample(support_available, 2)
                else:
                    support_picks = support_available
                
                # 나머지 1개
                others = [n for n in available 
                         if n not in core_picks + support_picks]
                if others:
                    other_pick = random.sample(others, 1)
                else:
                    other_pick = []
                
                combo = sorted(core_picks + support_picks + other_pick)
                
                # 6개 맞추기
                while len(combo) < 6:
                    extra = random.choice([n for n in available 
                                          if n not in combo])
                    combo.append(extra)
                    combo = sorted(combo)
                
                combinations.append(combo[:6])
            
            # 결과 저장
...             st.session_state.combinations = combinations
...         
...         # 조합 결과
...         if 'combinations' in st.session_state:
...             st.success(f"✅ {len(st.session_state.combinations)}개 조합 생성 완료!")
...             
...             for i, combo in enumerate(st.session_state.combinations, 1):
...                 # 번호 색상 구분
...                 core_in_combo = [n for n in combo if n in core_11]
...                 support_in_combo = [n for n in combo if n in support_16]
...                 
...                 combo_str = ", ".join([
...                     f"**{n}**" if n in core_in_combo else 
...                     f"*{n}*" if n in support_in_combo else str(n)
...                     for n in combo
...                 ])
...                 
...                 st.markdown(f"**{i}번:** {combo_str}")
...                 st.caption(f"핵심 {len(core_in_combo)}개 / 소외 {len(support_in_combo)}개")
...     else:
...         st.info("👈 왼쪽에서 10회차 데이터를 입력하고 분석을 시작하세요!")
... 
... # 하단: 설명
... st.divider()
... with st.expander("📖 사용 방법"):
...     st.markdown("""
...     ### 사용 순서
...     1. **왼쪽**: 최근 10회차 당첨번호 입력 (쉼표로 구분)
...     2. **분석 시작** 버튼 클릭
...     3. **오른쪽**: 빈도 분석 결과 확인
...     4. **조합 생성** 버튼 클릭
...     5. 생성된 조합 확인!
...     
...     ### 🎯 황금 비율 (3:2:1)
...     - **굵은 숫자**: 핵심 11구에서 선택 (3개)
...     - **기울임 숫자**: 소외 16구에서 선택 (2개)
...     - **일반 숫자**: 기타 흐름수 (1개)
