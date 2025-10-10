import pickle, requests, io, sys, textwrap
from contextlib import redirect_stdout
from IPython.display import display, HTML
from IPython import get_ipython

def _fetch_inouts(hw_num):
    url = f"https://github.com/litvinanna/intro_to_prog/raw/refs/heads/main/inouts/inouts{hw_num}.mp"
    resp = requests.get(url)
    resp.raise_for_status()
    return pickle.loads(resp.content)

def _get_student_code(solution_cell_index=None):
    ip = get_ipython()
    In = ip.user_ns.get("In", None)
    if In is None:
        raise RuntimeError("Cannot access In[] history. Must run inside Jupyter Notebook.")
    if solution_cell_index is None:
        source = In[-2]  # previous cell by default
    else:
        source = In[solution_cell_index]
    return source

def _make_assignments(vrs, test_input):
    """Generate variable assignment code for the current test."""
    if vrs is None or vrs.strip() in ("_", ""):
        return ""
    varnames = [v.strip() for v in vrs.split(",")]
    if test_input is None:
        return ""
    if len(varnames) == 1:
        return f"{varnames[0]} = {repr(test_input)}"
    else:
        try:
            it = list(test_input)
        except Exception:
            raise ValueError("Expected iterable for multiple variables")
        if len(it) != len(varnames):
            raise ValueError(f"Wrong number of test inputs for {vrs}: got {len(it)}")
        return "\n".join(f"{name} = {repr(value)}" for name, value in zip(varnames, it))


def checkit(hw_num, task_name, solution_cell_index=None):
    """Run all tests from inouts file against student's code using exec() and display styled HTML results."""
    # Load tests
    try:
        inouts = _fetch_inouts(hw_num)
    except Exception as e:
        display(HTML(f"<p style='color:red;'>Failed to load inouts file: {e}</p>"))
        return

    if task_name not in inouts:
        display(HTML(f"<p style='color:red;'>Task '{task_name}' not found in inouts{hw_num}.mp</p>"))
        return

    task_info = inouts[task_name]
    vrs = task_info.get("vrs", "_")
    tests = task_info.get("tests", [])
    if not tests:
        display(HTML(f"<p style='color:red;'>No tests found for {task_name}</p>"))
        return

    # Get student code
    try:
        student_code = _get_student_code(solution_cell_index)
    except Exception as e:
        display(HTML(f"<p style='color:red;'>Cannot read student code: {e}</p>"))
        return

    student_code = textwrap.dedent(student_code)
    total = len(tests)
    results_html = []

    for i, (test_input, expected) in enumerate(tests, start=1):
        try:
            assign_block = _make_assignments(vrs, test_input)
        except Exception as e:
            results_html.append(f"<p style='background-color:black; color:white; padding:6px; border-radius:6px;'>Test {i}/{total} failed. (Bad input: {e})</p>")
            continue

        # Prepare isolated namespace for this test
        ns = {}
        code_to_run = f"{assign_block}\n{student_code}"

        f = io.StringIO()
        try:
            with redirect_stdout(f):
                exec(code_to_run, ns)
        except Exception as e:
            results_html.append(
                f"<p style='background-color:black; color:white; padding:6px; border-radius:6px;'>Test {i}/{total} failed. (Error: {e})</p>"
            )
            continue

        output = f.getvalue().rstrip("\n")
        if output == expected:
            results_html.append(
                f"<p style='background-color:#96ead7; padding:6px; border-radius:6px; margin:2px 0;'>Test {i}/{total} passed.</p>"
            )
        else:
            results_html.append(
                f"<p style='background-color:black; color:white; padding:6px; border-radius:6px; margin:2px 0;'>Test {i}/{total} failed.</p>"
            )

    display(HTML("".join(results_html)))
