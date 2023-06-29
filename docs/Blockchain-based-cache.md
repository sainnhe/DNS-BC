# Blockchain based cache

Our novel design will use blockchain as the backend of the cache system. The setup procedure is relatively more complex.

First, let's bring up the blockchain network.

```shell
cd DNS-BC
./run.sh network up
```

If you want to add more node, execute the following command:

```shell
./run.sh network newNode
```

Next, we need to compile the smart contract. The smart contract is written in golang, we can use the following command to compile it:

```shell
./run.sh chaincode
```

On success, it will have the following output:

```text
Installed chaincodes on peer:
Package ID: basic_1.0:69de748301770f6ef64b42aa6bb6cb291df20aa39542c3ef94008615704007f3, Label: basic_1.0
```

Now we are going to approve the chain code and commit it to the nodes:

```shell
./run.sh approve basic_1.0:69de748301770f6ef64b42aa6bb6cb291df20aa39542c3ef94008615704007f3
./run.sh commit
```

Finally, change the `"type"` section in `config.json` to `"blockchain"` and start the server using the following command:

```shell
python src/server.py
```

The log will be placed in `blockchain.log` file.

Next, on our local machine, modify `config.json` and use the following command to start the client:

```shell
python src/client.py
```

The log will be placed in `client.log` file.

To stop the client, press Ctrl-C. To stop the server, execute `./run.sh network down`.
