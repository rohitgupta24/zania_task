This program uses OpenAI API with LangChain. The program ingests the pdf files present in Docs Folder and creates embeddings which are saved in db_faiss folder.

Responses from the program are saved as "responses.json"

To run the Assistant, follow these steps :
1. pip install -r "requirements.txt"
2. Add OpenAI API key in the model.py file
2. In the Terminal : go inside "task" Folder and "run model.py"
3. All the generated answers get saved as "response.json"
