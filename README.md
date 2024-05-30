
# Orbit

A framework for creating, managing, and executing a chain of agents in a graph-like structure.

## Installation

You can install the library using pip:

```bash
pip install Orbit
```

## Usage

### Creating an Agent

```python
from Orbit import Agent

# Define an Agent
agent = Agent(name, instructions, llm_model, input_keys, output_key)
```

- `name`: Name of the agent.
- `instructions`: Prompt instructions for the agent.
- `llm_model`: Language model for the agent.
- `input_keys`: List of input keys.
- `output_key`: Output key.

### Defining Routes

```python
from Orbit import Route

# Define a Route
route = Route(from_agent, to_agents, route_logic=None)
```

- `from_agent`: Name of the source agent.
- `to_agents`: List of destination agent names.
- `route_logic`: Route logic.

### Creating the Flow

```python
from Orbit import Flow

# Define a Flow
flow = Flow(name="MyGraph")
```

- `name`: Name of the flow.

### Adding Agents and Routes

```python
# Add Agents to the Flow
flow.add_agent(agent)

# Add Routes to the Flow
flow.add_route(route)
```

### Setting Entry Point and Compilation

```python
# Set the entry point of the flow
flow.set_entry_point(agent_name)

# Compile the flow
flow.compile()
```

### Running the Flow

```python
# Define initial state
initial_state = {...}

# Run the flow
final_state = flow.run(initial_state)
```

### Saving and Loading the Flow

```python
# Save the flow configuration
flow.save_flow(filename)

# Load the flow configuration
loaded_flow = Flow.load_flow(filename)
```
