import streamlit as st
import pandas as pd
import plotly.express as px
import warnings

# 모든 경고 메시지를 무시하도록 설정
warnings.filterwarnings('ignore')

# Streamlit 페이지 설정
st.set_page_config(
    page_title="두레팜 & 판다스 | 농업 폐기물에서 지속가능 에너지로",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 사용자 정의 CSS (Tailwind CSS 스타일을 Streamlit에 적용)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');

    html, body, [class*="st-emotion-"], .main, .block-container, .css-18e3th9 {
        font-family: 'Noto Sans KR', sans-serif;
        color: #333333; /* 기본 텍스트 색상 */
    }
    h1, h2, h3, h4, h5, h6 {
        color: #2C5F2D; /* 헤더 색상 (짙은 녹색) */
    }
    /* Streamlit 버튼 스타일 오버라이드 */
    .stButton>button {
        background-color: #97BC62; /* 버튼 배경색 (밝은 녹색) */
        color: white; /* 버튼 텍스트 색상 */
        border-radius: 9999px; /* 완전히 둥근 모서리 */
        padding-top: 12px;
        padding-bottom: 12px;
        padding-left: 32px;
        padding-right: 32px;
        font-weight: bold;
        transition: background-color 0.3s ease, transform 0.2s ease; /* 호버 애니메이션 */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
        border: none; /* 테두리 제거 */
    }
    .stButton>button:hover {
        background-color: #2C5F2D; /* 호버 시 버튼 배경색 (짙은 녹색) */
        transform: translateY(-2px); /* 호버 시 약간 위로 이동 */
        box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15); /* 호버 시 그림자 강화 */
    }
    /* 빠른 링크 버튼 스타일 */
    .quick-link-button {
        background-color: #f0f4ec !important; /* 밝은 녹색 계열 배경 */
        color: #2C5F2D !important; /* 짙은 녹색 텍스트 */
        transition: background-color 0.3s ease, transform 0.2s ease !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        border: 1px solid #97BC62 !important; /* 미묘한 테두리 */
        border-radius: 9999px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        text-decoration: none; /* 링크 밑줄 제거 */
        display: block; /* 컬럼 내에서 전체 너비 차지 */
        text-align: center; /* 텍스트 중앙 정렬 */
    }
    .quick-link-button:hover {
        background-color: #97BC62 !important; /* 호버 시 밝은 녹색 배경 */
        color: white !important; /* 호버 시 흰색 텍스트 */
        transform: translateY(-2px) !important;
        box_shadow: 0 6px 10px rgba(0, 0, 0, 0.15) !important;
    }
    /* 텍스트 줄바꿈 균등화 (CSS text-wrap: balance 역할) */
    .stMarkdown p {
        text-wrap: balance;
    }
    /* 차트 컨테이너 최대 너비 및 중앙 정렬 */
    .chart-container-plotly {
        max-width: 500px; /* 차트 최대 너비 제한 */
        margin: auto; /* 중앙 정렬 */
    }
    /* Streamlit 앱의 기본 배경색 설정 */
    .stApp {
        background-color: #F8F7F4;
    }
    </style>
