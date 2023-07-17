from typing import Dict
import json
from langchain import PromptTemplate
from langchain.llms import OpenAI
from utils import read_json
from connect import SqlConnector


class ChatSql:
    def __init__(self, config: str, info: str) -> None:
        self.conf: Dict[str, str] = read_json(config)
        self.llm: object = OpenAI(openai_api_key=self.conf["open_ai_key"], model_name="gpt-3.5-turbo")
        self.info: str = read_json(info)
        self.db = SqlConnector(config)

    def prompt_to_query(self, prompt: str) -> Dict[str, str]:
        template = """
        Please convert SQL query from given {prompt}. Use following database information for this purpose (info key is a database table name and info value is list of columns). {info}
        Put your query in the  JSON structure with key name as 'query'. Add a limit of 5 for all results that query records.
        """
        pr = PromptTemplate(input_variables=["prompt", "info"], template=template)
        final_prompt = pr.format(
            prompt=prompt,
            info=self.info,
        )
        gpt_query: Dict[str, str] = json.loads(self.llm(final_prompt))
        return gpt_query

    def query_to_raw_result(self, gpt_query: Dict[str, str]) -> str:
        return self.db.execute(gpt_query['query'])

    def raw_result_to_processed(self, prompt: str, raw_result: str) -> str:
        template = """
        Please convert database result to meaningful sentences for this prompt: {prompt}. Here is the database result: {database_result}
        """
        pr = PromptTemplate(
            input_variables=["prompt", "database_result"], template=template
        )
        final_prompt = pr.format(prompt=prompt, database_result=raw_result)
        procesed_result: str = self.llm(final_prompt)
        return procesed_result


if __name__ == "__main__":
    csql = ChatSql('./conf.json', './info.json')
    prompt = "Return the film IDs, description, and rental rates of films with the minimum rental rates."
    query = csql.prompt_to_query(prompt)
    print("CHATGPT QUERY------------------:")
    print(query["query"])
    raw_result = csql.query_to_raw_result(query)
    print("RAW RESULT------------------: ")
    print(raw_result)
    print("PROCESSED RESULT------------------ :")
    processed_res = csql.raw_result_to_processed(prompt, raw_result)
    print(processed_res)