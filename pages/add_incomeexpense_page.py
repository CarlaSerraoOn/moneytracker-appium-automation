from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class AddIncomeExpensePage(BasePage):
    """
    Page Object Model (POM) responsável pelas operações de inclusão, edição e validação
    de receitas (Income) e despesas (Expense) na tela principal de registros do aplicativo.
    """

    # ---------------------- ELEMENTOS DE INTERFACE ----------------------

    # Botões para adicionar receita ou despesa
    _btn_add_income = (AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/btnAddIncome")
    _btn_add_expense = (AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/btnAddExpense")

    # Campos de entrada de dados
    _input_price = (AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/etPrice")
    _input_title = (AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/etTitle")
    _input_category = (AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/etCategory")

    # Seleção de conta vinculada ao registro
    _spinner_account = (AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/spinnerAccount")

    # Botão padrão para concluir (salvar ou editar)
    _btn_done = (AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/fabDone")

    # Elementos para edição de registros
    _record_first_item = (AppiumBy.XPATH,
        "//android.widget.LinearLayout[@resource-id='com.blogspot.e_kanivets.moneytracker:id/container']"
        "/android.widget.LinearLayout[1]")
    _price_edit_field = (AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/etPrice")
    _save_edit_button = (AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/fabDone")

    # ---------------------- AÇÕES PRINCIPAIS ----------------------

    def click_add_income(self):
        """Abre o formulário de cadastro de receita (Income)."""
        self.click(*self._btn_add_income)

    def click_add_expense(self):
        """Abre o formulário de cadastro de despesa (Expense)."""
        self.click(*self._btn_add_expense)

    def fill_price(self, price):
        """Insere o valor no campo 'Price' do formulário."""
        self.send_keys(*self._input_price, text=price)

    def fill_title(self, title):
        """Insere o título no campo 'Title' do formulário."""
        self.send_keys(*self._input_title, text=title)

    def fill_category(self, category):
        """Insere a categoria no campo 'Category' do formulário."""
        self.send_keys(*self._input_category, text=category)

    def select_account(self, account_name):
        """
        Seleciona a conta à qual a receita/despesa será vinculada.

        :param account_name: Nome da conta cadastrada anteriormente.
        """
        self.click(*self._spinner_account)
        xpath = f"//android.widget.TextView[@text='{account_name}']"
        self.click(AppiumBy.XPATH, xpath)

    def save(self):
        """Confirma e salva o registro de Income ou Expense."""
        self.click(*self._btn_done)

    # ---------------------- VALIDAÇÕES ----------------------

    def is_income_visible(self, title):
        """
        Verifica se um registro com o título informado está visível na lista.
        Usado tanto para receitas quanto para despesas.

        :param title: Título do registro.
        :return: True se o item estiver visível.
        """
        xpath = f"//android.widget.TextView[@text='{title}']"
        return self.is_element_displayed(AppiumBy.XPATH, xpath)

    def is_error_message_displayed(self, text):
        """
        Verifica a presença de uma mensagem de erro (por exemplo:
        campo obrigatório, valor inválido, etc.).

        :param text: Parte do texto esperado no erro.
        """
        xpath = ("//android.widget.TextView[@resource-id="
                 "'com.blogspot.e_kanivets.moneytracker:id/textinput_error' "
                 f"and contains(@text, '{text}')]")
        return self.is_element_displayed(AppiumBy.XPATH, xpath)

    # Alias para compatibilidade com testes que utilizam outro nome
    def is_error_displayed(self, text="Field"):
        xpath = f"//android.widget.TextView[contains(@text, '{text}')]"
        return self.is_element_displayed(AppiumBy.XPATH, xpath)

    # ---------------------- EDIÇÃO DE REGISTROS ----------------------

    def open_first_record(self):
        """Abre os detalhes do primeiro item listado na tela Records."""
        self.click(*self._record_first_item)

    def update_price_value(self, new_price):
        """Atualiza o valor do campo 'Price' em um registro já aberto."""
        element = self.find(*self._price_edit_field)
        element.clear()
        element.send_keys(new_price)

    def save_edited_record(self):
        """Confirma a edição do registro utilizando o botão de salvar."""
        self.click(*self._save_edit_button)

    # ---------------------- SUPORTE A DATAS ----------------------

    def change_date(self, day, month, year):
        """
        Altera a data do registro no formulário de criação.

        :param day: Dia desejado.
        :param month: Mês em formato textual (ex.: 'October').
        :param year: Ano desejado.
        """
        self.open_date_picker()
        self.select_date(day, month, year)
        self.confirm_date()

    def open_date_picker(self):
        """Abre o seletor de data."""
        self.click(AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/tvDate")

    # ---------------------- SUPORTE GERAL ----------------------

    def count_records_by_title(self, title):
        """Conta quantos registros possuem o mesmo título."""
        xpath = f"//android.widget.TextView[@text='{title}']"
        return len(self.driver.find_elements(AppiumBy.XPATH, xpath))

    def open_income_details(self, title):
        """Abre os detalhes de um registro específico pelo título."""
        xpath = f"//android.widget.TextView[@text='{title}']"
        self.click(AppiumBy.XPATH, xpath)

    def is_expense_visible(self, title):
        """
        Verifica se uma despesa com o título informado está presente.
        Este método reutiliza a lógica de 'is_income_visible'.
        """
        return self.is_income_visible(title)
