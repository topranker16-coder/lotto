import streamlit as st

st.title("🎲 로또 예측 테스트 화면")
st.write("환영합니다! 스트림릿 웹 화면이 정상적으로 작동하고 있습니다.")

if st.button("번호 생성하기"):
    st.success("테스트 번호: 3, 12, 24, 31, 38, 45")
