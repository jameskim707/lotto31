import streamlit as st
from collections import Counter
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
    
    # 이전에 확인한 자동 번호를 기본값으로 유지
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
    
    unique_auto = sorted(list(set(auto_all))) # 중복 제거 로직
    
    if unique_auto:
        st.markdown(f"""
            <div style="background-color: #f0f7ff; padding: 15px; border-radius: 10px; border: 1px solid #4285f4; margin-top: 10px;">
                <strong style="color: #4285f4;">📋 자동 1장 유니크 번호 ({len(unique_auto)}개):</strong><br>
                <p style="font-size: 1.2rem; font-weight: bold; margin: 10px 0;">{", ".join(map(str, unique_auto))}</p>
                <small>중복이 제거된 깨끗한 번호 리스트입니다.</small>
            </div>
        """, unsafe_allow_html=True)

# --- [Step 2] 오른쪽: 사용자 전략 대입 및 조합 ---
with col2:
    st.header("🎯 Step 2. 전략 번호 대입")
    st.caption("자동 번호를 보면서 이번 주 7구와 10구를 대입하세요.")
    
    # 7구 10구 대입창 (화면에는 리스트 내용 노출 최소화)
    user_core = st.text_input("💎 핵심 7구 대입", value="5, 26, 27, 29, 30, 34, 45")
    user_support = st.text_input("🌿 소외 10구 대입", value="1, 2, 10, 12, 15, 16, 17, 20, 21, 44")
    
    core_list = [int(n.strip()) for n in user_core.split(',') if n.strip().isdigit()]
    support_list = [int(n.strip()) for n in user_support.split(',') if n.strip().isdigit()]
    
    # 10회귀 데이터 필터 (image_34c392.jpg 근거)
    reg_data = {16, 24, 25, 30, 31, 32, 9, 19, 29, 35, 37, 38, 3, 18, 40, 44, 5, 12, 26, 39, 42, 27, 28, 8, 15, 21, 36,
