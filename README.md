## Detalhes da Implementação
O projeto consiste em um servidor MCP (Model Context Protocol) que expõe uma ferramenta (`send_message`) para enviar mensagens de WhatsApp através do WAHA (WhatsApp HTTP API).

### Tool: `send_message`
- Recebe como parâmetros:
    - `phone_number`: Número do destinatário no formato internacional (ex: +5511999999999).
    - `message`: Texto da mensagem a ser enviada.
- Internamente, a tool formata o `phone_number` para o padrão `chatId` esperado pelo WAHA (ex: `5511999999999@c.us`).
- Realiza uma requisição POST para a API do WAHA na rota `http://localhost:3000/api/sendText` utilizando a sessão "default".

### Resource: `contatos`
- Um resource foi implementado no servidor MCP contendo uma lista de contatos pré-definidos.
- Cada contato possui um nome e um número de telefone.
- Exemplo de uso com um cliente MCP: "Envie uma mensagem de bom dia para o João". O servidor MCP identificará "João" no resource de contatos e utilizará o número associado para enviar a mensagem.

## Como Executar o Projeto (macOS Silicon)

### 1. Dependências do Projeto
- Python 3.x instalado (o projeto especifica >=3.13 em `pyproject.toml`).
- Docker instalado e rodando (necessário para o WAHA).
- As dependências Python principais são `requests`, `mcp[cli]`, e `httpx`. Elas foram originalmente adicionadas ao projeto e podem ser instaladas usando `uv`.
  Após criar e ativar um ambiente virtual (ex: `python -m venv .venv` e `source .venv/bin/activate` no Linux/macOS ou `.\.venv\Scripts\activate` no Windows), você pode instalar/garantir estas dependências com o comando utilizado durante o desenvolvimento:
  ```bash
  uv add requests "mcp[cli]" httpx
  ```
  Este comando irá adicionar ou atualizar as dependências no seu `pyproject.toml` e instalá-las.

  Para usuários que clonarem o repositório e desejam instalar as dependências conforme já definidas no `pyproject.toml` (forma padrão para replicar o ambiente):
  ```bash
  uv pip install .
  ```
  ou, para sincronizar o ambiente com o `uv.lock` (se presente):
  ```bash
  uv sync
  ```

### 2. Configuração do Servidor MCP no Cursor (Opcional)
Para facilitar a execução do servidor MCP diretamente pelo Cursor durante o desenvolvimento, você pode criar um arquivo de configuração específico.

1.  Crie uma pasta chamada `.cursor` na raiz do seu projeto (se ainda não existir).
2.  Dentro da pasta `.cursor`, crie um arquivo chamado `mcp.json`.
3.  Adicione o seguinte conteúdo ao arquivo `mcp.json`:

    ```json
    {
        "mcpServers": {
            "waha": { // Você pode nomear este servidor como preferir
                "command": "uv",
                "args": [
                    "--directory",
                    "/CAMINHO/ABSOLUTO/PARA/SEU/PROJETO/mcpWAHA", // ATENÇÃO: Substitua pelo caminho absoluto do seu projeto!
                    "run",
                    "whatsapp_sender.py"
                ]
            }
        }
    }
    ```

    **Importante:** Substitua `/CAMINHO/ABSOLUTO/PARA/SEU/PROJETO/mcpWAHA` pelo caminho absoluto correto para a pasta raiz deste projeto no seu computador.

### 3. Configuração do WAHA (WhatsApp HTTP API)
Siga os passos abaixo para configurar e executar o servidor WAHA localmente usando Docker:

1.  **Baixar a imagem Docker do WAHA para ARM:**
    ```bash
    docker pull devlikeapro/waha:arm
    ```
2.  **Renomear a imagem para facilitar o uso (opcional):**
    ```bash
    docker tag devlikeapro/waha:arm devlikeapro/waha
    ```
3.  **Executar o container Docker do WAHA:**
    ```bash
    docker run -it --rm -p 3000:3000/tcp --name waha devlikeapro/waha
    ```
    Isso iniciará o servidor WAHA e o deixará acessível em `http://localhost:3000`.

