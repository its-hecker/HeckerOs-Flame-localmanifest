# SPDX-License-Identifier: Apache-2.0
"""Keep optional boot builds separate and route the matching baseline/device."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
XML = ET.parse(ROOT / "floral.xml").getroot()
DEVICE = "flame" if XML.find("project[@path='vendor/google/flame']") is not None else "coral"


class NonKsuBootHelperTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.rom = Path(self.tmp.name)
        local = self.rom / "local"
        local.mkdir()
        self.helper = local / "build-nonksu-boot.sh"
        shutil.copy2(ROOT / self.helper.name, self.helper)
        (local / "build.sh").write_text(
            '#!/bin/bash\nprintf "%s\\n" "$HECKER_DEVICE|$OUT_DIR|$HECKER_NONKSU_BOOT_ONLY|$*"\n')
        tools = self.rom / "kernel/google/msm-4.14/tools/hecker"
        tools.mkdir(parents=True)
        (tools / "verify_nonksu.py").write_text(
            'import sys\nassert sys.argv[1:] == ["--source-root", "kernel/google/msm-4.14"]\n')
        (tools / "package_boot.py").write_text(
            'import sys\nassert "--preflight" in sys.argv\nprint("BASELINE_OK")\n')
        self.baseline = self.rom / "normal-out/target/product" / DEVICE
        self.baseline.mkdir(parents=True)
        self.output = self.rom / "nonksu-out"
        self.env = dict(os.environ, HECKER_DEVICE=DEVICE,
                        HECKER_KSU_PRODUCT_OUT=str(self.baseline), HECKER_NONKSU_OUT_DIR=str(self.output))

    def run_helper(self):
        return subprocess.run(["bash", str(self.helper), "--offline"], cwd=self.rom,
                              env=self.env, capture_output=True, text=True)

    def test_routes_preflight_and_preserves_device_mode_arguments(self):
        result = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("BASELINE_OK", result.stdout)
        self.assertIn(f"{DEVICE}|{self.output}|true|--offline", result.stdout)

    def test_missing_baseline_stops_before_preparation(self):
        self.env.pop("HECKER_KSU_PRODUCT_OUT")
        result = self.run_helper()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Set HECKER_KSU_PRODUCT_OUT", result.stderr)
        self.assertNotIn("BASELINE_OK", result.stdout)

    def test_overlapping_build_outputs_are_refused(self):
        for output in (self.rom / "normal-out", self.rom / "normal-out/child", self.rom):
            with self.subTest(output=output):
                self.env["HECKER_NONKSU_OUT_DIR"] = str(output)
                result = self.run_helper()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("separate normal and non-KSU", result.stderr)
                self.assertNotIn("BASELINE_OK", result.stdout)

    def test_other_device_is_refused(self):
        self.env["HECKER_DEVICE"] = "flame" if DEVICE == "coral" else "coral"
        result = self.run_helper()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("matching device manifest", result.stderr)

    def test_baseline_directory_must_belong_to_the_selected_device(self):
        self.env["HECKER_KSU_PRODUCT_OUT"] = str(self.rom / "normal-out/target/product/wrong")
        result = self.run_helper()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("target/product/<device>", result.stderr)


if __name__ == "__main__":
    unittest.main()
