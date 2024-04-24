import streamlit as st
from langchain_community.llms import Ollama

ollama = Ollama(model="llama3")

def analyze_code(user_code):
    prompt = ("1 : Calculate the complexity of the code,2: Determine the code coverage of the code,"
              "3: Identify code duplication in the code,4: Find all the issues in the code" + 
              "Code : " + user_code + "Give the response in the same format 1. 2. 3. 4. only give text-based crisp and short answers for the given 4 prompts\nGive it in dictionary format in python. only generate {} part, no other sentences.\n")
    formatted_response = ollama.invoke(prompt)
    start_index = formatted_response.find("{")
    end_index = formatted_response.find("}")
    data_str = formatted_response[start_index + 1:end_index]
    pairs = data_str.split("\n")
    result = {}
    for pair in pairs:
        key, value = pair.split(": ", 1)
        result[int(key)] = value.strip('"')
    return result

def main():
    st.title("Code Analysis App")
    st.write("Enter your code below:")
    user_code = st.text_area("Code")
    if st.button("Analyze"):
        if user_code.strip() == "":
            st.warning("Please enter some code!")
        else:
            result = analyze_code(user_code)
            st.write("Analysis Results:")
            st.write(result)

if __name__ == "__main__":
    main()
