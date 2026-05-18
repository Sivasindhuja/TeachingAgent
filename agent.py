import os

import streamlit as st

from agents.professor_agent import ProfessorAgent
from agents.advisor_agent import AdvisorAgent
from agents.librarian_agent import LibrarianAgent
from agents.ta_agent import TeachingAssistantAgent

from utils.doc_generator import create_doc
from utils.logger import logger
from RAG.rag import ask_question


st.set_page_config(
    page_title="AI Teaching Agent Team",
    layout="wide"
)

st.title("👨‍🏫 AI Teaching Agent Team")

st.markdown("""
A collaborative AI teaching system where multiple AI agents work together like a professional teaching faculty.
""")


if "outputs" not in st.session_state:

    st.session_state.outputs = {}

if "messages" not in st.session_state:

    st.session_state.messages = []



def generate_learning_package(topic):

    try:

        logger.info(f"Generation started for topic: {topic}")

        # SAFE TOPIC NAME
        safe_topic = (
            topic.lower()
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        # TOPIC FOLDER
        topic_folder = os.path.join(
            "generated_docs",
            safe_topic
        )

        os.makedirs(topic_folder, exist_ok=True)

        # AGENTS
        professor_agent = ProfessorAgent()

        advisor_agent = AdvisorAgent()

        librarian_agent = LibrarianAgent()

        ta_agent = TeachingAssistantAgent()

        # GENERATE CONTENT
        professor_output = professor_agent.generate(topic)

        advisor_output = advisor_agent.generate(topic)

        librarian_output = librarian_agent.generate(topic)

        ta_output = ta_agent.generate(topic)

        # FILE PATHS
        professor_file = os.path.join(
            topic_folder,
            "knowledge_base.docx"
        )

        advisor_file = os.path.join(
            topic_folder,
            "roadmap.docx"
        )

        librarian_file = os.path.join(
            topic_folder,
            "resources.docx"
        )

        ta_file = os.path.join(
            topic_folder,
            "practice_workbook.docx"
        )

        # CREATE DOCS
        create_doc(
            f"{topic} Knowledge Base",
            professor_output,
            professor_file
        )

        create_doc(
            f"{topic} Learning Roadmap",
            advisor_output,
            advisor_file
        )

        create_doc(
            f"{topic} Resource Guide",
            librarian_output,
            librarian_file
        )

        create_doc(
            f"{topic} Practice Workbook",
            ta_output,
            ta_file
        )

        # SAVE OUTPUTS
        st.session_state.outputs = {
            "professor": professor_output,
            "advisor": advisor_output,
            "librarian": librarian_output,
            "ta": ta_output,
            "files": {
                "professor": professor_file,
                "advisor": advisor_file,
                "librarian": librarian_file,
                "ta": ta_file
            }
        }

        logger.info(f"Generation completed for topic: {topic}")

        return True

    except Exception as e:

        logger.error(f"Main Generation Error: {str(e)}")

        st.error(f"Error: {str(e)}")

        return False



# INPUT
topic = st.text_input(
    "Enter Topic",
    placeholder="Example: Machine Learning"
)


# GENERATE BUTTON
if st.button("Generate Learning Package"):

    if topic:

        with st.spinner("⏳ AI Agents are working..."):

            success = generate_learning_package(topic)

            if success:

                st.success("✅ Learning package generated!")



# SHOW OUTPUTS
if st.session_state.outputs:

    outputs = st.session_state.outputs

    tab1, tab2, tab3, tab4,tab5 = st.tabs([
        "Professor",
        "Advisor",
        "Librarian",
        "Teaching Assistant",
         "Ask Questions"
    ])

    with tab1:
        st.markdown(outputs["professor"])

    with tab2:
        st.markdown(outputs["advisor"])

    with tab3:
        st.markdown(outputs["librarian"])

    with tab4:
        st.markdown(outputs["ta"])
    
    with tab5:

        st.subheader("💬 Ask Questions")

    topics = []

    if os.path.exists("generated_docs"):

        topics = [
            folder
            for folder in os.listdir("generated_docs")
            if os.path.isdir(
                os.path.join(
                    "generated_docs",
                    folder
                )
            )
        ]

    if topics:

        rag_topic = st.selectbox(
            "Choose Topic",
            topics,
            key="rag_topic"
        )

        # DISPLAY CHAT HISTORY
        for message in st.session_state.messages:

            with st.chat_message(message["role"]):

                st.markdown(message["content"])

        # USER INPUT
        if prompt := st.chat_input(
            "Ask a question about this topic..."
        ):

            # USER MESSAGE
            st.chat_message("user").markdown(prompt)

            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })

            # ASSISTANT RESPONSE
            with st.chat_message("assistant"):

                message_placeholder = st.empty()

                message_placeholder.markdown(
                    "🔍 Searching documents..."
                )

                try:

                    answer, docs = ask_question(
                        prompt,
                        rag_topic
                    )

                    message_placeholder.markdown(
                        answer
                    )

                    # SOURCES
                    with st.expander(
                        "📚 View Sources"
                    ):

                        for i, doc in enumerate(docs):

                            source = os.path.basename(
                                doc.metadata.get(
                                    "source",
                                    "Unknown"
                                )
                            )

                            st.write(
                                f"### Source {i+1}: {source}"
                            )

                            st.caption(
                                doc.page_content[:1000]
                            )

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                except Exception as e:

                    st.error(f"RAG Error: {e}")

    else:

        st.info(
            "Generate documents first to use RAG."
        )

    st.divider()

    st.subheader("📥 Download Documents")

    files = outputs["files"]

    for key, filepath in files.items():

        with open(filepath, "rb") as f:

            st.download_button(
                f"Download {key}",
                data=f,
                file_name=os.path.basename(filepath)
            )



# SIDEBAR
with st.sidebar:

    st.header("📚 Generated Topics")

    os.makedirs("generated_docs", exist_ok=True)

    all_items = os.listdir("generated_docs")

    folders = []

    # ONLY KEEP FOLDERS
    for item in all_items:

        full_path = os.path.join(
            "generated_docs",
            item
        )

        if os.path.isdir(full_path):

            folders.append(item)

    if folders:

        selected_topic = st.selectbox(
            "Select Topic",
            folders
        )

        topic_path = os.path.join(
            "generated_docs",
            selected_topic
        )

        files = os.listdir(topic_path)

        st.subheader("Documents")

        for file in files:

            st.write(f"📄 {file}")

    else:

        st.info("No generated topics yet")