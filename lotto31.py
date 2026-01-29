import streamlit as st
from collections import Counter
import random

# 페이지 설정
st.set_page_config(page_title="제이미 로또 31 - 자동 분석 모드", layout="wide")

# --- [비공개] 전략 번호 (CORE_7 / SUPPORT_10) ---
CORE_7 = [5, 26, 27, 29, 30, 34, 45]
SUPPORT_10 = [1, 2, 10, 12, 15, 16, 17, 20, 21, 44]

# 상단 대시보드
st.markdown("<h1 style='text-align: center;'>🎰 제이미 로또 31 분석 엔진</h1>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="text-align: center; border: 2px solid #ff4b4b; padding: 15px; border-radius: 15px; background-color: #f9f9f9; margin-bottom: 25px;">
        <h3 style="margin: 0; color: #333;">📅 1209회 추첨 예정일: <span style="color: #ff4b4b;">2026년 01월 31일</span></h3>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

# --- 왼쪽: 10계단 회귀 데이터 입력 (사진 데이터 기준) ---
with col1:
    st.header("📥 10계단 회귀 데이터")
    # 업로드하신 첫 번째 이미지(image_34c392.jpg)의 데이터를 기본값으로 설정했습니다.
    default_vals = {
        1199: "16, 24, 25, 30, 31, 32", 1189: "9, 19, 29, 35, 37, 38", 
        1179: "3, 16, 18, 24, 40, 44", 1169: "5, 12, 24, 26, 39, 42",
        1159: "3, 9, 27, 28, 38, 39", 1149: "8, 15, 19, 21, 32, 36",
        1139: "5, 12, 15, 30, 37, 40", 1129: "5, 10, 11, 17, 28, 34",
        1119: "1, 9, 12, 13, 20, 45", 1109: "10, 12, 13, 19, 33, 40"
    }
    
    regression_pool = []
    for r in range(1199, 1100, -10):
        val = st.text_input(f"📍 {r}회", value=default_vals.get(r, ""), key=f"inp_{r}")
        if val:
            regression_pool.extend([int(n.strip()) for n in val.split(',') if n.strip().isdigit()])
    unique_regression = set(regression_pool)

# --- 오른쪽: 자동 번호 입력 (영수증 데이터 입력란) ---
with col2:
    st.header("📝 자동 번호 입력 (ABCDE)")
    st.caption("영수증(image_345297.jpg)의 자동 번호를 입력하세요.")
    
    # 사진 속 번호를 기본값으로 예시 입력했습니다.
    auto_defaults = {
        'A': "2, 8, 17, 27, 30, 35", 'B': "8, 20, 30, 31, 36, 38",
        'C': "24, 25, 33, 39, 41, 42", 'D': "4, 19, 20, 25, 28, 29",
        'E': "6, 22, 24, 25, 41, 43"
    }
    
    all_auto_nums = []
    for label in ['A', 'B', 'C', 'D', 'E']:
        auto_val = st.text_input(f"게임 {label}", value=auto_defaults[label], key=f"auto_{label}")
        if auto_val:
            nums = [int(n.strip()) for n in auto_val.split(',') if n.strip().isdigit()]
            all_auto_nums.extend(nums)

    # --- [핵심] 중복 제거 및 유니크 리스트 출력 ---
    if all_auto_nums:
        unique_auto = sorted(list(set(all_auto_nums)))
        st.markdown(f"""
            <div style="background-color: #f0f7ff; padding: 15px; border-radius: 10px; border: 1px solid #4285f4; margin-top: 15px;">
                <strong style="color: #4285f4;">📋 자동 한 장 통합 리스트 (중복 제거)</strong><br>
                <span style="font-size: 1.1rem; letter-spacing: 1px;">{", ".join(map(str, unique_auto))}</span><br>
                <small style="color: #666;">총 {len(unique_auto)}개의 고유 번호가 추출되었습니다.</small>
            </div>
        """, unsafe_allow_html=True)

    st.divider()
    
    # 7구/10구 전략 매칭 로직
    matched_core = [n for n in CORE_7 if n in unique_regression]
    matched_support = [n for n in SUPPORT_10 if n in unique_regression]
    matched_others = [n for n in unique_regression if n not in CORE_7 and n not in SUPPORT_10]

    if st.button("🚀 분석 및 전략 조합 생성", type="primary", use_container_width=True):
        final_results = []
        for _ in range(5):
            try:
                c_pick = random.sample(matched_core, min(3, len(matched_core)))
                s_pick = random.sample(matched_support, min(2, len(matched_support)))
                o_pick = random.sample(matched_others, 6 - (len(c_pick) + len(s_pick)))
                final_results.append(sorted(c_pick + s_pick + o_pick))
            except: continue
        st.session_state.final_combos = final_results

    # 결과 출력
    if 'final_combos' in st.session_state:
        for i, res in enumerate(st.session_state.final_combos, 1):
            display = []
            for n in res:
                # 자동 번호에 포함된 숫자는 형광펜 효과
                style = "background-color: #ffff00;" if n in all_auto_nums else ""
                if n in CORE_7: display.append(f"<span style='{style}'>**{n}**</span>")
                elif n in SUPPORT_10: display.append(f"<span style='{style}'>*{n}*</span>")
                else: display.append(f"<span style='{style}'>{n}</span>")
            st.markdown(f"**조합 {i:02d}:** {' , '.join(display)}", unsafe_allow_html=True)
