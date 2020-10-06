## Install venv and prep requirements

    - create venv

    python -m venv venv
    
    - activate
    
    Linux: source venv/bin/activate
    Windows: venv\Scripts\activate
    
    - install requirements
    
    pip install -r requirements.txt
    
## Using modules

  ### integration example

    - importing
    
    from src.integration import Integrate
    
    f = lambda x: -4 + 3*x + x**2
    F = Integrate(f)
    
    - integrating from a to b
    
    a, b = 0, 10
    integrated_value = F(a, b)
    
    - setting an especific n
    
    n = 1e8
    integrated_value = F(a, b, n)

    - setting an especific method, default is simpson

    integrated_value = F(a, b, method='trapezoidal')
    integrated_value = F(a, b, method='midpoint')
    
