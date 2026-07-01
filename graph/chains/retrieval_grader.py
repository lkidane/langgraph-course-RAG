# So after we've implemented the retrieve node, we're going to implement now the document grader node.

# So when we enter this node we have in our state the retrieve documents.

# So now we want to iterate over those documents and to determine whether they are indeed relevant to

# our question or not.

# So for that we're going to be writing a retrieval grader chain, which is going to use structured output

# from our LLM and turning it into a Pydantic object that will have the information whether this document

# is relevant or not.

# And if the document is not relevant, we want to filter it out and keep only the documents which are

# relevant to the question.

# And if not all documents are relevant.

# So this means that at least one document is not relevant to our query.

# Then we want to mark the web search flag to be true.

# So we'll go in later.

# Search for this term.


from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama


llm = ChatOllama(name="mymodel", temperature=0)



# A Pydantic model is a way to define structured data with validation in Python ✅
# Think of it as:

# 🧠 “A strict data schema that automatically checks and cleans data”


class GradeDocuments(BaseModel): #pydantic model
    """Binary score for relevance check on retrieved documents."""
    binary_score: str = Field(

    )

structured_llm_grader = llm.with_structured_output(GradeDocuments)

system = """ YOu are a grader assessing relevance of a retrieved document to answer a user question. \n
    If the document contains keyword(s) or semantic mearning related to the question, grade it as relevant.
    Give a binary score 'yes' or 'no' score to indcate whether the document is relevant to the question."""


# So now we want to use the chat from template from messages method.

# And here we're going to plug in the system message.

# And we're going to put here a human message.

# And we're going to put a placeholder for the fetched document.

# So this is supposed to be the document we want to figure out if it's relevant or not.

grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
)


# And finally let's create the chain.

# We'll call it Retrieval Grader.

# And it's going to take the great prompt.

# And it's going to pipe it into the LLM with the structured output.
retrieval_grader = grade_prompt | structured_llm_grader