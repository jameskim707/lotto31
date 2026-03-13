import streamlit as st
import random

st.set_page_config(page_title="로또네오45", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@300;400;700&display=swap');
    .title-box {
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        border: 2px solid #e94560;
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        margin-bottom: 30px;
    }
</style>
<div class="title-box">
    <h1 style="color:#e94560; font-size:2.5rem; margin:0;">🎰 로또네오45</h1>
    <p style="color:#a0c4ff; margin:5px 0 0 0;">후나츠 분석 + Jamie Lotto 31 시스템</p>
</div>
""", unsafe_allow_html=True)

# ===== 사이드바: 마스터 번호 (한달 고정) =====
with st.sidebar:
    st.markdown("### 🔐 마스터 번호")
    st.caption("한달에 한번 업데이트")
    default_master = "1,4,5,6,7,9,11,17,18,19,20,21,22,23,25,26,29,32,34,35,36,38,39,40,41,42,43,45"
    master_input = st.text_area("💎 마스터 28개", value=default_master, height=120)
    master_list = sorted([int(n.strip()) for n in master_input.split(',') if n.strip().isdigit()])
    st.success(f"✅ 마스터 {len(master_list)}개")
    st.write(master_list)

master_set = set(master_list)

# ===== 탭 구조 =====
tab1, tab2, tab3 = st.tabs(["🔢 이웃수 계산기", "🎯 추천번호 매칭", "🚀 조합 생성기"])

# ==========================================
# TAB 1: 이웃수 계산기 (새로 추가)
# ==========================================
with tab1:
    st.markdown("### 🔢 이웃수 자동 계산기")
    st.caption("직전 회차 당첨번호 + 보너스 입력하면 이웃수 & 핵심/보조 자동 분류!")

    c1, c2 = st.columns([1, 1.5])
    with c1:
        win_input = st.text_input("🎯 당첨번호 6개", placeholder="예: 10, 15, 19, 27, 30, 33")
        bon_input = st.text_input("⭐ 보너스번호", placeholder="예: 14")

    win_nums = [int(n.strip()) for n in win_input.split(',') if n.strip().isdigit()]
    bon_nums = [int(bon_input.strip())] if bon_input.strip().isdigit() else []
    all_wins = win_nums + bon_nums

    if all_wins:
        nb_set = set()
        for n in all_wins:
            for d in [-3, -2, -1, 1, 2, 3]:
                nb = n + d
                if 1 <= nb <= 45:
                    nb_set.add(nb)
        nb_set -= set(all_wins)
        nb_list = sorted(nb_set)

        with c2:
            st.markdown(f"**📋 입력번호:** {all_wins}")
            st.markdown(f"**🔢 이웃수 총 {len(nb_list)}개:**")
            chips = " ".join([
                f'<span style="background:#2a2a4a;color:#fff;padding:5px 11px;border-radius:20px;margin:3px;display:inline-block;font-weight:bold;font-size:1rem;">{n}</span>'
                for n in nb_list
            ])
            st.markdown(chips, unsafe_allow_html=True)

        st.markdown("---")
        core_calc = sorted(master_set & nb_set)
        support_calc = sorted(master_set - nb_set)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**💎 핵심그룹 ({len(core_calc)}개)**")
            core_ch = " ".join([
                f'<span style="background:#e94560;color:white;padding:5px 13px;border-radius:20px;margin:3px;display:inline-block;font-weight:bold;font-size:1.05rem;">{n}</span>'
                for n in core_calc
            ])
            st.markdown(core_ch, unsafe_allow_html=True)

        with col_b:
            st.markdown(f"**🌿 보조그룹 ({len(support_calc)}개)**")
            sup_ch = " ".join([
                f'<span style="background:#0f3460;color:#a0c4ff;padding:5px 13px;border-radius:20px;margin:3px;border:1px solid #4a90d9;display:inline-block;font-size:1.05rem;">{n}</span>'
                for n in support_calc
            ])
            st.markdown(sup_ch, unsafe_allow_html=True)

    else:
        st.info("👈 당첨번호와 보너스번호를 입력하면 이웃수가 자동으로 계산됩니다!")


# ==========================================
# TAB 2: 추천번호 매칭
# ==========================================
with tab2:
    st.markdown("### 🎯 추천번호 매칭")
    st.caption("추천번호나 예상번호를 넣으면 마스터 28개와 매칭해드려요!")

    rec_input = st.text_area("📋 추천번호 입력 (쉼표로 구분)", placeholder="예: 3, 7, 12, 18, 24, 27, 33, 38, 41, 44", height=80)
    rec_nums = sorted([int(n.strip()) for n in rec_input.split(',') if n.strip().isdigit()])

    if rec_nums:
        rec_set = set(rec_nums)
        matched = sorted(master_set & rec_set)
        not_matched = sorted(rec_set - master_set)

        st.markdown(f"**📥 입력번호 {len(rec_nums)}개:** {rec_nums}")
        st.markdown("---")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**✅ 마스터 일치 ({len(matched)}개)**")
            if matched:
                chips = " ".join([
                    f'<span style="background:#e94560;color:white;padding:5px 13px;border-radius:20px;margin:3px;display:inline-block;font-weight:bold;font-size:1.1rem;">{n}</span>'
                    for n in matched
                ])
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.warning("일치하는 번호가 없어요")

        with col_b:
            st.markdown(f"**❌ 마스터 미포함 ({len(not_matched)}개)**")
            if not_matched:
                chips = " ".join([
                    f'<span style="background:#2a2a4a;color:#aaa;padding:5px 13px;border-radius:20px;margin:3px;display:inline-block;font-size:1.1rem;text-decoration:line-through;">{n}</span>'
                    for n in not_matched
                ])
                st.markdown(chips, unsafe_allow_html=True)
    else:
        st.info("👈 추천번호를 입력하면 마스터 28개와 매칭해드립니다!")

# ==========================================
# TAB 3: 기존 조합 생성기 (손 안 댐)
# ==========================================
with tab3:
    st.markdown("""
        <div style="text-align: center; border-bottom: 5px solid #ff4b4b; padding-bottom: 20px; margin-bottom: 30px; background-color: #fff5f5; border-radius: 15px;">
            <h1 style="margin: 0; color: #ff4b4b; font-size: 2.5rem; font-weight: 900;">🎰 로또네오45 베타버전</h1>
            <p style="color: #333; font-size: 1.2rem; font-weight: bold;">[ 실시간 자동 매칭 & 데이터 분석 시스템 ]</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📥 <span style='font-size: 1.4rem;'>Step 1. **자동 5게임** 입력</span>", unsafe_allow_html=True)
        auto_all = []
        labels = ['A', 'B', 'C', 'D', 'E']
        for label in labels:
            val = st.text_input(f"**🎮 자동 게임 {label}**", placeholder="예: 2, 8, 17...", key=f"final_v1_auto_{label}")
            if val:
                auto_all.extend([int(n.strip()) for n in val.split(',') if n.strip().isdigit()])
        unique_auto = sorted(list(set(auto_all)))
        if unique_auto:
            st.success(f"📋 추출된 유니크 번호: {unique_auto}")

    with col2:
        st.markdown("### 🎯 <span style='font-size: 1.4rem;'>Step 2. **이번 주 전략 번호 대입**</span>", unsafe_allow_html=True)

        user_core = st.text_input("💎 **핵심 그룹 (고수 다수 추천)**", value="5, 26, 27, 29, 30, 34, 45", key="final_v1_core")
        user_support = st.text_input("🌿 **보조 그룹 (보험용 추천)**", value="1, 2, 10, 12, 15, 16, 17, 20, 21, 44", key="final_v1_support")

        core_list = [int(n.strip()) for n in user_core.split(',') if n.strip().isdigit()]
        support_list = [int(n.strip()) for n in user_support.split(',') if n.strip().isdigit()]

        reg_data = {6, 27, 30, 36, 38, 42, 25, 16, 24, 32, 9, 19, 29, 35, 37, 3, 18, 40, 44, 5, 12, 26, 39, 15, 21, 10, 11, 17, 34, 1, 13, 20, 45, 33}

        matched_c = [n for n in core_list if n in unique_auto and n in reg_data]
        matched_s = [n for n in support_list if n in unique_auto and n in reg_data]

        if matched_c:
            st.markdown(f"#### ✅ 핵심 매칭: <span style='color:#ff4b4b;'>{matched_c}</span>", unsafe_allow_html=True)
        if matched_s:
            st.markdown(f"#### ✅ 보조 매칭: <span style='color:#007bff;'>{matched_s}</span>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀 황금 조합 생성", type="primary", use_container_width=True):
            if not unique_auto:
                st.error("먼저 Step 1에 자동 번호를 입력해주세요!")
            else:
                final_combos = []
                for _ in range(5):
                    try:
                        c_pick = random.sample(matched_c, min(3, len(matched_c)))
                        s_pick = random.sample(matched_s, min(2, len(matched_s)))
                        needed = 6 - (len(c_pick) + len(s_pick))
                        others = [n for n in unique_auto if n not in c_pick + s_pick]
                        o_pick = random.sample(others, min(needed, len(others)))
                        res = sorted(list(set(c_pick + s_pick + o_pick)))
                        while len(res) < 6:
                            extra = random.randint(1, 45)
                            if extra not in res: res.append(extra)
                        final_combos.append(sorted(res))
                    except:
                        continue

                st.subheader("✨ 생성된 조합")
                for i, combo in enumerate(final_combos, 1):
                    st.info(f"**조합 {i:02d}:** {combo}")

    st.markdown("## 📘 설명란")
    with st.expander("로또네오45 엔진 사용 설명서", expanded=False):
        st.markdown("""
#### 🔹 1단계: 자동 데이터 확보
5게임의 자동번호를 A~E 칸에 입력하세요. 숫자는 쉼표(,)로 구분.

#### 🔹 2단계: 고수 데이터 대입
핵심 그룹 / 보조 그룹 번호를 입력하세요.

#### 🔹 3단계: 매칭 및 조합 생성
황금 비율 (핵심 3 : 보조 2 : 기타 1) 기준으로 5세트 조합 생성.
        """)

st.markdown("---")
st.caption("💡 탭1: 이웃수 계산기 (매주 사용) | 탭2: 조합 생성기 | 마스터 28개: 한달 고정")

# 탭2 추천번호 매칭 삽입용 플래그
