from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class RecordsPage(BasePage):
    """
    Page Object Model (POM) que representa a tela 'Records' do aplicativo.
    Contém os elementos, ações e validações relacionadas a registros de receitas e despesas.
    """

    # ---------------------- ELEMENTOS DA TELA ----------------------

    # Acesso ao menu "Records" no menu lateral
    _records_menu_item = (AppiumBy.XPATH, "//android.widget.CheckedTextView[@text='Records']")

    # Elementos da lista de registros (dinâmicos conforme título/valor)
    _record_title_xpath = "//android.widget.TextView[@text='{}']"
    _record_price_xpath = ("//android.widget.TextView[@resource-id="
                           "'com.blogspot.e_kanivets.moneytracker:id/tvPrice' and contains(@text,'{}')]")

    # Elementos ao abrir os detalhes de um registro
    _edit_button = (AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/ivEdit")
    _edit_price_field = (AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/etPrice")
    _save_edit_button = (AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/ivDone")

    # Elementos de exclusão
    _delete_button = (AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/action_delete")
    _confirm_delete_button = (AppiumBy.ID, "android:id/button1")  # Botão de confirmação "YES"

    # ---------------------- AÇÕES ----------------------

    def open_records(self):
        """
        Abre a tela de registros (Records) utilizando o menu lateral.
        """
        self.click(*self._records_menu_item)

    def open_record_by_title(self, title):
        """
        Abre os detalhes de um registro pelo texto do título.
        """
        self.click(AppiumBy.XPATH, self._record_title_xpath.format(title))

    def click_edit_button(self):
        """
        Acessa o modo de edição do registro atualmente aberto.
        """
        self.click(*self._edit_button)

    def update_price(self, new_price):
        """
        Substitui o valor do campo 'Price' durante a edição de um registro.

        :param new_price: novo valor a ser inserido
        """
        field = self.find(*self._edit_price_field)
        field.clear()
        field.send_keys(new_price)

    def save_edit(self):
        """
        Confirma e salva a edição do registro.
        """
        self.click(*self._save_edit_button)

    def delete_record(self, title):
        """
        Exclui um registro com base no título informado.

        :param title: nome do registro a ser excluído
        """
        self.open_record_by_title(title)
        self.click(*self._delete_button)
        self.click(*self._confirm_delete_button)

    def delete_first_record(self):
        """
        Abre o primeiro registro da lista e realiza a exclusão.
        """
        first_record = (
            AppiumBy.XPATH,
            "//android.widget.LinearLayout[@resource-id='com.blogspot.e_kanivets.moneytracker:id/container']"
            "/android.widget.LinearLayout[1]"
        )
        self.click(*first_record)

        delete_button = (
            AppiumBy.XPATH,
            "//android.widget.TextView[@content-desc='Delete']"
        )
        self.click(*delete_button)

    # ---------------------- VALIDAÇÕES ----------------------

    def is_record_visible(self, title, price=None):
        """
        Verifica se um registro está visível na lista.

        :param title: título do registro
        :param price: valor opcional para validação adicional
        :return: True se encontrado, False caso contrário
        """
        title_ok = self.is_element_present(AppiumBy.XPATH, self._record_title_xpath.format(title))
        if price:
            price_ok = self.is_element_present(AppiumBy.XPATH, self._record_price_xpath.format(price))
            return title_ok and price_ok
        return title_ok

    def is_record_updated(self, new_price):
        """
        Verifica se o preço de um registro foi atualizado com sucesso.

        :param new_price: valor atualizado exibido na tela
        :return: True se o valor atualizado for encontrado, False caso contrário
        """
        price_text = f"+ {new_price}"
        price_xpath = (
            f"//android.widget.TextView[@resource-id='com.blogspot.e_kanivets.moneytracker:id/tvPrice' "
            f"and @text='{price_text}']"
        )
        return self.is_element_displayed(AppiumBy.XPATH, price_xpath)

    def is_record_deleted(self, title):
        """
        Verifica se um registro com o título informado não está mais visível na lista.

        :param title: título do registro a ser verificado
        :return: True se o registro foi removido, False caso contrário
        """
        xpath = f"//android.widget.TextView[@text='{title}']"
        return not self.is_element_present(AppiumBy.XPATH, xpath)

    def is_text_displayed(self, text):
        """
        Verifica se um texto específico está visível na tela de registros.

        :param text: texto a ser verificado
        :return: True se visível, False caso contrário
        """
        try:
            xpath = f"//android.widget.TextView[@text='{text}']"
            return self.is_element_displayed(AppiumBy.XPATH, xpath)
        except Exception:
            return False
