
# 画面に入力フォームを1つ用意し、入力フォームから送信したテキストをLangChainを使ってLLMにプロンプトとして渡し、回答結果が画面上に表示されるようにしてください。な
# ラジオボタンでLLMに振る舞わせる専門家の種類を選択できるようにし、Aを選択した場合はAの領域の専門家として、またBを選択した場合はBの領域の専門家としてLLMに振る舞わせるよう、選択値に応じてLLMに渡すプロンプトのシステムメッセージを変えてください。また用意する専門家の種類はご自身で考えてください。
# 「入力テキスト」と「ラジオボタンでの選択値」を引数として受け取り、LLMからの回答を戻り値として返す関数を定義し、利用してください。
# Webアプリの概要や操作方法をユーザーに明示するためのテキストを表示してください。

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
st.title("専門家アシスタントアプリ")
st.write("""
このアプリは、異なる専門家として振る舞うAIアシスタントです。
以下の入力フォームに質問を入力し、専門家の種類を選択してください。
AIが選択された専門家として回答します。
""")

def get_expert_response(user_input, expert_type):
    if expert_type == "医者":
        system_message = "あなたは優秀な医者です。患者の質問に対して専門的かつ丁寧に回答してください。"
    elif expert_type == "弁護士":
        system_message = "あなたは経験豊富な弁護士です。法律に関する質問に対して正確かつ分かりやすく回答してください。"
    elif expert_type == "エンジニア":
        system_message = "あなたは熟練したソフトウェアエンジニアです。技術的な質問に対して具体的かつ実用的に回答してください。"
    else:
        system_message = "あなたは知識豊富な専門家です。質問に対して適切に回答してください。"
    prompt = PromptTemplate(
        input_variables=["user_input"],
        template=f"{system_message}\n\n質問: {{user_input}}\n回答:"
    )
    llm = OpenAI(model_name="gpt-4o-mini", temperature=0.7, openai_api_key=OPENAI_API_KEY)
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(user_input=user_input)
    return response

user_input = st.text_area("質問を入力してください:")

expert_type = st.radio("専門家の種類を選択してください:", ("医者", "弁護士", "エンジニア"))

if st.button("送信"):
    if user_input:
        response = get_expert_response(user_input, expert_type)
        st.write("### 回答:")
        st.write(response)
    else:
        st.write("質問を入力してください。")        