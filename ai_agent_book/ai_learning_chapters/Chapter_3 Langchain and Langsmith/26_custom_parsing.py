from langchain_core.output_parser import BaseOutputParser
from typing import Dict, Any

class KeyValueParser(BaseOutputParser[Dict[str, Any]]):

    def parse(self,text:str)->Dict[str, Any]:
        """Parse the string(text) into Dict[Key Value Pair"""
        parsed_dict= {}
        lines = text.strip().split('\n')
        for line in lines:
            if ':' in line:
                key, value = line.split(':',1)
                parsed_dict[key.strip()] = value.strip()
        return parsed_dict
    def get_format_instruction(self)->str:
        """Instruction for the LLM"""
        return "Your response must be a list of key-value pairs, with each pair on a new line. For example:\n\nName: John Doe\nAge: 30 "
    
## Custome chain
custom_parse = KeyValueParser()
# chain =  prompt_template_asking_for_kv | model | custom_parser 