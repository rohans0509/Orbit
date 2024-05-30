import google.generativeai as genai

class Agent:
    def __init__(self, name, instructions, llm_model, input_keys, output_key):
        self.name = name
        self.instructions = instructions
        self.llm = genai.GenerativeModel(model_name=llm_model)
        self.input_keys = input_keys
        self.output_key = output_key
    
    def run(self, state):
        information = str(dict([(key,state[key]) for key in self.input_keys]))
        contents = [self.instructions] + [information]
        print(contents)
        result = self.llm.generate_content(contents=contents).text.strip()
        state[self.output_key] = result
        return state
    
    def __call__(self,state):
        return self.run(state)