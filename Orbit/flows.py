import yaml
import warnings
from .agents import Agent
from .routes import Route
from .utils import load_func
import os

COUNTER=0

class Flow:
    def __init__(self,name="MyGraph"):
        self.name=name
        self.agents = {}
        self.routes={}
        self.entry_point = None
        self.is_compiled=False

    def add_agent(self,agent):
        if self.is_compiled:
            raise ValueError(f"Flow Compiled")
        self.agents[agent.name] = agent
        
    def add_agents(self, agents):
        for agent in agents:
            self.add_agent(agent)

    def add_route(self, route):
        if self.is_compiled:
            raise ValueError(f"Flow Compiled")
        
        from_agent=route.from_agent

        if from_agent in self.routes:
            raise ValueError(f"Multiple routes found for same node currently not supporteed")
        self.routes[from_agent] = route

    def add_routes(self, routes):
        for route in routes:
            self.add_route(route)

    def set_entry_point(self, agent_name):
        if agent_name in self.agents:
            self.entry_point = agent_name
        else:
            raise ValueError(f"No agent found with the name {agent_name}")
        
    def compile(self):
        for agent, route in self.routes.items():
            route.agent_map=self.agents
            self.routes[agent]=route

        self.is_compiled=True

    def run(self, initial_state):
        if not self.is_compiled:
            raise ValueError("Flow not compiled")
        
        if not self.entry_point:
            raise ValueError("Entry point for the flow is not set.")
        
        current_agent_name = self.entry_point
        state = initial_state
        
        while current_agent_name:
            current_agent = self.agents[current_agent_name]
            state = current_agent(state)
            try:
                current_agent_name = self.routes[current_agent_name](state)

            except KeyError:
                print(f"Assuming we reached end at {current_agent_name}")
                break
        
        print("Final State after processing:")
        print(yaml.dump(state, sort_keys=True, default_flow_style=False))
        return state
    
    def save_flow(self, filename):
        flow_config = {
            "entry_point": self.entry_point,
            "agents": {name: self.serialize_agent(agent) for name, agent in self.agents.items()},
            "routes": {name: self.serialize_route(route) for name, route in self.routes.items()}
        }
        # check if folder not exist
          # Create directory if it does not exist
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(filename, 'w') as f:
            yaml.dump(flow_config, f)

    @classmethod
    def load_flow(cls, filename):
        flow = cls()

        with open(filename, 'r') as f:
            flow_config = yaml.safe_load(f)
        
        entry_point = flow_config.get("entry_point")
        agents_config = flow_config.get("agents", {})
        routes_config = flow_config.get("routes", {})
        
        agents = [cls.deserialize_agent(agent_config) for agent_config in agents_config.values()]
        routes = [cls.deserialize_route(route_config) for route_config in routes_config.values()]

        new_routes=[]

        for route in routes:
            if not type(route.route_logic)==dict:
                route.route_logic=load_func(route.route_logic)

            new_routes.append(route)
        
        flow.add_agents(agents)
        flow.add_routes(new_routes)
        flow.set_entry_point(entry_point)
        return flow

    @staticmethod
    def serialize_agent(agent):
        return {
            "name": agent.name,
            "instructions": agent.instructions,
            "llm_model": agent.llm.model_name,
            "output_key": agent.output_key,
            "input_keys": agent.input_keys
            }
    
    def serialize_route(self,route):
        route_logic=route.route_logic

        if callable(route_logic):
            if not route_logic.function_location:
                warnings.warn(f"Assuming route logic of {route} defined by {route_logic} is saved in route_functions.py")
                route_logic.function_location=f"route_functions.{route_logic.__name__}"
            return ({
                "from_agent": route.from_agent,
                "to_agents": route.to_agents,
                "route_logic": route.function_location
                })

        return ({
                "from_agent": route.from_agent,
                "to_agents": route.to_agents,
                "route_logic": route_logic
                })

    @staticmethod
    def deserialize_agent(data):
        return Agent(
            name=data["name"],
            llm_model=data["llm_model"],  # LLM needs to be set separately if required
            instructions=data["instructions"],
            output_key=data["output_key"],
            input_keys=data["input_keys"],
        )
    @staticmethod
    def deserialize_route(data):
        return Route(
            from_agent=data["from_agent"],
            to_agents=data["to_agents"],  # LLM needs to be set separately if required
            route_logic=data["route_logic"]
        )