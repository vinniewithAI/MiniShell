#!/usr/bin/env python3

# Importa as bibliotecas necessárias
import os
import sys
import subprocess
import threading
from pathlib import Path


class ShellSimples:
    def __init__(self):
        # Armazena o diretório atual
        self.diretorio_atual = os.getcwd()
        # Controla se o shell está funcionando
        self.rodando = True

    def analisar_comando(self, linha_comando):
        # Faz o parse da linha de comando e retorna os comandos processados
        linha_comando = linha_comando.strip()
        if not linha_comando:
            return []

        # Verifica se há redirecionamento
        if '>' in linha_comando:
            return self.analisar_redirecionamento(linha_comando)

        # Verifica se há comandos em paralelo (&)
        if '&' in linha_comando:
            return self.analisar_paralelo(linha_comando)

        # Verifica se há comandos em sequência (;)
        if ';' in linha_comando:
            return self.analisar_sequencia(linha_comando)

        # Comando simples
        return [{'tipo': 'simples', 'comando': linha_comando.split()}]

    def analisar_redirecionamento(self, linha_comando):
        # Analisa comandos com redirecionamento de saída
        partes = linha_comando.split('>', 1)
        if len(partes) != 2:
            return [{'tipo': 'erro', 'mensagem': 'Sintaxe de redirecionamento inválida'}]

        comando = partes[0].strip().split()
        arquivo_saida = partes[1].strip()

        return [{'tipo': 'redirecionamento', 'comando': comando, 'arquivo_saida': arquivo_saida}]

    def analisar_paralelo(self, linha_comando):
        # Analisa comandos para execução em paralelo
        comandos_brutos = linha_comando.split('&')
        comandos_analisados = []

        # Percorre cada comando separado por &
        for cmd in comandos_brutos:
            cmd = cmd.strip()
            if cmd:  # Se o comando não está vazio
                comandos_analisados.append({'tipo': 'paralelo', 'comando': cmd.split()})

        return comandos_analisados

    def analisar_sequencia(self, linha_comando):
        # Analisa comandos para execução em sequência
        comandos_brutos = linha_comando.split(';')
        comandos_analisados = []

        # Percorre cada comando separado por ;
        for cmd in comandos_brutos:
            cmd = cmd.strip()
            if cmd:  # Se o comando não está vazio
                comandos_analisados.append({'tipo': 'sequencia', 'comando': cmd.split()})

        return comandos_analisados

    def executar_comandos(self, comandos_analisados):
        # Executa os comandos que foram analisados
        if not comandos_analisados:
            return

        # Separa comandos por tipo para processar adequadamente
        comandos_paralelos = []
        comandos_sequenciais = []
        outros_comandos = []

        # Classifica cada comando pelo seu tipo
        for cmd in comandos_analisados:
            if cmd.get('tipo') == 'paralelo':
                comandos_paralelos.append(cmd)
            elif cmd.get('tipo') == 'sequencia':
                comandos_sequenciais.append(cmd)
            else:
                outros_comandos.append(cmd)

        # Executa comandos em paralelo
        if comandos_paralelos:
            self.executar_paralelo(comandos_paralelos)

        # Executa comandos em sequência
        if comandos_sequenciais:
            self.executar_sequencia(comandos_sequenciais)

        # Executa outros tipos de comandos
        for cmd in outros_comandos:
            if cmd.get('tipo') == 'redirecionamento':
                self.executar_redirecionamento(cmd)
            elif cmd.get('tipo') == 'simples':
                self.executar_comando_unico(cmd['comando'])
            elif cmd.get('tipo') == 'erro':
                print(cmd['mensagem'])

    def executar_paralelo(self, comandos):
        # Executa comandos em paralelo usando threads
        threads = []

        # Cria uma thread para cada comando
        for cmd in comandos:
            thread = threading.Thread(target=self.executar_comando_unico, args=(cmd['comando'],))
            threads.append(thread)
            thread.start()

        # Aguarda todos os threads terminarem
        for thread in threads:
            thread.join()

    def executar_sequencia(self, comandos):
        # Executa comandos em sequência (um após o outro)
        for cmd in comandos:
            self.executar_comando_unico(cmd['comando'])

    def executar_redirecionamento(self, dados_comando):
        # Executa comando com redirecionamento de saída
        comando = dados_comando['comando']
        arquivo_saida = dados_comando['arquivo_saida']

        if not comando:
            return

        # Verifica se é comando interno
        if self.eh_comando_interno(comando[0]):
            try:
                # Abre arquivo para escrita
                with open(arquivo_saida, 'w') as arquivo:
                    # Salva a saída padrão original
                    saida_original = sys.stdout
                    # Redireciona saída para o arquivo
                    sys.stdout = arquivo
                    # Executa o comando interno
                    self.executar_comando_interno(comando)
                    # Restaura a saída padrão
                    sys.stdout = saida_original
            except IOError as e:
                print(f"Erro ao escrever no arquivo {arquivo_saida}: {e}")
        else:
            # Comando externo
            try:
                with open(arquivo_saida, 'w') as arquivo:
                    subprocess.run(comando, stdout=arquivo, stderr=subprocess.PIPE,
                                   cwd=self.diretorio_atual, check=False)
            except IOError as e:
                print(f"Erro ao escrever no arquivo {arquivo_saida}: {e}")

    def executar_comando_unico(self, comando):
        # Executa um único comando
        if not comando:
            return

        nome_comando = comando[0]

        # Verifica se é comando interno ou externo
        if self.eh_comando_interno(nome_comando):
            self.executar_comando_interno(comando)
        else:
            self.executar_comando_externo(comando)

    def eh_comando_interno(self, nome_comando):
        # Verifica se o comando é interno (implementado no shell)
        comandos_internos = ['exit', 'pwd', 'cd', 'cat', 'ls', 'echo']
        return nome_comando in comandos_internos

    def executar_comando_interno(self, comando):
        # Executa comandos internos
        nome_comando = comando[0]
        argumentos = comando[1:]

        # Chama o método apropriado para cada comando
        if nome_comando == 'exit':
            self.comando_exit()
        elif nome_comando == 'pwd':
            self.comando_pwd()
        elif nome_comando == 'cd':
            self.comando_cd(argumentos)
        elif nome_comando == 'cat':
            self.comando_cat(argumentos)
        elif nome_comando == 'ls':
            self.comando_ls()
        elif nome_comando == 'echo':
            self.comando_echo(argumentos)

    def executar_comando_externo(self, comando):
        # Executa comandos externos (do sistema operacional)
        try:
            resultado = subprocess.run(comando, cwd=self.diretorio_atual,
                                       capture_output=False, text=True)
        except FileNotFoundError:
            print(f"{comando[0]}: comando não encontrado")
        except Exception as e:
            print(f"Erro ao executar comando: {e}")

    # Implementação dos comandos internos
    def comando_exit(self):
        # Comando exit - finaliza o shell
        self.rodando = False
        print("Tchau!")

    def comando_pwd(self):
        # Comando pwd - exibe diretório atual
        print(self.diretorio_atual)

    def comando_cd(self, argumentos):
        # Comando cd - muda diretório
        # Se não tem exatamente 1 argumento, não faz nada
        if len(argumentos) != 1:
            return

        caminho = argumentos[0]

        try:
            # Expande ~ para diretório home do usuário
            if caminho.startswith('~'):
                caminho = os.path.expanduser(caminho)

            # Converte para caminho absoluto se necessário
            if not os.path.isabs(caminho):
                caminho = os.path.join(self.diretorio_atual, caminho)

            # Normaliza o caminho (remove .. e . desnecessários)
            caminho = os.path.normpath(caminho)

            # Verifica se o diretório existe
            if os.path.isdir(caminho):
                self.diretorio_atual = caminho
                os.chdir(caminho)
            else:
                print("diretório não encontrado")

        except PermissionError:
            print("permissão negada")
        except Exception as e:
            print(f"cd: erro - {e}")

    def comando_cat(self, argumentos):
        # Comando cat - exibe conteúdo de arquivo
        if not argumentos:
            print("cat: nome do arquivo necessário")
            return

        # Processa cada arquivo nos argumentos
        for nome_arquivo in argumentos:
            try:
                # Determina o caminho completo do arquivo
                if not os.path.isabs(nome_arquivo):
                    caminho_arquivo = os.path.join(self.diretorio_atual, nome_arquivo)
                else:
                    caminho_arquivo = nome_arquivo

                # Abre e lê o arquivo
                with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                    conteudo = arquivo.read()
                    print(conteudo, end='')

            except FileNotFoundError:
                print(f"cat: {nome_arquivo}: Arquivo não encontrado")
            except PermissionError:
                print(f"cat: {nome_arquivo}: Permissão negada")
            except UnicodeDecodeError:
                print(f"cat: {nome_arquivo}: Não é possível decodificar arquivo (arquivo binário?)")
            except Exception as e:
                print(f"cat: erro ao ler {nome_arquivo}: {e}")

    def comando_ls(self):
        # Comando ls - lista conteúdo do diretório
        try:
            # Obtém lista de itens no diretório atual
            itens = os.listdir(self.diretorio_atual)
            itens.sort()  # Ordena alfabeticamente

            # Imprime cada item
            if itens:
                for item in itens:
                    print(item)

        except PermissionError:
            print("ls: permissão negada")
        except Exception as e:
            print(f"ls: erro - {e}")

    def comando_echo(self, argumentos):
        # Comando echo - imprime texto
        if argumentos:
            # Junta argumentos com espaços
            texto = ' '.join(argumentos)

            # Remove aspas se estiverem presentes
            if (texto.startswith('"') and texto.endswith('"')) or \
                    (texto.startswith("'") and texto.endswith("'")):
                texto = texto[1:-1]

            print(texto)
        else:
            # Se não há argumentos, imprime linha vazia
            print()

    def executar(self):
        # Loop principal do shell
        print("Shell Simples - Digite 'exit' para sair")

        while self.rodando:
            try:
                # Cria e exibe o prompt
                prompt = f"{os.path.basename(self.diretorio_atual)} > "
                linha_comando = input(prompt)

                # Analisa e executa os comandos
                comandos_analisados = self.analisar_comando(linha_comando)
                self.executar_comandos(comandos_analisados)

            except KeyboardInterrupt:
                print("\nUse 'exit' para sair do shell")
            except EOFError:
                print("\nTchau!")
                break
            except Exception as e:
                print(f"Erro: {e}")


def main():
    # Função principal - cria e executa o shell
    shell = ShellSimples()
    shell.executar()


if __name__ == "__main__":
    main()