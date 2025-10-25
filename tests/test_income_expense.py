import pytest
import time
from data.data import AccountData, IncomeExpenseData
from pages.home_page import HomePage
from pages.accounts_page import AccountsPage
from pages.add_account_page import AddAccountPage
from pages.add_incomeexpense_page import AddIncomeExpensePage
from appium.webdriver.common.appiumby import AppiumBy

@pytest.mark.usefixtures("setup")
class TestIncomeExpense:
    """
    Classe de testes responsável pela validação das funcionalidades de registro de receitas (Income)
    e despesas (Expense) no aplicativo MoneyTracker.
    """

    def test_tc09_add_valid_income(self):
        """
        TC09 - Verifica se é possível adicionar um Income válido com todos os campos obrigatórios preenchidos.
        """
        home = HomePage(self.driver)
        accounts = AccountsPage(self.driver)
        add_account = AddAccountPage(self.driver)
        add_income = AddIncomeExpensePage(self.driver)

        # Criação de conta para vincular o Income
        home.open_menu()
        accounts.open_accounts()
        accounts.click_add_account()
        add_account.add_account(AccountData.VALID_ACCOUNT_NAME, AccountData.VALID_ACCOUNT_VALUE)

        assert accounts.is_account_visible(AccountData.VALID_ACCOUNT_NAME), \
            "Erro: Conta válida não foi criada para cadastro de Income."

        self.driver.back()

        # Abertura da tela de Income e preenchimento dos campos
        add_income.click_add_income()
        add_income.fill_price(IncomeExpenseData.VALID_INCOME_PRICE)
        add_income.fill_title(IncomeExpenseData.VALID_INCOME_TITLE)
        add_income.fill_category(IncomeExpenseData.VALID_INCOME_CATEGORY)
        add_income.select_account(AccountData.VALID_ACCOUNT_NAME)
        add_income.save()

        # Validação do registro
        assert add_income.is_income_visible(IncomeExpenseData.VALID_INCOME_TITLE), \
            "Erro: Income não foi exibido na lista de registros."

    def test_tc10_add_valid_expense(self):
        """
        TC10 - Verifica se é possível adicionar um Expense válido com todos os campos obrigatórios preenchidos.
        """
        home = HomePage(self.driver)
        accounts = AccountsPage(self.driver)
        add_account = AddAccountPage(self.driver)
        add_income = AddIncomeExpensePage(self.driver)

        # Criação de conta
        home.open_menu()
        accounts.open_accounts()
        accounts.click_add_account()
        add_account.add_account(AccountData.VALID_ACCOUNT_NAME, AccountData.VALID_ACCOUNT_VALUE)

        assert accounts.is_account_visible(AccountData.VALID_ACCOUNT_NAME), \
            "Conta não foi criada para adicionar Expense."

        self.driver.back()

        # Abertura da tela de Expense e preenchimento
        add_income.click_add_expense()
        time.sleep(0.5)
        add_income.fill_price(IncomeExpenseData.VALID_EXPENSE_PRICE)
        add_income.fill_title(IncomeExpenseData.VALID_EXPENSE_TITLE)
        add_income.fill_category(IncomeExpenseData.VALID_EXPENSE_CATEGORY)
        add_income.select_account(AccountData.VALID_ACCOUNT_NAME)
        add_income.save()

        assert add_income.is_income_visible(IncomeExpenseData.VALID_EXPENSE_TITLE), \
            "Expense não apareceu na lista de registros."

    def test_tc11_add_income_without_price(self):
        """
        TC11 - Valida que o aplicativo bloqueia o cadastro de Income sem o preenchimento do preço.
        """
        home = HomePage(self.driver)
        accounts = AccountsPage(self.driver)
        add_account = AddAccountPage(self.driver)
        add_income = AddIncomeExpensePage(self.driver)

        home.open_menu()
        accounts.open_accounts()
        accounts.click_add_account()
        add_account.add_account(AccountData.VALID_ACCOUNT_NAME, AccountData.VALID_ACCOUNT_VALUE)

        self.driver.back()

        add_income.click_add_income()
        time.sleep(0.5)

        add_income.fill_title(IncomeExpenseData.VALID_INCOME_TITLE)
        add_income.fill_category(IncomeExpenseData.VALID_INCOME_CATEGORY)
        add_income.select_account(AccountData.VALID_ACCOUNT_NAME)
        add_income.save()

        assert add_income.is_error_message_displayed("Field"), \
            "Erro: App permitiu salvar Income sem preencher o campo Price."

    def test_tc12_add_income_without_title(self):
        """
        TC12 - Verifica se o aplicativo permite indevidamente salvar um Income sem título.
        Caso o teste falhe, indica possível falha de validação no aplicativo.
        """
        home = HomePage(self.driver)
        accounts = AccountsPage(self.driver)
        add_account = AddAccountPage(self.driver)
        add_income = AddIncomeExpensePage(self.driver)

        home.open_menu()
        accounts.open_accounts()
        accounts.click_add_account()
        add_account.add_account(AccountData.VALID_ACCOUNT_NAME, AccountData.VALID_ACCOUNT_VALUE)

        self.driver.back()

        add_income.click_add_income()
        time.sleep(0.5)

        add_income.fill_price(IncomeExpenseData.VALID_INCOME_PRICE)
        add_income.fill_category(IncomeExpenseData.VALID_INCOME_CATEGORY)
        add_income.select_account(AccountData.VALID_ACCOUNT_NAME)
        add_income.save()

        error_present = add_income.is_error_message_displayed("Field")

        assert not error_present, \
            "BUG: O aplicativo deveria impedir salvar Income sem título, mas salvou com sucesso."

    def test_tc13_add_income_without_category(self):
        """
        TC13 - Garante que o sistema bloqueia o cadastro de um Income sem categoria definida.
        """
        home = HomePage(self.driver)
        accounts = AccountsPage(self.driver)
        add_account = AddAccountPage(self.driver)
        add_income = AddIncomeExpensePage(self.driver)

        home.open_menu()
        accounts.open_accounts()
        accounts.click_add_account()
        add_account.add_account(AccountData.VALID_ACCOUNT_NAME, AccountData.VALID_ACCOUNT_VALUE)
        self.driver.back()

        add_income.click_add_income()
        time.sleep(0.5)

        add_income.fill_price(IncomeExpenseData.VALID_INCOME_PRICE)
        add_income.fill_title(IncomeExpenseData.VALID_INCOME_TITLE)
        add_income.select_account(AccountData.VALID_ACCOUNT_NAME)
        add_income.save()

        assert add_income.is_error_message_displayed("Field"), \
            "Erro: O aplicativo permitiu salvar Income sem categoria."

    def test_tc14_add_income_with_different_date(self):
        """
        TC14 - Verifica se é possível adicionar um Income com data diferente da atual 
        e se ele aparece corretamente no filtro de período 'All time'.
        """
        home = HomePage(self.driver)
        accounts = AccountsPage(self.driver)
        add_account = AddAccountPage(self.driver)
        add_income = AddIncomeExpensePage(self.driver)

        home.open_menu()
        accounts.open_accounts()
        accounts.click_add_account()
        add_account.add_account(AccountData.VALID_ACCOUNT_NAME, AccountData.VALID_ACCOUNT_VALUE)
        self.driver.back()

        add_income.click_add_income()
        add_income.change_date("02", "October", "2025")
        add_income.fill_price(IncomeExpenseData.VALID_INCOME_PRICE)
        add_income.fill_title("Salário Outubro")
        add_income.fill_category(IncomeExpenseData.VALID_INCOME_CATEGORY)
        add_income.select_account(AccountData.VALID_ACCOUNT_NAME)
        add_income.save()

        home.select_all_time_filter()

        assert add_income.is_income_visible("Salário Outubro"), \
            "Income com data futura não apareceu no filtro 'All time'."

    def test_tc15_edit_existing_income(self):
        """
        TC15 - Verifica se um Income existente pode ser editado com sucesso, alterando 
        título e valor, e se os novos dados são refletidos na lista de registros.
        """
        home = HomePage(self.driver)
        accounts = AccountsPage(self.driver)
        add_account = AddAccountPage(self.driver)
        add_income = AddIncomeExpensePage(self.driver)

        # Criação de conta
        home.open_menu()
        accounts.open_accounts()
        accounts.click_add_account()
        add_account.add_account(AccountData.VALID_ACCOUNT_NAME, AccountData.VALID_ACCOUNT_VALUE)

        self.driver.back()

        # Cadastro de Income inicial
        add_income.click_add_income()
        add_income.fill_price(IncomeExpenseData.VALID_INCOME_PRICE)
        add_income.fill_title("Salário Antigo")
        add_income.fill_category(IncomeExpenseData.VALID_INCOME_CATEGORY)
        add_income.select_account(AccountData.VALID_ACCOUNT_NAME)
        add_income.save()

        home.select_all_time_filter()
        assert add_income.is_income_visible("Salário Antigo"), "Income inicial não foi localizado."

        # Edição do registro
        add_income.open_income_details("Salário Antigo")
        add_income.fill_title("Salário Editado")
        add_income.fill_price("2000")
        add_income.save()

        assert add_income.is_income_visible("Salário Editado"), \
            "Income não foi editado corretamente."
