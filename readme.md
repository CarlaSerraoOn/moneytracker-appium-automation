# 💰 MoneyTracker - Automação de Testes Mobile com Appium

Este projeto tem como objetivo automatizar os testes do aplicativo **MoneyTracker**, que realiza controle financeiro (Incomes & Expenses).  
A automação foi construída utilizando **Appium + Python + Pytest**, aplicando o padrão **Page Objects** para manter o código limpo, reutilizável e escalável.

---

## ✅ Objetivos do Projeto

✔️ Validar as principais funcionalidades do app MoneyTracker:  
- Cadastro de contas, receitas (Income) e despesas (Expense)  
- Edição e exclusão de registros  
- Validação de mensagens de erro  
- Bloqueio de dados inválidos ou vazios  
- Geração de relatórios (Records e Report)

✔️ Garantir qualidade com **automação mobile real** (Appium + Android Emulator)  
✔️ Organizar projeto com **Page Objects + Data Driven (classes Data)**  
✔️ Gerar **relatório HTML e cobertura de testes (pytest + pytest-html + Jacoco)**  

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia          | Versão             |
|---------------------|---------------------|
| **Python**          | 3.13.1              |
| **Appium Server**   | 3.1.0               |
| **Appium-Python**   | 3.x                 |
| **Emulador**        | Pixel 4 - Android 10 (Q) - API 33 |
| **Pytest**          | 8.x                 |
| **pytest-html**     | 4.x                 |
| **pytest-cov**      | 7.x                 |
| **Java / Gradle**   | Usado p/ gerar Jacoco Coverage |
| **MoneyTracker.apk**| App em teste (instrumented APK) |

---

## 📁 Estrutura do Projeto

📂 TrabalhoAppium-PageObjects

│

├── 📂 pages/ → Page Objects (Home, Accounts, AddIncomeExpense etc.)

├── 📂 data/ → Massa de dados (IncomeExpenseData, AccountData)

├── 📂 tests/ → Casos de testes (pytest)

├── 📂 reports/ → Relatórios HTML e Coverage

├── pytest.ini → Configurações gerais

├── requirements.txt → Bibliotecas do projeto

└── README.md → Este arquivo 💙



---

## 📱 Como Configurar o Ambiente

### 1️⃣ Instalar Dependências Python
```bash
pip install -r requirements.txt

2️⃣ Baixar o Appium Server

* npm install -g appium@3.1.0

3️⃣ Iniciar Appium

* appium

4️⃣ Criar e Iniciar Emulador Android (AVD)
Dispositivo: Pixel 4

Android: API 33 (Android Q / 10)

* emulator -avd Pixel_4_API_33

5️⃣ Instalar o APK do MoneyTracker no emulador:

* adb install caminho/para/app_moneytracker.apk

▶️ Como Executar os Testes
✅ Rodar todos os testes:
* pytest -s
✅ Gerar relatório HTML:

* pytest --html=reports/report.html --self-contained-html

✅ Rodar teste específico:

* pytest -k "test_tc17" -s

📊 Como Gerar Coverage (Cobertura de Testes)
✔️ Python (pytest-cov):

* pytest --cov=pages --cov-report=html
Resultado em: htmlcov/index.html

✔️ Java/Kotlin - Jacoco (no Android Studio):
mathematica

Gradle → Tasks → verification → jacocoFullReport
Arquivo gerado em:

* app/build/reports/jacoco/jacocoFullReport/html/index.html

✅ 6. Casos de Teste Implementados

ID	                Caso de Teste      	                         Resultado
TC01	       Abrir tela Accounts pelo menu 🚪	                      ✅
TC02	       Criar conta válida 💾	                              ✅
TC03	       Não criar conta com campos vazios ⚠️	                  ✅
TC04	       Impedir números no nome da conta 🔢	                  ❌
TC05	       Impedir mais de 20 caracteres no título ✂️	          ❌
TC06	       Salvar conta sem valor inicial	                      ✅
TC07	       Cancelar criação de conta	                          ✅
TC08	       Impedir contas duplicadas                              ❌	                
TC09	       Adicionar Income válido 💰	                          ✅
TC10	       Adicionar Expense válido 💸	                          ✅
TC11–TC13      Campos obrigatórios vazios (Price, Title, Category)   ✅
TC14	       Alterar data do Income 📆	                             ✅
TC15	       Editar Income existente ✏️	                           ✅
TC16	       Validar exibição em Records	                          ❌
TC17	       Editar Income direto na tela Records	                   ✅
TC18	       Excluir Expense pela tela Records 🗑️	                   ❌
TC19	       Bloquear Income com campos vazios	                    ✅
TC20	       Impedir duplicidade de Incomes	                        ✅
TC21	       Acessar tela Report e verificar totais 📊	            ❌


📌 7. Como este projeto se destaca?

✔ Estrutura Page Object Model (POM) bem organizada
✔ Testes data-driven com classes centralizadas em data/
✔ Valida não só resultados positivos, mas também erros, duplicidades e restrições de formulário
✔ Geração automática de relatório HTML + Coverage Jacoco
✔ Código pronto para CI/CD e reuso em grandes times

🎯 8. Autor

📌 Carla Oliveira
📧 carla.suporteam@gmail.com

💼 Portfólio: https://www.linkedin.com/in/carlaserraooli-qa/
