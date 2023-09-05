from langchain.chat_models import ChatOpenAI
import langchain
from langchain.memory import ChatMessageHistory
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.agents.agent_toolkits import (
    # create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo,
)
from typing import List
from langchain.tools import BaseTool
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain.agents.mrkl import prompt


langchain.verbose = True


# ドキュメントをベクトル化してVectorStoreに保存
def create_index() -> VectorStoreIndexWrapper:
    loader = DirectoryLoader('./files', glob="*.*")
    return VectorstoreIndexCreator().from_loaders([loader])


# indexを元にツールを作る関数
def create_tools(index: VectorStoreIndexWrapper) -> [BaseTool]:
    vectorstore_info = VectorStoreInfo(
        # VectoreStoreの情報
        name="udemy-langchain source code",
        description="Source code of application named udemy-langchain",
        vectorstore=index.vectorstore
    )
    # toolとはAgentが使えるアクションみたいなもの
    toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)
    return toolkit.get_tools()


def chat(message: str, history: ChatMessageHistory,
         index: VectorStoreIndexWrapper) -> str:
    llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)

    tools = create_tools(index)

    search = SerpAPIWrapper()
    tools.append(
        Tool.from_function(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events"
        )
    )

    memory = ConversationBufferMemory(
        chat_memory=history, memory_key="chat_history", return_messages=True
        )

    # agent_kwargs = {
    #     "suffix": """開始!ここからの会話は全て日本語で行われる。

    #     以前のチャット履歴
    #     {chat_history}

    #     新しいインプット: {input}
    #     {agent_scratchpad}""",
    # }

    agent_chain = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        agent_kwargs=dict(suffix='Answer should be in Japanese.' + prompt.SUFFIX)
        )

    # llm=llmとしないと別のモデルを使用してしまう
    return agent_chain.run(input=message)


#     return index.query(question=message, llm=llm)

    # # historyからメッセージ一覧を取り出す
    # messages = history.messages
    # # 最後にメッセージを追加
    # messages.append(HumanMessage(content=message))
