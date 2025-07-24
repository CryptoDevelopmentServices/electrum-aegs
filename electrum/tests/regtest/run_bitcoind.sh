#!/usr/bin/env bash
export HOME=~
set -eux pipefail
mkdir -p ~/.aegisum
cat > ~/.aegisum/aegisum.conf <<EOF
regtest=1
txindex=1
printtoconsole=1
rpcuser=doggman
rpcpassword=donkey
rpcallowip=127.0.0.1
zmqpubrawblock=tcp://127.0.0.1:29332
zmqpubrawtx=tcp://127.0.0.1:29333
fallbackfee=0.0002
[regtest]
rpcbind=0.0.0.0
rpcport=19554
EOF
rm -rf ~/.aegisum/regtest
aegisumd -regtest &
sleep 6
aegisum-cli createwallet test_wallet
addr=$(aegisum-cli getnewaddress)
aegisum-cli generatetoaddress 150 $addr
tail -f ~/.aegisum/regtest/debug.log
