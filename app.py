import streamlit as st
import sqlite3
from datetime import datetime
import pytz
from streamlit_mic_recorder import speech_to_text

# =================================
# PAGE CONFIG
# =================================

st.set_page_config(
    page_title="ESU Intelligent Student Assistant",
    page_icon="🎓",
    layout="wide"
)

# =================================
# DATABASE SETUP
# =================================

conn = sqlite3.connect("knowledge.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS knowledge (
    question TEXT UNIQUE,
    answer TEXT
)
""")

conn.commit()

# =================================
# PREMIUM CSS
# =================================

st.markdown("""
<style>

/* =========================================================
ESU INTELLIGENT STUDENT ASSISTANT
COMPLETE PREMIUM CSS
========================================================= */

/* =========================================================
GOOGLE FONT
========================================================= */

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html,
body,
[class*="css"] {

    font-family: 'Poppins', sans-serif;
}

/* =========================================================
REMOVE STREAMLIT DEFAULT BACKGROUND
========================================================= */

.stApp,
.main,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"] {

    background: transparent !important;
}

/* =========================================================
DARK THEME BACKGROUND
========================================================= */

html[data-theme="dark"] .stApp {

    background:
        linear-gradient(
            135deg,
            #020617 0%,
            #0F172A 45%,
            #1E293B 100%
        ) !important;
}

/* =========================================================
LIGHT THEME BACKGROUND
========================================================= */

html[data-theme="light"] .stApp {

    background:
        linear-gradient(
            135deg,
            #F8FAFC 0%,
            #EEF2FF 40%,
            #FFFFFF 100%
        ) !important;
}

/* =========================================================
FLOATING GLOW EFFECTS
========================================================= */

[data-testid="stAppViewContainer"]::before {

    content: "";

    position: fixed;

    top: -120px;

    left: -120px;

    width: 380px;

    height: 380px;

    background:
        radial-gradient(
            circle,
            rgba(59,130,246,0.18),
            transparent 70%
        );

    border-radius: 50%;

    filter: blur(60px);

    animation:
        floatGlow1 12s ease-in-out infinite alternate;

    pointer-events: none;

    z-index: 0;
}

[data-testid="stAppViewContainer"]::after {

    content: "";

    position: fixed;

    bottom: -120px;

    right: -120px;

    width: 420px;

    height: 420px;

    background:
        radial-gradient(
            circle,
            rgba(255,116,108,0.14),
            transparent 70%
        );

    border-radius: 50%;

    filter: blur(70px);

    animation:
        floatGlow2 14s ease-in-out infinite alternate;

    pointer-events: none;

    z-index: 0;
}

/* =========================================================
LIGHT THEME GLOW REDUCTION
========================================================= */

html[data-theme="light"]
[data-testid="stAppViewContainer"]::before,

html[data-theme="light"]
[data-testid="stAppViewContainer"]::after {

    opacity: 0.08;
}

/* =========================================================
GLOW ANIMATIONS
========================================================= */

@keyframes floatGlow1 {

    from {

        transform:
            translate(0px, 0px)
            scale(1);
    }

    to {

        transform:
            translate(50px, 60px)
            scale(1.08);
    }
}

@keyframes floatGlow2 {

    from {

        transform:
            translate(0px, 0px)
            scale(1);
    }

    to {

        transform:
            translate(-50px, -40px)
            scale(1.12);
    }
}

/* =========================================================
SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {

    backdrop-filter: blur(18px);

    -webkit-backdrop-filter: blur(18px);

    border-right:
        1px solid rgba(255,255,255,0.08);
}

/* DARK SIDEBAR */

html[data-theme="dark"]
section[data-testid="stSidebar"] {

    background:
        rgba(2,6,23,0.82) !important;
}

/* LIGHT SIDEBAR */

html[data-theme="light"]
section[data-testid="stSidebar"] {

    background:
        rgba(255,255,255,0.88) !important;

    border-right:
        1px solid rgba(15,23,42,0.06);
}