""", unsafe_allow_html=True)

# 페이지 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- 함수 정의: 각 페이지의 콘텐츠 ---

def display_home_page():
    # Streamlit의 빈 공간을 활용하여 페이지를 중앙에 배치
    col_left, col_center, col_right = st.columns([1, 4, 1])

    with col_center:
        st.markdown(f"""
            <div style="
                background-color: #F8F7F4; /* 밝은 베이지색 배경 */
                height: 80vh; /* 화면의 80% 높이 차지 */
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                color: #333333; /* 기본 텍스트 색상 */
                padding: 2rem;
                border-radius: 0.75rem; /* 둥근 모서리 */
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); /* 그림자 */
                margin-top: 5vh; /* 상단 여백 추가 */
                margin-bottom: 5vh; /* 하단 여백 추가 */
            ">
                <h1 style="font-size: 2.5rem; font-weight: 700; line-height: 1.2; margin-bottom: 1rem; color: #2C5F2D;">버섯 농가 여러분을 환영합니다!</h1>
                <p style="font-size: 1.125rem; max-width: 40rem; margin: auto 0 2rem 0; color: #4B5563;">
                    두레팜은 버섯 폐배지 수거를 통해 농가의 부담을 덜고, 지속 가능한 친환경 에너지 생산에 기여합니다.<br>
                    아래에서 필요한 서비스를 선택해 주세요.
                </p>
                <div style="display: flex; flex-direction: column; gap: 1rem; width: 100%; max-width: 25rem;">
        """, unsafe_allow_html=True)

        if st.button("폐배지 수거 요청", key="request_btn"):
            st.session_state.page = 'request'
            st.rerun()
        
        if st.button("폐배지 수거 현황 확인", key="status_btn"):
            st.session_state.page = 'status'
            st.rerun()
        
        st.markdown(f"""
                </div>
                <p style="margin-top: 2rem; font-size: 0.9rem; color: #6B7280;">
                    두레팜의 사업 구상에 대해 더 자세히 알고 싶으시면 아래로 스크롤하거나<br> 상단 메뉴 '회사소개'를 클릭해 주세요.
                </p>
            </div>
        """, unsafe_allow_html=True)

def display_request_page():
    st.markdown('<div style="background-color: white; padding: 5rem 1rem;">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #2C5F2D; margin-bottom: 2rem; font-size: 2.25rem; font-weight: 700;'>폐배지 수거 요청</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.125rem; color: #6B7280; max-width: 50rem; margin: auto;'>폐배지 수거를 요청하시려면 아래 정보를 입력해 주세요.</p>", unsafe_allow_html=True)

    with st.form("collection_request_form"):
        st.markdown("<div style='background-color: #F8F7F4; padding: 2rem; border-radius: 0.5rem;'>", unsafe_allow_html=True)
        farm_name = st.text_input("농가 이름")
        contact_person = st.text_input("담당자 이름")
        contact_phone = st.text_input("연락처 (휴대폰)")
        collection_address = st.text_area("수거 주소 (상세 주소 포함)")
        waste_type = st.selectbox("폐배지 종류", ["참송이", "느타리", "새송이", "기타"])
        estimated_quantity = st.number_input("예상 수거량 (톤)", min_value=0.1, max_value=1000.0, value=1.0, step=0.1)
        preferred_date = st.date_input("희망 수거일")
        notes = st.text_area("특이사항 (선택 사항)")

        submitted = st.form_submit_button("수거 요청 제출하기")

        if submitted:
            st.success("수거 요청이 접수되었습니다! 빠른 시일 내에 연락드리겠습니다.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.button("뒤로 가기", on_click=lambda: st.session_state.update(page='home'))
    st.markdown("</div>", unsafe_allow_html=True)

def display_status_page():
    st.markdown('<div style="background-color: white; padding: 5rem 1rem;">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #2C5F2D; margin-bottom: 2rem; font-size: 2.25rem; font-weight: 700;'>폐배지 수거 현황 확인</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.125rem; color: #6B7280; max-width: 50rem; margin: auto;'>요청하신 폐배지 수거 현황을 아래에서 확인하실 수 있습니다.</p>", unsafe_allow_html=True)

    status_data = {
        '요청번호': ['REQ001', 'REQ002', 'REQ003'],
        '농가명': ['행복농장', '건강농장', '두레농장'],
        '수거량 (톤)': [10.5, 20.0, 5.2],
        '수거상태': ['수거 완료', '수거 예정', '처리 중'],
        '예정일': ['2024-07-01', '2024-07-15', '2024-07-20']
    }
    df_status = pd.DataFrame(status_data)

    st.subheader("나의 수거 요청 내역")
    st.dataframe(df_status, use_container_width=True)

    st.button("뒤로 가기", on_click=lambda: st.session_state.update(page='home'))
    st.markdown("</div>", unsafe_allow_html=True)

# --- 메인 페이지 로직 ---

# 현재 페이지 상태에 따라 다른 콘텐츠를 렌더링
if st.session_state.page == 'home':
    display_home_page()
else: # 'request' or 'status' page
    if st.session_state.page == 'request':
        display_request_page()
    elif st.session_state.page == 'status':
        display_status_page()

    # 나머지 기존 섹션들은 항상 표시되도록 유지 (스크롤로 접근 가능)
    # 빠른 링크 섹션
    st.markdown('<div style="text-align: center; padding: 3rem 1rem; background-color: #F8F7F4;">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #2C5F2D; margin-bottom: 2rem; font-size: 2.25rem; font-weight: 700;'>두레팜의 사업 구상에 대해 더 알아보기</h2>", unsafe_allow_html=True)

    ql_col1, ql_col2, ql_col3, ql_col4 = st.columns(4)

    with ql_col1:
        st.markdown('<a href="#problem_section" class="quick-link-button">문제</a>', unsafe_allow_html=True)
    with ql_col2:
        st.markdown('<a href="#business_concept_section" class="quick-link-button">사업 구상</a>', unsafe_allow_html=True)
    with ql_col3:
        st.markdown('<a href="#impact_section" class="quick-link-button">가치</a>', unsafe_allow_html=True)
    with ql_col4:
        st.markdown('<a href="#market_section" class="quick-link-button">시장</a>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


    # 3. 문제 (Problem Section)
    st.markdown('<a name="problem_section"></a>', unsafe_allow_html=True)
    st.markdown("<div style='background-color: white; padding: 5rem 1rem;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #2C5F2D; margin-bottom: 1rem; font-size: 2.25rem; font-weight: 700;'>골칫거리 농업 폐기물의 현실</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.125rem; color: #6B7280; max-width: 50rem; margin: auto;'>매년 막대한 양의 버섯 폐배지가 버려지며 환경 문제와 농가 부담을 야기하고 있습니다. 이는 단순한 폐기물 문제를 넘어, 활용되지 못한 거대한 자원의 기회입니다.</p>", unsafe_allow_html=True)

    problem_col1, problem_col2 = st.columns(2)

    with problem_col1:
        waste_data = pd.DataFrame({
            'Category': ['재활용 (16.9%)', '미활용/폐기 (83.1%)'],
            'Value': [16.9, 83.1]
        })
        fig_doughnut = px.pie(waste_data, values='Value', names='Category', hole=0.7,
                              color_discrete_sequence=['#97BC62', '#E5E7EB'])
        fig_doughnut.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="'Noto Sans KR', sans-serif")
        )
        st.plotly_chart(fig_doughnut, use_container_width=True)

    with problem_col2:
        st.markdown(f"""
            <div style='display: flex; flex-direction: column; gap: 2rem;'>
                <div>
                    <p style='font-size: 3rem; font-weight: 800; color: #2C5F2D;'>800,000톤</p>
                    <p style='font-size: 1.25rem; color: #4B5563; font-weight: 500;'>연간 총 버섯 폐배지 발생량</p>
                    <p style='color: #6B7280; margin-top: 0.25rem;'>국내 농업 환경에 심각한 부담을 주고 있는 규모입니다.</p>
                </div>
                <div>
                    <p style='font-size: 3rem; font-weight: 800; color: #2C5F2D;'>175,000원</p>
                    <p style='font-size: 1.25rem; color: #4B5563; font-weight: 500;'>농가 폐기물 처리 비용 (톤당)</p>
                    <p style='color: #6B7280; margin-top: 0.25rem;'>농가의 수익성을 저해하는 주된 요인 중 하나입니다.</p>
                </div>
                <div>
                    <p style='font-size: 3rem; font-weight: 800; color: #2C5F2D;'>664,000톤 이상</p>
                    <p style='font-size: 1.25rem; color: #4B5563; font-weight: 500;'>연간 미활용 및 폐기되는 양</p>
                    <p style='color: #6B7280; margin-top: 0.25rem;'>막대한 잠재적 가치가 매년 사라지고 있습니다.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


    # 4. 사업 구상 (Business Concept Section)
    st.markdown('<a name="business_concept_section"></a>', unsafe_allow_html=True)
    st.markdown("<div style='background-color: #F8F7F4; padding: 5rem 1rem;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #2C5F2D; margin-bottom: 1rem; font-size: 2.25rem; font-weight: 700;'>두레팜의 사업 구상: 농업 폐기물을 고부가가치 에너지로</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.125rem; color: #6B7280; max-width: 50rem; margin: auto;'>두레팜과 판다스는 버섯 재배 과정에서 발생하는 폐배지의 환경 문제와 농가의 부담을 해결하기 위한 혁신적인 사업 아이디어를 제시합니다. 우리는 버려지던 폐배지를 발전소에서 필요로 하는 고품질 목재 펠릿으로 전환하여 지속 가능한 순환 경제 모델을 구축하고자 합니다.</p>", unsafe_allow_html=True)

    concept_col1, concept_col2 = st.columns(2)
    with concept_col1:
        st.image("https://raw.githubusercontent.com/pandasmc/pandasmc.github.io/refs/heads/main/img/%EB%AA%A9%EC%9E%AC%ED%8E%A0%EB%A6%BF.jpg", caption="버섯 폐배지를 활용한 바이오펠릿 생산 구상", use_container_width=True)
    with concept_col2:
        st.markdown(f"""
            <div style='display: flex; flex-direction: column; gap: 1.5rem;'>
                <div>
                    <h3 style='font-size: 1.5rem; font-weight: bold; color: #2C5F2D;'>폐기물 문제를 해결하는 혁신적인 접근</h3>
                    <p style='color: #4B5563;'>매년 발생하는 막대한 양의 버섯 폐배지를 단순한 폐기물이 아닌, 잠재력 높은 바이오 에너지 자원으로 인식합니다. 이는 환경 부담을 줄이고 자원 효율성을 극대화하는 첫걸음입니다.</p>
                </div>
                <div>
                    <h3 style='font-size: 1.5rem; font-weight: bold; color: #2C5F2D;'>고품질 바이오펠릿 생산을 위한 비전</h3>
                    <p style='color: #4B5563;'>버섯 폐배지의 특성을 활용하여, 발전소의 요구 사항을 충족하는 안정적이고 효율적인 목재 펠릿을 생산하는 것을 목표로 합니다. 이는 한국의 재생에너지 목표 달성에 기여할 것입니다.</p>
                </div>
                <div>
                    <h3 style='font-size: 1.5rem; font-weight: bold; color: #2C5F2D;'>농가와 상생하는 지속 가능한 모델</h3>
                    <p style='color: #4B5563;'>폐배지를 수거하여 농가의 처리 비용 부담을 덜어주고, 새로운 수익원을 제공함으로써 농업과 산업이 함께 성장하는 상생의 생태계를 구축하고자 합니다.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


    # 5. 가치 (Impact Section)
    st.markdown('<a name="impact_section"></a>', unsafe_allow_html=True)
    st.markdown("<div style='background-color: white; padding: 5rem 1rem;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #2C5F2D; margin-bottom: 1rem; font-size: 2.25rem; font-weight: 700;'>지속가능한 가치 창출</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.125rem; color: #6B7280; max-width: 50rem; margin: auto;'>두레팜의 사업은 환경 보호를 넘어 농가, 지역사회, 국가 경제에 실질적인 이익을 가져오는 상생의 모델입니다.</p>", unsafe_allow_html=True)

    impact_cols = st.columns(4)
    impact_data = [
        {"icon": "🌍", "title": "환경 보호", "description": "폐기물 매립/소각으로 인한 토양·대기오염 방지 및 탄소 배출 저감"},
        {"icon": "👨‍🌾", "title": "농가 소득 증대", "description": "폐기물 처리 비용 절감 및 폐배지 판매를 통한 새로운 수익원 창출"},
        {"icon": "⚡️", "title": "에너지 안보 강화", "description": "연간 7천억 원에 달하는 수입 펠릿을 대체하고, 국내 에너지 자급률 향상"},
        {"icon": "🤝", "title": "지역 경제 활성화", "description": "생산 시설 운영을 통한 농촌 지역의 안정적인 일자리 창출"}
    ]

    for i, data in enumerate(impact_data):
        with impact_cols[i]:
            st.markdown(f"""
                <div style="
                    text-align: center;
                    padding: 2rem;
                    background-color: white;
                    border-radius: 0.5rem;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                ">
                    <div style="font-size: 3rem; margin-bottom: 1rem; color: #97BC62;">{data['icon']}</div>
                    <h3 style="font-size: 1.25rem; font-weight: bold; margin-bottom: 0.5rem; color: #2C5F2D;">{data['title']}</h3>
                    <p style="color: #4B5563;">{data['description']}</p>
                </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


    # 6. 시장 (Market Section)
    st.markdown('<a name="market_section"></a>', unsafe_allow_html=True)
    st.markdown("<div style='background-color: #F8F7F4; padding: 5rem 1rem;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #2C5F2D; margin-bottom: 1rem; font-size: 2.25rem; font-weight: 700;'>기회의 시장, 현명한 선택</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.125rem; color: #6B7280; max-width: 50rem; margin: auto;'>대한민국 재생에너지 정책은 국내산 '미이용 바이오매스'에 강력한 인센티브를 제공합니다. 두레팜의 바이오펠릿은 발전소의 RPS 의무 이행과 수익성 확보를 위한 가장 확실한 파트너입니다.</p>", unsafe_allow_html=True)

    market_col1, market_col2 = st.columns([3, 2])
    with market_col1:
        market_chart_data = pd.DataFrame({
            '연도': ['2021', '2022', '2023', '2024 (예상)'],
            '수입량 (만 톤)': [350, 365, 373, 400]
        })
        st.bar_chart(market_chart_data.set_index('연도'), color='#97BC62')
        st.markdown("<h3 style='text-align: center; font-size: 1.25rem; font-weight: bold; color: #2C5F2D;'>국내 발전용 목재 펠릿 수입량 추이</h3>", unsafe_allow_html=True)

    with market_col2:
        st.markdown(f"""
            <div style='display: flex; flex-direction: column; gap: 1.5rem;'>
                <div>
                    <h3 style='font-size: 1.25rem; font-weight: bold; color: #2C5F2D;'>RPS 정책의 핵심: REC 가중치</h3>
                    <p style='color: #4B5563;'>정부는 2025년부터 수입 목재 펠릿의 REC 가중치를 축소하지만, 두레팜의 펠릿과 같은 '미이용 바이오매스'는 현행 가중치를 유지합니다. 이는 압도적인 경제적 우위를 의미합니다.</p>
                </div>
                <div>
                    <h3 style='font-size: 1.25rem; font-weight: bold; color: #2C5F2D;'>지속가능성 인증</h3>
                    <p style='color: #4B5563;'>ISCC, ISO 9001/14001 등 국제 표준 인증 획득을 통해 제품의 신뢰성과 글로벌 기준 준수를 증명하여 발전소의 ESG 경영에 기여합니다.</p>
                </div>
                <div>
                    <h3 style='font-size: 1.25rem; font-weight: bold; color: #2C5F2D;'>안정적인 국내 공급망</h3>
                    <p style='color: #4B5563;'>국제 정세나 환율 변동에 영향을 받지 않는 안정적인 국내 생산 및 공급 체계를 통해 예측 가능한 파트너십을 제공합니다.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


    # 7. 문의 (Contact Section)
    st.markdown('<a name="contact_section"></a>', unsafe_allow_html=True)
    st.markdown("<div style='background-color: white; padding: 5rem 1rem;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #2C5F2D; margin-bottom: 1rem; font-size: 2.25rem; font-weight: 700;'>함께 만들어갈 지속가능한 미래</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.125rem; color: #6B7280; max-width: 40rem; margin: auto;'>두레팜과 판다스는 혁신적인 기술과 열정으로 더 나은 세상을 만들어갑니다.<br>사업 파트너십, 투자, 원료 공급에 대해 궁금한 점이 있으시면 언제든지 연락 주십시오.</p>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div style='background-color: white; padding: 2rem; border-radius: 0.5rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); max-width: 40rem; margin: 2rem auto;'>", unsafe_allow_html=True)
        with st.form("contact_form"):
            name = st.text_input("이름")
            company = st.text_input("회사명")
            email = st.text_input("이메일")
            message = st.text_area("문의 내용")

            submitted = st.form_submit_button("문의하기")

            if submitted:
                st.success("문의가 성공적으로 제출되었습니다. 빠른 시일 내에 연락드리겠습니다!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown(f"""
        <div style="
            background-color: #1F2937; /* 회색-800 */
            color: white;
            text-align: center;
            padding: 2rem;
        ">
            <p>(주)판다스 | 대표: 황진경</p>
            <p style="font-size: 0.875rem; color: #9CA3AF; margin-top: 0.5rem;">자연과 함께 건강한 가치를 전하는 농장, 두레팜</p>
            <p style="font-size: 0.75rem; color: #6B7280; margin-top: 1rem;">&copy; 2024 Durefarm & Pandas Inc. All Rights Reserved.</p>
        </div>
    """, unsafe_allow_html=True)