4.  **Configurar a Sessão no WAHA:**
    *   Acesse `http://localhost:3000` no seu navegador.
    *   Inicie uma nova sessão (geralmente chamada "default" ou crie uma com esse nome).
    *   Escaneie o QR Code exibido utilizando o aplicativo WhatsApp no seu celular (Configurações > Aparelhos conectados > Conectar um aparelho).
    *   Aguarde a autenticação e sincronização. A sessão "default" deve estar ativa.

### 4. Utilizando Clientes MCP
Com o servidor WAHA configurado (conforme passo 3) e o servidor MCP deste projeto em execução (seja via Cursor com a configuração do passo 2, ou rodando `uv run whatsapp_sender.py` manualmente no seu terminal após ativar o ambiente virtual), você pode utilizar diferentes clientes MCP para interagir com ele.

#### a. Cursor
1.  Utilize o Cursor para interagir com o servidor.
2.  Você pode testar a tool `send_message` diretamente:
    *   Ex: "tool call send_message com phone_number='+5511999999999' e message='Olá do MCP!'"
3.  Você pode testar o resource `contatos`:
    *   Ex: "Envie uma mensagem de bom dia para o João" (assumindo que "João" está no seu resource de contatos).

#### b. Claude Desktop

##### Utilizando Ferramentas (Tools) no Claude Desktop
1.  **Identifique o Ícone de Ferramentas:** Na parte inferior direita da janela de entrada do Claude Desktop, você verá um ícone de martelo 🛠️. Este ícone indica que o Claude reconheceu as ferramentas disponíveis através do seu servidor MCP.
2.  **Acesse as Ferramentas:**
    *   Clique no ícone de martelo para visualizar a lista de ferramentas disponíveis.
    *   Selecione a ferramenta desejada, como `send_message`.
3.  **Utilize as Ferramentas via Prompt:**
    *   Você pode chamar as ferramentas diretamente em suas mensagens. Por exemplo:
        "Envie uma mensagem para +5511912345678 dizendo 'Olá, esta é uma mensagem de teste via WAHA!'"
    *   O Claude identificará a intenção e utilizará a ferramenta correspondente, solicitando sua autorização antes de executar a ação.

##### Utilizando Recursos (Resources) no Claude Desktop
1.  **Acesse o Ícone de Anexos:** Na interface do Claude Desktop, clique no ícone de clipe de papel 📎 para abrir o menu de anexos.
2.  **Selecione o Servidor MCP:**
    *   Dentro do menu de anexos, você verá uma lista dos servidores MCP disponíveis.
    *   Escolha o seu servidor (ex: `waha`, conforme configurado no `mcp.json` ou o nome que seu servidor MCP anuncia).
3.  **Anexe Recursos:**
    *   Após selecionar o servidor, você verá os recursos disponíveis (ex: `contatos`).
    *   Escolha o recurso que deseja anexar à conversa.
4.  **Interaja com os Recursos:**
    *   Uma vez anexado, você pode referenciar o recurso em suas mensagens. Por exemplo:
        "Por favor, leia o conteúdo do recurso `contatos` anexado e forneça um resumo." ou "Envie uma mensagem de bom dia para o João" (o Claude usará o resource `contatos` se anexado).

## Demonstração de Funcionalidade
A pasta `prints_usage/` neste repositório contém prints de tela que demonstram o correto funcionamento do servidor MCP. Ela está organizada da seguinte forma:

-   `prints_usage/cursor_usage/`: Contém screenshots relacionados à configuração e uso do servidor MCP com o editor Cursor.
-   `prints_usage/claude_desktop_usage/`: Apresenta screenshots da comunicação com o servidor MCP utilizando um cliente desktop (Claude), demonstrando o uso da tool `send_message` e do resource `contatos`, confirmando que tudo está funcionando corretamente.

Este setup permitirá o envio de mensagens WhatsApp através do servidor MCP, utilizando o WAHA como gateway.