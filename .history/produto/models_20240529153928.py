from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.conf import settings
import os
from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField(max_length=800)
    imagem = models.ImageField(upload_to='produto/imagens/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField(
        verbose_name='Preço',
        default=0.0,
        validators=[MaxValueValidator(99.00)],
    )
    preco_marketing_promocional = models.FloatField(
        verbose_name='Preço Promo.',
        validators=[MinValueValidator(0.01)],
    )
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples'),
        )
    )
    opcoes_tamanho = models.CharField(max_length=100, blank=True, null=True, help_text='Separadas por vírgula')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)
        if self.imagem:
            self.resize_image(self.imagem)
            
    def get_preco_formatado(self):
        return f'R$ {self.preco_marketing:.2f}'

    def get_preco_promocional_formatado(self):
        return f'R$ {self.preco_marketing_promocional:.2f}'

    def __str__(self):
        return self.nome

    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        if original_width <= new_width:
            img_pil.close()
            return

        new_height = round((new_width * original_height) / original_width)
        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )


class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco_marketing = models.FloatField(blank=True, null=True, verbose_name='Preço')
    preco_marketing_promocional = models.FloatField(blank=True, null=True, verbose_name='Preço de Marketing')
    estoque = models.PositiveIntegerField(default=1)
    descricao = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'

    def __str__(self):
        return self.nome if self.nome else f'Variação de {self.produto.nome}'

    def get_preco_formatado(self):
        return utils.formata_preco(self.produto.preco_marketing)
    get_preco_formatado.short_description = 'Preço'

    def get_preco_promocional_formatado(self):
        return utils.formata_preco(self.preco_marketing_promocional)
    get_preco_promocional_formatado.short_description = 'Preço Promo'
    

class Carrinho(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through='ItemCarrinho')
    ativo = models.BooleanField(default=True)

    objects = models.Manager()  # Não esquecer esse gerenciador 



class ItemCarrinho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, to='produto.Carrinho')
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, to='produto.Produto')
    quantidade = models.PositiveIntegerField(default=1)
    # Outros campos conforme necessário