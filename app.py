import streamlit as st
import pandas as pd
from pathlib import Path
import gspread

# --- 페이지 설정 ---
st.set_page_config(
    page_title="카메라 사용자 설문조사",
    page_icon="📸"
)

# --- Session State 초기화 ---
# 제출 상태를 저장하여 재제출을 방지
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# --- 설문조사 제목 ---
st.title("📸 카메라 사용 경험에 대한 설문조사")

# --- 설문조사 폼 ---
if not st.session_state.submitted:
    st.write("잠시 시간을 내어 아래 질문에 답변해주시면 서비스 개선에 큰 도움이 됩니다.")
    st.divider()

    # --- 설문조사 문항 ---
    st.subheader("1. 미러리스 or DSLR을 사용하게 된 이유가 있나요?")
    q1_response = st.radio(
        "q1",
        ("스마트폰보다 더 좋은 화질을 원해서",
         "아웃포커싱 등 특별한 사진 효과를 위해서",
         "렌즈 교체와 다양한 촬영 환경을 시도해보고 싶어서",
         "여행, 기록 등 개인적인 만족과 즐거움을 위해서",
         "사진을 본격적인 취미로 삼기 위해",
         "의도는 없었지만, 일·행사 등 필요에 의해 사용하게 되어서"),
        label_visibility="collapsed", index=None
    )
    st.divider()

    st.subheader("2. 사진의 밝기를 바꾸는 기본 요소(조리개, 셔터속도, ISO)를 알고 계신가요?")
    q2_response = st.radio(
        "q2",
        ("잘 알고 있다 (이름과 역할을 이해한다)",
         "들어본 적은 있다 (이름은 알지만 역할은 잘 모른다)",
         "전혀 모른다"),
        label_visibility="collapsed", index=None
    )
    st.divider()

    # --- 2번 질문에 대한 조건부 문항 ---
    q2_1_response = None
    q2_1_1_response = None
    q2_1_2_response = None
    q2_1_2_other = ""
    q2_1_3_response = None
    q2_1_3_other = ""

    if q2_response:
        if q2_response in ["잘 알고 있다 (이름과 역할을 이해한다)", "들어본 적은 있다 (이름은 알지만 역할은 잘 모른다)"]:
            st.subheader("2-1. 해당 요소들을 어떤 방식으로 사용해 보셨나요?")
            q2_1_response = st.radio(
                "q2_1",
                ("수동 모드를 자유롭게 사용한다",
                 "반자동 모드(A/S 모드 등)로 일부 값만 조정한다",
                 "전혀 조작해본 적 없고 자동 모드만 사용한다"),
                label_visibility="collapsed", index=None
            )

            if q2_1_response in ["수동 모드를 자유롭게 사용한다", "반자동 모드(A/S 모드 등)로 일부 값만 조정한다"]:
                with st.expander("세부 질문 보기"):
                    st.subheader("2-1-1. 세 가지 요소 중에서 가장 조절하기 어렵다고 느낀 것은 무엇인가요?")
                    q2_1_1_response = st.radio("q2_1_1", ("조리개", "셔터 속도", "ISO", "잘 모르겠다"), label_visibility="collapsed", index=None)

                    st.subheader("2-1-2. 조작할 때 가장 어려운 점은 무엇인가요?")
                    q2_1_2_response = st.radio(
                        "q2_1_2",
                        ("조작 방법 자체가 헷갈린다",
                         "어떤 결과를 초래하는지 모르겠다",
                         "결과는 알지만 원하는 대로 표현하기 어렵다",
                         "기타"),
                        label_visibility="collapsed", index=None
                    )
                    if q2_1_2_response == "기타":
                        q2_1_2_other = st.text_input("기타 의견을 적어주세요 (2-1-2)")
            
        elif q2_response == "전혀 모른다":
            with st.expander("세부 질문 보기"):
                st.subheader("2-1-3. 조작을 하지 않은 이유는 무엇인가요?")
                q2_1_3_response = st.radio(
                    "q2_1_3",
                    ("방법 자체를 몰라서",
                     "방법을 알지만, 조절했을 때 결과가 어떻게 될지 몰라서",
                     "자동 모드만 사용해도 충분하다고 생각해서",
                     "기타"),
                    label_visibility="collapsed", index=None
                )
                if q2_1_3_response == "기타":
                    q2_1_3_other = st.text_input("기타 의견을 적어주세요 (2-1-3)")
    st.divider()

    st.subheader("3. ISO, 셔터스피드, 조리개의 변경이 사진에 어떻게 반영되는지 모를 때, 어떻게 대처하나요?")
    q3_response = st.radio("q3", ("자동/반자동 모드를 활용한다.", "지인, SNS, 유튜브 등 다양한 채널을 통해 경험자들의 노하우를 배운다.", "설정을 하나씩 바꿔가며 촬영하고 결과를 비교한다.", "기타"), label_visibility="collapsed", index=None)
    st.divider()

    st.subheader("4. 다음 사진을 본인이 찍었다고 가정할 때, 어떤 사진이 가장 잘 찍었다고 고를 것 같나요?")
    col1, col2, col3 = st.columns(3)
    with col1: st.image("https://placehold.co/300x300/AAAAAA/FFFFFF?text=초점/선명도", caption="사진 A")
    with col2: st.image("https://placehold.co/300x300/CCCCCC/FFFFFF?text=색감", caption="사진 B")
    with col3: st.image("https://placehold.co/300x300/EEEEEE/FFFFFF?text=구도", caption="사진 C")
    q4_response = st.radio("q4", ("초점 / 선명도", "색감", "구도"), label_visibility="collapsed", index=None)

    st.subheader("4-1. 사진을 고른 이유는 무엇인가요(주관식)?")
    q4_1_response = st.text_area("q4_1", placeholder="예) 색감이 마음에 든다/ 초점이 맞아 선명하다/ 구도가 역동적이다 등", label_visibility="collapsed")
    st.divider()

    st.subheader("5. 사진을 찍을 때 가장 어려웠던 것은 무엇인가요?")
    q5_response = st.radio("q5", ("구도", "색감", "초점", "ISO, 조리개, 셔터스피드 값 조정", "기타"), label_visibility="collapsed", index=None)
    st.subheader("5-1. 예상과 실제 결과물이 다른 경우 어떻게 하시나요?")
    q5_1_response = st.radio("q5_1", ("삭제", "후보정", "촬영방법에 대한 공부", "주변에 물어보기", "기타"), label_visibility="collapsed", index=None)
    st.divider()

    st.subheader("6. 사진을 찍은 후 어떤 부분에서 아쉬움을 느끼셨나요? (2개 선택)")
    q6_response = st.multiselect("q6", ["화질이 마음에 들지 않음", "색감이 별로임", "구도가 생각한대로 되지 않음", "초점이 맞지 않음", "특정 부분이 밝게 날아감", "기타"], max_selections=2, label_visibility="collapsed")
    st.divider()

    st.subheader("7. 사진 촬영할 때 핸드폰을 어떻게 사용하시나요?")
    q7_response = st.radio("q7", ("원하는 사진촬영에 대한 방법", "일기예보 확인", "촬영스팟 검색", "카메라 사진 폰으로 옮기기", "활용하지 않음", "기타"), label_visibility="collapsed", index=None)
    st.divider()

    # --- 제출 버튼 및 데이터 저장 로직 ---
    submit_button = st.button("설문 완료 및 제출하기")

    if submit_button:
        # --- 필수 항목 유효성 검사 ---
        if not all([q1_response, q2_response, q3_response, q4_response, q5_response, q5_1_response, q7_response]):
            st.warning("⚠️ 답변하지 않은 필수 항목이 있습니다. 모든 질문에 답변해주세요.")
        else:
            try:
                # --- Google Sheets Connection ---
                gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
                spreadsheet = gc.open("Survey-Results")
                worksheet = spreadsheet.sheet1
                # --- End of Connection ---

                new_data = {
                    "1. 사용 이유": q1_response,
                    "2. 밝기 요소 인지": q2_response,
                    "2-1. 사용 방식": q2_1_response,
                    "2-1-1. 가장 어려운 요소": q2_1_1_response,
                    "2-1-2. 어려운 점": q2_1_2_response,
                    "2-1-2. 기타": q2_1_2_other,
                    "2-1-3. 미조작 이유": q2_1_3_response,
                    "2-1-3. 기타": q2_1_3_other,
                    "3. 모를 때 대처법": q3_response,
                    "4. 가장 잘 찍은 사진 기준": q4_response,
                    "4-1. 잘 찍은 이유(주관식)": q4_1_response,
                    "5. 가장 어려웠던 것": q5_response,
                    "5-1. 결과물이 다를 때 대처법": q5_1_response,
                    "6. 아쉬운 점(최대 2개)": ", ".join(q6_response),
                    "7. 핸드폰 사용법": q7_response,
                }

                if worksheet.cell(1, 1).value is None:
                    worksheet.append_row(list(new_data.keys()))
                worksheet.append_row(list(new_data.values()))
                
                st.session_state.submitted = True
                st.rerun()

            except Exception as e:
                st.error("오류가 발생했습니다. 구글 시트 연동 설정을 다시 확인해주세요.")
                st.error(f"에러 상세 정보: {e}")

else:
    st.success("✅ 설문에 참여해주셔서 감사합니다!")
    st.balloons()
    st.write("새로운 응답을 제출하시려면 페이지를 새로고침 해주세요.") # 사용자가 원할 경우를 대비한 안내