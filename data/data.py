class AccountData:
    """
    Dados de teste relacionados à criação de contas.
    Utilizado para validar campos obrigatórios, limites e comportamentos inválidos.
    """

    # Dados válidos para cadastro de conta
    VALID_ACCOUNT_NAME = "ContaTeste01"
    VALID_ACCOUNT_VALUE = "5000"

    # Nome contendo números (não permitido) – usado no TC04
    NAME_ONLY_LETTERS_ALLOWED = "Conta123"

    # Nome que excede o limite de 20 caracteres – usado no TC05
    VALUE_EXCEEDS_20CHARACTERS = "MinhaContaMuitoGrande123"

    # Valor inválido (não numérico) – usado no TC06
    INVALID_ACCOUNT_VALUE = "abc"

    # Campos vazios – usados nos cenários TC02 e TC03
    EMPTY_ACCOUNT_NAME = ""
    EMPTY_ACCOUNT_VALUE = ""

    # Valor com mais de 13 dígitos – usado no TC07
    VALUE_EXCEEDS_13CHARACTERS = "12345678901234"

    # Nome de conta duplicado – usado no TC08
    DUPLICATE_ACCOUNT_NAME_VALUE = "ContaDuplicada"


class IncomeExpenseData:
    """
    Dados de teste para criação, validação, edição e exclusão de incomes e expenses.
    Estrutura utilizada para garantir consistência das entradas durante a automação.
    """

    # Dados válidos para cadastro de income
    VALID_INCOME_PRICE = "1000"
    VALID_INCOME_TITLE = "Salário"
    VALID_INCOME_CATEGORY = "Trabalho"

    # Dados válidos para cadastro de expense
    VALID_EXPENSE_PRICE = "300"
    VALID_EXPENSE_TITLE = "Padaria"
    VALID_EXPENSE_CATEGORY = "Alimentação"

    # Campo de preço vazio (validar obrigatoriedade)
    EMPTY_PRICE = ""

    # Categoria inválida – contém números
    INVALID_CATEGORY_NUMBERS = "123Cat"

    # Título com mais de 20 caracteres – validar limite de caracteres
    TITLE_EXCEEDS_20_CHARS = "DespesaDeMercadoExtensaTeste"

    # Dados para lançamento com data futura (não permitido)
    FUTURE_DATE_TITLE = "TesteFuturo"
    FUTURE_DATE_CATEGORY = "Erro"
    FUTURE_DATE_PRICE = "400"

    # Dados para lançamento com data passada (permitido)
    PAST_DATE_TITLE = "DespesaPassada"
    PAST_DATE_CATEGORY = "Compras"
    PAST_DATE_PRICE = "200"

    # Dados para teste de edição de income
    INCOME_EDIT_OLD_TITLE = "Extra"
    INCOME_EDIT_OLD_PRICE = "800"
    INCOME_EDIT_OLD_CATEGORY = "Freelance"

    # Novo valor utilizado na edição de income
    INCOME_EDIT_NEW_PRICE = "1000"

    # Dados duplicados para validação de registros repetidos
    DUPLICATE_TITLE = "Duplicado"
    DUPLICATE_PRICE = "100"
    DUPLICATE_CATEGORY = "Teste"


class RecordData:
    """
    Dados para validação de registros exibidos na tela de Records (extratos).
    Utilizado em cenários de verificação de exibição e exclusão.
    """

    VALID_RECORD_NAME = "Conta Teste"
    VALID_RECORD_VALUE = "000"
