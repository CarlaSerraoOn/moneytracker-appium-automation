from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class HomePage(BasePage):
    """
    Page Object responsável pelas interações com a tela inicial (Home) do aplicativo.
    Esta tela permite acesso ao menu lateral, à tela de registros (Records) e ao filtro de período.
    """

    # ---------------------- ELEMENTOS DA INTERFACE ----------------------

    # Botão para abrir o menu lateral (ícone tipo "hambúrguer")
    _menu_button = (
        AppiumBy.XPATH,
        "//android.widget.ImageButton[@content-desc='Open navigation drawer']"
    )

    # Item "Records" localizado dentro do menu lateral
    _records_button = (
        AppiumBy.XPATH,
        "//android.widget.CheckedTextView[@text='Records']"
    )

    # Spinner responsável por filtrar registros por período (Week, Month, All time)
    _spinner_filter = (
        AppiumBy.XPATH,
        '//android.widget.Spinner[@resource-id="com.blogspot.e_kanivets.moneytracker:id/spinner"]'
    )

    # Opção "All time" disponível no filtro de períodos
    _option_all_time = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@resource-id="android:id/text1" and @text="All time"]'
    )

    # ---------------------- AÇÕES ----------------------

    def open_menu(self):
        """
        Abre o menu lateral de navegação.
        Este método é utilizado como ação inicial para acessar outras telas.
        """
        self.click(*self._menu_button)

    def open_records(self):
        """
        Abre a tela 'Records' através do menu lateral.
        A chamada de open_menu() é feita para garantir que o menu está visível antes do clique.
        """
        self.open_menu()
        self.click(*self._records_button)

    def select_all_time_filter(self):
        """
        Seleciona a opção 'All time' no filtro de período exibido na parte superior da tela 'Records'.
        Esta ação é utilizada para garantir que todos os registros, independentemente da data,
        sejam exibidos na listagem.
        """
        self.click(*self._spinner_filter)
        self.click(*self._option_all_time)
