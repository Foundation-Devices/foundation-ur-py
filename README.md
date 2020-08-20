# [Foundation Devices Python UR Library](https://github.com/Foundation-Devices/foundation-ur-py)

**UR Implementation in Python -- ported from the [C++ Reference Implementation by Blockchain Commons](https://github.com/BlockchainCommons/bc-ur)**

## Introduction

URs ("Uniform Resources") are a method for encoding structured binary data for transport in URIs and QR Codes. They are described in [BCR-2020-005](https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-005-ur.md).

There also another reference implementation in Swift: [URKit](https://github.com/blockchaincommons/URKit), and a demo app that uses it to display and read multi-part animated QR codes: [URDemo](https://github.com/blockchaincommons/URDemo).

## Installation

```
TBD
```

This sequence runs the module's unit tests.

## Use

1. Include the source folder in your Python project
2. `import ur` and use `ur.encode()` and `ur.decode()`

The highest-level APIs are found in `ur-encoder.py` and `ur-decoder.py`.

## Notes for Maintainers

Before accepting a PR that can affect build or unit tests, make sure the following command succeeds:

```
python test.py
```

## Origin, Authors, Copyright & Licenses

Unless otherwise noted (either in this [/README.md](./README.md) or in the file's header comments) the contents of this repository are Copyright © 2020 by Foundation Devices Inc., and are [licensed](./LICENSE) under the [TBD](http://tbd).

This code is a Python portof the original C++ reference implementation by Blockchain Commons.  See
[Blockchain Commons UR Library](https://github.com/BlockchainCommons/bc-ur) for the original version.



### Dependencies

Either `hashlib` in a normal Python environment or `uhashlib` in MicroPython must be available.

## Contributing

TBD

We encourage public contributions through issues and pull-requests! Please review [CONTRIBUTING.md](./CONTRIBUTING.md) for details on our development process. All contributions to this repository require a GPG signed [Contributor License Agreement](./CLA.md).

### Questions & Support

If you have questions or problems, please use this repository's [issues](./issues) feature.

### Credits

The following people directly contributed to this repository. You can add your name here by getting involved — the first step is to learn how to contribute from our [CONTRIBUTING.md](./CONTRIBUTING.md) documentation.

| Name          | Role         | Github                                             | Email                         | GPG Fingerprint |
| ------------- | ------------ | -------------------------------------------------- | ----------------------------- | --------------- |
| Ken Carpenter | Initial Port | [@FoundationKen](https://github.com/FoundationKen) | \<ken@foundationdevices.com\> | TBD             |

## Responsible Disclosure

We want to keep all our software safe for everyone. If you have discovered a security vulnerability, we appreciate your help in disclosing it to us in a responsible manner. We are unfortunately not able to offer bug bounties at this time.

We do ask that you offer us good faith and use best efforts not to leak information or harm any user, their data, or our developer community. Please give us a reasonable amount of time to fix the issue before you publish it. Do not defraud our users or us in the process of discovery. We promise not to bring legal action against researchers who point out a problem provided they do their best to follow the these guidelines.

### Reporting a Vulnerability

Please report suspected security vulnerabilities in private via email to ChristopherA@BlockchainCommons.com (do not use this email for support). Please do NOT create publicly viewable issues for suspected security vulnerabilities.

The following keys may be used to communicate sensitive information to developers:

| Name            | Fingerprint |
| --------------- | ----------- |
| security@...TBD | TBD         |

You can import a key by running the following command with that individual’s fingerprint: `gpg --recv-keys "<fingerprint>"` Ensure that you put quotes around fingerprints that contain spaces.

## Version History

### 0.1.0, 08/20/2020 - TBD

* Initial testing release.
