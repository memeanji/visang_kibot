import streamlit as st
import re

# CSS 스타일 추가
# Header와 Footer를 같은 행에 배치
col1, col2 = st.columns([4, 1])

with col1:
    st.markdown(
        "<h1 style='font-size: 32px; font-weight: bold; color: #4CAF50;'>🐣 KIBOT</h1>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        "<p style='font-size: 14px; color: #777; text-align: right;'>© 2025 meanji. <br> All rights reserved by meanji.</p>",
        unsafe_allow_html=True
    )
# 스타일 적용
st.markdown(
        """
    <style>
        .chat-container {
            max-width: 700px;
            margin: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .chat-message {
            padding: 12px;
            margin: 8px 0;
            border-radius: 20px;
            max-width: 70%;
            word-wrap: break-word;
            font-size: 16px;
            line-height: 1.4;
            display: inline-block;
        }
          .user-message {
            background-color: #F0F8FF;
            border-radius: 20px 20px 0px 20px;
            text-align: right;
            float: right;
            clear: both;
            padding: 10px;
            color: #000000;
        }
        .bot-message {
            background-color: #EAEAEA;
            border-radius: 20px 20px 20px 0px;
            text-align: left;
            float: left;
            clear: both;
            padding: 10px;
            color: black;
        }

        .chat-wrapper {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        details {
            background-color: #f8f9fa;
            padding: 10px;
            margin: 8px 0;
            border-radius: 8px;
            border: 1px solid #ddd;
            cursor: pointer;
        }
        
        summary {
            list-style: none; /* 기본 화살표 숨기기 */
            display: flex;
            align-items: center;
        }
       summary::-webkit-details-marker {
            display: none; /* 기본 화살표 숨기기 */
        }

        summary::before {
            content: "▶"; /* 기본 상태에서는 ▶ */
            color: red;
            margin-right: 10px;
            font-size: 16px;
            transition: transform 0.2s ease-in-out;
        }

        details[open] summary::before {
            content: "▼"; /* 열렸을 때는 ▼ */
        
        /* details 요소에도 여백을 추가 */
        details {
         margin-top: -20px;  /* 상단 여백을 줄여서 위로 이동 */
         margin-bottom: -20px;  /* 하단 여백을 음수로 설정하여 아래쪽 공간을 줄임 */
         position: relative;
         top: -20px;  /* 필요시 위로 이동 */
        }   
        /* 만약 상위 컨테이너의 여백을 줄여야 한다면 */
        .container {
        margin-top: -20px;  /* 컨테이너의 상단 여백을 줄여서 위로 올리기 */
        }
    </style>

   <div style="background-color: #f0f0f0; padding: 10px; border-radius: 10px; text-align: center;">
        📚 <b>라키비움 운영 안내</b><br>
        🕒 운영시간: 월~금 09:00~18:00 <br>
        📍 위치: 경기도 과천시 과천대로2길 54 그라운드브이 ○○ <br>
        📖 문의: 02-1544-0554
    </div>
    <br>

    <details>
        <summary><b>자주 묻는 질문 (FAQ)</b></summary>
        <p><b>Q KIBOT은 어떤 서비스인가요?</b><br>A. 🐣 KIBOT은 챗봇 서비스입니다.</p>
        <p><b>Q. 라키비움이란?</b><br>A. 책+아카이브+미술관이 결합된 공간입니다.</p>
        <p><b>Q. 입장료가 있나요?</b><br>A. 아니요, 무료로 이용할 수 있습니다.
    </details>
    """,
    unsafe_allow_html=True
)


# 세션 상태 초기화
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "bot", "text": "안녕하세요! 저는 KIBOT이에요 🐣"}
    ]

