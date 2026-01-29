import streamlit as st
import random

# 1. 페이지 설정
st.set_page_config(page_title="제이미 로또 31 - 무제한 전략 모드", layout="wide")

st.markdown("""
    <div style="text-align: center; border-bottom: 5px solid #ff4b4b; padding-bottom: 20px; margin-bottom: 30px; background-color: #fff5f5; border-radius: 15px;">
        <h1 style="margin: 0; color: #ff4b4b; font-size: 2.5rem; font-weight: 900;">🎰 제이미 로또 31 (전략 확장형)</h1>
        <p style="color: #333; font-size: 1.2rem; font-weight: bold;">[ 번호 개수 제한 없음 - 고수 데이터 대량 유입 대응 ]</p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

# --- [Step 1] 왼쪽: 자동 5게임 (유지형) ---
with col1:
    st.markdown("### 📥 <span style='font-size: 1.4rem;'>Step 1. **자동 5게임** 입력</span>", unsafe_allow_html=True)
    auto_all = []
    for label in ['A', 'B', 'C', 'D', 'E']:
        val = st.text_input(f"**🎮 자동 게임 {label}**", placeholder="예: 1, 10, 23...", key=f"inf_auto_{label}")
        if val:
            auto_all.extend([int(n.strip()) for n in val.split(',') if n.strip().isdigit()])
    unique_auto = sorted(list(set(auto_all)))
    if unique_auto:
        st.success(f"📋 유니크 번호 추출: {unique_auto}")

# --- [Step 2] 오른쪽: 전략 무제한 대입 ---
with col2:
    st.markdown("### 🎯 <span style='font-size: 1.4rem;'>Step 2. **전략 번호** 대입 (개수 무관)</span>", unsafe_allow_html=True)
    
    # 이번 주는 테스트용 번호 기본 입력
    user_core = st.text_input("💎 **핵심 그룹 (고수 다수 추천수)**", value="5, 26, 27, 29, 30, 34, 45", key="inf_core")
    user_support = st.text_input("🌿 **보조 그룹 (나머지 추천수)**", value="1, 2, 10, 12, 15, 16, 17, 20, 21, 44", key="inf_support")
    
    core_list = [int(n.strip()) for n in user_core.split(',') if n.strip().isdigit()]
    support_list = [int(n.strip()) for n in user_support.split(',') if n.strip().isdigit()]
    
    # 10회귀 데이터 교차 검증 로직
    reg_data = {6, 27, 30, 36, 38, 42, 25, 16, 24, 32, 9, 19, 29, 35, 37, 3, 18, 40, 44, 5, 12, 26, 39, 15, 21, 10, 11, 17, 34, 1, 13, 20, 45, 33}
    
    matched_c = [n for n in core_list if n in unique_auto and n in reg_data]
    matched_s = [n for n in support_list if n in unique_auto and n in reg_data]

    if matched_c: st.markdown(f"#### ✅ 핵심 매칭 ({len(matched_c)}개): <span style='color:#ff4b4b;'>{matched_c}</span>", unsafe_allow_html=True)
    if matched_s: st.markdown(f"#### ✅ 보조 매칭 ({len(matched_s)}개): <span style='color:#007bff;'>{matched_s}</span>", unsafe_allow_html=True)

    # 조합 생성 버튼 및 로직 (들여쓰기 수정 완료)
    if st.button("🚀 무제한 데이터 기반 조합 생성", type="primary", use_container_width=True):
        if not unique_auto:
            st.error("먼저 Step 1에 자동 번호를 입력해주세요!")
        else:
            final_combos = []
            for _ in range(5):
                try:
                    # 핵심(3개) + 보조(2개) + 기타(1개) 비율 조합
                    c_pick = random.sample(matched_c, min(3, len(matched_c)))
                    s_pick = random.sample(matched_s, min(2, len(matched_s)))
                    needed = 6 - (len(c_pick) + len(s_pick))
                    
                    # 남은 숫자는 전체 자동 풀에서 보충
                    others = [n for n in unique_auto if n not in c_pick + s_pick]
                    o_pick = random.sample(others, min(needed, len(others)))
                    
                    res = sorted(list(set(c_pick + s_pick + o_pick)))
                    while len(res) < 6: # 부족할 경우 무작위 보충
                        extra = random.randint(1, 45)
                        if extra not in res: res.append(extra)
                    final_combos.append(sorted(res))
                except: continue
            
            st.subheader("✨ 추출된 황금 조합")
            for i, combo in enumerate(final_combos, 1):
                st.info(f"**조합 {i:02d}:** {combo}")

# --- 하단 설명란 ---
st.write("---")
st.markdown("## 📘 **설명란**")
with st.expander("제이미 로또 31 엔진 사용 설명서 (클릭)", expanded=False):
    st.markdown("""
### 🔹 1단계: 자동 데이터 확보
**입력 방법** : 새로 구매한 자동 영수증 **5게임의 번호를 입력**하세요.

### 🔹 2단계: 고수 데이터 대입
**핵심/보조 그룹** : 이번 주는 **테스트용**으로 미리 설정해두었습니다. 내일 고수들의 데이터를 받으면 이 칸에 더 많이 입력하셔도 무방합니다.

### 🔹 3단계: 매칭 및 조합 생성
**매칭 확인** : ✅ 표시는 내 자동 번호와 고수 추천수가 일치한다는 뜻입니다.
**조합 생성** : 버튼을 누르면 **최적의 비율**로 5개 조합을 완성합니다.
""")
