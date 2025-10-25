import pytest
from data.data import AccountData
from pages.home_page import HomePage
from pages.accounts_page import AccountsPage
from pages.add_account_page import AddAccountPage

@pytest.mark.usefixtures("setup")
class TestAddAccount:
    """
    Classe de testes responsável por validar os cenários relacionados
    ao cadastro de contas na aplicação MoneyTracker.
    """

    def test_tc01_add_account_success(self):
        """
        Cenário: Cadastro de conta com dados válidos.
        Resultado esperado: Conta deve ser exibida na lista após a criação.
        """
        home = HomePage(self.driver)
        accounts = AccountsPage(self.driver)
        add_page = AddAccountPage(self.driver)

        home.open_menu()
        accounts.open_accounts()
        accounts.click_add_account()
        add_page.add_account(AccountData.VALID_ACCOUNT_NAME, AccountData.VALID_ACCOUNT_VALUE)

        assert accounts.is_account_visible(AccountData.VALID_ACCOUNT_NAME), \
            "Conta válida não foi criada corretamente."

    def test_tc02_add_account_empty_title(self):
        """
        Cenário: Tentativa de cadastrar conta com campo 'Name' vazio.
        Resultado esperado: Aplicação deve exibir mensagem de erro.
        """
        home = HomePage(self.driver)
        accounts = AccountsPage(self.driver)
        add_page = AddAccountPage(self.driver)

        home.open_menu()
        accounts.open_accounts()
        accounts.click_add_account()
        add_page.add_account(AccountData.EMPTY_ACCOUNT_NAME, AccountData.VALID_ACCOUNT_VALUE)

        assert add_page.is_error_message_displayed("Field can't be empty"), \
            "Aplicação não exibiu mensagem de erro ao salvar conta sem título."

    def test_tc03_add_account_empty_value(self):
        """
        Cenário: Tentativa de cadastrar conta com campo 'Initial Sum' vazio.
        Resultado esperado: Aplicação deve exibir mensagem de erro.
        """
        home = HomePage(self.driver)
        accounts = AccountsPage(self.driver)
        add_page = AddAccountPage(self.driver)

        home.open_menu()
        accounts.open_accounts()
        accounts.click_add_account()
        add_page.add_account(AccountData.VALID_ACCOUNT_NAME, AccountData.EMPTY_ACCOUNT_VALUE)

        assert add_page.is_error_message_displayed("Field can't be empty"), \
            "Aplicação não exibiu erro ao tentar salvar conta com valor vazio."

    def test_tc04_add_account_title_with_numbers(self):
        """
        Cenário: Tentativa de cadastrar conta com nome contendo números.
        Resultado esperado: Aplicação deve exibir erro ou impedir a criação.
        """
        home = HomePage(self.driver)
        accounts = AccountsPage(self.driver)
        add_page = AddAccountPage(self.driver)

        home.open_menu()
        accounts.open_accounts()
        accounts.click_add_account()

        invalid_title = AccountData.NAME_ONLY_LETTERS_ALLOWED

        add_page.add_account(invalid_title, AccountData.VALID_ACCOUNT_VALUE)

        # Verificação se o erro foi exibido ou registro foi bloqueado
        if add_page.is_error_message_displayed("letters") or \
           add_page.is_error_message_displayed("invalid") or \
           add_page.is_error_message_displayed("only") or \
           add_page.is_error_message_displayed("Field"):
            return

        if not accounts.is_account_visible(invalid_title):
            return

        pytest.fail("Aplicação permitiu criação de conta com números no nome, violando as regras de validação.")

    def test_tc05_add_account_title_exceeds_20_chars(self):
        """
        Cenário: Tentativa de cadastrar conta com nome superior a 20 caracteres.
        Resultado esperado: Sistema deve exibir erro ou impedir o registro.
        """
        home = HomePage(self.driver)
        accounts = AccountsPage(self.driver)
        add_page = AddAccountPage(self.driver)

        home.open_menu()
        accounts.open_accounts()
        accounts.click_add_account()

        long_title = AccountData.VALUE_EXCEEDS_20CHARACTERS

        add_page.add_account(long_title, AccountData.VALID_ACCOUNT_VALUE)

        # Caso o sistema exiba mensagem de erro
        if add_page.is_error_message_displayed("Field") or \
           add_page.is_error_message_displayed("long") or \
           add_page.is_error_message_displayed("20"):
            return

        # Caso o sistema apenas não salve a conta
        if not accounts.is_account_visible(long_title):
            return

        pytest.fail("Aplicação permitiu salvar conta com título superior a 20 caracteres.")

    def test_tc06_add_account_initial_sum_with_letters(self):
        """
        Cenário: Inserção de letras no campo 'Initial Sum'.
        Resultado esperado: Sistema deve impedir o cadastro ou exibir erro.
        """
        home = HomePage(self.driver)
        accounts = AccountsPage(self.driver)
        add_page = AddAccountPage(self.driver)

        home.open_menu()
        accounts.open_accounts()
        accounts.click_add_account()
        add_page.add_account(AccountData.VALID_ACCOUNT_NAME, AccountData.INVALID_ACCOUNT_VALUE)

        assert add_page.is_error_message_displayed("Field") or \
               not accounts.is_account_visible(AccountData.VALID_ACCOUNT_NAME), \
               "Aplicação aceitou letras no campo 'Initial Sum'."

    def test_tc07_add_account_value_exceeds_13_digits(self):
        """
        Cenário: Inserção de valor superior a 13 dígitos no campo 'Initial Sum'.
        Resultado esperado: Aplicação deve exibir erro ou impedir a criação.
        """
        home = HomePage(self.driver)
        accounts = AccountsPage(self.driver)
        add_page = AddAccountPage(self.driver)

        home.open_menu()
        accounts.open_accounts()
        accounts.click_add_account()

        try:
            add_page.add_account(AccountData.VALID_ACCOUNT_NAME, AccountData.VALUE_EXCEEDS_13CHARACTERS)
        except Exception:
            pytest.fail("Aplicação apresentou erro inesperado ao inserir valor com mais de 13 dígitos.")

        if add_page.is_error_message_displayed("You can't be so rich or so poor"):
            return

        if not accounts.is_account_visible(AccountData.VALID_ACCOUNT_NAME):
            return

        pytest.fail("Aplicação permitiu salvar conta com valor superior a 13 dígitos.")

    def test_tc08_add_duplicate_account(self):
        """
        Cenário: Tentativa de cadastrar uma conta com nome já existente.
        Resultado esperado: Aplicação deve emitir alerta de duplicidade ou impedir o registro.
        """
        home = HomePage(self.driver)
        accounts = AccountsPage(self.driver)
        add_page = AddAccountPage(self.driver)

        # Primeira criação da conta
        home.open_menu()
        accounts.open_accounts()
        accounts.click_add_account()
        add_page.add_account(AccountData.DUPLICATE_ACCOUNT_NAME_VALUE, AccountData.VALID_ACCOUNT_VALUE)

        assert accounts.is_account_visible(AccountData.DUPLICATE_ACCOUNT_NAME_VALUE), \
            "Falha ao criar a primeira conta para teste de duplicidade."

        # Tentativa de criar conta duplicada
        accounts.click_add_account()
        add_page.add_account(AccountData.DUPLICATE_ACCOUNT_NAME_VALUE, AccountData.VALID_ACCOUNT_VALUE)

        if add_page.is_error_message_displayed("already") or add_page.is_error_message_displayed("exist"):
            return

        duplicate_count = accounts.count_accounts_with_name(AccountData.DUPLICATE_ACCOUNT_NAME_VALUE)
        if duplicate_count == 1:
            return

        pytest.fail(f"Aplicação permitiu criação de contas duplicadas. Quantidade encontrada: {duplicate_count}.")
