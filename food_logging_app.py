import streamlit as st
import os
from PIL import Image
import uuid
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import koreanize_matplotlib  # ✅ 한글 깨짐 방지용

# 세션 상태 초기화
if "food_counts" not in st.session_state:
    st.session_state.food_counts = {}
if "log" not in st.session_state:
    st.session_state.log = []

st.set_page_config(page_title="🍽️ 음식 기록 & 분석", layout="centered")
st.title("📸 음식 사진 기록 & 소비 분석 앱")

# 음식 이름 입력
label = st.text_input("🍴 음식 이름을 입력하세요 (예: 김치, 사과, 라면 등)")

# 카메라로 사진 찍기
img = st.camera_input("📷 음식 사진을 찍어주세요")

# 사진 업로드 기능 (선택사항)
uploaded_file = st.file_uploader("📁 또는 사진 파일을 업로드하세요", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    img = uploaded_file

if img and label:
    # 저장 폴더 만들기
    save_dir = os.path.join("dataset", label)
    os.makedirs(save_dir, exist_ok=True)

    # 이미지 저장
    filename = f"{uuid.uuid4()}.jpg"
    save_path = os.path.join(save_dir, filename)
    Image.open(img).save(save_path)

    # 세션 상태에 기록 추가
    st.session_state.food_counts[label] = st.session_state.food_counts.get(label, 0) + 1

    # CSV 로그에 추가할 항목
    now = datetime.now().strftime("%Y-%m-%d")
    weekday = datetime.now().strftime("%A")  # 요일 저장
    st.session_state.log.append({"날짜": now, "요일": weekday, "음식": label, "파일명": filename})

    st.success(f"✅ '{label}' 사진 저장 완료! 총 {st.session_state.food_counts[label]}개 기록됨")

    # CSV 파일에 저장
    df = pd.DataFrame(st.session_state.log)
    df.to_csv("food_log.csv", index=False, encoding="utf-8-sig")

# 분석 차트 표시
if st.session_state.food_counts:
    st.markdown("---")
    st.subheader("🍕 음식 기록 통계 (비율 기준)")

    labels = list(st.session_state.food_counts.keys())
    sizes = list(st.session_state.food_counts.values())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

    # 📈 날짜별 음식 소비 기록 표시
    st.markdown("---")
    st.subheader("📅 날짜별 음식 소비 기록")

    df = pd.DataFrame(st.session_state.log)
    if not df.empty:
        grouped = df.groupby(["날짜", "음식"]).size().unstack(fill_value=0)
        st.bar_chart(grouped)

    # 📆 요일별 소비 패턴 표시
    st.markdown("---")
    st.subheader("📆 요일별 소비 패턴")

    weekday_grouped = df.groupby(["요일", "음식"]).size().unstack(fill_value=0)
    st.bar_chart(weekday_grouped)

    # ✅ 파일 저장 경로 표시
    st.markdown("📁 저장된 CSV 파일: `food_log.csv`")

# 📱 모바일 보기 최적화 (간단한 여백 조정)
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)
