from chatsql import ChatSql

if __name__ == "__main__":
    csql = ChatSql('./conf.json', './info.json')
    print("Ask any question about the data. Enter 'q' to quit.")

    while True:
        prompt = input("Prompt:")
        if prompt.lower() == 'q':
            break
        query = csql.prompt_to_query(prompt)
        print("CHATGPT QUERY------------------:")
        print(query["query"])
        try:
            raw_result = csql.query_to_raw_result(query)
            print("RAW RESULT------------------: ")
            print(raw_result)
            print("PROCESSED RESULT------------------ :")
            processed_res = csql.raw_result_to_processed(prompt, raw_result)
            print(processed_res)
        except Exception as e:
            print(e)