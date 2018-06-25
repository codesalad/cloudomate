Cloudomate
==========

[![Build Status](https://jenkins.tribler.org/buildStatus/icon?job=pers/Cloudomate)](https://jenkins.tribler.org/job/pers/job/Cloudomate/)

![Cloudomate logo](https://files.slack.com/files-pri/T546HRL3H-F5KQ13400/cloudomate-logo.png?pub_secret=1234824941)

Overview
--------

Cloudomate is an unpermissioned open compute API which provides an
automated way to buy VPS instances and VPN servers from multiple
providers. The easiest way to use Cloudomate is via the command-line
interface.

Requirements
------------

-   Python 2 or 3
-   Works on Linux, Mac OSX, BSD
-   An active [Electrum](https://electrum.org/) wallet with sufficient
    funds

Installation
------------

The project can be installed through pip: :

    pip3 install cloudomate

Providers
---------

### VPS

Currently the following VPS providers are implemented:

    blueangelhost         https://www.blueangelhost.com/
    ccihosting            http://www.ccihosting.com/
    crowncloud            http://crowncloud.net/
    linevast              https://linevast.de/
    pulseservers          https://pulseservers.com/
    undergroundprivate    https://undergroundprivate.com/
    twosync               https://ua.2sync.org/
    proxhost              Self-hosted using ProxMox

This same list can be accessed through the list command: :

    cloudomate vps list

### VPN

Currently the following VPN providers are implemented: :

    azirevpn       https://www.azirevpn.com

This same list can be accessed through the list command: :

    cloudomate vpn list


### Compatibility

The stability of cloudomate depends on its ability to read and fill in registration forms on the provider webpages. Not all providers offer the same forms and differ in functionalities (user may not be able to send their chosen root password during registration). The following table depicts the current state of the providers that have been implemented in Cloudomate.

| Provider           | Type | Compatible | Control panel | ClientArea | Email parsing | Rootpassword | Settings | Notes                |
|--------------------|:----:|:----------:|:-------------:|------------|:-------------:|:------------:|----------|----------------------|
| BlueAngelHost      |  vps |     yes    |       -       | extended   |      yes      |  from email  |          | >12h purchase processing        |
| CCIHosting         |  vps |      no     |       -       | default    |       -       |       -      |          | Gateway broken       |
| CrownCloud         |  vps |      no     |       -       | default    |       -       |       -      |          | Manual order reviews |
| LineVast           |  vps |     yes    |      yes      | extended   |      yes      | registration | TUN/TAP  | PlebNet compatible   |
| PulseServers       |  vps |      no     |       -       | default    |       -       |       -      |          | Gateway broken       |
| TwoSync            |  vps |     yes    |       -       | extended   |               |  from email  | TUN/TAP  |                      |
| UndergrowndPrivate |  vps |     yes    |       -       | default    |       -       | registration |          |                      |
| ProxHost (TBTC)    |  vps |     yes    |       -       | none       |       -       | registration |          | Emulated             |
| AzireVPN           |  vpn |     yes    |       -       | none       |       -       | registration |          |                      |
 
**Incompatible** providers need to be fixed in order for them to work. The providers were not removed as there is a possibility that they could be fixed later on.

**Control panel** is the added feature for some providers, allowing Cloudomate to change settings such as TUN/TAP for VPN. The control panel could be further implemented to be able to change more settings.

**ClientArea** The client area contains general information such as the VPS' IP address and access to emails.

**Email parsing** With extended ClientAreas, emails can be parsed to gain access to the control panel.

### Configuration

For some commands, mainly purchase, user configuration is required. The
main way to do this is through a configruation file. For Linux, the
default location for the configuration file is
\$HOME/.config/cloudomate.cfg.

A configuration file looks like this: :

    [user]
    email =
    firstname =
    lastname =
    password =
    companyname =
    phonenumber =
    username =

    [address]
    address =
    city =
    state =
    countrycode =
    zipcode =

    [payment]
    walletpath =

    [server]
    ns1 =
    ns2 =
    hostname =
    root_password =

Section can be overridden for specific providers by adding a section,
for example a [linevast] section can contain a separate email address
only to be used for [Linevast](https://linevast.de/en/).

### Basic usage

    usage: cloudomate [-h] {vps,vpn} ...

    Cloudomate

    positional arguments:
      {vps,vpn}

    optional arguments:
      -h, --help            show this help message and exit

#### VPS

    usage: cloudomate vps [-h] 
                          {list,options,purchase,status,setrootpw,getip,ssh,info}
                          ...

    positional arguments:
      {list,options,purchase,status,setrootpw,getip,ssh,info}
        list                List VPS providers
        options             List VPS provider configurations
        purchase            Purchase VPS
        status              Get the status of the VPS services
        setrootpw           Set the root password of the last activated service
        getip               Get the IP address of the specified service
        ssh                 SSH into an active service
        info                Get information of the specified VPS service

    optional arguments:
      -h, --help            show this help message and exit

#### VPN

    usage: cloudomate [-h] {vps,vpn} ...

    positional arguments:
      {list,options,purchase,status,info}
        list                List VPN providers
        options             List VPN provider configurations
        purchase            Purchase VPN
        status              Get the status of the VPN services
        info                Get information of the specified VPN service

    optional arguments:
      -h, --help            show this help message and exit

### options

List the options for [Linevast](https://linevast.de/en/) :

    $ cloudomate vps options linevast

    Options for linevast:

       #    Name              CPU (cores)       RAM (GB)          Storage (GB)      Bandwidth (TB)    Connection (Mbps) Est. Price (mBTC) Price
       0    Basis OVZ         1                 2                 50                unmetered         1000              1.03              EUR 6.99
       1    Business OVZ      2                 4                 150               unmetered         1000              1.64              EUR 12.99
       2    Advanced OVZ      4                 8                 300               unmetered         1000              2.35              EUR 19.99
       3    Black OVZ         8                 16                1000              unmetered         1000              2.96              EUR 25.99
       4    Basic KVM         1                 2                 30                unmetered         1000              1.03              EUR 6.99
       5    Business KVM      2                 4                 50                unmetered         1000              1.64              EUR 12.99
       6    Advanced KVM      4                 8                 75                unmetered         1000              2.96              EUR 25.99
       7    Black KVM         6                 16                100               unmetered         1000              4.18              EUR 37.99

### Purchase

Use the purchase command to purchase a VPS instance. An account is
created and the instance is paid through an Electrum wallet. :

    $ cloudomate vps purchase linevast 0

    Selected configuration:
    Name           CPU            RAM            Storage        Bandwidth      Est.Price
    Basis OVZ      1              2              50             unmetered      6.99
    Purchase this option? (y/N)

Additionally, a `randomuser` could be generated for a purchase:
```
    $ cloudomate vps purchase linevast 0 --randomuser
```
The configuration file is stored in `~/.config/cloudomate.cfg`.

For **ProxHost**, a server could be bought using testnet Bitcoins:
```
    $ cloudomate vps purchase proxhost 0 --testnet
```


### Manage

#### VPS

The following functions can be used to manage a purchased VPS instance :

    status              Get the status of the service.
    info                Get information of the specified service
    setrootpw           Set the root password of the last activated service.
    getip               Get the ip of the specified service.

#### VPN

The following functions can be used to manage a purchased VPN instance :

    status              Get the status of the service.
    info                Get configuration of the specified service

Tests
-----

To run the project's tests (make sure to install with extra\_requires:
[test]) :

    python -m unittest discover
