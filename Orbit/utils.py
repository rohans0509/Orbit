from importlib import import_module

def load_func(dotpath: str):
    """Load function in module. Function is the right-most segment."""
    module_, func = dotpath.rsplit(".", maxsplit=1)
    m = import_module(module_)
    return getattr(m, func)

def save_code(code :str, save_path="code_out.py"):
    code=code.replace("```","").replace("python","")
    # save
    with open(save_path, "w") as f:
        f.write(code)

    # run
    # exec(code)