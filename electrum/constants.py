# -*- coding: utf-8 -*-
#
# Electrum - lightweight Bitcoin client
# Copyright (C) 2018 The Electrum developers
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import json

from .util import inv_dict, all_subclasses
from . import bitcoin


def read_json(filename, default):
    path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(path, 'r') as f:
            r = json.loads(f.read())
    except Exception:
        r = default
    return r


GIT_REPO_URL = "https://github.com/CryptoDevelopmentServices/electrum-aegs"
GIT_REPO_ISSUES_URL = "https://github.com/CryptoDevelopmentServices/electrum-aegs/issues"
BIP39_WALLET_FORMATS = read_json('bip39_wallet_formats.json', [])


class AbstractNet:

    NET_NAME: str
    TESTNET: bool
    WIF_PREFIX: int
    ADDRTYPE_P2PKH: int
    ADDRTYPE_P2SH: int
    SEGWIT_HRP: str
    BOLT11_HRP: str
    GENESIS: str
    BLOCK_HEIGHT_FIRST_LIGHTNING_CHANNELS: int = 0
    BIP44_COIN_TYPE: int
    LN_REALM_BYTE: int

    @classmethod
    def max_checkpoint(cls) -> int:
        return max(0, len(cls.CHECKPOINTS) * 2016 - 1)

    @classmethod
    def rev_genesis_bytes(cls) -> bytes:
        return bytes.fromhex(bitcoin.rev_hex(cls.GENESIS))


class BitcoinMainnet(AbstractNet):

    NET_NAME = "mainnet"
    TESTNET = False
    WIF_PREFIX = 0x80
    ADDRTYPE_P2PKH = 24
    ADDRTYPE_P2SH = 23
    SEGWIT_HRP = "aegs"
    BOLT11_HRP = SEGWIT_HRP
    GENESIS = "d01de46801bba7913c039b4feabb42878e0a3e24ceef2365ed2a8d780c5aa9cd"
    DEFAULT_PORTS = {'t': '50001', 's': '50002'}
    DEFAULT_SERVERS = read_json('servers.json', {})
    CHECKPOINTS = read_json('checkpoints.json', [])
    BLOCK_HEIGHT_FIRST_LIGHTNING_CHANNELS = 49700000

    XPRV_HEADERS = {
        'standard':    0x0488ade4,  # xprv
        'p2wpkh-p2sh': 0x049d7878,  # yprv
        'p2wsh-p2sh':  0x0295b005,  # Yprv
        'p2wpkh':      0x04b2430c,  # zprv
        'p2wsh':       0x02aa7a99,  # Zprv
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard':    0x0488b21e,  # xpub
        'p2wpkh-p2sh': 0x049d7cb2,  # ypub
        'p2wsh-p2sh':  0x0295b43f,  # Ypub
        'p2wpkh':      0x04b24746,  # zpub
        'p2wsh':       0x02aa7ed3,  # Zpub
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 2
    LN_REALM_BYTE = 0
    LN_DNS_SEEDS = [
        'aegs.nodes.lightning.directory.',
        # TODO(loshy): replace with valid ln dns seeder
    ]


class BitcoinTestnet(AbstractNet):

    NET_NAME = "testnet"
    TESTNET = True
    WIF_PREFIX = 0xbf
    ADDRTYPE_P2PKH = 111
    ADDRTYPE_P2SH = 58
    SEGWIT_HRP = "taegs"
    BOLT11_HRP = SEGWIT_HRP
    GENESIS = "150d58fcb28f605e98d9d8de663b734e24f2bdab5e0f39223010bfb583762df1"
    DEFAULT_PORTS = {'t': '51001', 's': '51002'}
    DEFAULT_SERVERS = read_json('servers_testnet.json', {})
    CHECKPOINTS = read_json('checkpoints_testnet.json', [])

    XPRV_HEADERS = {
        'standard':    0x04358394,  # tprv
        'p2wpkh-p2sh': 0x044a4e28,  # uprv
        'p2wsh-p2sh':  0x024285b5,  # Uprv
        'p2wpkh':      0x045f18bc,  # vprv
        'p2wsh':       0x02575048,  # Vprv
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard':    0x043587cf,  # tpub
        'p2wpkh-p2sh': 0x044a5262,  # upub
        'p2wsh-p2sh':  0x024289ef,  # Upub
        'p2wpkh':      0x045f1cf6,  # vpub
        'p2wsh':       0x02575483,  # Vpub
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 1
    LN_REALM_BYTE = 1
    LN_DNS_SEEDS = [  # TODO investigate this again
    ]


class BitcoinRegtest(BitcoinTestnet):

    NET_NAME = "regtest"
    SEGWIT_HRP = "raegs"
    BOLT11_HRP = SEGWIT_HRP
    GENESIS = "d347ca1218939242a9e4dae9a8c1b2036384616c764a7f6aeed71e2cb98d252a"
    DEFAULT_SERVERS = read_json('servers_regtest.json', {})
    CHECKPOINTS = []
    LN_DNS_SEEDS = []


class BitcoinSimnet(BitcoinTestnet):

    NET_NAME = "simnet"
    WIF_PREFIX = 0x64
    ADDRTYPE_P2PKH = 0x3f
    ADDRTYPE_P2SH = 0x7b
    SEGWIT_HRP = "sb"
    BOLT11_HRP = SEGWIT_HRP
    GENESIS = "683e86bd5c6d110d91b94b97137ba6bfe02dbbdb8e3dff722a669b5d69d77af6"
    DEFAULT_SERVERS = read_json('servers_regtest.json', {})
    CHECKPOINTS = []
    LN_DNS_SEEDS = []


class BitcoinSignet(BitcoinTestnet):

    NET_NAME = "signet"
    BOLT11_HRP = "tbs"
    GENESIS = "00000008819873e925422c1ff0f99f7cc9bbb232af63a077a480a3633bee1ef6"
    DEFAULT_SERVERS = read_json('servers_signet.json', {})
    CHECKPOINTS = []
    LN_DNS_SEEDS = []


NETS_LIST = tuple(all_subclasses(AbstractNet))

# don't import net directly, import the module instead (so that net is singleton)
net = BitcoinMainnet

def set_signet():
    global net
    net = BitcoinSignet

def set_simnet():
    global net
    net = BitcoinSimnet

def set_mainnet():
    global net
    net = BitcoinMainnet

def set_testnet():
    global net
    net = BitcoinTestnet

def set_regtest():
    global net
    net = BitcoinRegtest
