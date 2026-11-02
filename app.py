import streamlit as st
import numpy as np
import pandas as pd

# 스트림릿 페이지 설정
st.set_page_config(page_title="역·중용 로또 예측 엔진", page_icon="🎲", layout="centered")

class UnifiedPhilosophyLottoEngine:
    def __init__(self, historical_data):
        """
        historical_data: 회차별 6개 번호의 리스트 (예: [[1, 2, 3, 4, 5, 6], ...])
        """
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

    def calculate_markov_state_weights(self):
        """1단계: 마르코프 체인 및 물극필반(物極必反) 국면 전이 가중치 산출"""
        if not self.history:
            return {'Low': 1.0, 'Mid': 1.0, 'High': 1.0}

        recent_total = sum(self.history[-1])
        current_state = 'Low' if recent_total < 115 else ('Mid' if recent_total <= 155 else 'High')
        
        # 음양이 극에 달하면 반대 국면으로 전이하는 성질 반영
        state_weights = {'Low': 1.0, 'Mid': 1.0, 'High': 1.0}
        if current_state == 'Low':
            state_weights['High'] = 1.4
            state_weights['Mid'] = 1.2
        elif current_state == 'High':
            state_weights['Low'] = 1.4
            state_weights['Mid'] = 1.2
            
        return state_weights

    def calculate_element_weights(self):
        """2단계: 최근 10회차 음양오행 상생상극 에너지 균형 가중치 산출"""
        element_counts = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
        recent_draws = self.history[-10:] if len(self.history) >= 10 else self.history
        
        for draw in recent_draws:
            for num in draw:
                element_counts[self.element_map[num]] += 1
                
        total_count = sum(element_counts.values()) if sum(element_counts.values()) > 0 else 1
        element_weights = {}
        for el, count in element_counts.items():
            ratio = count / total_count
            # 출현 빈도가 적은(쇠한) 기운에 가중치를 부여하여 균형 회복
            element_weights[el] = max(0.2, 1.5 - ratio * 2)
            
        return element_weights, element_counts

    def generate_balanced_combination(self):
        """3단계: 중용 필터링 및 몬테카를로 시뮬레이션 조합 도출"""
        elem_w, _ = self.calculate_element_weights()
        
        number_weights = []
        for num in self.num_pool:
            el = self.element_map
