# HeckerOS non-KSU boot build — Pixel 4 (`flame`)

This `nonksu` branch selects the optional
[Floral kernel without KernelSU Next](https://github.com/its-hecker/HeckerOsfloral-Kernel-NonKsu).
The normal manifest branch continues selecting the regular KSU kernel. Every other
platform, device, vendor, plugin and Suite selection is retained from this device's
normal manifest. KernelSU Next and SUSFS are removed; the non-root kernel code,
configuration and GameSpace charging driver are preserved.

## Build the optional image

First build the normal HeckerOS ROM and retain its complete output. Use a separate
Android source checkout for the non-KSU build, with the **same release source pins,
build configuration and signing settings**. Use the initialized provider/Byobu/RBE
session and the normal Android 17 prerequisites, Git LFS, Python, Java, Pillow and numpy.

```bash
mkdir -p ~/heckeros-flame-nonksu
cd ~/heckeros-flame-nonksu
repo init -u https://github.com/its-hecker/HeckerOS -b feat/suite-polish --git-lfs
git clone --branch nonksu https://github.com/its-hecker/HeckerOs-Flame-localmanifest .repo/local_manifests
repo sync -c -j8 --fail-fast --no-clone-bundle --no-tags
HECKER_KSU_PRODUCT_OUT=~/heckeros-flame/out/target/product/flame \
  HECKER_BUILD_JOBS=8 bash .repo/local_manifests/build-nonksu-boot.sh
```

Set `HECKER_KSU_PRODUCT_OUT` to the normal build's actual `target/product/flame`
directory. The helper requires its boot image, properties, kernel config, release
and Module.symvers. It uses a separate `out-nonksu` directory; optionally override
it with `HECKER_NONKSU_OUT_DIR`. It refuses overlapping normal/non-KSU outputs.

The existing feature preparation runs normally, followed by Android's `bootimage`
target. Android handles the original recovery-as-boot, DTB, boot header and AVB
packaging. After compilation, the release check verifies root absence, the device,
boot metadata/DTB, the actual packaged kernel and compatibility of every non-root
exported module CRC and the kernel release with the normal ROM.

On success, the normal ROM output's `nonksu-release/` directory contains:

- `HeckerOS_flame_NonKSU_boot_<hash>.img`;
- JSON provenance tying the image to the baseline ROM fingerprint and kernel revisions;
- SHA-256 checksums.

If ABI checks fail, no boot-only release is prepared. Investigate the mismatch or
build a complete consistent non-KSU ROM/module set. Running this branch's ordinary
`build.sh` builds a complete non-KSU ROM in the separate output directory; use
`build-nonksu-boot.sh` for the optional image intended to accompany the normal ROM.

## Kernel layout and compatibility

The device tree stays at `device/google/coral`, the kernel at `kernel/google/msm-4.14`
and the vendor at `vendor/google/flame`. There is no KernelSU submodule to sync.
Use a fresh checkout so an old populated root submodule is not left in the kernel.

Flame and Coral share kernel source. A complete boot image also contains recovery,
a ramdisk and build/device metadata. Distribute **one matching image per device and
ROM release** until actual output comparison and testing prove a shared boot works.
Rebuild the optional image for each ROM release. Root-dependent Suite operations
remain subject to their existing privilege requirements.

## Validation

```bash
python3 tools/validate.py
bash -n build.sh build-nonksu-boot.sh
python3 -m unittest discover -s tests -p 'test_*.py'
```

Source and host checks cover root removal, configuration, preserved charging code,
boot packaging rejection cases and build separation. They do not compile or boot
Android. The first target ARM64 kernel/boot build, real module ABI comparison and
phone acceptance remain required. `floral.xml` and `source-revisions.json` retain the
immutable source selections and provenance.
