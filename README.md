# HeckerOS for Google Pixel 4 (Flame)

Android 17 build integration for `hecker_flame-hecker_suite-userdebug`. Flame uses
the shared HeckerOS feature sources with its own retained hardware, framework and kernel pins: native Suite,
Hecker/One UI Quick Settings, launcher/Pixel Recents, GameSpace/popup apps and charging
controls, Dolby, GCam, LibrePods, 3D Face Unlock, Motion Sense, charging/AOD, lyrics,
NetLab, Spoofing hub, App Lock, customization and boot/recovery branding. Existing
Coral limitations still apply; the first full Flame build and phone validation
remain pending.

## Shared status-bar feature sources

This feature branch selects shared status-bar lyrics and optional dual rows on top
of Living Flow clocks, wake blur and Hecker QS. Both new switches default off under
Hecker Suite → Status bar. LRCLIB fetching/cache/media timing is shared with the
independent lock-screen switch and continues while unlocked. Native 44/52/60 dp
height overlays update app/SystemUI insets; row spacing, icon size and lyric
alignment/width/font/colour/fade/marquee are configurable.

The original Flame device, vendor, framework and kernel selections remain intact.
The normal and optional non-KSU manifests select the same new Suite revision.
Provider/layout/overlay host checks, locked SDK/Compose and the Flame framework
adapter checks pass. Full ROM builds and physical Flame acceptance remain pending.
See [controls, implementation and device checks](https://github.com/its-hecker/HeckerOS/blob/feat/statusbar-lyrics-dual-20261029/docs/statusbar-lyrics-dual.md).

## Complete build from mkdir

Start in a separate source directory with the same Android 17 prerequisites as Coral:
Git LFS, Python 3.12+, Java 21+, Pillow and numpy. Use the provider's initialized
Byobu/RBE environment if building on ServerHive.

```bash
mkdir -p ~/heckeros-flame &&
cd ~/heckeros-flame &&
git lfs install &&
repo init -u https://github.com/its-hecker/HeckerOS.git -b feat/suite-polish --git-lfs &&
git clone --branch feat/statusbar-lyrics-dual-20261029 --single-branch https://github.com/its-hecker/HeckerOs-Flame-localmanifest.git .repo/local_manifests &&
repo sync -c -j8 --fail-fast --no-clone-bundle --no-tags &&
HECKER_DEVICE=flame HECKER_BUILD_VARIANT=userdebug HECKER_BUILD_JOBS=8 bash .repo/local_manifests/build.sh
```

Copy the entire block in the initialized build shell. The `&&` chain stops
at the first failure; the helper performs environment setup, target selection,
preparation and compilation. Keep ServerHive's existing RBE settings.

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
| Kernel | Shared Floral kernel; this branch's exact pin is recorded in `floral.xml` |
| Features | Shared `its-hecker/HeckerOS` on `feat/statusbar-lyrics-dual-20261029`, retaining Flame's existing dependency pins |

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

## Pakistan IMS test configuration

This manifest pins the shared Suite with VoLTE/Wi-Fi Calling defaults and
dedicated IMS APNs for Jazz/Warid, Ufone, Zong and Telenor. Independent icon
switches are under Hecker Suite > Status bar > Calling indicators; icons follow
actual IMS voice registration and availability for each SIM.

Source, SDK and host checks pass. Working calls and a compatible Pakistan modem
profile remain unverified; rebuild and test the individual SIMs before marking
a carrier as supported. See the [IMS implementation and device checks](https://github.com/its-hecker/HeckerOS/blob/b976e56ce5458e74db7a854a023611c92d374f50/ims/README.md).
