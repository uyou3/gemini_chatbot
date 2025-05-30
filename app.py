import streamlit as st
import google.generativeai as genai

# Google API 키 설정
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    if not GOOGLE_API_KEY:
        st.error("GOOGLE_API_KEY가 설정되지 않았습니다. .streamlit/secrets.toml 파일을 확인해주세요.")
        st.stop()
except Exception as e:
    st.error(f"API 키를 불러오는 중 오류가 발생했습니다: {str(e)}")
    st.stop()

# Gemini 모델 초기화
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error(f"Gemini 모델 초기화 중 오류가 발생했습니다: {str(e)}")
    st.stop()

# 세션 상태 초기화
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 페이지 설정
st.set_page_config(
    page_title="Gemini 챗봇",
    page_icon="🤖",
    layout="wide"
)

# 타이틀과 설명
st.title("Gemini 챗봇")
st.markdown("Gemini API를 활용한 기본 챗봇 프레임워크입니다.")

# 이전 대화 기록 표시
with st.expander("이전 대화 보기", expanded=False):
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    else:
        st.info("아직 대화 기록이 없습니다.")

# 채팅 입력창
user_input = st.text_input("메시지를 입력하세요:", key="user_input")

# 전송 버튼
if st.button("전송"):
    if user_input:
        # 사용자 메시지 표시
        with st.chat_message("user"):
            st.write(user_input)
        
        # 사용자 메시지를 대화 기록에 추가
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        try:
            # Gemini 모델에 메시지 전송 및 응답 받기
            response = st.session_state.chat.send_message(user_input)
            
            # AI 응답 표시
            with st.chat_message("assistant"):
                st.write(response.text)
            
            # AI 응답을 대화 기록에 추가
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"응답 생성 중 오류가 발생했습니다: {str(e)}")
    else:
        st.warning("메시지를 입력해주세요.")
