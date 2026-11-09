# HeckerOS smoothness test for Google Pixel 4 (Flame)

This branch builds `hecker_flame-hecker_suite-userdebug` from the Coral stable
feature baseline. It includes HeckerVault, WireGuard with a scrollable test log,
the Material You headphone popup, grouped navigation settings, the Motion Sense
companion, app compatibility and the Google-signed SIM Manager update.

The shared SystemUI source includes quicker Quick Settings dismissal. The kernel
and KernelSU use Coral's stable pins. The device
tree retains Flame's camera provider and panel configuration, including the
60 Hz low-brightness zone. The vendor retains Flame's firmware and radio images.
The Motion Sense and FaceID pins use their existing plugin branches.

## Build from a fresh directory

Use an initialized ServerHive RBE shell with Repo, Git LFS, Python 3.12+,
Java 21+, Pillow and NumPy.

```bash
mkdir -p ~/heckeros-flame-smoothness &&
cd ~/heckeros-flame-smoothness &&
repo init -u https://github.com/its-hecker/HeckerOS.git -b perf/flame-smoothness --git-lfs &&
git clone --branch perf/flame-smoothness --single-branch https://github.com/its-hecker/HeckerOs-Flame-localmanifest.git .repo/local_manifests &&
repo sync -c --fail-fast --no-clone-bundle --no-tags &&
env -u HECKER_BUILD_JOBS USE_RBE=true HECKER_DEVICE=flame HECKER_BUILD_VARIANT=userdebug bash .repo/local_manifests/build.sh
```

Build output goes to `out/target/product/flame/`. The helper verifies pinned
sources and the KernelSU submodule, fetches and checks all 11 Flame radio images,
prepares the ROM, builds the target and checks the installed files.

## Source branches

| Component | Branch and checkout |
| --- | --- |
| Suite and Repo manifest | `HeckerOS` on `perf/flame-smoothness` |
| Local manifest | `HeckerOs-Flame-localmanifest` on `perf/flame-smoothness` |
| Device tree | `heckeros-floral-devicetree` on `flame-cnb_latest_stable` at `device/google/coral` |
| Vendor | `HeckerOs-Flame-vendor` on `cnb_latest_stable` at `vendor/google/flame` |

`floral.xml` records the exact dependency commits. `source-revisions.json`
records the Coral baseline and Flame integration.

## Source checks and first boot

```bash
python3 tools/validate.py
bash -n build.sh
python3 -m unittest discover -s tests -p 'test_*.py'
```

Full ROM compilation and on-device verification are pending. Check boot, display,
cameras, Soli, Face Unlock, eSIM setup, mobile radio, Wi-Fi and Bluetooth on Flame
before promoting this branch to the default. Motion feedback is available under
HeckerLab → Status bar. The shared Pakistan IMS defaults retain the Jazz/Warid,
Ufone, Zong and Telenor APNs, with working calls subject to device and carrier
testing.
