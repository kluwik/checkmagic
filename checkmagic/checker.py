#!/usr/bin/env python
import io, contextlib, pickle, requests
from IPython.core.magic import register_cell_magic
from IPython.display import display, HTML

ANSWERS = {}

def magicCheckOn():
    @register_cell_magic
    def check(line, cell):
        """
        Usage:
        %%check hw_XX task_name
        <student code>
        """
        global ANSWERS

        # Parse line: expect "hw_03 task_3"
        parts = line.strip().split()
        if len(parts) != 2:
            display(HTML(f"<p style='background-color:red; color:white; padding:6px;'>"
                         f"Usage: %%check hw_XX task_name</p>"))
            return

        hw, task = parts
        if not hw.startswith("hw_") or not hw[3:].isdigit():
            display(HTML(f"<p style='background-color:red; color:white; padding:6px;'>"
                         f"Invalid homework format '{hw}'. Use hw_XX.</p>"))
            return

        hw_num = hw[3:]  # e.g., "03"

        # Load answers if not already loaded or if homework changed
        if hw not in ANSWERS:
            PICKLE_URL = f"https://github.com/litvinanna/intro_to_prog/raw/refs/heads/main/inouts{hw_num}.mp"
            try:
                response = requests.get(PICKLE_URL, headers={"User-Agent": "Python requests"})
                response.raise_for_status()
                ANSWERS[hw] = pickle.loads(response.content)
            except Exception as e:
                display(HTML(f"<p style='background-color:red; color:white; padding:6px;'>"
                             f"Failed to load tests for {hw}: {e}. Report to TAs.</p>"))
                return

        hw_answers = ANSWERS[hw]

        if task not in hw_answers:
            display(HTML(f"<p style='background-color:orange; padding:6px;'>Unknown task '{task}' in {hw}</p>"))
            return

        task_info = hw_answers[task]
        varnames = [v.strip() for v in task_info.get("vrs", "").split(",")] if task_info.get("vrs") else []
        tests = task_info.get("tests", [])

        results_html = ""
        total = len(tests)

        for i, (input_data, expected_output) in enumerate(tests, start=1):
            local_vars = {}

            # Assign variables
            if len(varnames) == 1:
                local_vars[varnames[0]] = input_data
            elif len(varnames) > 1:
                for name, value in zip(varnames, input_data):
                    local_vars[name] = value

            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    exec(cell, {}, local_vars)
                student_output = buf.getvalue().strip()
            except Exception as e:
                student_output = f"Error: {type(e).__name__}: {e}"

            passed = student_output == expected_output.strip()

            if passed:
                results_html += (
                    f"<p style='background-color:#96ead7; padding:6px; border-radius:6px; margin:2px 0;'>"
                    f"Test {i}/{total} passed</p>"
                )
            else:
                results_html += (
                    f"<p style='background-color:black; color:white; padding:6px; border-radius:6px; margin:2px 0;'>"
                    f"Test {i}/{total} failed</p>"
                )

        display(HTML(results_html))
