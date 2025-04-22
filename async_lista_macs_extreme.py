#!/usr/bin/env python
import argparse
import asyncio
import concurrent.futures
import os
import sys

import dotenv
import pexpect


def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("--ips", nargs="+", type=str, help="IPs of the Switches")
    parser.add_argument(
        "--switchuser", type=str, help="switchuser", default=os.getenv("SWITCHUSER")
    )
    parser.add_argument(
        "--password", type=str, help="Password", default=os.getenv("PASSWORD")
    )
    parser.add_argument(
        "--command",
        nargs="?",
        default="show interfaces gigabitEthernet fdb-entry 1/1-1/48",
    )
    options = parser.parse_args(args)
    return options


def fetch_macs(ip, switchuser, password, command):
    try:
        child = pexpect.spawn(
            f"ssh {switchuser}@{ip} -o StrictHostKeyChecking='no'",
            timeout=10,
        )
        child.expect(["password:", ".*Press any key.*"], timeout=5)
        child.sendline(password)
        child.expect("SW.*")
        child.sendline("terminal more disable")
        child.expect("SW.*")
        child.sendline("enable")
        child.expect("SW.*")
        child.sendline(command)
        # child.expect("\*")
        child.expect("SW.*")
        output = child.before.decode("utf-8")
        child.sendline("exit")
        return ip, output
    except (pexpect.EOF, pexpect.TIMEOUT):
        return ip, None


def parse_mac_table(output):
    dados = []
    for linha in output.splitlines():
        if "learned" in linha:
            colunas = linha.split()
            vlan_id, mac_address, interface = colunas[0], colunas[2], colunas[3]
            dados.append(
                {"vlan_id": vlan_id, "mac_address": mac_address, "interface": interface}
            )
    return dados


async def run_in_executor(executor, func, *args):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, func, *args)
    return result


async def main():
    dotenv.load_dotenv()
    args = getOptions()
    # print(f"args.switchuser: {args.switchuser}")
    # print(f"args.password: {args.password}")
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(args.ips))
    tasks = [
        run_in_executor(
            executor, fetch_macs, ip, args.switchuser, args.password, args.command
        )
        for ip in args.ips
    ]

    results = await asyncio.gather(*tasks)

    mac_tables = []
    for ip, output in results:
        if output:
            macs = parse_mac_table(output)
            for mac in macs:
                mac_tables.append({"switch": ip, **mac})

    for entry in mac_tables:
        print(entry)


if __name__ == "__main__":
    asyncio.run(main())
