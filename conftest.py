import pytest
import subprocess
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import WebDriverException

# Nome do pacote do aplicativo sob teste
PACKAGE = "com.blogspot.e_kanivets.moneytracker"


def start_driver():
    """
    Inicializa uma nova sessão Appium com as capacidades desejadas.
    Define parâmetros de estabilidade e timeout para evitar falhas no UiAutomator2.
    """
    capabilities = {
        "platformName": "Android",
        "appium:deviceName": "emulator-5554",
        "appium:automationName": "UiAutomator2",
        "appium:appPackage": PACKAGE,
        "appium:appActivity": "com.blogspot.e_kanivets.moneytracker.activity.record.MainActivity",
        "appium:noReset": True,  # Mantém o app instalado, apenas limpa dados
        "appium:newCommandTimeout": 120000,  # Timeout estendido para evitar desconexões
        "appium:uiautomator2ServerInstallTimeout": 60000,  # Timeout para instalação do servidor UiAutomator2
        "appium:adbExecTimeout": 200000  # Timeout para comandos ADB
    }

    return webdriver.Remote(
        "http://127.0.0.1:4723",
        options=UiAutomator2Options().load_capabilities(capabilities)
    )


def is_uiautomator_running(driver):
    """
    Verifica se o processo UiAutomator2 ainda está em execução.
    Retorna True se o driver responder, False caso contrário.
    """
    try:
        _ = driver.current_activity
        return True
    except Exception:
        return False


def restart_appium_session():
    """
    Reinicia a sessão Appium/Uiautomator2 em caso de falha ou crash do servidor.
    Garante a retomada dos testes sem necessidade de reiniciar manualmente o Appium Server.
    """
    print("Reiniciando sessão Appium/Uiautomator2...")
    try:
        subprocess.run(f"adb shell am force-stop {PACKAGE}", shell=True)
    except Exception:
        pass

    # Recria a sessão Appium
    return start_driver()


@pytest.fixture(scope="function")
def setup(request):
    """
    Fixture de inicialização utilizada em todos os testes.
    - Limpa os dados do aplicativo antes de cada execução.
    - Concede permissões necessárias.
    - Inicia uma nova sessão Appium.
    - Finaliza o aplicativo ao término do teste.
    """
    print("\nLimpando cache e dados do aplicativo (sem desinstalar)...")
    subprocess.run(f"adb shell pm clear {PACKAGE}", shell=True)

    print("Concedendo permissões necessárias...")
    subprocess.run(f"adb shell pm grant {PACKAGE} android.permission.READ_EXTERNAL_STORAGE", shell=True)
    subprocess.run(f"adb shell pm grant {PACKAGE} android.permission.WRITE_EXTERNAL_STORAGE", shell=True)

    print("Iniciando sessão Appium...")
    driver = start_driver()
    request.cls.driver = driver

    yield  # Execução do teste ocorre aqui

    print("Encerrando aplicativo após o teste...")
    try:
        driver.terminate_app(PACKAGE)
    except Exception:
        pass


def pytest_runtest_setup(item):
    """
    Hook do pytest executado antes de cada caso de teste.
    Este método detecta se o UiAutomator2 crashou e, se necessário, recria a sessão Appium automaticamente.
    Evita falhas em cadeia nos testes subsequentes.
    """
    driver = getattr(item.cls, "driver", None)

    if driver and not is_uiautomator_running(driver):
        print("UiAutomator2 não está respondendo. Criando nova sessão Appium...")
        new_driver = restart_appium_session()
        item.cls.driver = new_driver
