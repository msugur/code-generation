"""
ReAct Agent Implementation with Mistral API Integration

This demonstrates a ReAct (Reasoning and Acting) agent that combines
reasoning steps with tool execution to solve problems iteratively.
"""

import re
import json
import urllib.request
import urllib.error
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv

load_dotenv()


class StepType(Enum):
    THOUGHT = "thought"
    ACTION = "action"
    OBSERVATION = "observation"
    ANSWER = "answer"


@dataclass
class Step:
    type: StepType
    content: str


class Tool:
    """Base class for tools that the agent can use"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def execute(self, *args, **kwargs) -> str:
        raise NotImplementedError


class AddTodoTool(Tool):
    """Tool for adding a new todo item"""
    
    def __init__(self, api_url="http://localhost:5001"):
        super().__init__(
            name="add_todo",
            description="Add a new todo item. Input should be the title of the todo."
        )
        self.api_url = api_url
    
    def execute(self, title: str) -> str:
        try:
            url = f"{self.api_url}/todos"
            data = json.dumps({"title": title}).encode('utf-8')
            
            req = urllib.request.Request(url, data=data)
            req.add_header('Content-Type', 'application/json')
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                return f"Successfully added todo: '{result['title']}' with ID {result['id']}"
        except Exception as e:
            return f"Error adding todo: {str(e)}"


class DeleteTodoTool(Tool):
    """Tool for deleting a todo item"""
    
    def __init__(self, api_url="http://localhost:5001"):
        super().__init__(
            name="delete_todo",
            description="Delete a todo item. Input should be the ID of the todo to delete."
        )
        self.api_url = api_url
    
    def execute(self, todo_id: str) -> str:
        try:
            # First, try to get the todo to confirm it exists
            url = f"{self.api_url}/todos/{todo_id}"
            req = urllib.request.Request(url, method='DELETE')
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                return f"Successfully deleted todo with ID {todo_id}"
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return f"Todo with ID {todo_id} not found"
            return f"Error deleting todo: HTTP {e.code}"
        except Exception as e:
            return f"Error deleting todo: {str(e)}"


class ListTodosTool(Tool):
    """Tool for listing all todos"""
    
    def __init__(self, api_url="http://localhost:5001"):
        super().__init__(
            name="list_todos",
            description="List all todo items. No input required."
        )
        self.api_url = api_url
    
    def execute(self, query: str = "") -> str:
        try:
            url = f"{self.api_url}/todos"
            req = urllib.request.Request(url)
            
            with urllib.request.urlopen(req) as response:
                todos = json.loads(response.read().decode('utf-8'))
                
                if not todos:
                    return "No todos found. The list is empty."
                
                todo_list = []
                for todo in todos:
                    status = "✓" if todo.get('completed', False) else "○"
                    todo_list.append(f"{status} [{todo['id']}] {todo['title']}")
                
                return "Current todos:\n" + "\n".join(todo_list)
        except Exception as e:
            return f"Error listing todos: {str(e)}"


class MistralLLMClient:
    """Client for Mistral API (OpenAI compatible)"""
    
    def __init__(self):
        self.base_url = "https://mistral-llm.apps.cluster-gg696.gg696.sandbox3157.opentlc.com/v1"
        self.api_key = os.getenv("API_KEY", "")
        self.model = "mistral"
    
    def chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """Make a chat completion request to Mistral API"""
        url = f"{self.base_url}/chat/completions"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 500
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data)
        req.add_header('Content-Type', 'application/json')
        
        if self.api_key:
            req.add_header('Authorization', f'Bearer {self.api_key}')
        
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"]
                return ""
        except Exception as e:
            print(f"Error calling Mistral API: {e}")
            return ""


class ReActAgent:
    """
    ReAct Agent that combines reasoning (thought) with acting (tool use)
    to solve problems step by step.
    """
    
    def __init__(self, tools: List[Tool], llm_client=None, max_steps: int = 10, verbose: bool = True):
        self.tools = {tool.name: tool for tool in tools}
        self.llm_client = llm_client or MistralLLMClient()
        self.max_steps = max_steps
        self.verbose = verbose
        self.history: List[Step] = []
    
    def _get_tools_description(self) -> str:
        """Generate a description of available tools"""
        descriptions = []
        for tool in self.tools.values():
            descriptions.append(f"- {tool.name}: {tool.description}")
        return "\n".join(descriptions)
    
    def _parse_action(self, text: str) -> Optional[tuple[str, str]]:
        """Parse action from text in format: Action: tool_name[input]"""
        action_patterns = [
            r"Action:\s*(\w+)\[(.*?)\]",
            r"Action:\s*(\w+)\((.*?)\)",
            r"I'll use (\w+) with input: (.*)",
            r"Using (\w+): (.*)"
        ]
        
        for pattern in action_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).lower(), match.group(2).strip()
        return None
    
    def _execute_action(self, tool_name: str, tool_input: str) -> str:
        """Execute a tool and return the observation"""
        if tool_name in self.tools:
            return self.tools[tool_name].execute(tool_input)
        return f"Error: Tool '{tool_name}' not found"
    
    def _generate_prompt(self, question: str) -> str:
        """Generate prompt for the LLM"""
        context = self._create_context()
        
        prompt = f"""You are a ReAct agent that helps manage a todo list application.

