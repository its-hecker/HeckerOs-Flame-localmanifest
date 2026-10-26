#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Run from a separate, synced non-KSU Android source checkout.
set -eo pipefail
export HECKER_DEVICE="${HECKER_DEVICE:-flame}"
if [[ "$HECKER_DEVICE" != flame ]]; then
    echo "This manifest builds flame; use the matching device manifest." >&2
    exit 1
fi
if [[ -z "${HECKER_KSU_PRODUCT_OUT:-}" ]]; then
    echo "Set HECKER_KSU_PRODUCT_OUT to the matching rooted ROM's out/target/product/$HECKER_DEVICE." >&2
    exit 1
fi
export OUT_DIR="${HECKER_NONKSU_OUT_DIR:-out-nonksu}"
python3 - "$OUT_DIR" "$HECKER_KSU_PRODUCT_OUT" "$HECKER_DEVICE" <<'PY_GUARD'
from pathlib import Path
import sys
nonksu = Path(sys.argv[1]).resolve()
baseline = Path(sys.argv[2]).resolve()
if baseline.parts[-3:] != ("target", "product", sys.argv[3]):
    raise SystemExit("Use the matching target/product/<device> baseline directory")
normal = baseline.parents[2]
if nonksu == normal or nonksu.is_relative_to(normal) or normal.is_relative_to(nonksu):
    raise SystemExit("Use separate normal and non-KSU output directories")
PY_GUARD
python3 kernel/google/msm-4.14/tools/hecker/verify_nonksu.py --source-root kernel/google/msm-4.14
python3 kernel/google/msm-4.14/tools/hecker/package_boot.py \
    --preflight --device "$HECKER_DEVICE" --rooted-out "$HECKER_KSU_PRODUCT_OUT"
export HECKER_NONKSU_BOOT_ONLY=true
nonksu_setup_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$nonksu_setup_dir/build.sh" "$@"
