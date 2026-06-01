from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

docs=[

Document(

page_content=

"Replay attack from emulator"

),

Document(

page_content=

"Low blink detected"

)

]

embed=HuggingFaceEmbeddings(

model_name=

"BAAI/bge-small-en-v1.5"
)

db=Chroma.from_documents(

docs,

embed,

persist_directory=

"./vector_db"
)