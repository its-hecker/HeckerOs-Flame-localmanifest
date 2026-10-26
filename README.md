# HeckerOS for Google Pixel 4 (Flame)

Android 17 build integration for `hecker_flame-hecker_suite-userdebug`. Flame uses
the same current HeckerOS feature sources and platform pins as Coral: native Suite,
Hecker/One UI Quick Settings, launcher/Pixel Recents, GameSpace/popup apps and charging
controls, Dolby, GCam, LibrePods, 3D Face Unlock, Motion Sense, charging/AOD, lyrics,
NetLab, Spoofing hub, App Lock, customization and boot/recovery branding. Existing
Coral limitations still apply; the first full Flame build and phone validation
remain pending.

## Sync and build

Start in a separate source directory with the same Android 17 prerequisites as Coral:
Git LFS, Python 3.12+, Java 21+, Pillow and numpy. Use the provider's initialized
Byobu/RBE environment if building on ServerHive.

```bash
mkdir -p ~/heckeros-flame
cd ~/heckeros-flame
repo init -u https://github.com/its-hecker/HeckerOS -b feat/suite-polish --git-lfs
git clone --branch main https://github.com/its-hecker/HeckerOs-Flame-localmanifest .repo/local_manifests
repo sync -c -j8 --fail-fast --no-clone-bundle --no-tags
HECKER_BUILD_JOBS=8 bash .repo/local_manifests/build.sh
```

The helper defaults to Flame, fetches its radio images through the preserved upstream
LFS endpoint, prepares the same guarded feature adapters as Coral, selects
`hecker_flame-hecker_suite-userdebug` and runs `m heckeros`. Installed output is checked
under `out/target/product/flame`. Later builds use:

```bash
HECKER_BUILD_JOBS=8 bash .repo/local_manifests/build.sh
```

## Hardware and feature sources

| Component | Selection |
| --- | --- |
| Shared device tree | `its-hecker/heckeros-floral-devicetree`, branch `flame`, path `device/google/coral` |
| Flame hardware variant | Original `flame/` configuration: 1080x2280, 440 dpi, Flame overlays/audio/thermal/CHRE |
| Vendor | `its-hecker/HeckerOs-Flame-vendor`, path `vendor/google/flame` |
| Kernel | Same exact Floral kernel and KernelSU submodule pin as Coral |
| Features | Shared `its-hecker/HeckerOS` on `feat/suite-polish`, with the same framework/Settings/plugins/Dolby pins as Coral |

`device/google/coral` is the common source directory for both phones and remains
that path for Flame. The Flame branch selects a `-flame` camera build module, retains
its stock executable/init/VINTF identity and includes the same ROM policy as Coral.
The vendor import preserves the original Flame proprietary files and radio pointers,
adding the camera/init and eight FaceID install-ownership fixes used on Coral.

`floral.xml` pins the complete dependency graph, including the reviewed Suite revision.
`source-revisions.json` records provenance. Update the pins deliberately when bringing
in later Coral features; do not replace Flame's vendor with the Coral vendor.

## Checks and first boot

```bash
python3 tools/validate.py
bash -n build.sh
python3 -m unittest discover -s tests -p 'test_*.py'
```

Source checks validate manifest pins, helper routing and build regressions. Product
inheritance is tested in the shared HeckerOS repository. These checks do not compile
or boot Android. Test display, touch, cameras/infrared, Face Unlock, Soli, mobile radio,
Wi-Fi/Bluetooth, audio, thermal/charging behavior, GameSpace/bypass/popup apps,
launcher/Recents, Quick Settings, AOD and Suite features after the first full build.

[Detailed Flame notes](https://github.com/its-hecker/HeckerOS/blob/feat/suite-polish/docs/flame-bringup.md)
