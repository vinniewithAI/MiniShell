# 🐚 Simple Shell
Este repositório implementa um shell básico em Python com funcionalidades similares ao Bash.
Um interpretador de linha de comando completo que oferece:
- **Comandos internos** essenciais para navegação e manipulação
- **Execução paralela** de comandos usando threading
- **Redirecionamento de saída** para arquivos
- **Tratamento robusto de erros** e casos especiais

## 🚀 Funcionalidades
- Comandos internos implementados:
  - `exit` - Finaliza o shell
  - `pwd` - Exibe diretório atual
  - `cd <caminho>` - Navega entre diretórios
  - `cat <arquivo>` - Lê conteúdo de arquivos
  - `ls` - Lista arquivos e diretórios
  - `echo <texto>` - Imprime texto na tela
- Redirecionamento de saída (`comando > arquivo`)
- Execução em paralelo (`cmd1 & cmd2 & cmd3`)
- Execução sequencial (`cmd1; cmd2; cmd3`)
- Tratamento de erros e casos especiais

## 🛠️ Tecnologias
![Python](https://img.shields.io/badge/Python-3.6+-blue?logo=python)
![OS](https://img.shields.io/badge/OS-Cross_Platform-green?logo=linux)
![Threading](https://img.shields.io/badge/Threading-Concurrent-orange?logo=python)

## 📦 Pré-requisitos para desenvolver
- Python 3.6 ou superior
- Sistema operacional Linux, macOS ou Windows
- Conhecimentos básicos de linha de comando

## 🔧 Como usar
```bash
# Clone o repositório
git clone <url-do-repositorio>

# Execute o shell
python3 simple_shell.py
```

### Exemplos de comandos:
```bash
# Navegação básica
> pwd
/home/user
> cd Documents
> ls

# Redirecionamento
> ls > arquivos.txt
> echo "Hello World" > teste.txt

# Execução paralela
> echo "Comando 1" & echo "Comando 2" & echo "Comando 3"

# Execução sequencial
> pwd; ls; echo "Concluído"

# Sair do shell
> exit
```

## 📋 Funcionalidades Implementadas
- [x] Loop principal do shell com prompt personalizado
- [x] Parse de comandos com diferentes operadores
- [x] Execução de comandos internos e externos
- [x] Redirecionamento de saída padrão
- [x] Execução paralela com threading
- [x] Execução sequencial de comandos
- [x] Tratamento de erros e exceções
- [x] Suporte a caminhos relativos e absolutos

## ⚠️ Limitações
- Não suporta pipes (|)
- Não suporta redirecionamento de entrada (<)
- Não suporta append (>>)
- Argumentos com espaços devem estar sem aspas
- Não suporta variáveis de ambiente personalizadas

# Sair do shell
> exit
