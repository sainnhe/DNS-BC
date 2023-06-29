# Initialization

## Server

Assuming you want to run the server in [AWS Lightsail](https://lightsail.aws.amazon.com/).

First of all, let's create an instance and open necessary ports:

1. Register an account and click "Create instance".
2. Platform: Linux/Unix; Blueprint -> OS Only -> Ubuntu 20.04 TLS
3. After creating the instance, we need to open 3456 port. Click "Networking" tab -> IPv4 Firewall -> Add rule -> Custom, TCP, 3456

In the home page of this instance, we can find the IPv4 address of this instance, then we can connect to it in your local host using this command:

```shell
ssh ubuntu@<ip-addr>
```

Where `<ip-addr>` is the ip address.

To test TLS and HTTPS, we need to bind a custom domain to this IP address.

If you don't have a custom domain, you can buy one in Google Domain or elsewhere.

Assuming your custom domain is hosted in Google Domain, open dashboard and add a new A record pointed to `<your-domain>`, and set the value to `<ip-addr>`.

After a while, you can test if the new domain has already been added by executing this command:

```shell
dig <your-domain>
```

If the response is equal to `<ip-addr>`, it means the record has been successfully added.

Now you can connect to the instance via your new domain:

```shell
ssh ubuntu@<your-domain>
```

After connecting to the instance, we need to login as root. **All the following steps should be executed via root.**

```shell
sudo su
```

Then we are going to clone this repository and install some dependencies:

```shell
cd ~
apt update
apt upgrade
apt install -y git
git clone https://github.com/sainnhe/DNS-BC.git
cd DNS-BC
./run.sh init
```

Now let's generate 2 pairs of certificates.

We first generate the server certificates:

```shell
./run.sh cert server
```

When asking you for "Common Name", input `<your-domain>`. For other sections, press Enter with no inputs.

Then let's generate the client certificates:

```shell
./run.sh cert client
```

When asking you for "Common Name", input `localhost`. For other sections, press Enter with no inputs.

Now use `scp` or other tools to copy all the newly generated `cert` directory to the root directory of this repository on your local machine.

We also need to install some python libraries:

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

The example configuration file is named as `config.example.json`. This file should not be modified, we should copy it to `config.json` and modify the content in it:

THIS STEP IS REQUIRED! YOU MUST COPY THIS FILE TO GET IT WORK!

```shell
cp config.example.json config.json
```

## Client

On your local machine, assuming you are using Linux or macOS, you must have the following programs installed:

- git
- openssl
- python

Clone this git repository and install python libraries:

```shell
git clone https://github.com/sainnhe/DNS-BC.git
cd DNS-BC
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then copy `config.example.json` to `config.json`, and modify the content in it.

```shell
cp config.example.json config.json
# Edit config.json, change "host" to your domain
```