/* SIDEBAR TEXT */

html[data-theme="dark"]
section[data-testid="stSidebar"] * {

    color: #FFFFFF !important;
}

html[data-theme="light"]
section[data-testid="stSidebar"] * {

    color: #0F172A !important;
}

/* =========================================================
TITLE
========================================================= */

.main-title {

    font-size: 60px;

    font-weight: 800;

    color: #FF746C !important;

    text-shadow:
        0 0 10px rgba(255,116,108,0.40),
        0 0 22px rgba(255,116,108,0.22);

    animation:
        titleGlow 3s ease-in-out infinite alternate;
}

/* =========================================================
GREETING
========================================================= */

.greeting-text {

    font-size: 38px;

    font-weight: 700;
}

/* DARK GREETING */

html[data-theme="dark"] .greeting-text {

    color: #FFFFFF !important;

    text-shadow:
        0 0 10px rgba(255,255,255,0.18);
}

/* LIGHT GREETING */

html[data-theme="light"] .greeting-text {

    color: #0F172A !important;
}

/* =========================================================
SUBTITLE
========================================================= */

.subtitle-text {

    font-size: 18px;

    font-weight: 500;
}

/* DARK SUBTITLE */

html[data-theme="dark"] .subtitle-text {

    color: #F8FAFC !important;
}

/* LIGHT SUBTITLE */

html[data-theme="light"] .subtitle-text {

    color: #334155 !important;
}

/* =========================================================
TITLE ANIMATION
========================================================= */

@keyframes titleGlow {

    from {

        text-shadow:
            0 0 10px rgba(255,116,108,0.28);
    }

    to {

        text-shadow:
            0 0 20px rgba(255,116,108,0.55),
            0 0 40px rgba(255,116,108,0.28);
    }
}

/* =========================================================
USER MESSAGE
========================================================= */

.user-message {

    padding: 18px 22px;

    border-radius: 22px;

    margin-bottom: 16px;

    font-size: 17px;

    font-weight: 500;

    backdrop-filter: blur(18px);

    -webkit-backdrop-filter: blur(18px);

    transition: all 0.3s ease;
}

/* DARK USER MESSAGE */

html[data-theme="dark"] .user-message {

    background:
        linear-gradient(
            135deg,
            rgba(59,130,246,0.28),
            rgba(37,99,235,0.18)
        );

    border:
        1px solid rgba(255,255,255,0.08);

    color: #FFFFFF !important;

    box-shadow:
        0 8px 24px rgba(59,130,246,0.18);
}

/* LIGHT USER MESSAGE */

html[data-theme="light"] .user-message {

    background:
        linear-gradient(
            135deg,
            rgba(59,130,246,0.10),
            rgba(96,165,250,0.08)
        );

    border:
        1px solid rgba(15,23,42,0.06);

    color: #0F172A !important;

    box-shadow:
        0 4px 16px rgba(15,23,42,0.05);
}

/* =========================================================
BOT MESSAGE
========================================================= */

.bot-message {

    padding: 20px 24px;

    border-radius: 22px;

    margin-bottom: 16px;

    font-size: 17px;

    line-height: 1.7;

    border-left:
        4px solid #FF746C;

    backdrop-filter: blur(18px);

    -webkit-backdrop-filter: blur(18px);

    transition: all 0.3s ease;
}

/* DARK BOT MESSAGE */

html[data-theme="dark"] .bot-message {

    background:
        rgba(15,23,42,0.55);

    border:
        1px solid rgba(255,255,255,0.08);

    color: #FFFFFF !important;

    box-shadow:
        0 8px 24px rgba(0,0,0,0.22);
}

/* LIGHT BOT MESSAGE */

html[data-theme="light"] .bot-message {

    background:
        rgba(255,255,255,0.82);

    border:
        1px solid rgba(15,23,42,0.06);

    color: #0F172A !important;

    box-shadow:
        0 4px 16px rgba(15,23,42,0.05);
}

