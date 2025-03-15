import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from io import StringIO
import sys
import traceback

def execute_code(code):
    """
    Execute the generated code in a Jupyter notebook environment.
    Returns the execution output.
    """
    # Create a new notebook
    nb = nbformat.v4.new_notebook()
    code_cell = nbformat.v4.new_code_cell(code)
    nb.cells.append(code_cell)

    # Create output capture
    output = StringIO()
    sys.stdout = output

    try:
        # Execute the notebook
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(nb)
        
        # Get the execution output
        execution_output = output.getvalue()
        return {
            'status': 'success',
            'output': execution_output
        }

    except Exception as e:
        error_trace = traceback.format_exc()
        return {
            'status': 'error',
            'error': str(e),
            'traceback': error_trace
        }

    finally:
        # Restore stdout
        sys.stdout = sys.__stdout__
