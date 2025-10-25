from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class AddAccountPage(BasePage):
    # 📌 Elementos da tela
    _title_input = (AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/etTitle")
    _initial_sum_input = (AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/et_init_sum")
    _save_button = (AppiumBy.ID, "com.blogspot.e_kanivets.moneytracker:id/action_done")

    _error_message = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@resource-id='com.blogspot.e_kanivets.moneytracker:id/textinput_error']"
    )

    # ✅ Preenche os campos e clica em salvar
    def add_account(self, title, initial_sum):
        self.send_keys(*self._title_input, text=title)
        self.send_keys(*self._initial_sum_input, text=initial_sum)
        self.click(*self._save_button)

    # ✅ Retorna o texto da mensagem de erro, caso exista
    def get_error_message(self):
        try:
            return self.get_text(*self._error_message)
        except:
            return None

    # ✅ Verifica se a mensagem de erro contém o texto esperado
    def is_error_message_displayed(self, expected_text="Field"):
        error = self.get_error_message()
        return error is not None and expected_text.lower() in error.lower()
    
    def is_title_input_visible(self):
      try:
          return self.driver.find_element(*self._title_input).is_displayed()
      except:
          return False

    def click_add_account(self):
      try:
          self.click(*self._add_account_button_top)
      except Exception:
          self.wait_for_element(*self._add_account_button)  # aguardar visibilidade
          self.click(*self._add_account_button)