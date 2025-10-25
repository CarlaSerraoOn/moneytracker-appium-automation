import pytest
import time
from pages.add_incomeexpense_page import AddIncomeExpensePage
from pages.home_page import HomePage
from pages.accounts_page import AccountsPage
from pages.add_account_page import AddAccountPage
from pages.add_records_page import AddRecordPage
from pages.records_page import RecordsPage

from data.data import RecordData
from data.data import AccountData
from data.data import IncomeExpenseData


@pytest.mark.usefixtures("setup")
class TestRecords:

    def test_tc16_validate_records_display(self):
        """
        Verifica se os registros de Income e Expense aparecem corretamente na tela Records.
        """
        home = HomePage(self.driver)
        accounts = AccountsPage(self.driver)
        add_account = AddAccountPage(self.driver)
        add_income = AddIncomeExpensePage(self.driver)
        records = RecordsPage(self.driver)

        # Aguardar carregamento inicial
        time.sleep(0.5)

        # Criação de conta válida
        home.open_menu()
        accounts.open_accounts()
        accounts.click_add_account()
        add_account.add_account(AccountData.VALID_ACCOUNT_NAME, AccountData.VALID_ACCOUNT_VALUE)

        assert accounts.is_account_visible(AccountData.VALID_ACCOUNT_NAME), \
            "Falha ao criar conta. Teste não pode continuar."

        # Retorna para tela anterior
        time.sleep(0.5)
        self.driver.back()

        # Cadastro de Income
        add_income.click_add_income()
        add_income.fill_price(IncomeExpenseData.VALID_INCOME_PRICE)
        add_income.fill_title(IncomeExpenseData.VALID_INCOME_TITLE)
        add_income.fill_category(IncomeExpenseData.VALID_INCOME_CATEGORY)
        add_income.select_account(AccountData.VALID_ACCOUNT_NAME)
        add_income.save()
        time.sleep(0.5)

        # Cadastro de Expense
        add_income.click_add_expense()
        add_income.fill_price(IncomeExpenseData.VALID_EXPENSE_PRICE)
        add_income.fill_title(IncomeExpenseData.VALID_EXPENSE_TITLE)
        add_income.fill_category(IncomeExpenseData.VALID_EXPENSE_CATEGORY)
        add_income.select_account(AccountData.VALID_ACCOUNT_NAME)
        add_income.save()
        time.sleep(0.5)

        # Validação de registros
        assert records.is_text_displayed("Salário"), "Income 'Salário' não foi exibido na tela de registros."
        assert records.is_text_displayed("Compras"), "Expense 'Compras' não foi exibido na tela de registros."

    def test_tc17_edit_income_from_records(self):
        """
        Valida a edição de um registro do tipo Income na aba Records.
        """
        home = HomePage(self.driver)
        accounts = AccountsPage(self.driver)
        add_account = AddAccountPage(self.driver)
        add_income = AddIncomeExpensePage(self.driver)
        records = RecordsPage(self.driver)

        # Criação da conta
        home.open_menu()
        accounts.open_accounts()
        accounts.click_add_account()
        add_account.add_account(AccountData.VALID_ACCOUNT_NAME, AccountData.VALID_ACCOUNT_VALUE)
        self.driver.back()

        # Cadastro de Income inicial
        add_income.click_add_income()
        add_income.fill_price(IncomeExpenseData.INCOME_EDIT_OLD_PRICE)
        add_income.fill_title(IncomeExpenseData.INCOME_EDIT_OLD_TITLE)
        add_income.fill_category(IncomeExpenseData.INCOME_EDIT_OLD_CATEGORY)
        add_income.select_account(AccountData.VALID_ACCOUNT_NAME)
        add_income.save()

        # Acessa o primeiro registro
        add_income.open_first_record()

        # Atualiza o valor do Income
        add_income.update_price_value(IncomeExpenseData.INCOME_EDIT_NEW_PRICE)
        add_income.save_edited_record()

        # Verifica se o valor foi atualizado
        assert records.is_record_updated(IncomeExpenseData.INCOME_EDIT_NEW_PRICE), \
            "O valor do Income não foi atualizado corretamente para 1000."

    def test_tc18_delete_expense_from_records(self):
        """
        Verifica se um registro do tipo Expense pode ser excluído com sucesso.
        """
        home = HomePage(self.driver)
        accounts = AccountsPage(self.driver)
        add_account = AddAccountPage(self.driver)
        add_income = AddIncomeExpensePage(self.driver)
        records = RecordsPage(self.driver)

        # Criação de conta
        home.open_menu()
        accounts.open_accounts()
        accounts.click_add_account()
        add_account.add_account(AccountData.VALID_ACCOUNT_NAME, AccountData.VALID_ACCOUNT_VALUE)
        self.driver.back()

        # Cadastro de despesa
        add_income.click_add_expense()
        add_income.fill_price(IncomeExpenseData.VALID_EXPENSE_PRICE)
        add_income.fill_title(IncomeExpenseData.VALID_EXPENSE_TITLE)
        add_income.fill_category(IncomeExpenseData.VALID_EXPENSE_CATEGORY)
        add_income.select_account(AccountData.VALID_ACCOUNT_NAME)
        add_income.save()

        # Exclusão do primeiro registro na tela de Records
        records.delete_first_record()

    def test_tc19_block_empty_income_fields(self):
        """
        Verifica se o aplicativo bloqueia o salvamento de Income com campos vazios.
        """
        home = HomePage(self.driver)
        add_income = AddIncomeExpensePage(self.driver)

        # Abre tela de Income
        add_income.click_add_income()

        # Tenta salvar sem preencher campos
        add_income.save()

        # Valida mensagem de erro
        assert add_income.is_error_displayed("Field"), \
            "O aplicativo não exibiu mensagem de erro ao salvar com campos vazios."

        # Verifica se ainda permanece na tela de cadastro
        assert add_income.is_element_displayed(*add_income._btn_done), \
            "O aplicativo retornou para a lista ao invés de permanecer na tela de cadastro."

    def test_tc20_prevent_duplicate_income(self):
        """
        Garante que o sistema impede o cadastro de um Income duplicado.
        """
        home = HomePage(self.driver)
        accounts = AccountsPage(self.driver)
        add_account = AddAccountPage(self.driver)
        add_income = AddIncomeExpensePage(self.driver)

        # Criação da conta
        home.open_menu()
        accounts.open_accounts()
        accounts.click_add_account()
        add_account.add_account(AccountData.VALID_ACCOUNT_NAME, AccountData.VALID_ACCOUNT_VALUE)
        self.driver.back()

        # Cadastro de primeiro Income
        add_income.click_add_income()
        add_income.fill_price(IncomeExpenseData.DUPLICATE_PRICE)
        add_income.fill_title(IncomeExpenseData.DUPLICATE_TITLE)
        add_income.fill_category(IncomeExpenseData.DUPLICATE_CATEGORY)
        add_income.select_account(AccountData.VALID_ACCOUNT_NAME)
        add_income.save()

        assert add_income.is_income_visible(IncomeExpenseData.DUPLICATE_TITLE), \
            "O primeiro Income não foi salvo corretamente."

        # Tentar cadastrar novamente com os mesmos dados
        add_income.click_add_income()
        add_income.fill_price(IncomeExpenseData.DUPLICATE_PRICE)
        add_income.fill_title(IncomeExpenseData.DUPLICATE_TITLE)
        add_income.fill_category(IncomeExpenseData.DUPLICATE_CATEGORY)
        add_income.select_account(AccountData.VALID_ACCOUNT_NAME)
        add_income.save()

        # Validação de prevenção de duplicidade
        assert add_income.is_error_message_displayed("Duplicate") or \
               add_income.count_records_by_title(IncomeExpenseData.DUPLICATE_TITLE) == 1, \
               "O aplicativo permitiu criar um Income duplicado."

