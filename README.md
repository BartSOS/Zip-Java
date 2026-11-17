# Zip-Java

Script em Python que prepara a entrega de um trabalho Java da disciplina de Programação Orientada a Objetos: compila o projeto, gera o `.jar` executável e empacota tudo num `.zip` com o nome da pasta, conferindo a integridade do arquivo no fim.

```text
<pasta>/src/**/*.java ──▶ javac ──▶ <pasta>/bin/*.class ──▶ jar (Main-Class: App) ──▶ <pasta>/<pasta>.jar
                                                                                         │
<pasta>/src/**/*.java + arquivos .csv .jar .md .png da raiz ─────────────────────────────┴──▶ <pasta>/<pasta>.zip
```

## Requisitos

- Python 3 (só biblioteca padrão).
- JDK com `javac` e `jar` no `PATH`.

## Uso

```bash
python zip.py              # usa a pasta atual
python zip.py <pasta>      # usa a pasta indicada
```

Mais de um argumento encerra com a mensagem de uso.

## Estrutura esperada do projeto

```text
<pasta>/
├── src/            # fontes .java (subpastas permitidas)
├── bin/            # criada pelo script, se não existir
├── README.md       # opcional: entra no zip
├── dados.csv       # opcional: .csv, .md, .png e .jar da raiz entram no zip
└── ...
```

A classe principal precisa se chamar **`App`** e ficar no pacote padrão (sem `package`): o `.jar` é criado com `jar cfe <pasta>.jar App`.

## O que o script faz

1. **Compila:** procura todos os `.java` dentro de `src/` (recursivo) e roda `javac -d bin` com a lista inteira.
2. **Gera o JAR:** junta os `.class` de `bin/` em `<pasta>/<pasta>.jar`, com `App` como ponto de entrada. Falha ao criar o JAR encerra o script com erro.
3. **Empacota:** cria `<pasta>/<pasta>.zip` (compressão DEFLATE) com:
   - os arquivos `.csv`, `.jar`, `.md` e `.png` que estão **direto na raiz** da pasta (subpastas não entram);
   - todos os `.java` de `src/`, preservando o caminho relativo (`src/...`).
   O zip **não** leva `bin/` nem os `.class`.
4. **Confere:** reabre o zip, roda `testzip()` e imprime quantos arquivos `.java` e quantas entradas foram incluídos.

## Observações

- Se não houver `src/`, se não houver `.java` ou se a compilação falhar, o script avisa, **pula o JAR e gera o zip mesmo assim**. Confira a saída do `javac` antes de entregar: um `.jar` antigo que já esteja na raiz da pasta entra no zip.
- O zip e o JAR são gravados dentro da própria pasta do projeto e são sobrescritos a cada execução.
- Se houver `.java` em `src/` e o `javac` não estiver no `PATH`, o script para com `FileNotFoundError` antes de gerar o zip.
- No Windows, com a saída redirecionada ou num console que não usa UTF-8, as mensagens com emoji podem dar `UnicodeEncodeError`. Nesse caso, rode `python -X utf8 zip.py <pasta>`.
