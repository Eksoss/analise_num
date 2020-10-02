## Install venv and prep requirements

    - create venv

    python -m venv venv
    
    - activate
    
    Linux: source venv/Scripts/activate
    Windows: venv\Scripts\activate
    
    - install requirements
    
    pip install -r requirements.txt
    
## Using modules

  ### integration example

    - importing
    
    from src.integration import Simpson
    
    f = lambda x: -4 + 3*x + x**2
    F = Simpson(f)
    
    - integrating from a to b
    
    a, b = 0, 10
    integrated_value = F(a, b)
    
    - setting an especific n
    
    n = 1e8
    integrated_value = F(a, b, n)
    
