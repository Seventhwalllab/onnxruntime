# Unofficial, unmodified copy of Microsoft's ONNX Runtime 1.19.2

Not affiliated with or endorsed by Microsoft or the ONNX project.

This repository keeps a copy of the ONNX Runtime 1.19.2 shared libraries **as
Microsoft built and published them, byte for byte**, together with Microsoft's
MIT licence and the release's third-party notices.

ONNX Runtime is Microsoft's project (https://onnxruntime.ai), licensed under the
MIT licence. This copy is not affiliated with, endorsed by or supported by
Microsoft or the ONNX project. Problems with ONNX Runtime itself belong to its
authors, not here.

## Why this copy exists

Since November 2026 the per-platform archives of release 1.19.2 at
github.com/microsoft/onnxruntime cannot be downloaded. Software that pins these
exact files downloads them from here instead.

## Release v1.19.2

| Asset | Platform | Library inside | SHA-256 of the library |
|---|---|---|---|
| `onnxruntime-osx-x86_64-1.19.2.tgz` | macOS, Intel (x86_64) | `lib/libonnxruntime.1.19.2.dylib` | `386c781370f99636b9218f9b7db3aa53e95af53e363dc279fe250709ad897b9f` |
| `onnxruntime-linux-x64-1.19.2.tgz` | Linux, x86_64 | `lib/libonnxruntime.so.1.19.2` | `9c8139e1856568f068f1cad78fc9798084941db50be7c201a1dbdcfd18105433` |
| `onnxruntime-linux-aarch64-1.19.2.tgz` | Linux, aarch64 | `lib/libonnxruntime.so.1.19.2` | `d9abfb42ddd120855f93ccb3c97a0918ac5bef209485db0dc3a36a3d188671ab` |

SHA-256 of the archives: `SHA256SUMS`. Each archive holds `LICENSE`,
`ThirdPartyNotices.txt`, `VERSION_NUMBER`, `README.md` and `lib/`.

## What is changed and what is not

* **Library bytes: unchanged.** No strip, patchelf, install_name_tool, lipo,
  code signing or rebuild. The macOS library is unsigned, as Microsoft
  published it.
* **File name: ours.** The Maven archive calls every library
  `libonnxruntime.so` or `libonnxruntime.dylib`. Here they carry the names
  Microsoft used in its own per-platform archives of this release:
  `libonnxruntime.so.1.19.2` (its SONAME is `libonnxruntime.so.1`) and
  `libonnxruntime.1.19.2.dylib` (its install name is
  `@rpath/libonnxruntime.1.19.2.dylib`), plus symbolic links.
* **Archive layout: ours.** Not included: headers, CMake and pkg-config files
  of Microsoft's original archives; Java classes, JNI libraries, debug symbols
  and the Apple-silicon library of the Maven archive.

## Where the bytes come from

Maven Central, `com.microsoft.onnxruntime:onnxruntime:1.19.2`, file
`onnxruntime-1.19.2.jar` (93,522,952 bytes):

* SHA-256 `ddab9113a453c0200ac16caf308b76bc8e84653ddc11969983b783dff34397b2`
* SHA-1 `b54699472d9ead8dc3d58d834457d03b815124a9`
* signature `onnxruntime-1.19.2.jar.asc`, key
  `369E 7711 78C4 1DE2 6253 F280 E963 73C2 5092 C07A`
  ("ONNX Runtime <onnxruntime@microsoft.com>")

The libraries are the jar entries
`ai/onnxruntime/native/{osx-x64,linux-x64,linux-aarch64}/libonnxruntime.*`;
`ThirdPartyNotices.txt` is the jar's own. The jar does not contain the licence
text (its pom names the MIT License); `LICENSE` here is the file from
Microsoft's original `onnxruntime-linux-x64-1.19.2.tgz`.

To check: download the jar from
https://repo1.maven.org/maven2/com/microsoft/onnxruntime/onnxruntime/1.19.2/ ,
verify it (`gpg --verify onnxruntime-1.19.2.jar.asc onnxruntime-1.19.2.jar`),
unzip it and compare SHA-256 with the table above — or run `repack.py` on it,
which rebuilds the three archives byte for byte.

## Source code

* ONNX Runtime 1.19.2 is revision `ffceed9d44f2f3efb9dd69fa75fea51163c91d91`
  of microsoft/onnxruntime, archived at
  https://archive.softwareheritage.org/browse/revision/ffceed9d44f2f3efb9dd69fa75fea51163c91d91/
* Eigen, compiled into these libraries under the Mozilla Public License 2.0,
  is revision `e7248b26a1ed53fa030c5c459f7ea095dfd276ac` of
  https://gitlab.com/libeigen/eigen . A copy of that source is attached to
  release v1.19.2 as `eigen-e7248b26a1ed53fa030c5c459f7ea095dfd276ac.zip`.
* Every other third-party component and its licence: `ThirdPartyNotices.txt`.

## Licence

ONNX Runtime: MIT licence, Copyright (c) Microsoft Corporation — see `LICENSE`.
Its third-party components: `ThirdPartyNotices.txt`.
The files written for this repository (`README.md`, `SHA256SUMS`, `repack.py`)
are dedicated to the public domain under CC0-1.0.
ONNX is a trademark of LF Projects, LLC. ONNX Runtime is a Microsoft project.
Names are used only to identify the software in this copy.

