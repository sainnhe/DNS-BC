# Configuration

To make the code work as expected, you need to copy `config.example.json` to `config.json`. The program will the read data in `config.json`.

The content of `config.json` is typically as follows:

```json
{
    "type": "hashmap",
    "arch": "mono",
    "protocol": "tcp",
    "host": "0.0.0.0",
    "port": 3456,
    "message_size": 1024,
    "records": {
        "www.google.com": ["172.217.160.68", "Authority"],
        "www.microsoft.com": ["210.192.117.42", "Resolver"]
    },
    "credibility": {
        "Authority": "1",
        "Resolver": "0.8"
    }
}
```

The meaning of each section is described as follows:

- `"type"`: The type of this cache system. Possible values are:
  - `"hashmap"`: Use Hashmap as backend.
  - `"blockchain"`: Use Blockchain as backend.
- `"arch"`: The architecture of this cache system. Possible values are:
  - `"mono"`: Monolithic implementation.
  - `"soa"`: Service-Oriented Architecture implementation.
- `"protocol"`: The network protocol to be used. Possible values are:
  - `"tcp"`: Raw TCP protocol, no encryption.
  - `"dok"`: DoK protocol, encrypted by ECDSA.
  - `"tls"`: TCP + TLS
  - `"https"`: HTTP/1.1 + TLS
  - `"tcp+aes"`: TCP + AES
- `"host"`: The host of the server.
  - On the server side, the value should always be `0.0.0.0`.
  - On the client side, the value should be the domain name of the server.
- `"port"`: The port number of the server.
- `"message_size"`: The size of a message, in bytes.
- `"records"`: The existing DNS records in the cache, each of them consist of an array of length 2.
  - `records[0]`: The first element is the A record of a domain name.
  - `records[1]`: The second element is the owner of this record cache.
- `"credibility"`: The credibility of each owner.

In this simulation, we will use 2 nodes to verify the functionality and performance:

- `"Authority"`: Represent Authoritative DNS servers. The credibility of them should always be `1`.
- `"Resolver"`: Represent recursive DNS resolver.

