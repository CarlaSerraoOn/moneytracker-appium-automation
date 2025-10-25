from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time

class BasePage:
    """
    Classe base para todas as páginas do projeto (Page Objects).
    Centraliza métodos de interação com elementos, espera explícita
    e tratamento de falhas comuns no UiAutomator2.
    """

    def __init__(self, driver):
        """
        Inicializa a classe com a instância do driver e define
        uma espera explícita padrão de 15 segundos.
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    # ---------------------- MÉTODOS GENÉRICOS DE INTERAÇÃO ----------------------

    def find(self, by, locator):
        """
        Localiza um elemento na tela utilizando espera explícita.
        Em caso de Timeout, realiza uma segunda tentativa.
        Em caso de falha no UiAutomator2, reinicia a sessão automaticamente.

        :param by: Estratégia de localização (ex.: AppiumBy.ID, AppiumBy.XPATH)
        :param locator: Caminho/localizador do elemento
        :return: WebElement localizado
        """
        try:
            return self.wait.until(EC.presence_of_element_located((by, locator)))
        except TimeoutException:
            # Realiza nova tentativa após breve espera
            time.sleep(1)
            return self.wait.until(EC.presence_of_element_located((by, locator)))
        except WebDriverException:
            # Tratamento de travamento do UiAutomator2
            print("UiAutomator2 não respondeu. Reiniciando sessão...")
            from conftest import restart_appium_session
            self.driver = restart_appium_session()
            self.wait = WebDriverWait(self.driver, 15)
            return self.wait.until(EC.presence_of_element_located((by, locator)))

    def click(self, by, locator):
        """
        Realiza clique em um elemento localizado na interface.
        """
        self.find(by, locator).click()

    def send_keys(self, by, locator, text):
        """
        Limpa um campo de entrada e insere texto.

        :param text: Valor a ser digitado no elemento
        """
        element = self.find(by, locator)
        element.clear()
        element.send_keys(text)

    def is_element_displayed(self, by, locator):
        """
        Verifica se determinado elemento está visível na tela.

        :return: True caso visível, False caso contrário
        """
        try:
            return self.find(by, locator).is_displayed()
        except Exception:
            return False

    def get_text(self, by, locator):
        """
        Retorna o texto de um elemento visível na tela,
        removendo espaços em branco no início e fim.

        :return: String com o texto capturado
        """
        return self.find(by, locator).text.strip()