/* =========================================================
MESSAGE TEXT FIX
========================================================= */

.user-message *,
.bot-message * {

    color: inherit !important;
}

/* =========================================================
HOVER EFFECTS
========================================================= */

.user-message:hover,
.bot-message:hover {

    transform:
        translateY(-2px);

    box-shadow:
        0 12px 28px rgba(0,0,0,0.12);
}

/* =========================================================
BUTTONS
========================================================= */

.stButton button {

    width: 100%;

    border-radius: 16px;

    padding: 12px;

    font-weight: 600;

    transition: all 0.3s ease;

    backdrop-filter: blur(14px);

    -webkit-backdrop-filter: blur(14px);
}

/* DARK BUTTON */

html[data-theme="dark"] .stButton button {

    background:
        rgba(59,130,246,0.18) !important;

    border:
        1px solid rgba(255,255,255,0.08);

    color:
        #FFFFFF !important;

    box-shadow:
        0 8px 22px rgba(59,130,246,0.16);
}

/* LIGHT BUTTON */

html[data-theme="light"] .stButton button {

    background:
        rgba(255,255,255,0.82) !important;

    border:
        1px solid rgba(15,23,42,0.08);

    color:
        #0F172A !important;

    box-shadow:
        0 4px 16px rgba(15,23,42,0.05);
}

/* BUTTON HOVER */

.stButton button:hover {

    transform:
        translateY(-2px)
        scale(1.02);
}

/* =========================================================
CHAT INPUT
========================================================= */

.stChatInput input {

    border-radius: 18px !important;

    padding: 16px !important;

    backdrop-filter: blur(16px);

    -webkit-backdrop-filter: blur(16px);
}

/* DARK INPUT */

html[data-theme="dark"] .stChatInput input {

    background:
        rgba(255,255,255,0.08) !important;

    border:
        1px solid rgba(255,255,255,0.08) !important;

    color:
        #FFFFFF !important;
}

/* LIGHT INPUT */

html[data-theme="light"] .stChatInput input {

    background:
        rgba(255,255,255,0.96) !important;

    border:
        1px solid rgba(15,23,42,0.08) !important;

    color:
        #0F172A !important;
}

/* PLACEHOLDER */

html[data-theme="dark"] .stChatInput input::placeholder {

    color:
        rgba(255,255,255,0.65) !important;
}

html[data-theme="light"] .stChatInput input::placeholder {

    color:
        rgba(15,23,42,0.42) !important;
}

/* =========================================================
DETAILS / EXPANDERS
========================================================= */

details {

    border-radius: 16px;

    padding: 10px;
}

/* DARK DETAILS */

html[data-theme="dark"] details {

    background:
        rgba(255,255,255,0.04);

    border:
        1px solid rgba(255,255,255,0.06);
}

/* LIGHT DETAILS */

html[data-theme="light"] details {

    background:
        rgba(255,255,255,0.72);

    border:
        1px solid rgba(15,23,42,0.06);
}

/* =========================================================
MENU FIX
========================================================= */

div[role="menu"] {

    border-radius: 18px !important;

    backdrop-filter: blur(18px);

    -webkit-backdrop-filter: blur(18px);
}

/* DARK MENU */

html[data-theme="dark"] div[role="menu"] {

    background:
        rgba(15,23,42,0.94) !important;

    border:
        1px solid rgba(255,255,255,0.08);
}

/* LIGHT MENU */

html[data-theme="light"] div[role="menu"] {

    background:
        rgba(255,255,255,0.98) !important;

    border:
        1px solid rgba(15,23,42,0.08);
}

/* MENU TEXT */

html[data-theme="dark"] div[role="menu"] * {

    color:
        #FFFFFF !important;
}

html[data-theme="light"] div[role="menu"] * {

    color:
        #0F172A !important;
}

