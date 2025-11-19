#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Futuro do Trabalho - Console App (JSON + APIs públicas)
Sem POO, JSON only, sem list/dict comprehensions.
Com fallback para urllib se 'requests' não estiver instalado.
"""

from __future__ import annotations
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

# Import robusto de 'requests' com fallback
try:
    import requests  # type: ignore
    _HAS_REQUESTS = True
except Exception:
    _HAS_REQUESTS = False
    import urllib.request
    import urllib.error
    import ssl

ARQ_DADOS = "dados_futuro_trabalho.json"


def carregar_dados(caminho: str) -> Dict[str, Any]:
    dados: Dict[str, Any] = {"usuarios": []}
    if not os.path.exists(caminho):
        return dados
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = json.load(f)
            if isinstance(conteudo, dict) and "usuarios" in conteudo:
                return conteudo
    except Exception:
        pass
    return dados


def salvar_dados(caminho: str, dados: Dict[str, Any]) -> bool:
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        return True
    except OSError:
        return False


def pausar() -> None:
    try:
        input("\n[Enter] para continuar...")
    except EOFError:
        pass


def solicitar_int(mensagem: str, minimo: int, maximo: int) -> int:
    while True:
        txt = input(mensagem).strip()
        try:
            v = int(txt)
            if v < minimo or v > maximo:
                print(f"Valor fora do intervalo ({minimo}–{maximo}).")
            else:
                return v
        except ValueError:
            print("Digite um número inteiro.")


def listar_usuarios(dados: Dict[str, Any]) -> None:
    print("\n=== USUÁRIOS ===")
    if len(dados["usuarios"]) == 0:
        print("Nenhum usuário cadastrado.")
        return
    i = 0
    while i < len(dados["usuarios"]):
        u = dados["usuarios"][i]
        print(f"[{i}] {u.get('nome','(sem nome)')}")
        i += 1


def escolher_usuario(dados: Dict[str, Any]) -> Optional[int]:
    if len(dados["usuarios"]) == 0:
        print("Cadastre um usuário primeiro.")
        return None
    listar_usuarios(dados)
    return solicitar_int("Selecione o índice do usuário: ", 0, len(dados["usuarios"]) - 1)


def cadastrar_usuario(dados: Dict[str, Any]) -> None:
    nome = input("Nome do usuário: ").strip()
    if nome == "":
        print("Nome não pode ser vazio.")
        return
    dados["usuarios"].append({"nome": nome, "habilidades": [], "plano": [], "sessoes": []})
    print("Usuário cadastrado." if salvar_dados(ARQ_DADOS, dados) else "Falha ao salvar.")


def adicionar_habilidade(dados: Dict[str, Any]) -> None:
    idx = escolher_usuario(dados)
    if idx is None:
        return
    nome_hab = input("Habilidade (ex: Python, UX, Dados): ").strip()
    if nome_hab == "":
        print("Habilidade não pode ser vazia.")
        return
    nivel = solicitar_int("Nível (0–100): ", 0, 100)

    existe = False
    i = 0
    while i < len(dados["usuarios"][idx]["habilidades"]):
        h = dados["usuarios"][idx]["habilidades"][i]
        if h.get("nome", "").lower() == nome_hab.lower():
            h["nivel"] = nivel
            existe = True
            break
        i += 1
    if not existe:
        dados["usuarios"][idx]["habilidades"].append({"nome": nome_hab, "nivel": nivel})

    print("Habilidade registrada." if salvar_dados(ARQ_DADOS, dados) else "Falha ao salvar.")


def planejar_estudo(dados: Dict[str, Any]) -> None:
    idx = escolher_usuario(dados)
    if idx is None:
        return
    habilidade = input("Habilidade-alvo: ").strip()
    recurso = input("Recurso (curso, playlist, livro...): ").strip()
    horas = solicitar_int("Carga horária estimada (h): ", 1, 2000)
    dados["usuarios"][idx]["plano"].append({"habilidade": habilidade, "recurso": recurso, "horas": horas})
    print("Plano atualizado." if salvar_dados(ARQ_DADOS, dados) else "Falha ao salvar.")


def registrar_sessao(dados: Dict[str, Any]) -> None:
    idx = escolher_usuario(dados)
    if idx is None:
        return
    habilidade = input("Habilidade estudada: ").strip()
    minutos = solicitar_int("Minutos estudados: ", 1, 24 * 60)
    notas = input("Notas/Observações: ").strip()
    agora = datetime.now().strftime("%Y-%m-%d %H:%M")
    dados["usuarios"][idx]["sessoes"].append(
        {"data": agora, "habilidade": habilidade, "minutos": minutos, "notas": notas}
    )
    print("Sessão registrada." if salvar_dados(ARQ_DADOS, dados) else "Falha ao salvar.")


def relatorio_usuario(dados: Dict[str, Any]) -> None:
    idx = escolher_usuario(dados)
    if idx is None:
        return
    u = dados["usuarios"][idx]
    print(f"\n=== RELATÓRIO: {u.get('nome','')} ===")

    print("\n-- Habilidades --")
    if len(u["habilidades"]) == 0:
        print("Sem habilidades.")
    else:
        i = 0
        while i < len(u["habilidades"]):
            h = u["habilidades"][i]
            print(f"- {h.get('nome','?')}: {h.get('nivel',0)}/100")
            i += 1

    print("\n-- Plano de Estudos --")
    if len(u["plano"]) == 0:
        print("Sem itens no plano.")
    else:
        j = 0
        while j < len(u["plano"]):
            p = u["plano"][j]
            print(f"- {p.get('habilidade','?')} | {p.get('recurso','?')} | {p.get('horas',0)}h")
            j += 1

    print("\n-- Tempo Estudado (min) por Habilidade --")
    acumulado: Dict[str, int] = {}
    k = 0
    while k < len(u["sessoes"]):
        s = u["sessoes"][k]
        hab = s.get("habilidade", "Desconhecida")
        mins = int(s.get("minutos", 0))
        if hab in acumulado:
            acumulado[hab] = acumulado[hab] + mins
        else:
            acumulado[hab] = mins
        k += 1
    if len(acumulado) == 0:
        print("Nenhuma sessão registrada.")
    else:
        for hab_nome in acumulado:
            print(f"- {hab_nome}: {acumulado[hab_nome]} min")


# ==================== HTTP com fallback ====================

def _http_get_json_requests(url: str, *, name: str, timeout: int = 12) -> Tuple[Optional[object], Optional[str]]:
    try:
        with requests.Session() as s:  # type: ignore[name-defined]
            s.headers.update({"User-Agent": "FuturoTrabalho/1.0 (+local)"})
            r = s.get(url, timeout=timeout)
            if r.status_code != 200:
                return None, f"{name}: HTTP {r.status_code}"
            try:
                return r.json(), None
            except json.JSONDecodeError:
                return None, f"{name}: resposta não-JSON"
    except Exception as e:
        return None, f"{name}: erro de rede ({type(e).__name__})"


def _http_get_json_urllib(url: str, *, name: str, timeout: int = 12) -> Tuple[Optional[object], Optional[str]]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "FuturoTrabalho/1.0 (+stdlib)"})
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            status = resp.getcode()
            body = resp.read()
            if status != 200:
                return None, f"{name}: HTTP {status}"
            try:
                data = json.loads(body.decode("utf-8"))
                return data, None
            except json.JSONDecodeError:
                return None, f"{name}: resposta não-JSON via urllib"
    except Exception:
        return None, f"{name}: erro urllib"


def http_get_json(url: str, *, name: str, timeout: int = 12) -> Tuple[Optional[object], Optional[str]]:
    if _HAS_REQUESTS:
        return _http_get_json_requests(url, name=name, timeout=timeout)
    return _http_get_json_urllib(url, name=name, timeout=timeout)


def dica_motivacional() -> Optional[str]:
    data, err = http_get_json("https://zenquotes.io/api/random", name="ZenQuotes")
    if err is None and isinstance(data, list) and len(data) > 0:
        item = data[0]
        if isinstance(item, dict) and "q" in item and "a" in item:
            return f"{item['q']} — {item['a']}"
    data2, err2 = http_get_json("https://api.adviceslip.com/advice", name="AdviceSlip")
    if err2 is None and isinstance(data2, dict) and "slip" in data2 and "advice" in data2["slip"]:
        return data2["slip"]["advice"]
    return None


def manchetes_tech(limit: int = 5) -> List[str]:
    titulos: List[str] = []
    ids, err = http_get_json("https://hacker-news.firebaseio.com/v0/topstories.json", name="HN/list")
    if err is None and isinstance(ids, list):
        i = 0
        pegou = 0
        while i < len(ids) and pegou < limit:
            item, err2 = http_get_json(
                f"https://hacker-news.firebaseio.com/v0/item/{ids[i]}.json",
                name=f"HN/item {ids[i]}"
            )
            if err2 is None and isinstance(item, dict) and "title" in item:
                titulos.append(str(item["title"]))
                pegou = pegou + 1
            i += 1

    if len(titulos) == 0:
        data, err3 = http_get_json("https://hn.algolia.com/api/v1/search?tags=front_page", name="HN/algolia")
        if err3 is None and isinstance(data, dict) and "hits" in data:
            hits = data["hits"]
            j = 0
            while j < len(hits) and len(titulos) < limit:
                h = hits[j]
                if isinstance(h, dict) and "title" in h and h["title"]:
                    titulos.append(str(h["title"]))
                j += 1
    return titulos


# ==================== Loop principal ====================

def menu() -> None:
    dados = carregar_dados(ARQ_DADOS)
    while True:
        print("\n========= FUTURO DO TRABALHO =========")
        print("[1] Cadastrar usuário")
        print("[2] Adicionar/Atualizar habilidade")
        print("[3] Planejar estudo")
        print("[4] Registrar sessão")
        print("[5] Relatório do usuário")
        print("[6] Dica motivacional ")
        print("[7] Noticias tech ")
        print("[0] Sair")

        opcao = solicitar_int("Escolha uma opção: ", 0, 7)
        match opcao:
            case 1:
                cadastrar_usuario(dados); pausar()
            case 2:
                adicionar_habilidade(dados); pausar()
            case 3:
                planejar_estudo(dados); pausar()
            case 4:
                registrar_sessao(dados); pausar()
            case 5:
                relatorio_usuario(dados); pausar()
            case 6:
                msg = dica_motivacional()
                print("\nDica/Quote:")
                print("(Não foi possível obter a dica agora.)" if msg is None else f"- {msg}")
                pausar()
            case 7:
                print("\nTop manchetes:")
                ts = manchetes_tech(5)
                if len(ts) == 0:
                    print("(Falha ao obter manchetes.)")
                else:
                    i = 0
                    while i < len(ts):
                        print(f"- {ts[i]}")
                        i += 1
                pausar()
            case 0:
                print("Até logo!"); break
            case _:
                print("Opção inválida.")


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário. Salvando e saindo...")
