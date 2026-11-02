import streamlit as st
import numpy as np
import pandas as pd

# 스트림릿 페이지 설정
st.set_page_config(page_title="역·중용 로또 예측 엔진", page_icon="🎲", layout="centered")

class UnifiedPhilosophyLottoEngine:
    def __init__(self, historical_data):
        self.history = historical_data
        self.num_pool = list(range(1, 46))
        self.element_map = {n: self._get_element(n) for n in self.num_pool}
        
    def _get_element(self, num):
        rem = num % 5
        if rem == 1: return '木'
        elif rem == 2: return '火'
        elif rem == 3: return '土'
        elif rem == 4: return '金'
        else: return '水'

    def calculate_element_weights(self):
        element_counts = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
        recent_draws = self.history[-10:] if len(self.history) >= 10 else self.history
        for draw in recent_draws:
            for num in draw:
                element_counts[self.element_map[num]] += 1
                
        total_count = sum(element_counts.values()) if sum(element_counts.values()) > 0 else 1
        element_weights = {}
        for el, count in element_counts.items():
            ratio = count / total_count
            element_weights[el] = max(0.2, 1.5 - ratio * 2)
            
        return element_weights, element_counts

    def generate_balanced_combination(self):
        elem_w, _ = self.calculate_element_weights()
        
        number_weights = []
        for num in self.num_pool:
            el = self.element_map[num]
            number_weights.append(elem_w[el])
            
        number_weights = np.array(number_weights)
        number_weights = number_weights / np.sum(number_weights)
        
        while True:
            candidate = sorted(np.random.choice(self.num_pool, size=6, replace=False, p=number_weights))
            total = sum(candidate)
            odds_count = sum(1 for n in candidate if n % 2 != 0)
            
            # 중용 필터 (합계 115~155, 홀짝 비율 2:4 ~ 4:2)
            if 115 <= total <= 155 and 2 <= odds_count <= 4:
                return candidate, total, odds_count

# --- 스트림릿 UI 구성 ---
st.title("🎲 역(易)·중용(中庸) 통합 로또 예측 엔진")
st.markdown("동양철학의 변화와 균형(중용 필터)을 융합한 확률 모델입니다.")

# 샘플 역사 데이터
history_data = [
    [5, 12, 23, 28, 34, 41],
    [2, 15, 22, 33, 39, 44],
    [8, 11, 19, 25, 37, 45],
    [3, 14, 21, 30, 38, 42],
    [7, 16, 24, 29, 35, 40]
]

engine = UnifiedPhilosophyLottoEngine(history_data)

if st.button("🔮 철학적 최적 번호 조합 추출하기", type="primary"):
    with st.spinner("우주의 에너지 흐름과 중용의 상태를 계산 중입니다..."):
        numbers, total_sum, odds_count = engine.generate_balanced_combination()
        
    st.success("조합 도출 완료!")
    
    cols = st.columns(6)
    for i, num in enumerate(numbers):
        cols[i].metric(label=f"번호 {i+1}", value=f"{num:02d}")
        
    st.info(f"📊 **통계적 검증 (`중용 필터` 통과)**\n- 번호 총합: **{total_sum}** (정규분포 중심 구간: 115~155)\n- 홀수 개수: **{odds_count}개** / 짝수 개수: **{6-odds_count}개**")
