# Hashmap based cache

Classic implementation of a cache system is using a hashmap. In this simulation, we will use python dictionary to implement it.

Change the `"type"` section in `config.json` to `"hashmap"`.

Go back to the root directory of this repository and start the server.

```shell
cd ..
python src/server.py
```

Now we have successfully started the server on AWS Lightsail. The server will listen on `"port"` specified in `config.json`, default to `3456`. We must open this port on AWS Lightsail dashboard as described in [Initialization](./Initialization.md).

The log will be placed in `hashmap.log` file.

Next, we are going to start the client on our local machine, don't forget to update `config.json`:

```shell
python src/client.py
```

Now we can start the client and send requests to the server.

The log will be placed in `client.log` file.

To stop the client or the server, simply press Ctrl-C.
