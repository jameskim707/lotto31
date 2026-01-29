import streamlit as st
import random

# 1. 페이지 설정
st.set_page_config(page_title="제이미 로또 31 - 공식 엔진", layout="wide")

# 2. [디자인] 중앙 타이틀 및 날짜 배치
st.markdown("""
    <div style="text-align: center; border-bottom: 3px solid #ff4b4b; padding-bottom: 20px; margin-bottom: 30px;">
        <h1 style="margin: 0; color: #333; font-size: 3rem;">🎰 제이미 로또 31 분석 엔진</h1>
        <div style="background-color: #fff5f5; display: inline-block; padding: 10px 40px; border-radius: 50px; border: 1px solid #ff4b4b; margin-top: 15px;">
            <h2 style="margin: 0; color: #ff4b4b;">제 1209 회 추첨일</h2>
            <h3 style="margin: 5px 0; color: #333;">2026년 1월 31일 (토요일)</h3>
        </div>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

# --- [Step 1] 왼쪽: 자동 번호 입력 및 유니크 추출 ---
with col1:
    st.header("📥 Step 1. 자동 번호 통합 입력")
    st.caption("구매하신 자동 영수증의 게임별 번호를 입력하세요.")
    
    auto_defaults = {
        'A': "2, 8, 17, 27, 30, 35", 'B': "8, 20, 30, 31, 36, 38",
        'C': "24, 25, 33, 39, 41, 42", 'D': "4, 19, 20, 25, 28, 29",
        'E': "6, 22, 24, 25, 41, 43"
    }
    
    auto_all = []
    for label in ['A', 'B', 'C', 'D', 'E']:
        val = st.text_input(f"🎮 게임 {label}", value=auto_defaults.get(label, ""), key=f"auto_{label}")
        if val:
            auto_all.extend([int(n.strip()) for n in val.split(',') if n.strip().isdigit()])
    
    unique_auto = sorted(list(set(auto_all))) 
    
    if unique_auto:
        st.markdown(f"""
            <div style="background-color: #f0f7ff; padding: 15px; border-radius: 10px; border: 1px solid #4285f4; margin-top: 10px;">
                <strong style="color: #4285f4;">📋 자동 1장 유니크 번호 ({len(unique_auto)}개):</strong><br>
                <p style="font-size: 1.2rem; font-weight: bold; margin: 10px 0;">{", ".join(map(str, unique_auto))}</p>
            </div>
        """, unsafe_allow_html=True)

# --- [Step 2] 오른쪽: 사용자 전략 대입 및 조합 ---
with col2:
    st.header("🎯 Step 2. 전략 번호 대입")
    st.caption("자동 번호를 보면서 이번 주 7구와 10구를 대입하세요.")
    
    user_core = st.text_input("💎 핵심 7구 대입", value="5, 26, 27, 29, 30, 34, 45")
    user_support = st.text_input("🌿 소외 10구 대입", value="1, 2, 10, 12, 15, 16, 17, 20, 21, 44")
    
    core_list = [int(n.strip()) for n in user_core.split(',') if n.strip().isdigit()]
    support_list = [int(n.strip()) for n in user_support.split(',') if n.strip().isdigit()]
    
    # 10회귀 데이터 필터 (누락된 괄호 수정 완료)
    reg_data = {
        16, 24, 25, 30, 31, 32, 9, 19, 29, 35, 37, 38, 3, 18, 40, 44, 5, 12, 26, 39, 42, 
        27, 28, 8, 15, 21, 36, 10, 11, 17, 34, 1, 13, 20, 45, 33
    }

    st.divider()
    
    matched_c = [n for n in core_list if n in unique_auto and n in reg_data]
    matched_s = [n for n in support_list if n in unique_auto and n in reg_data]
    other_pool = [n for n in unique_auto if n in reg_data and n not in core_list and n not in support_list]

    if st.button("🚀 분석 및 황금 조합 생성", type="primary", use_container_width=True):
        if not matched_c and not matched_s:
            st.error("매칭된 번호가 부족합니다. 전략 번호를 확인해주세요.")
        else:
            final_combos = []
            for _ in range(5):
                try:
                    c_pick = random.sample(matched_c, min(3, len(matched_c)))
                    s_pick = random.sample(matched_s, min(2, len(matched_s)))
                    o_remain = 6 - (len(c_pick) + len(s_pick))
                    o_pick = random.sample(other_pool, min(o_remain, len(other_pool)))
                    
                    # 6개가 안 될 경우 추가 번호 보충
                    combo = sorted(c_pick + s_pick + o_pick)
                    while len(combo) < 6:
                        extra = random.choice([n for n in unique_auto if n not in combo])
                        combo.append(extra)
                        combo.sort()
                    final_combos.append(combo)
                except: continue
            
            st.session_state.final_results = final_combos

    if 'final_results' in st.session_state:
        st.subheader("✨ 추출된 황금 조합")
        for i, res in enumerate(st.session_state.final_results, 1):
            display = []
            for n in res:
                if n in core_list: display.append(f"**{n}**")
                elif n in support_list: display.append(f"*{n}*")
                else: display.append(str(n))
            st.markdown(f"**조합 {i:02d}:** {' , '.join(display)}", unsafe_allow_html=True)
