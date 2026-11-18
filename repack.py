#!/usr/bin/env python3
# Rebuilds the three archives of release v1.19.2 of github.com/Seventhwalllab/onnxruntime,
# byte for byte, from Microsoft's Maven archive.
#
#   python3 repack.py onnxruntime-1.19.2.jar LICENSE out/
#
# onnxruntime-1.19.2.jar: Maven Central com.microsoft.onnxruntime:onnxruntime:1.19.2
# LICENSE: the LICENSE file of this repository (Microsoft's MIT text; the jar has none)
# Library bytes are copied unchanged; only file names, links, README and layout are ours.
# CC0-1.0.
import gzip
import hashlib
import io
import os
import sys
import tarfile
import zipfile

JAR_SHA256 = "ddab9113a453c0200ac16caf308b76bc8e84653ddc11969983b783dff34397b2"
MTIME = 1725060000  # 2024-08-30, the date of the entries in the Maven archive

PLATFORMS = [
    # archive platform, human name, jar dir, jar file, our file name, links (name -> target)
    ("osx-x86_64", "macOS on Intel (x86_64)", "osx-x64", "libonnxruntime.dylib",
     "libonnxruntime.1.19.2.dylib", [("libonnxruntime.dylib", "libonnxruntime.1.19.2.dylib")]),
    ("linux-x64", "Linux on x86_64", "linux-x64", "libonnxruntime.so",
     "libonnxruntime.so.1.19.2", [("libonnxruntime.so.1", "libonnxruntime.so.1.19.2"),
                                  ("libonnxruntime.so", "libonnxruntime.so.1")]),
    ("linux-aarch64", "Linux on aarch64", "linux-aarch64", "libonnxruntime.so",
     "libonnxruntime.so.1.19.2", [("libonnxruntime.so.1", "libonnxruntime.so.1.19.2"),
                                  ("libonnxruntime.so", "libonnxruntime.so.1")]),
]

README = """ONNX Runtime 1.19.2 by Microsoft — unmodified copy

This archive holds Microsoft's ONNX Runtime 1.19.2 shared library for
{platform} exactly as Microsoft built it, byte for byte, with Microsoft's MIT
LICENSE and the release's ThirdPartyNotices.txt. It is not affiliated with or
endorsed by Microsoft.

Ours: the file name of the library (the name Microsoft used in its own
archives of this release), the symbolic links, this README and the layout.
Nothing else.

Library:   lib/{name}
SHA-256:   {lib_sha}
Bytes:     Maven Central, com.microsoft.onnxruntime:onnxruntime:1.19.2,
           onnxruntime-1.19.2.jar (SHA-256
           {jar_sha}),
           entry ai/onnxruntime/native/{jar_dir}/{jar_file}
Notices:   ThirdPartyNotices.txt from the same jar, unchanged.
LICENSE:   from Microsoft's original onnxruntime-linux-x64-1.19.2.tgz (the jar
           does not carry the text; its pom names the MIT License).

Source code:
  ONNX Runtime 1.19.2 — revision ffceed9d44f2f3efb9dd69fa75fea51163c91d91,
    https://archive.softwareheritage.org/browse/revision/ffceed9d44f2f3efb9dd69fa75fea51163c91d91/
  Eigen (MPL-2.0), compiled into this library — revision
    e7248b26a1ed53fa030c5c459f7ea095dfd276ac, https://gitlab.com/libeigen/eigen ;
    a copy is attached to
    https://github.com/Seventhwalllab/onnxruntime/releases/tag/v1.19.2
  Other components — see ThirdPartyNotices.txt.
"""


def info(name, size=0, mode=0o644):
    ti = tarfile.TarInfo(name)
    ti.size, ti.mtime, ti.mode = size, MTIME, mode
    ti.uid = ti.gid = 0
    ti.uname = ti.gname = ""
    return ti


def main(jar_path, license_path, out_dir):
    jar_bytes = open(jar_path, "rb").read()
    if hashlib.sha256(jar_bytes).hexdigest() != JAR_SHA256:
        sys.exit("not the Maven onnxruntime-1.19.2.jar (SHA-256 differs)")
    licence = open(license_path, "rb").read()
    os.makedirs(out_dir, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(jar_bytes)) as jar:
        notices = jar.read("ThirdPartyNotices.txt")
        for plat, human, jar_dir, jar_file, name, links in PLATFORMS:
            lib = jar.read(f"ai/onnxruntime/native/{jar_dir}/{jar_file}")
            lib_sha = hashlib.sha256(lib).hexdigest()
            readme = README.format(platform=human, name=name, lib_sha=lib_sha,
                                   jar_sha=JAR_SHA256, jar_dir=jar_dir,
                                   jar_file=jar_file).encode("utf-8")
            top = f"onnxruntime-{plat}-1.19.2"
            raw = io.BytesIO()
            with tarfile.open(fileobj=raw, mode="w", format=tarfile.USTAR_FORMAT) as t:
                for fname, data, mode in (("LICENSE", licence, 0o644),
                                          ("ThirdPartyNotices.txt", notices, 0o644),
                                          ("README.md", readme, 0o644),
                                          ("VERSION_NUMBER", b"1.19.2\n", 0o644),
                                          ("lib/" + name, lib, 0o755)):
                    t.addfile(info(f"{top}/{fname}", len(data), mode), io.BytesIO(data))
                for link, target in links:
                    ti = info(f"{top}/lib/{link}", 0, 0o777)
                    ti.type, ti.linkname = tarfile.SYMTYPE, target
                    t.addfile(ti)
            path = os.path.join(out_dir, top + ".tgz")
            with open(path, "wb") as f, gzip.GzipFile(filename="", mode="wb", fileobj=f,
                                                       mtime=MTIME, compresslevel=9) as g:
                g.write(raw.getvalue())
            arch_sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
            print(f"{arch_sha}  {top}.tgz  (library {lib_sha})")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__ or "usage: repack.py onnxruntime-1.19.2.jar LICENSE out/")
    main(*sys.argv[1:])