Available tools:
{self._get_tools_description()}

To use a tool, format your response EXACTLY as:
Thought: [your reasoning about what to do next]
Action: tool_name[input]

After receiving an observation, think again and either use another tool or provide the final answer.

Question: {question}

{context}

What is your next thought and action? Remember to format as:
Thought: [reasoning]
Action: tool_name[input]
"""
        return prompt
    
    def _call_llm(self, question: str) -> str:
        """Call the LLM to generate the next step"""
        prompt = self._generate_prompt(question)
        
        messages = [
            {"role": "system", "content": "You are a helpful ReAct agent that manages todos."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm_client.chat_completion(messages)
        return response if response else self._fallback_response(question)
    
    def _fallback_response(self, question: str) -> str:
        """Fallback response when LLM is not available"""
        if "add" in question.lower():
            return "Thought: I need to add a new todo item.\nAction: add_todo[New todo item]"
        elif "delete" in question.lower() or "remove" in question.lower():
            return "Thought: I need to delete a todo item.\nAction: delete_todo[1]"
        elif "list" in question.lower() or "show" in question.lower():
            return "Thought: I need to list all todos.\nAction: list_todos[]"
        else:
            return "Thought: I'm not sure what to do with this request."
    
    def run(self, question: str) -> Dict[str, Any]:
        """
        Run the ReAct agent loop to answer a question.
        Returns a dictionary with the answer and history.
        """
        
        if self.verbose:
            print(f"Question: {question}")
            print("-" * 50)
        
        for step_num in range(self.max_steps):
            # Generate thought and action from LLM
            llm_response = self._call_llm(question)
            
            # Extract thought
            thought_match = re.search(r"Thought:\s*(.*?)(?=Action:|$)", llm_response, re.IGNORECASE | re.DOTALL)
            if thought_match:
                thought = thought_match.group(1).strip()
                self.history.append(Step(StepType.THOUGHT, thought))
                if self.verbose:
                    print(f"Thought {step_num + 1}: {thought}")
            
            # Parse and execute action
            action_parsed = self._parse_action(llm_response)
            
            if action_parsed:
                tool_name, tool_input = action_parsed
                action_str = f"{tool_name}[{tool_input}]"
                self.history.append(Step(StepType.ACTION, action_str))
                
                if self.verbose:
                    print(f"Action {step_num + 1}: {action_str}")
                
                # Execute tool and get observation
                observation = self._execute_action(tool_name, tool_input)
                self.history.append(Step(StepType.OBSERVATION, observation))
                
                if self.verbose:
                    print(f"Observation {step_num + 1}: {observation}")
                    print("-" * 30)
                
                # Check if task is complete
                if "successfully" in observation.lower() or step_num >= self.max_steps - 2:
                    answer = self._generate_answer(question)
                    self.history.append(Step(StepType.ANSWER, answer))
                    if self.verbose:
                        print(f"Answer: {answer}")
                    return {"answer": answer, "history": self.get_history_dict()}
            else:
                # No action found, generate final answer
                answer = self._generate_answer(question)
                self.history.append(Step(StepType.ANSWER, answer))
                if self.verbose:
                    print(f"Answer: {answer}")
                return {"answer": answer, "history": self.get_history_dict()}
        
        # Max steps reached
        answer = "I've reached the maximum number of steps. " + self._generate_answer(question)
        self.history.append(Step(StepType.ANSWER, answer))
        return {"answer": answer, "history": self.get_history_dict()}
    
    def _generate_answer(self, question: str) -> str:
        """Generate final answer based on the history"""
        observations = [step.content for step in self.history 
                       if step.type == StepType.OBSERVATION]
        
        if observations:
            last_observation = observations[-1]
            if "successfully" in last_observation.lower():
                return last_observation
            return f"Based on my actions: {last_observation}"
        
        return "I couldn't complete the requested task."
    
    def _create_context(self) -> str:
        """Create context from history for the next thought"""
        if not self.history:
            return ""
        
        context_parts = ["Previous steps:"]
        for step in self.history[-6:]:  # Last 6 steps for context
            context_parts.append(f"{step.type.value.capitalize()}: {step.content}")
        return "\n".join(context_parts)
    
    def get_history_dict(self) -> List[Dict[str, str]]:
        """Return the history as a list of dictionaries"""
        return [{"type": step.type.value, "content": step.content} for step in self.history]
    
    def reset(self):
        """Reset the agent's history"""
        self.history = []


def main():
    """Test the ReAct agent with todo operations"""
    
    # Initialize tools
    tools = [
        AddTodoTool(),
        DeleteTodoTool(),
        ListTodosTool()
    ]
    
    # Create agent with Mistral LLM
    agent = ReActAgent(tools, verbose=True)
    
    # Test queries
    queries = [
        "Show me all the todos",
        "Add a todo to buy groceries",
        "Delete todo with ID 1"
    ]
    
    for query in queries:
        print("\n" + "=" * 60)
        print(f"Processing: {query}")
        print("=" * 60)
        
        result = agent.run(query)
        
        # Reset for next query
        agent.reset()
        print("\n")


if __name__ == "__main__":
    main()