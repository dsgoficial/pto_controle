# Rotinas de Pontos de Controle

## 📌 Definição

Repositório que contém um conjunto de ferramentas para a coleta de Pontos de Controle.

---

## 📖 Documentação e Guias de Aplicação

A documentação está acessível por meio da **EBNet**. Para mais informações, entre em contato com a **DGEO do 1° CGEO**.

---

## 📂 Estrutura de Pastas

### 📁 `arquivos`
Pasta que contém arquivos de exemplo para auxiliar na explicação da ferramenta aos operadores, é essencial manter o padrão de nomeclatura das pastas conforme o exemplo.

### 📁 `ferramentas_pto_controle`
Contém o plugin utilizado pelo usuário no **QGIS**.

### 📁 `rotinas_complementares_pto_controle`
Inclui scripts e rotinas utilizadas fora do **QGIS**, fazendo parte do processo de geração dos arquivos para o **Banco de Pontos de Controle**, complementando as rotinas contidas no plugin do **QGIS**.

---

## ⚙️ Procedimentos de Instalação

### 1️⃣ Criando o Ambiente Virtual

Recomenda-se criar um ambiente virtual chamado `pto_controle` para isolar as dependências do projeto. Execute os seguintes comandos:

```sh
python -m venv pto_controle
```

Para ativar o ambiente virtual:

- **Windows (CMD/Powershell):**
  
  ```sh
  pto_controle\Scripts\activate
  ```

- **Linux/macOS:**
  
  ```sh
  source pto_controle/bin/activate
  ```

---

### 2️⃣ Configuração das Variáveis de Ambiente

No **Windows**, adicione os seguintes caminhos à variável `PATH`, caso ainda não estejam configurados:

- Caminho do Python (exemplo):
  ```
  C:\Users\SeuUsuario\AppData\Local\Programs\Python\PythonXX
  ```
- Caminho do Scripts (exemplo):
  ```
  C:\Users\SeuUsuario\AppData\Local\Programs\Python\PythonXX\Scripts
  ```

No **Linux/macOS**, utilize o seguinte comando para adicionar o caminho do Python ao `PATH`:

```sh
echo 'export PATH="/caminho/do/python:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

---

### 3️⃣ Instalação das Dependências

Com o ambiente virtual ativado, instale as dependências do projeto executando:

```sh
pip install -r requirements.txt
```

Caso ocorra algum erro na instalação das dependências, tente as seguintes soluções:


1. Verifique a compatibilidade da versão do **Python** com as dependências.

2. Instale as dependências manualmente:
   
   ```sh
   pip install nome_do_pacote
   ```

Se persistirem problemas, consulte a documentação de cada dependência ou verifique a versão correta no `requirements.txt`.

---

### 4️⃣ Executando o Projeto da monografia

Com o ambiente virtual ativado e as dependências instaladas, você pode executar os scripts do projeto normalmente.

**Exemplo de execução no Windows (CMD/Powershell):**

```sh
python generateMonograpy.py "C:\caminho\arquivo" localhost 5432 Nome_banco usuario senha
```

✅ **Dica:** Certifique-se de estar dentro do diretório correto antes de executar os comandos.

