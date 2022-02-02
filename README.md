___
# TAXES BCB API
___
### Consumo de taxas, câmbio e produtos financeiros <br> direto do Banco Central do Brasil.

#### O Open Taxes é um software habilitado para nuvem, ligado por api ao Banco Central do Brasil, pronto para dispositivos móveis e desenvolvido em Python 3.9.7.

## Recursos
___
> Taxa da Selic do dia.
> Taxa do IPCA do dia.
> Dolar: Compra e Venda do dia.
> Euro: Compra e Venda do dia.


## Recursos em Desenvolvimento
___
> Taxa por data dia/mes/ano.
> Taxa por data mes/ano.
> Taxa por data ano.


## Instalação
___
Clone o repositpório

```sh
cd bcb-taxes-api
python3 bcb-taxes.py 
```

Para ambientes de produção...

```sh

```
## Uso
```py
Request: http://127.0.0.1:5000/api/v1/taxes/
```
```py
Response:
{
    "open_taxes": {
        "dolar": {
            "compra": "5.295",
            "venda": "5.2956"
        },
        "euro": {
            "compra": "5.9812",
            "venda": "5.984"
        },
        "ipca": "10.06",
        "selic": "9.25"
    }
}
```

```py
Request: http://127.0.0.1:5000/api/v1/taxes/selic/
```
```py
Response:
{
    "open_taxes": {
        "selic": "9.25"
    }
}
```
```py
http://127.0.0.1:5000/api/v1/taxes/dolar/compra/
```
```py
Response:
{
    "open_taxes": {
        "dolar": "5.295"
    }
}
```
## Dependências
___
São poucas, mas temos umas importantes:

| Dependência | Link |
| ------ | ------ |
| Dropbox | [plugins/dropbox/README.md][PlDb] |
| GitHub | [plugins/github/README.md][PlGh] |


## Licença
___
General Public License 3.0 (GPL 3.0)
Os fundamentos da GPL

> Ninguém deve ser restrito pelo software que eles usam. 
> **Existem quatro liberdades que todos os usuários devem ter:**

> 01 - a liberdade de usar o software para qualquer finalidade, 02 - a liberdade de mudar o software de acordo com suas necessidades, 03 - a liberdade de compartilhar o software com seus amigos e vizinhos e 04 - a liberdade de compartilhar as mudanças que você faz.

[https://www.gnu.org/licenses/quick-guide-gplv3.pt-br.html](https://www.gnu.org/licenses/quick-guide-gplv3.pt-br.html)

**Software Aberto, Hell Yeah!**
___
Isso é tudo! 
Bons Codes! #uhuuuuuuuu
___