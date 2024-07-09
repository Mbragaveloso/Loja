import re

def valida_cpf(cpf):
    # Lógica de validação do CPF aqui
    cpf = re.sub(r'\D', '', cpf)  # Remove caracteres não numéricos
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    # Mais validações conforme necessário
    return True

def valida_cep(cep):
    # Lógica de validação do CEP aqui
    if re.search(r'[^0-9]', cep) or len(cep) != 8:
        return False
    return True