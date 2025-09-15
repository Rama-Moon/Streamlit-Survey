import streamlit as st
import pandas as pd
from pathlib import Path
import gspread

# --- 페이지 설정 ---
st.set_page_config(
    page_title="미니 설문조사",
    page_icon="📋"
)

# --- 설문조사 제목 ---
st.title("📋 미니 설문조사 프로토타입")
st.write("잠시 시간을 내어 아래 4가지 질문에 답변해주세요.")

# --- 설문조사 문항 ---

# 질문 1
q1_response = st.radio(
    "**1. 저희 서비스를 처음 알게 된 경로는 무엇인가요?**",
    ("SNS 광고", "지인 추천", "검색 엔진", "기타"),
    key="q1",
    horizontal=True
)

st.divider()

# 질문 2 (이미지 포함)
st.write("**2. 다음 두 가지 로고 시안 중 어떤 디자인이 더 마음에 드시나요?**")

col1, col2 = st.columns(2)

with col1:
    st.image("https://placehold.co/300x300/003366/FFFFFF?text=Logo+A", caption="로고 A")

with col2:
    st.image("https://placehold.co/300x300/4B8BBE/FFFFFF?text=Logo+B", caption="로고 B")

q2_response = st.radio(
    "선호하는 로고를 선택해주세요.",
    ("로고 A", "로고 B", "둘 다 마음에 들지 않음"),
    key="q2",
    horizontal=True
)

st.divider()

# 질문 3
q3_response = st.radio(
    "**3. 새로운 기능이 추가된다면 어떤 기능을 가장 원하시나요?**",
    ("AI 추천 기능", "다크 모드", "외부 서비스 연동", "오프라인 모드"),
    key="q3",
    horizontal=True
)

st.divider()

# 질문 4
q4_response = st.radio(
    "**4. 저희 서비스의 전반적인 만족도는 어떠신가요?**",
    ("매우 만족", "만족", "보통", "불만족", "매우 불만족"),
    key="q4",
    horizontal=True
)

st.divider()

# --- 제출 버튼 및 데이터 저장 로직 ---
submit_button = st.button("설문 완료 및 제출하기")

if submit_button:
    try:
        # --- Google Sheets Connection ---
        # Streamlit의 Secrets를 사용하여 서비스 계정 인증 정보 로드
        gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])

        # "Survey-Results"라는 이름의 스프레드시트 열기
        spreadsheet = gc.open("Survey-Results")

        # 첫 번째 워크시트 선택
        worksheet = spreadsheet.sheet1
        # --- End of Connection ---

        # 데이터를 딕셔너리 형태로 정리
        new_data = {
            "알게된 경로": q1_response,
            "선호 로고": q2_response,
            "원하는 기능": q3_response,
            "전반적 만족도": q4_response,
        }

        # --- Data Appending ---
        # 시트의 첫 행이 비어있을 경우, 헤더(질문) 추가
        if worksheet.cell(1, 1).value is None:
            worksheet.append_row(list(new_data.keys()))

        # 새로운 설문 데이터를 다음 행에 추가
        worksheet.append_row(list(new_data.values()))
        # --- End of Appending ---

        st.success("✅ 설문이 구글 시트에 성공적으로 저장되었습니다!")
        st.balloons()

    except Exception as e:
        st.error("오류가 발생했습니다. 구글 시트 연동 설정을 다시 확인해주세요.")
        st.error(f"에러 상세 정보: {e}")