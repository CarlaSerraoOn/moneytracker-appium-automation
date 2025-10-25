from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class AccountsPage(BasePage):
    """
    Página responsável por interações com a tela de contas (Accounts) do aplicativo.
    Contém métodos para navegação, criação e validação de contas.
    """

    # Localizador do menu "Accounts" no menu lateral
    _accounts_menu = (AppiumBy.XPATH, "//android.widget.CheckedTextView[@text='Accounts']")

    # Localizador do botão "Add Account" na parte inferior da tela (layout antigo)
    _add_account_button = (
        AppiumBy.XPATH,
        "//android.widget.Button[@resource-id='com.blogspot.e_kanivets.moneytracker:id/btn_add_account']"
    )

    # Localizador do botão "Add Account" na parte superior da tela (versões mais recentes do app)
    _add_account_button_top = (
        AppiumBy.XPATH,
        "//android.widget.ImageButton[@resource-id='com.blogspot.e_kanivets.moneytracker:id/fab_add_account']"
    )

    def open_accounts(self):
        """
        Abre a tela de contas a partir do menu lateral.
        """
        self.click(*self._accounts_menu)

    def click_add_account(self):
        """
        Clica no botão para adicionar uma nova conta.
        O método tenta primeiro o botão superior (mais recente). 
        Caso não exista, utiliza o botão inferior (layout antigo).
        """
        try:
            self.click(*self._add_account_button_top)
        except Exception:
            self.click(*self._add_account_button)

    def is_account_visible(self, name):
        """
        Verifica se uma conta com determinado nome está visível na lista de contas.

        Parâmetros:
            name (str): Nome da conta a ser verificada.

        Retorno:
            bool: True se a conta estiver visível, False caso contrário.
        """
        xpath = f"//android.widget.TextView[@text='{name}']"
        return self.is_element_displayed(AppiumBy.XPATH, xpath)

    def count_accounts_with_name(self, name):
        """
        Conta a quantidade de contas exibidas com o nome especificado.
        Utilizado para validar duplicidade de contas.

        Parâmetros:
            name (str): Nome da conta a ser contado.

        Retorno:
            int: Número de contas encontradas com o nome informado.
        """
        xpath = f"//android.widget.TextView[@text='{name}']"
        return len(self.driver.find_elements(AppiumBy.XPATH, xpath))
