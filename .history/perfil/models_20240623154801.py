from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .validators import valida_cpf
import re

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    idade = models.PositiveBigIntegerField()
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11)
    endereco = models.CharField(max_length=100)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=30)
    bairro = models.CharField(max_length=40)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=40)
    estado = models.CharField(
        max_length=2,
        default='SP',
        choices=(
            ('Ac', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('Ms', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    def __str__(self):  
       return f"Perfil de {self.user.username}"
    
    def clean(self):
        error_messages = {}
        
        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Digite um CPF válido'
            
        if re.search(r'[^0-9]', self.cpf) or len(self.cep) < 9:
            error_messages['cep'] = 'CEP inválido, digite 8 dígitos do CEP.'
            
        if error_messages:
            raise ValidationError(error_messages)
        
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
