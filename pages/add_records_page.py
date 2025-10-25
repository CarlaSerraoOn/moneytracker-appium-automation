from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class AddRecordPage(BasePage):
    """
    Page Object responsável pelo cadastro de registros financeiros na aplicação,
    incluindo receitas (Income) e despesas (Expense).
    Esta classe segue o padrão POM (Page Object Model) e encapsula ações da tela 
    de inserção de registros.
    """

    # ---------------------- ELEMENTOS DA INTERFACE ----------------------

    # Campos de entrada de dados
    _price_input = (AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/et_price")
    _title_input = (AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/et_title")

    # Seletor de categorias
    _category_spinner = (AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/sp_category")

    # Botão para salvar o registro
    _save_button = (AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/fab_done")

    # ---------------------- MÉTODOS PRIVADOS ----------------------

    def _select_category(self, category_name):
        """
        Seleciona uma categoria no componente Spinner de categorias.

        :param category_name: Nome da categoria a ser selecionada.
        """
        self.click(*self._category_spinner)
        xpath = f"//android.widget.TextView[@text='{category_name}']"
        self.click(AppiumBy.XPATH, xpath)

    # ---------------------- AÇÕES PÚBLICAS ----------------------

    def add_income(self, price, title, category):
        """
        Adiciona um novo registro de receita (Income).

        :param price: Valor da receita.
        :param title: Título da receita.
        :param category: Categoria associada.
        """
        self.send_keys(*self._price_input, text=price)
        self.send_keys(*self._title_input, text=title)
        self._select_category(category)
        self.click(*self._save_button)

    def add_expense(self, price, title, category):
        """
        Adiciona um novo registro de despesa (Expense).

        :param price: Valor da despesa.
        :param title: Descrição da despesa.
        :param category: Categoria associada.
        """
        self.send_keys(*self._price_input, text=price)
        self.send_keys(*self._title_input, text=title)
        self._select_category(category)
        self.click(*self._save_button)
