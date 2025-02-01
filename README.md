# Resume Evaluator
For any given resume, we first extract all the textual data from it using OCR and then pass the extracted text along with a prompt to a LLM. The LLM extracts the all the key data points define in the prompt and formats it to a nice JSON format. The project matches the skills extracted from the uploaded resume with the skills inputted by the user and shows a match percentage.


## Prerequisites
- Clone this GitHub project
- Create a python virtual environment and activate it (optional) \
  Steps: https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/
- Install all the required python packages: \
  `pip install -r requirements.txt`
- Install Tesseract for OCR: \
  Windows Executable: https://github.com/UB-Mannheim/tesseract/wiki
- Update the .env file with your OpenAI key and Tesseract installation path


## Steps to run the application
#### FastAPI backend
- Open a new terminal in the cloned project
- Run the following command: \
  `uvicorn main:app --reload`
- Keep this REST endpoint open in one terminal

#### Streamlit UI
- Open another new terminal inside the cloned project
- Run the following command: \
  `streamlit run streamlit.py`
- Open opening the localhost provided by this command, you should see the UI for our application


## Making modifications
#### Prompt
You can edit the prompt message written in `prompt.py` file. You can edit teh system prompt as well as the data points we have asked OpenAI to extract. I would suggest keeping the structure of the prompt similar to what I have shared for better results. Just update the data points you would like to extract.

#### Skills matching algorithm
The current implementation for skill matching algorithm might not be sufficient for a lot of people. The current algorithm only supports direct skill matching (user input skills and extracted skills in the pdf should exactly match). If you would like to introduce your own skills matching algorithm, you can simply do that by implementing `skill_interface.py`

#### Output
You may want your output to be structured differently or have some different fields from what is currently defined. You can go to `main.py` and inside the `upload_resume` function you can define the output json structure. You may also add any additional logic required to properly format or calculate the value.

#### UI
You can open `streamlit.py` and modify/add/remove any UI components easily using the streamlit package.
