import streamlit as st
import random

# 1. 페이지 설정
st.set_page_config(page_title="제이미 로또 31 - 공식 엔진", layout="wide")

# 2. [디자인] 1208회 당첨 결과 및 1209회 추첨일 안내
st.markdown("""
    <div style="text-align: center; border-bottom: 3px solid #ff4b4b; padding-bottom: 20px; margin-bottom: 30px;">
        <h1 style="margin: 0; color: #333; font-size: 3rem;">🎰 제이미 로또 31 분석 엔진</h1>
        <div style="margin-top: 15px;">
            <div style="display: inline-block; background-color: #f8f9fa; padding: 10px 20px; border-radius: 10px; border: 1px solid #dee2e6; margin-right: 10px;">
                <span style="color: #666; font-weight: bold;">최근 1208회 당첨번호:</span><br>
                <span style="font-size: 1.2rem; color: #007bff; font-weight: bold;">6, 27, 30, 36, 38, 42 + <span style="color: #ff4b4b;">25</span></span>
            </div>
            <div style="display: inline-block; background-color: #fff5f5; padding: 10px 20px; border-radius: 10px; border: 1px solid #ff4b4b;">
                <span style="color: #ff4b4b; font-weight: bold;">차주 1209회 추첨일:</span><br>
                <span style="font-size: 1.2rem; color: #333; font-weight: bold;">2026년 1월 31일 (토요일)</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

# --- [Step 1] 왼쪽: 자동 번호 통합 입력 ---
with col1:
    st.header("📥 Step 1. 자동 번호 통합 입력")
    # 사용자가 직접 입력할 수 있는 빈 칸 제공
    auto_all = []
    for label in ['A', 'B', 'C', 'D', 'E']:
        val = st.text_input(f"🎮 자동 게임 {label}", key=f"auto_input_{label}")
        if val:
            auto_all.extend([int(n.strip()) for n in val.split(',') if n.strip().isdigit()])
    
    unique_auto = sorted(list(set(auto_all)))
    if unique_auto:
        st.success(f"📋 추출된 유니크 번호 ({len(unique_auto)}개): {unique_auto}")

# --- [Step 2] 오른쪽: 전략 대입 및 매칭 ---
with col2:
    st.header("🎯 Step 2. 전략 번호 대입")
    user_core = st.text_input("💎 핵심 7구 대입", value="5, 26, 27, 29, 30, 34, 45")
    user_support = st.text_input("🌿 소외 10구 대입", value="1, 2, 10, 12, 15, 16, 17, 20, 21, 44")
    
    core_list = [int(n.strip()) for n in user_core.split(',') if n.strip().isdigit()]
    support_list = [int(n.strip()) for n in user_support.split(',') if n.strip().isdigit()]
    
    # [업데이트] 1208회 당첨 번호를 회귀 데이터셋에 추가
    reg_data = {
        6, 27, 30, 36, 38, 42, 25, # 1208회 최신 번호 반영
        16, 24, 32, 9, 19, 29, 35, 37, 3, 18, 40, 44, 5, 12, 26, 39, 15, 21, 10, 11, 17, 34, 1, 13, 20, 45, 33
    }

    if st.button("🚀 1209회 황금 조합 생성", type="primary", use_container_width=True):
        if not unique_auto:
            st.error("먼저 왼쪽 Step 1에 자동 번호를 입력해주세요.")
        else:
            # 매칭 및 조합 생성 로직 (생략 - 이전과 동일)
            st.info("매칭된 번호 기반으로 최적의 조합을 생성합니다.")