# 정규식 기반 응답 함수
def get_response(user_input):
    responses = {
        r"이름": "🐣 KIBOT이야!",
        r"나이|몇살": "나는 3살이야! 🐣",
        r"안녕|반가워": "반가워요! 😊 어떻게 도와드릴까요?",
        r"김민지|민지|민지cp|김민지 cp": "민지 CP님은 FC 콘텐츠 개발 3cell에서 동계 연수 중이고 청순한 외모에 리더십까지 겸비한 소중한 3조의 리더예요👑\n\n 그 어떤 어려움도 민지 CP님의 책임감 있는 리더십과 따뜻한 미소가 함께라면 문제 없답니다 🐇💕",
        r"황다인|다인|다인cp|황다인 cp": "다인 CP님은 FC 콘텐츠 개발 3cell에서 동계 연수 중이고 작고 귀엽고 소중한 본인을 닮은 키움이 창시자랍니다! 🎨💖 창의적인 디자인 감각으로 모든 프로젝트에서 큰 기여를 한 다인 CP님은 멋진 모습도,\n 팀 분위기를 화목하게 만들어 주는 유머러스한 모습도 지닌 팀의 비타민 같은 존재입니다 😄🌟",
        r"조지훈|지훈|지훈cp|조지훈 cp": "지훈 CP님은 사회 3 cell에서 동계 연수 중이고 디자인을 다룰 줄 아는 능력자이자 3조의 쩝쩝박사 타이틀을 보유 중이에요.🌍❄🍽\n\n 디자인뿐 아니라 팀에서 필요한 역할을 성실하게 수행하는 믿음직한 존재 지훈 CP님은 팀에 반드시 필요한 존재랍니다 💪🖥️",
        r"윤예서|예서|예서cp|윤예서 cp": "예서 CP님은 국어 5 cell에서 동계 연수 중이고 말티즈처럼 귀엽고\n사랑스러움을 겸비하고 있답니다.🐶💕\n\n 매일같이 더해지는 귀여움 뒤에 책임감과 성실함도 가득 지니고 있는 팀의 든든한 존재!\n\n 예서 CP님은 읽는 사람에게 따뜻한 감동을 주며, 팀 내에서 필요한 모든 글을 완벽하게 처리해 주는 능력자! ✍️💖",
        r"김다영|다영|다영cp|김다영 cp": "다영 CP님은 영어 3cell에서 동계 연수 중이고 지나가다 마주치면\n\n 힐링될 정도의 미친 외모를 담당중이여오📚❄️✨",
        r"유민|유민cp": "유민 CP님 FC 콘텐츠 개발 2cell에서 동계연수중이고 부드러운 외모와 미친 집중력을 가진 FC의 웃음 미녀!🔥😆\n\n 한 번 집중하면 누구도 못 말리는 몰입력과 반짝이는 센스로 모두를 사로잡는 존재! 💡✨",
        r"권미진|미진|미진cp|권미진 cp": "미진 CP님은 인사 관리 cell에서 동계 연수 중이고 책임감은 물론, 언제나 간담회의 분위기를 자연스럽게 유하게 만들어주는 매력적인 존재예요.😄✨\n\n 출퇴근길에 책을 읽으며 자기계발을 게을리하지 않는 갓생러 미진 CP님의 책임감과 성실함에 감동하지 않을 수 없답니다 📚💼",
        r"김도연|도연|도연cp|김도연 cp": "도연 CP님은 에듀테크 1cell에서 동계 연수 중이고 비상교육 연수생 카페의 연예인과 같은 존재세요🌟\n\n 파워블로거가 되겠다는 일념 하에 재미있는 마니또 인증을 통해 연수생들의 하루에 한 줄기 웃음을 주셨답니다 간담회 당시에는 직접 마니또에게 하고 싶은 말을 전하는 용기까지!\n 쇼맨십도 겸비한 최고의 연수생이랍니다💚",
        r"김은수|은수|은수cp|김은수 cp": "은수 CP님은 국어 4cell에서 동계 연수 중이고 하계에 이어 이번에 두 번째로 비상교육 현장실습에 참여하셨어요🍉\n\n 지난 연수 때 업무 능력이 얼마나 좋으셨던 건지!💫 이번 동계 연수에서도 시작부터 국어셀 내에서 능력자로 소문이 자자했답니다! 연수 기간 내내 같은 국어셀 연수생들에게 길잡이가 되어 주셨어요🦄💖",
        r"김태희|태희|태희cp|김태희 cp": "태희 CP님은 영어 3cell에서 동계 연수 중이에요.📚❄️",
        r"류은우|은우|은우cp|류은우 cp": "은우 CP님은 영어 2 cell에서 동계 연수 중이고 책임감 있는 영어 2 Cell의 든든한 존재입니다✨\n\n CP님들께서 도움을 필요로 하시는 곳에 적절한 도움과 역할을 수행할 줄 아는 해결사예요! 👏📈",
        r"문지영|지영|지영cp|문지영 cp": "지영 CP님은 영어 3cell에서 동계 연수 중이에요.📚❄️",
        r"박서연|서연|서연cp|박서연 cp": "서연 CP님은 영어 4 cell에서 동계 연수 중이고 귀여움과 다정함으로 모두를 사로잡는답니다.😄💖\n\n 귀여움 뒤에 성실함과 책임감까지 가득 지니고 있는 서연 CP님은 언제나 따뜻한 말과 행동 그리고 재치 있는 유머들로 분위기를 환하게 만들어 줍니다.✨",
        r"서예지|예지|예지cp|서예지 cp": "예지 CP님은 영어 3cell에서 동계 연수 중이에요.📚❄️",
        r"변서윤|서윤|서윤cp|변서윤 cp": "서윤 CP님은 에듀테크콘텐츠 2 cell에서 동계 연수 중이고 언제나 섬세하고 멋진 작업을 손끝에서 뽑아내는 능력자예요!✂️🎨\n\n 언제나 부드럽고 따뜻한 말투를 지니고 있는 서윤 CP님은 계속해서 대화를 이어가고 싶게 만드는 매력을 지니셨답니다 💖🌸",
        r"송혜빈|혜빈|혜빈cp|송혜빈 cp": "혜빈 CP님은 영어 3cell에서 동계 연수 중이에요.📚❄️",
        r"심예원|예원|예원cp|심예원 cp": "예원 CP님은 FC 콘텐츠 개발 2cell 차분함 속에 알잘딱깔센 능력을 장착한 FC의 황금막내!💫✨\n\n 조용하지만 할 일은 확실하게! 센스 넘치는 완벽한 업무 처리로 모두를 감탄하게 만드는 숨은 강자!💛🔥",
        r"유헤진|혜진|혜진cp|유혜진 cp": "혜지 CP님은 영어 3cell에서 동계 연수 중이에요.📚❄️",
        r"윤성은|성은|성은cp|윤성은 cp": "성은 CP님은 FC 콘텐츠 개발1cell에서 동계 연수 중이고\n\n 우월한 기럭지와 아름다운 분위기를 가진 존재! 🌟✨ 하지만 실제로는 귀엽고 똑 부러지는 똑순이! 🐥💡 반전 매력으로 모두를 사로잡는 센스쟁이입니다💖",
        r"윤지혜|지혜|지혜cp|윤지혜 cp": "지혜 CP님은 국어 2cell에서 동계 연수 중이고 국어셀의 귀염핑이랍니다🐻\n\n 요즘 유행하는 '-핑'이라는 말투를 자주 사용하시는데요,\n\n 그럴 때마다 아이로 돌아간 듯한 동심과 정겨움을 느끼게 해주신답니다  13층에서 항상 출근 시간 1등을 다투는 부지런쟁이로, \n\n가장 안쪽 자리에 제일 먼저 도착해 출근하는 연수생들을 반갑게 맞아주실 때마다 추웠던 마음까지 따뜻해져요🌷",
        r"이다원|다원|다원cp|이다원 cp": "다원 CP님은 영어 3cell에서 동계 연수 중이에요.📚❄️",
        r"이상훈|상훈|상훈cp|이상훈 cp": "상훈 CP님은 FC 콘텐츠 개발 3cell 과묵한 듯하지만, 속에는 꼼꼼함과 세심함이 가득한 완벽주의자!🧐✨\n\n 조용히 일처리를 착착 해내는 프로페셔널한 면모 속에, 가끔 던지는 한 마디가 의외로 웃음 포인트!🎯\n 알고 보면 매력 넘치는 과묵 boy! 💼🔥",
        r"이영빈|영빈|영빈cp|이영빈 cp": "영빈 CP님은 창의융합콘텐츠 Cell에서 동계 연수 중!❄️🎨 시각디자인과의 멋진 감각을 가진 창의력 넘치는 분입니다✨\n 뮤지컬과 야구에 대한 깊은 애정까지! ⚾🎭 감성+센스를 겸비한 다재다능한 CP님! 💡🔥",
        r"이지현|지현|지현cp|이지현 cp": "지현 CP님은 에듀테크콘텐츠 3cell에서 동계 연수 중! ❄️✨ 스케이트를 타고 여행을 즐기는 자유로운 영혼 ⛸️🌍 직접 대화를 나눠보지 못한 게 아쉬울 만큼, 분명 멋진 매력을 지닌 CP님! 💙",
        r"이혜지|혜지|혜지cp|이혜지 cp": "혜지 CP님은 앱서비스 Cell에서 동계 연수 중! 📱✍️ 다이어리 쓰기를 목표로 차곡차곡 기록을 남기는 감성러! 📝💕 SZA의 노래를 사랑하는 음악 감성까지! 🎶💫",
        r"임서진|서진|서진cp|임서진 cp": "서진 CP님은 FC 콘텐츠 개발3cell에서 동계 연수 중이에요.📘❄️",
        r"정지원|지원|지원cp|정지원 cp": "지원 CP님은 영어 1 cell에서 동계 연수 중이고 아침형 인간의 대표 주자입니다.💼\n 일찍 일어나는 ‘똑순이’ 지원 CP님은 언제나 일찍 사무실에 도착해 \n\n활기차게 하루를 시작하는 멋쟁이랍니다.🌅💪",
        r"정혜인|혜인|혜인cp|정혜인 cp": "혜인 CP님은 과학 3cell에서 동계 연수 중! 🔬📖 연극, 뮤지컬, 독서를 즐기는 깊이 있는 취향의 소유자! 🎭📚 그리고 제 마니또였다는 소중한 인연까지! 💝✨",
        r"조수빈|수빈|수빈cp|조수빈 cp": "수빈 CP님은 인사 Cell에서 근무 중이시며, 카리스마 넘치고 따뜻한 마음을 가진 멋진 분! ✨ 자주 뵙진 못했지만, 은근히 귀여운 면도 있어 친근감을 주는 매력적인 모습 💖 예의 바르고 세련된 모습 속에 숨은 귀여움까지! 😊",
        r"최진경|진경|진경cp|최진경 cp": "진경 CP님은 국어 1cell에서 동계 연수 중이고 특유의 따스함으로 주변에 있는 같은 연수생들의 업무에 큰 도움을 주신답니다🧡🌞\n\n  연수 막바지에 접어들며 연수생 프로젝트와 업무를 병행하기 어려웠을 텐데도 책임감 있게 매일 업무를 완료하고 가시는 집중력에 항상 놀라고 있어요😆\n\n 옆에 앉은 같은 국어셀 연수생들에게 든든한 버팀목이 되어 주시는 존재랍니다💙",
        r"함성주|성주|성주cp|함성주 cp": "성주 CP님은 국정교과서 Cell에서 동계 연수 중! ❄️📚 런닝과 헬스처럼 활동적인 취미는 물론, 독어와 같은 정적인 취미까지 섭렵한 다재다능한 CP님! 🏃‍♂️💪📖 몸과 마음 모두 건강하게 즐기는 멋진 인재! ✨",
        r"홍채연|채연|채연cp|홍채연 cp": "채연 CP님은 스마트러닝전략 2cell에서 동계 연수 중! ⚽🌍 해외 축구를 사랑하는 열정 가득한 축구팬! 🏆🔥 직접 이야기 나눠보지 못했지만, 분명 멋진 매력을 가진 CP님! 💙",
        r"팀원|조원": "3조 팀원 🐧: \n\n 1. FC 콘텐츠 개발: 김민지, 황다인\n\n 2. 국어 Cell: 윤예서\n\n 3. 사회 Cell: 조지훈\n\n 4. 영어 Cell: 김다영",
        r"영어3 Cell|영어3 Cell": "CP님들 안녕하세요 다영입니다 ☺️ \n이 키봇은 저희 팀 프로젝트의 일부인 챗봇으로, 저희 팀원들끼리 각자 셀 시피님들께 감사한 마음을 담아서 특별 명령어를 삽입해 편지를 적어 보자는 생각에서 준비한 이벤트입니다 ㅎㅎ\n 두 달이라는 시간 동안 CP님들과 함께하며 많은 것을\n 배우고 경험할 수 있었던 것에 대해 진심으로 감사했다는 말씀 키봇을 통해 재차 드리고 싶었어요.<br><br> &nbsp;그동안 잘 챙겨 주시고 가르침과 조언을 아끼지 않아 주셔서 두 달이라는 시간 동안 많은 성장을 할 수 있었습니다! \n CP님들과 함께했던 행복하고 소중했던 시간들 잊지 않고 꾸준히 성장해 나가도록 하겠습니다 ❤︎ 영어 3 Cell에서 근무할 수 있어 진심으로 행복했습니다 ㅎㅎ 함께할 수 있었던 식사 자리와 평소에도 틈틈이 해 주시던 격려들과 가르침들이 제게 너무 소중한 기억으로 남아서 평생 잊지 못 할 것 같아요. 🥺\n\n &nbsp;이번 겨울 CP님들 덕분에 행복했던 것만큼 CP님들께서도 앞으로 항상 행복한 일만 가득하셨으면 좋겠습니다 🥰 항상 건강하시고 진심으로 감사했습니다 ☺\n\n김다영 드림",
        r"FC콘텐츠개발3cell|fc콘텐츠개발3cell|FC콘텐츠개발 3cell": "&nbsp;안녕하세요! FC 콘텐츠 개발 3Cell 연수생 김민지입니다! 😊\n\n히히, 다름이 아니라 제가 미니 프로젝트 콘텐츠 중 하나로 챗봇을 구현했어요! (우와아아 ✨) 그래서 작은 이벤트처럼 감사의 마음을 전하고자 이렇게 메시지를 남깁니다! 💌\n\n &nbsp;비상에서의 두 달 동안 정말 많은 걸 배우고 성장할 수 있었던 시간이었어요. CP님들 덕분에 새로운 시작을 잘할 수 있었고, 좋은 기운을 많이 받아간 것 같아요. 🙌\n\n &nbsp;또, 새로운 업무를 맡을 때마다 친절하게 알려주셔서 빠르게 적응할 수 있었고, 그 모든 과정이 저에게 큰 힘이 되었습니다. 🥺 이번 겨울, CP님들과 함께한 시간이 정말 행복했고, 그 기억을 간직하며 앞으로도 계속 열심히 성장해 나가겠습니다! 💖\n\n &nbsp;CP님들께서도 항상 행복한 일만 가득하시길 바랄게요. 건강하시고, 진심으로 감사드립니다! 😘\n\n김민지 드림",
        r"국어5 Cell|국어 5 Cell|": "&nbsp;국어5 Cell CP님들, 안녕하세요! 이번 25년 동계 연수생 윤예서입니다 :) 비상에서의 두 달은 소중한 만큼이나 저에게는 너무 빨랐는데요, 연수를 마치며 감사한 마음을 담아 이렇게 짧은 글을 남기게 되었어요. 이 키봇은 연수생 프로젝트에서 저희 팀의 애정을 담아 만든 캐릭터를 활용한 챗봇이랍니다 ㅎㅎ!<br><br> &nbsp;연수 기간 동안 업무적으로 5셀에 함께하지 못해 아쉬운 마음이 있었는데, 시피님들께서 어느 연수생보다도 부족함 없이 챙겨주신 덕분에 좋은 기억들만 가득 채워가요! 진심으로 감사드리고, 또 제 첫 사회생활을 5셀에서 할 수 있어 영광이었습니다. 시피님들을 뵐 때마다 스스로 꾸준히 발전하는 사람이 되겠다는 다짐을 매일 같이 했어요. 이 마음 잊지 않고 성장해서 꼭 하계 때 더욱 발전한 연수생으로 다시 뵐 수 있도록 노력하겠습니다!!<br><br> &nbsp;짧은 글로 다하지 못할 만큼 마음 깊이 감사드려요.남은 2025년도 5셀 시피님들 모두 건강하고 행복하시길 제가 진심으로 바랄게요!<br> 시피님들 생각 많이 날 것 같아요 ㅠㅠ\n\n &nbsp;사랑하는 5셀, 안녕히 계세요 ❤️",
        r"책가도": "&nbsp;'책가도'는 전시 초입에 위치한 책가의 모델로, 책과 도자기, 향로, 꽃 등이 책장 안에 놓인 모습을 그린 조선시대 그림입니다. 🖼️<br><br> &nbsp;비상 라키비움은 책을 사랑했던 선조들의 마음을 담기 위해, 책가도의 형식을 차용해 전시 공간을 절제되고 모던한 책가도로 디자인되었습니다. ✨<br><br>&nbsp;비상교육의 책에 대한, 교과서에 대한 진정성과 전문성을, 책가도를 통해 확인해볼 수 있습니다. 📖",
        r"라키비움": "\n\n라키비움은 '도서관'(Library), '수장고'(Archives), '박물관'(Museum)의 합성어로, 통합적인 공간을 상징합니다. 🏛️\n\n 비상 라키비움은 한글과 함께 성장한 교과서의 역사, 그 교과서와 함께한 우리 문학 작품들을 총망라한 공간입니다. 📚",
        r"운영안내|운영시간|운영 안내|운영 시간": "\n\n⏰ 운영 시간: 09:00 ~ 18:00 (* 마감 1시간 전 입장 종료)\n\n 📅 휴관일 : 일요일, 공휴일 휴관❌\n\n 🍔 외부 음식 반입 금지 🚫\n\n📚 도서 대출 불가📖❌ \n\n 💰 이용료 :무료🎉" ,
        r"라키비움 진행 프로그램 및 이벤트|진행 프로그램|진행프로그램|테마|이벤트|행사": "📌현재프로그램\n\n2월 : 신학기 준비는 <비상>✨📚\n\n 📌지난프로그램\n\n 11월 : 농업인의 날, 부산국제아동도서전 내 그림책 작가 전시 📖\n\n  12월: 크리스마스🎅🎁\n\n 1월: 새해 맞이 운세, 덕담🍀 ",
        
    }
    
    for pattern, response in responses.items():
        if re.search(pattern, user_input.lower()):
            return response
    
    return "알 수 없는 명령입니다. 다시 입력해 주세요."

# 이전 대화 기록 출력
for msg in st.session_state['messages']:
    role_class = "user-message" if msg["role"] == "user" else "bot-message"
    st.markdown(f'<div class="chat-message {role_class}">{msg["text"]}</div>', unsafe_allow_html=True)

# 사용자 입력 폼
if user_input := st.chat_input("메시지를 입력하세요..."):
    st.session_state['messages'].append({"role": "user", "text": user_input})
    response = get_response(user_input)
    st.session_state['messages'].append({"role": "bot", "text": response})
    st.rerun()
