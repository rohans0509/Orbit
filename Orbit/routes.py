class Route:
    def __init__(self, from_agent : str, to_agents : list, route_logic=None, agent_map=None):
        self.from_agent = from_agent
        self.to_agents = to_agents
        self.route_logic=route_logic
        self.agent_map=agent_map

    def run(self, state):
        assert self.agent_map
        if isinstance(self.route_logic, dict):
                output=state.get(self.agent_map[self.from_agent].output_key)
                next_agent = self.route_logic.get(output)
                return next_agent
        elif callable(self.route_logic):
            return self.route_logic(state)
        elif len(self.to_agents)==1:
            return self.to_agents[0]
        
        return None
    
    def __call__(self,state):
        return self.run(state)