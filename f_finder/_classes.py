#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os.path import dirname
from sys import exit
import contextlib
import random
import time
from foxcolor import Cores
import httpx
import socksio
from colorama import Fore, Style
from tqdm.auto import tqdm

import f_finder as meta

blue = Fore.BLUE
red = Fore.RED
cyan = Fore.CYAN
purple = Cores.violeta
magenta = Fore.MAGENTA
RESET = Fore.RESET
DIM = Style.DIM
NORMAL = Style.NORMAL
BOLD = Style.BRIGHT
RESET_ALL = Style.RESET_ALL


class okadminfinder:
    @contextlib.contextmanager
    def credit(self):
        t0 = time.time()
        print(
            purple,
            BOLD,
            f"""
         _____      ______ _____ _   _ _____  ______ _____  
        |  ____|    |  ____|_   _| \ | |  __ \|  ____|  __ \ 
        | |__ ______| |__    | | |  \| | |  | | |__  | |__) |
        |  __|______|  __|   | | | . ` | |  | |  __| |  _  / 
        | |         | |     _| |_| |\  | |__| | |____| | \ \ 
        |_|         |_|    |_____|_| \_|_____/|______|_|  \_|
                                                      
                                                      

            🎩 Versão ⟫ {meta.__version__} Criado por: {meta.__creator__} 🎩

            """,  # noqa: W605 E501
            RESET_ALL,
        )

        yield
        print(purple, """\tObrigado por usar meu pograma 🎩💜""", RESET_ALL)
        print(
            purple, DIM, f"\t⏱️ Tempo Necessário : {(time.time() - t0):.2f}", RESET_ALL
        )  # noqa: E501

    def get_agents(self):
        agents_path = str(dirname(meta.__file__) + "/LinkFile/user-agent.txt")
        with open(agents_path, "r") as ua:
            for line in ua:
                rua = random.choice(list(ua))
                agent = {"user-agent": rua.rstrip()}
            return agent

    def get_links():
        links_path = str(dirname(meta.__file__) + "/LinkFile/adminpanellinks.txt")
        links = []
        with open(links_path, "r") as apl:
            for line in apl:
                links.append(line.replace("\n", ""))
        return links

    def create_link(website):
        try:
            url = httpx.URL(website)
            reqlinks = []
        except httpx.InvalidURL:
            exit(
                """
            Url inválido: example.com
            URL válido: http://examplo.com, http://www.examplo.com
            """
            )
        if url.host[0:4] == "www.":
            website = url.host.replace("www.", "")
            for n in okadminfinder.get_links():
                req_link = url.scheme + "://" + n.format(website)
                reqlinks.append(req_link.replace("\n", ""))
        else:
            website = url.host
            for n in okadminfinder.get_links():
                req_link = url.scheme + "://" + n.format(website)
                reqlinks.append(req_link.replace("\n", ""))
        return reqlinks

    def check_url(website, headers, proxies):
        with httpx.Client(headers=headers, proxies=proxies) as client:
            try:
                req = client.get(website)
                req.raise_for_status
                return True
            except (httpx.HTTPError, httpx.NetworkError):
                return False

    def get_proxy(prox):
        return prox

    def proxy(self, prox, headers):
        try:
            proxies = okadminfinder.get_proxy(prox)
            with httpx.Client(headers=headers, proxies=proxies) as client:
                client.get("https://httpbin.org/get")
        except (
            httpx.NetworkError,
            httpx.ProxyError,
            httpx.ReadTimeout,
            httpx.ConnectTimeout,
            socksio.exceptions.ProtocolError,
        ):
            print(
                "\n\t┎───[", red, BOLD, "Proxy/Network Error", RESET_ALL, "]"
            )  # noqa: E501
            print(
                "\t┠───╸",
                magenta,
                BOLD,
                "Cheque o formmato da proxy | Reminder::: http(s) format:: 127.0.0.1:8080  ,  socks format:: socks5://127.0.0.1:1080",
                RESET_ALL,
            )
            print(
                "\t┠───╸", magenta, BOLD, "Cheque a qualidade da proxy", RESET_ALL
            )  # noqa: E501
            print("\t┖───╸", magenta, BOLD, "Verifique a sua conexão", RESET_ALL)
            exit(1)

        except (KeyboardInterrupt):
            print(red, "\n\tProcesso cancelado", RESET_ALL)
            exit(0)
        return proxies

    async def url(self, website, headers, proxies):
        try:
            if okadminfinder.check_url(website, headers, proxies):
                print(
                    magenta,
                    BOLD,
                    website,
                    RESET_ALL,
                    purple,
                    "É estável\n",
                    RESET_ALL,  # noqa: E501
                )
            else:
                print(red, DIM, "Aparentemente há algo errado com url", RESET_ALL)
                exit(1)
            urls = okadminfinder.create_link(website)
            admin_count = 0
            total_count = len(urls)
            pbar = tqdm(
                total=total_count,
                leave=False,
                bar_format=(
                    "{l_bar}"
                    + DIM
                    + "{bar}"
                    + RESET_ALL
                    + "|{n_fmt}/{total_fmt}{postfix}"
                ),
            )
            async with httpx.AsyncClient(
                headers=headers, proxies=proxies
            ) as client:  # noqa: E501
                for url in urls:
                    pbar.update()
                    try:
                        response = await client.get(url)
                        if (
                            response.status_code == httpx.codes.OK
                            or response.status_code == httpx.codes.MOVED_PERMANENTLY
                        ):
                            tqdm.write(
                                f"{purple} ⁜ Econtrado: {cyan} {url} {RESET_ALL} \n"
                            )  # noqa: E501
                            admin_count += 1
                        else:
                            continue
                    except (
                        httpx.NetworkError,
                        httpx.ReadTimeout,
                        httpx.ConnectTimeout,
                        httpx.ProxyError,
                    ):
                        continue
                pbar.close()
            print("\n\n\t╔═══[✔️]", purple, BOLD, " Completo", RESET_ALL)
            print("\t╟───╸📑️", str(admin_count), "Total de página de administração econtradas")
            print("\t╚═══[📚️]", str(total_count), "Total de páginas verificadas")
        except (KeyboardInterrupt):
            pbar.close()
            print(red, "\n\tProcesso cancelado", RESET_ALL)
            exit(0)
        except (SystemExit):
            print(red, "\n\tProcesso cancelado", RESET_ALL)
            exit(1)