/* =========================================================
SCROLLBAR
========================================================= */

::-webkit-scrollbar {

    width: 8px;
}

::-webkit-scrollbar-thumb {

    background:
        #FF746C;

    border-radius: 10px;
}

/* =========================================================
SPACING
========================================================= */

.block-container {

    padding-top: 1rem !important;
}

</style>
""", unsafe_allow_html=True)

# =================================
# GREETING FUNCTION
# =================================

def get_greeting():

    sri_lanka = pytz.timezone("Asia/Colombo")

    current_time = datetime.now(sri_lanka)

    hour = current_time.hour

    if hour < 12:

        return "🌤️ Good Morning"

    elif hour < 18:

        return "☀️ Good Afternoon"

    else:

        return "🌙 Good Evening"
# =================================
# NLP PREPROCESSING
# =================================

def preprocess_text(text):

    text = text.lower()

    stop_words = [
        "what", "is", "the", "are",
        "do", "you", "can", "i",
        "a", "an", "of", "to"
    ]

    words = text.split()

    processed = []

    for word in words:

        if word not in stop_words:

            if word.endswith("s"):
                word = word[:-1]

            processed.append(word)

    return " ".join(processed)

# =================================
# SAVE KNOWLEDGE
# =================================

def save_new_knowledge(question, answer):

    try:

        cursor.execute(
            """
            INSERT OR IGNORE INTO knowledge
            (question, answer)
            VALUES (?, ?)
            """,
            (
                question.lower(),
                answer
            )
        )

        conn.commit()

    except Exception as e:

        print(e)

# =====================================================
# DEFAULT KNOWLEDGE BASE
# =====================================================

default_knowledge = [

    (
        "what course streams are available",
        "ESOFT offers Computing, Business & Law, Engineering, Hospitality, and Life Sciences pathways."
    ),

    (
        "what computing courses are available",
        "Computing programs include Software Engineering, Data Science, Cyber Security, and Networking."
    ),

    (
        "what business courses are available",
        "Business & Law programs include Business Management, Accounting & Finance, HRM, and Marketing."
    ),

    (
        "what engineering courses are available",
        "Engineering programs include Mechanical, Electrical, and Electronic Engineering."
    ),

    (
        "what hospitality courses are available",
        "Hospitality programs include Hospitality Management and Travel & Tourism Management."
    ),

    (
        "what life science courses are available",
        "Life Science programs include Biomedical Science and Biotechnology."
    ),

    (
        "how long does the software engineering course take",
        "The full pathway usually takes around 3 years including Foundation, HND, and Top-up Degree."
    ),

    (
        "what is the study pathway",
        "Most students follow a Foundation to HND to Top-up Degree pathway awarded by London Metropolitan University."
    ),

    (
        "how much are foundation course fees",
        "Foundation programs usually range from LKR 40,000 to LKR 75,000."
    ),

    (
        "how much are hnd fees",
        "Pearson BTEC HNDs usually include registration fees, semester fees, and Pearson UK registration fees."
    ),

    (
        "how much are british degree fees",
        "British Top-up Degrees usually include a university fee in GBP or USD and a local tuition fee."
    ),

    (
        "how much are short course fees",
        "Short courses such as English or IT certificates usually range from LKR 19,500 to LKR 25,000."
    ),

    (
        "are installment plans available",
        "Yes. Most programs offer monthly installment plans for students and parents."
    ),

    (
        "does esoft provide scholarships",
        "Yes. ESOFT provides LEAP Foundation Scholarships and government interest-free student loan opportunities."
    ),

    (
        "what is the leap scholarship",
        "LEAP Foundation Scholarships provide full or half scholarships through a pay-it-forward model after graduation."
    ),

    (
        "what is the government student loan",
        "ESOFT is approved under the Ministry of Education Interest-Free Student Loan Scheme."
    ),

    (
        "how much does the government loan cover",
        "The government loan can cover up to LKR 800,000 for 4-year degrees and LKR 600,000 for 3-year degrees."
    ),

    (
        "who is eligible for the government loan",
        "Students who passed A/Ls in recent years depending on the current intake cycle are usually eligible."
    ),

    (
        "what documents are needed for registration",
        "Students usually need NIC or Passport copies, O/L and A/L result sheets, passport photos, and the registration fee."
    ),

    (
        "how much is the registration fee",
        "Registration fees usually range between LKR 3,000 and LKR 5,000 depending on the course."
    ),

    (
        "can i register with pending results",
        "Yes. Foundation programs may allow registration with pending results."
    ),

    (
        "why choose esoft",
        "ESOFT offers globally recognized UK degrees, flexible study modes, installment plans, and a large branch network."
    ),

    (
        "are esoft degrees internationally recognized",
        "Yes. ESOFT degrees awarded by UK partners are globally recognized."
    ),

    (
        "can i migrate with an esoft degree",
        "Yes. UK partner degrees are useful for migration and postgraduate studies abroad."
    ),

    (
        "does esoft offer weekend classes",
        "Yes. ESOFT offers weekday, weekend, and online study modes."
    ),

    (
        "can working students study at esoft",
        "Yes. Flexible weekend and online learning options are available for working students."
    ),

    (
        "does esoft have branches outside colombo",
        "Yes. ESOFT has more than 40 branches across Sri Lanka including Trincomalee, Kandy, and many other cities."
    )

]

# =====================================================
# INSERT DEFAULT KNOWLEDGE INTO DATABASE
# =====================================================

for question, answer in default_knowledge:

    cursor.execute(
        "SELECT * FROM knowledge WHERE question=?",
        (question,)
    )

    existing = cursor.fetchone()

    if not existing:

        cursor.execute(
            """
            INSERT INTO knowledge (question, answer)
            VALUES (?, ?)
            """,
            (question.lower(), answer)
        )

conn.commit()


# =================================
# GET ANSWER
# =================================

from difflib import SequenceMatcher

def similarity(a, b):

    return SequenceMatcher(
        None,
        a.lower(),
        b.lower()
    ).ratio()

def get_answer(user_question):

    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    if user_question.lower().strip() in greetings:

        return (
            f"{get_greeting()}! 👋 "
            "How can I assist you with ESOFT Metro Campus today?"
        )

    cursor.execute(
        "SELECT question, answer FROM knowledge"
    )

    rows = cursor.fetchall()

    best_match = None
    best_score = 0

    for db_question, db_answer in rows:

        processed_user = preprocess_text(user_question)
        processed_db = preprocess_text(db_question)

        score = similarity(
            processed_user,
            processed_db
        )       

        if score > best_score:

            best_score = score
            best_match = db_answer

    # similarity threshold

    if best_score >= 0.25:

        return best_match

    return None

# =================================
# SESSION STATE
# =================================

if "messages" not in st.session_state:

    st.session_state.messages = [

    {
        "role": "bot",
        "content":
        f"{get_greeting()}! Welcome to the ESU Intelligent Student Assistant. How may I help you today?"
    }

]
    
if "unknown_question" not in st.session_state:

    st.session_state.unknown_question = None

# =================================
# SIDEBAR
# =================================

st.sidebar.title("🎓 ESU Assistant")

st.sidebar.write("""
This AI chatbot helps students and parents with:

