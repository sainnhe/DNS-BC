#!/usr/bin/env bash

# Author: Tianfu Gao
# Email: tfgao@stu.xidian.edu.cn
# License: GPL-3

# Usage:
# ./run.sh init
# ./run.sh network up
# ./run.sh chaincode
# ./run.sh approve basic_1.0:a59a3240526cad6576ee46b17892fc5aa19e6ebad1fe6fb3d2d49ad6cb883fb8
# ./run.sh commit
# ./run.sh invoke '{"function":"InitLedger","Args":[]}'
# ./run.sh query '{"Args":["GetAllAssets"]}'
# ./run.sh invoke '{"function":"CreateAsset","Args":["test.example.com", "127.0.0.1", "Authority", "0", "NULL"]}'
# ./run.sh invoke '{"function":"UpdateAsset","Args":["test.example.com", "192.168.0.3", "Authority", "0", "NULL"]}'
# ./run.sh invoke '{"function":"DeleteAsset","Args":["test.example.com"]}'
# ./run.sh network down

root_dir="$(git rev-parse --show-toplevel)"
fabric_version="2.4.9"
ca_version="1.5.5"

source "${root_dir}/fabric/envs/init.env"

if [ "$(whoami)" != "root" ]; then
    echo "The current user is not root."
    echo "This script is tended to be run via root."
    exit 1
fi

if [ ! "$(command -v apt)" ]; then
    echo "This script is tended to be run in Debian/Ubuntu."
    exit 2
fi

init() {
    cd "${root_dir}"
    echo ">> Installing dependencies ..."
    apt update
    apt install -y \
        git \
        curl \
        docker-compose \
        jq \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        openssl
    echo ">> Updating git submodules ..."
    git submodule update --init --recursive
    if [ ! "$(command -v go)" ]; then
        echo ">> Go not found. Installing to /usr/local/go ..."
        curl -fSLO https://go.dev/dl/go1.20.2.linux-amd64.tar.gz
        tar -C /usr/local -xvf go1.20.2.linux-amd64.tar.gz
        rm go1.20.2.linux-amd64.tar.gz
        ln -s /usr/local/go/bin/go /usr/local/bin/go
        ln -s /usr/local/go/bin/gofmt /usr/local/bin/gofmt
    fi
    curl -sSLO https://raw.githubusercontent.com/hyperledger/fabric/main/scripts/install-fabric.sh && \
        chmod +x install-fabric.sh
    ln -s "$(pwd)/fabric/samples" fabric-samples
    echo ">> Downloading binary ..."
    ./install-fabric.sh \
        -f "${fabric_version}" \
        -c "${ca_version}" \
        binary
    echo ">> Pulling docker images ..."
    ./install-fabric.sh \
        -f "${fabric_version}" \
        -c "${ca_version}" \
        docker
    rm install-fabric.sh fabric-samples
}

network() {
    cd "${root_dir}/fabric/samples/test-network"
    if [ "${1}" == "up" ]; then
        ./network.sh up createChannel
    elif [ "${1}" == "down" ]; then
        ./network.sh down
    else
        cd addOrg3
        ./addOrg3.sh up
    fi
}

chaincode() {
    cd "${root_dir}"
    peer lifecycle chaincode package basic.tar.gz \
        --path "${root_dir}/fabric/chaincode/" \
        --lang golang \
        --label basic_1.0
    source "${root_dir}/fabric/envs/org1.env"
    peer lifecycle chaincode install basic.tar.gz
    source "${root_dir}/fabric/envs/org2.env"
    peer lifecycle chaincode install basic.tar.gz
}

approve() {
    cd "${root_dir}"
    export CC_PACKAGE_ID="${1}"
    source "${root_dir}/fabric/envs/org1.env"
    peer lifecycle chaincode approveformyorg \
        -o localhost:7050 \
        --ordererTLSHostnameOverride orderer.example.com \
        --channelID mychannel \
        --name basic \
        --version 1.0 \
        --package-id "${CC_PACKAGE_ID}" \
        --sequence 1 \
        --tls \
        --cafile "${root_dir}/fabric/samples/test-network/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem"
    source "${root_dir}/fabric/envs/org2.env"
    peer lifecycle chaincode approveformyorg \
        -o localhost:7050 \
        --ordererTLSHostnameOverride orderer.example.com \
        --channelID mychannel \
        --name basic \
        --version 1.0 \
        --package-id "${CC_PACKAGE_ID}" \
        --sequence 1 \
        --tls \
        --cafile "${root_dir}/fabric/samples/test-network/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem"
}

commit() {
    # Using any member would be OK
    source "${root_dir}/fabric/envs/org1.env"
    peer lifecycle chaincode commit \
        -o localhost:7050 \
        --ordererTLSHostnameOverride orderer.example.com \
        --channelID mychannel \
        --name basic \
        --version 1.0 \
        --sequence 1 \
        --tls \
        --cafile "${root_dir}/fabric/samples/test-network/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
        --peerAddresses localhost:7051 \
        --tlsRootCertFiles "${root_dir}/fabric/samples/test-network/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" \
        --peerAddresses localhost:9051 \
        --tlsRootCertFiles "${root_dir}/fabric/samples/test-network/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt"
    # Comfirm
    peer lifecycle chaincode querycommitted --channelID mychannel --name basic
}

invoke() {
    source "${root_dir}/fabric/envs/org1.env"
    peer chaincode invoke \
        -o localhost:7050 \
        --ordererTLSHostnameOverride orderer.example.com \
        --tls \
        --cafile "${root_dir}/fabric/samples/test-network/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
        -C mychannel \
        -n basic \
        --peerAddresses localhost:7051 \
        --tlsRootCertFiles "${root_dir}/fabric/samples/test-network/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" \
        --peerAddresses localhost:9051 \
        --tlsRootCertFiles "${root_dir}/fabric/samples/test-network/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt" \
        -c "${1}"
}

query() {
    source "${root_dir}/fabric/envs/org1.env"
    peer chaincode query \
        -C mychannel \
        -n basic \
        -c "${1}"
}

cert() {
    cd "${root_dir}"
    mkdir -p cert
    cd cert
    echo ">> Generating ${1} cert..."
    openssl genrsa -out "${1}.key" 2048
    openssl req -new -key "${1}.key" -out "${1}.csr"
    openssl x509 -req -days 365 -in "${1}.csr" -signkey "${1}.key" -out "${1}.crt"
}

case "${1}" in
init)
    init
    ;;
network)
    network "${2}"
    ;;
chaincode)
    chaincode
    ;;
approve)
    approve "${2}"
    ;;
commit)
    commit
    ;;
invoke)
    invoke "${2}"
    ;;
query)
    query "${2}"
    ;;
cert)
    cert "${2}"
    ;;
*)
    echo ">> Invalid input."
    ;;
esac
