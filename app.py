import random
import numpy as np
import pandas as pd

class UnifiedPhilosophyLottoEngine:
    def __init__(self, historical_data):
        """
        historical_data: 역대 당첨 번호 리스트의 리스트 (예: [[3, 12, 24, 31, 35, 42], ...])
        """
        self.history = historical_data
        self.num_pool = list(range(1, 46))
        
        # 1. 오행 매핑 (1~45번을 목, 화, 토, 금, 수로 분류)
        self.element_map = {n: self._get_element(n) for n in self.num_pool}
        self.elements = ['木', '火', '土', '金', '水']
        
    def _get_element(self, num):
        # 낙서(洛書) 및 하도(河圖) 또는 오행 배정의 철학적 기준 적용
        rem = num % 5
        if rem == 1: return '木'
        elif rem == 2: return '火'
        elif rem == 3: return '土'
        elif rem == 4: return '金'
        else: return '水'

    def calculate_markov_state_weights(self):
        """1단계: 마르코프 체인 기반 국면 전이 확률 가중치 산출"""
        # 총합의 변화를 국면(State)으로 정의 (저/중/고)
        states = []
        for draw in self.history:
            total = sum(draw)
            if total < 115: states.append('Low')
            elif total <= 155: states.append('Mid')
            else: states.append('High')
            
        # 전이 확률 간략화 계산 (최근 상태에 따른 가중치 조정)
        recent_total = sum(self.history[-1]) if self.history else 135
        current_state = 'Low' if recent_total < 115 else ('Mid' if recent_total <= 155 else 'High')
        
        # '물극필반(物極必反)' 철학 적용: 한쪽으로 치우치면 반대편 국면의 확률을 높임
        state_weights = {'Low': 1.0, 'Mid': 1.0, 'High': 1.0}
        if current_state == 'Low':
            state_weights['High'] = 1.5  # 극에 달했으니 반대로 전이될 확률 가중
        elif current_state == 'High':
            state_weights['Low'] = 1.5
            
        return state_weights

    def calculate_element_weights(self):
        """2단계: 음양오행 상생상극 에너지 균형 가중치 산출"""
        element_counts = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
        
        # 최근 10회차의 오행 편중도 분석
        recent_draws = self.history[-10:] if len(self.history) >= 10 else self.history
        for draw in recent_draws:
            for num in draw:
                element_counts[self.element_map[num]] += 1
                
        # 중용의 원리: 가장 부족한(쇠한) 에너지를 보완하는 방향으로 가중치 부여
        total_count = sum(element_counts.values()) if sum(element_counts.values()) > 0 else 1
        element_weights = {}
        for el, count in element_counts.items():
            ratio = count / total_count
            # 부족할수록 가중치를 높임 (음양오행의 균형 회복)
            element_weights[el] = max(0.2, 1.0 - ratio + 0.5)
            
        return element_weights

    def generate_balanced_combination(self):
        """3단계: 중용 필터링 및 몬테카를로 시뮬레이션 조합 도출"""
        state_w = self.calculate_markov_state_weights()
        elem_w = self.calculate_element_weights()
        
        # 개별 번호에 철학적 가중치 결합
        number_weights = []
        for num in self.num_pool:
            el = self.element_map[num]
            base_w = elem_w[el]
            number_weights.append(base_w)
            
        # 확률 분포 정규화 (Probability Normalization)
        number_weights = np.array(number_weights)
        number_weights = number_weights / np.sum(number_weights)
        
        # 몬테카를로 시뮬레이션을 통한 최적 조합 탐색 (중용 기준: 합계 115~155, 홀짝 비율 3:3 또는 4:2)
        while True:
            candidate = sorted(np.random.choice(self.num_pool, size=6, replace=False, p=number_weights))
            total = sum(candidate)
            odds_count = sum(1 for n in candidate if n % 2 != 0)
            
            # 채근담의 '중용' 필터: 극단적 치우침 배제
            if 115 <= total <= 155 and 2 <= odds_count <= 4:
                return candidate

# --- 시뮬레이션 실행 예시 ---
if __name__ == "__main__":
    # 가상의 역대 데이터 (실제 데이터 연동 시 DataFrame 또는 CSV 파싱 활용)
    mock_history = [
        [5, 12, 23, 28, 34, 41],
        [2, 15, 22, 33, 39, 44],
        [8, 11, 19, 25, 37, 45],
        [3, 14, 21, 30, 38, 42]
    ]
    
    engine = UnifiedPhilosophyLottoEngine(mock_history)
    predicted_numbers = engine.generate_balanced_combination()
    
    print("=== [역·중용 확률 예측 엔진이 도출한 철학적 조합] ===")
    print(predicted_numbers)