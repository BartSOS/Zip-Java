import os
import sys
import subprocess
import zipfile

sufixo_jar = ".jar"
sufixo_java = ".java"
CAMINHO_JAVA = "src"
CAMINHO_BIN = "bin"
sufixo_csv = ".csv"
sufixo_md = ".md"
sufixo_png = ".png"

def is_file_one(sufixo):
    return sufixo == sufixo_csv or sufixo == sufixo_jar or sufixo == sufixo_md or sufixo == sufixo_png

def compila_java(pasta):
    print("☕ Compilando o código Java...")
    pasta_src = os.path.join(pasta, CAMINHO_JAVA)
    if not os.path.exists(pasta_src):
        print("Não existe a pasta src, não há arquivos java para compilar.")
        return False

    pasta_bin = os.path.join(pasta, CAMINHO_BIN)
    if not os.path.exists(pasta_bin):
        os.makedirs(pasta_bin)

    arquivos_java = []
    for root, dirs, files in os.walk(pasta_src):
        for file in files:
            if file.endswith(sufixo_java):
                caminho_absoluto = os.path.join(root, file)
                arquivos_java.append(caminho_absoluto)

    if len(arquivos_java) == 0:
        print("Não há arquivos java para compilar.")
        return False

    print(f"Compilando {len(arquivos_java)} arquivos java...")
    comando = ["javac", "-d", pasta_bin] + arquivos_java
    resultado = subprocess.run(comando)

    if resultado.returncode != 0:
        print("Erro ao compilar arquivos java:")
        return False

    return True

def cria_jar(pasta):
    print("📦 Criando o arquivo JAR...")
    pasta_bin = os.path.join(pasta, CAMINHO_BIN)
    if not os.path.exists(pasta_bin):
        print("Não existe a pasta bin, não há arquivos compilados para criar o JAR.")
        return False

    arquivos_class = []
    for root, dirs, files in os.walk(pasta_bin):
        for file in files:
            if file.endswith(".class"):
                caminho_absoluto = os.path.join(root, file)
                caminho_relativo = os.path.relpath(caminho_absoluto, pasta_bin)
                arquivos_class.append(caminho_relativo)

    if len(arquivos_class) == 0:
        print("Não há arquivos .class para criar o JAR.")
        return False

    nome_jar = os.path.basename(pasta) + sufixo_jar
    destino_jar = os.path.join(pasta, nome_jar)
    comando = ["jar", "cfe", destino_jar, "App"] + arquivos_class
    resultado = subprocess.run(comando, cwd=pasta_bin)

    if resultado.returncode != 0:
        print("Erro ao criar o arquivo JAR:")
        return False

    print(f"Arquivo JAR criado com sucesso: {destino_jar}")
    return True

def main(pasta):
    pasta = os.path.abspath(pasta)
    
    if not os.path.exists(pasta):
        sys.exit(f"ERRO: a pasta {pasta} não existe.")

    if (compila_java(pasta)):
        if not cria_jar(pasta):
            sys.exit("ERRO: falha ao criar o arquivo JAR.")

    nome = os.path.basename(pasta)
    destino = os.path.join(pasta, nome + ".zip")
    arquivos_java = {}
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        arquivos_na_pasta = os.listdir(pasta)
        
        for arquivo in arquivos_na_pasta:
            file_src, ext = os.path.splitext(arquivo)
    
            if is_file_one(ext):
                z.write(os.path.join(pasta, arquivo), arquivo)

        pasta_src = os.path.join(pasta, CAMINHO_JAVA)

        if os.path.exists(pasta_src): 
            z.writestr(CAMINHO_JAVA + "/", "")
            for root, dirs, files in os.walk(pasta_src):
                for file in files:
                    if file.endswith(sufixo_java):
                        caminho_absoluto = os.path.join(root, file)
                        arquivos_java[file] = caminho_absoluto
                        caminho_relativo = os.path.relpath(caminho_absoluto, pasta)
                        z.write(caminho_absoluto, caminho_relativo)

    with zipfile.ZipFile(destino) as z:
        if z.testzip() is not None:
            sys.exit("ERRO: zip corrompido.")
        n = len(z.namelist())
    print(f"{destino}: acho que ta tudo ai chefe. Tem {len(arquivos_java)} arquivos java. ({n} entradas)")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main(os.getcwd())
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        sys.exit("ERRO: uso incorreto. Use: python zip.py [pasta]")

