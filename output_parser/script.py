from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from typing import List
from dotenv import load_dotenv
load_dotenv()

class Suggestions(BaseModel):
    words: List[str] = Field(description="list of substitue words based on context")

    @validator('words')
    def not_start_with_number(cls, field):
        for item in field:
            if item[0].isnumeric():
                raise ValueError("The word can not start with numbers!")
        return field

parser = PydanticOutputParser(pydantic_object=Suggestions)


template = """
Offer a list of suggestions to substitue the specified target_word based the presented context.
{format_instructions}
target_word={target_word}
context={context}
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["target_word", "context"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

model_input = prompt.format_prompt(
			target_word="behaviour",
			context="The behaviour of the students in the classroom was disruptive and made it difficult for the teacher to conduct the lesson."
)

# Before executing the following code, make sure to have
# your OpenAI key saved in the “OPENAI_API_KEY” environment variable.
model = OpenAI(model_name='text-davinci-003', temperature=0.0)

output = model(model_input.to_string())

parser.parse(output)

parsed_output = parser.parse(output)

print(parsed_output)
