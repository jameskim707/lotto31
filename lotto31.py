import streamlit as st
from collections import Counter
import random

# 페이지 설정
st.set_page_config(page_title="제이미 로또 31 - 2단계 매칭", layout="wide")

# 상단 디자인
st.markdown("<h1 style='text-align: center;'>🎰 제이미 로또 31 전략 대입 엔진</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

# --- [1단계] 자동 번호 입력 및 유니크 추출 ---
with col1:
    st.header("Step 1. 자동 번호 입력")
    st.caption("구매하신 자동 영수증의 A~E 게임을 입력하세요.")
    
    auto_inputs = []
    for label in ['A', 'B', 'C', 'D', 'E']:
        # 이전 대화의 데이터를 예시로 넣어두었습니다.
        default_auto = ""
        if label == 'A': default_auto = "2, 8, 17, 27, 30, 35"
        val = st.text_input(f"게임 {label}", value=default_auto, key=f"auto_step1_{label}")
        if val:
            auto_inputs.extend([int(n.strip()) for n in val.split(',') if n.strip().isdigit()])
    
    unique_auto = sorted(list(set(auto_inputs)))
    
    if unique_auto:
        st.success(f"✅ 자동 한 장 추출 번호 ({len(unique_auto)}개):")
        st.code(", ".join(map(str, unique_auto)))
        st.info("위의 번호들을 확인하고 오른쪽 Step 2의 전략에 대입하세요.")

# --- [2단계] 전략 번호 대입 및 최종 조합 생성 ---
with col2:
    st.header("Step 2. 전략 번호 대입")
    st.caption("자동에서 나온 번호 중 '핵심 7구'와 '소외 10구'로 쓸 번호를 직접 결정하세요.")
    
    # 사용자가 직접 입력하는 전략창
    user_core = st.text_input("💎 핵심 7구 대입 (예: 5, 26, 27, 29, 30, 34, 45)", value="5, 26, 27, 29, 30, 34, 45")
    user_support = st.text_input("🌿 소외 10구 대입 (예: 1, 2, 10, 12, 15, 16, 17, 20, 21, 44)", value="1, 2, 10, 12, 15, 16, 17, 20, 21, 44")
    
    core_list = [int(n.strip()) for n in user_core.split(',') if n.strip().isdigit()]
    support_list = [int(n.strip()) for n in user_support.split(',') if n.strip().isdigit()]
    
    # 10회귀 데이터 (고정 필터)
    regression_data = [16, 24, 25, 30, 31, 32, 9, 19, 29, 35, 37, 38, 3, 16, 18, 24, 40, 44, 5, 12, 24, 26, 39, 42, 3, 9, 27, 28, 38, 39, 8, 15, 19, 21, 32, 36, 5, 12, 15, 30, 37, 40, 5, 10, 11, 17, 28, 34, 1, 9, 12, 13, 20, 45, 10, 12, 13, 19, 33, 40]
    unique_reg = set(regression_data)

    st.divider()
    
    # 매칭 로직: (자동 추출 번호) AND (사용자 대입 전략) AND (10회귀 흐름)
    final_matched_core = [n for n in core_list if n in unique_auto and n in unique_reg]
    final_matched_support = [n for n in support_list if n in unique_auto and n in unique_reg]
    
    st.write(f"🎯 **매칭된 핵심수:** {final_matched_core}")
    st.write(f"🎯 **매칭된 소외수:** {final_matched_support}")

    if st.button("🚀 최종 황금 조합 생성", type="primary", use_container_width=True):
        if not final_matched_core or not final_matched_support:
            st.warning("자동 입력 번호와 전략 번호 간에 매칭되는 숫자가 부족합니다.")
        else:
            final_combos = []
            # 10회귀 데이터 중 전략에 포함되지 않은 기타 번호들
            other_pool = [n for n in unique_reg if n in unique_auto and n not in core_list and n not in support_list]
            
            for _ in range(5):
                try:
                    c_pick = random.sample(final_matched_core, min(3, len(final_matched_core)))
                    s_pick = random.sample(final_matched_support, min(2, len(final_matched_support)))
                    o_pick = random.sample(other_pool, 6 - (len(c_pick) + len(s_pick)))
                    final_combos.append(sorted(c_pick + s_pick + o_pick))
                except: continue
            
            for i, res in enumerate(final_combos, 1):
                display = []
                for n in res:
                    if n in core_list: display.append(f"**{n}**")
                    elif n in support_list: display.append(f"*{n}*")
                    else: display.append(str(n))
                st.markdown(f"**조합 {i:02d}:** {' , '.join(display)}", unsafe_allow_html=True)
