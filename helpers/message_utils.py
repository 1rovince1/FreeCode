from langchain_core.messages import convert_to_openai_messages


def normalize_messages(messages: list):
    normalized_messages = convert_to_openai_messages(messages)
    return normalized_messages