- Degree Information
- HND Programmes
- Payment Plans
- Career Guidance
- UK Transfer Options
- Campus Information
- Lecture Schedules
""")

st.sidebar.markdown("---")

st.sidebar.subheader("📘 User Manual")

manual_topics = [

    "Degree Programmes",
    "HND Courses",
    "Payment Plans",
    "Internships & Careers",
    "UK Transfer Options",
    "Lecture Schedules",
    "Student Facilities",
    "Campus Information",
    "Awarding Body"
]

for topic in manual_topics:

    st.sidebar.write(f"✅ {topic}")

st.sidebar.markdown("---")



# =================================
# HEADER
# =================================

st.markdown(f"""
<h1 class="main-title">
🎓 ESU Intelligent Student Assistant
</h1>

<h3 class="greeting-text">
{get_greeting()}
</h3>

<p class="subtitle-text">
AI-Powered Educational Support Chatbot for Students & Parents
</p>
""", unsafe_allow_html=True)

# =================================
# LAYOUT
# =================================

left_col, center_col, right_col = st.columns([0.2, 3, 1])

# =================================
# SUPPORTED QUESTIONS
# =================================

with st.expander(
    "💡 Supported Questions",
    expanded=False
):

    try:

        cursor.execute(
            "SELECT DISTINCT question FROM knowledge"
        )

        all_questions = cursor.fetchall()

        if all_questions:

            for index, row in enumerate(all_questions):

                question = row[0]

                if st.button(
                    question,
                    key=f"supported_{index}_{question}"
                ):

                    st.session_state.messages.append(
                        {
                            "role": "user",
                            "content": question
                        }
                    )

                    answer = get_answer(question)

                    if answer:

                        st.session_state.messages.append(
                            {
                                "role": "bot",
                                "content": answer
                            }
                        )

                    else:

                        st.session_state.messages.append(
                            {
                                "role": "bot",
                                "content":
                                "I do not know the answer yet."
                            }
                        )

                    st.rerun()

        else:

            st.info(
                "No supported questions found."
            )

    except Exception as e:

        st.error(f"Database Error: {e}")

# =================================
# CHAT AREA
# =================================

with center_col:

    for message in st.session_state.messages:

        if message["role"] == "user":

            st.markdown(
                f"""
                <div class="user-message">
                🧑 {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="bot-message">
                🤖 {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

    voice_col, text_col = st.columns([1, 6])

    user_input = None

    with voice_col:

        spoken_text = speech_to_text(

            language='en',

            start_prompt="🎤",

            stop_prompt="⏹️",

            just_once=True,

            use_container_width=True,

            key='voice_input'
        )

        if spoken_text:

            user_input = spoken_text

            st.success(f"🗣️ You said: {spoken_text}")

    with text_col:

        typed_input = st.chat_input(
            "Type your question here..."
        )

        if typed_input:

            user_input = typed_input
    
# =================================
# CLEAR CHAT HISTORY BUTTON
# =================================

if st.button(
    "🗑️ Clear Chat History",
    key="clear_chat"
):

    st.session_state.messages = [

        {
            "role": "bot",
            "content":
            f"{get_greeting()}! Welcome to the ESU Intelligent Student Assistant. How may I help you today?"
        }

    ]

    st.rerun()

# =================================
# CHATBOT LOGIC
# =================================

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    answer = get_answer(user_input)

    if answer:

        st.session_state.messages.append(
            {
                "role": "bot",
                "content": answer
            }
        )

    else:

        st.session_state.messages.append(
            {
                "role": "bot",
                "content":
                "I do not know the answer yet. Please teach me below."
            }
        )

        st.session_state.unknown_question = user_input

    st.rerun()

# =================================
# TEACH CHATBOT
# =================================

if st.session_state.messages:

    last_message = (
        st.session_state.messages[-1]["content"]
    )

    # Show ONLY when chatbot doesn't know answer

    if "I do not know the answer yet" in last_message:

        st.markdown(
            "## 🧠 Teach the Chatbot"
        )

        new_answer = st.text_area(
            "Enter the correct answer:"
        )

        if st.button(
            "Save New Knowledge"
        ):

            question_to_save = (
                st.session_state.messages[-2]["content"]
            )

            cursor.execute(
                "INSERT INTO knowledge VALUES (?, ?)",
                (
                    question_to_save.lower(),
                    new_answer
                )
            )

            conn.commit()

            st.success(
                "✅ Knowledge saved successfully!"
            )

            st.rerun()