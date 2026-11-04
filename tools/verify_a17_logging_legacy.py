#!/usr/bin/env python3
"""Archived PE Android14 logging source inventory — not a CTS or device test."""
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[1]

def chk(ok,msg):
    if not ok: raise AssertionError(msg)
    print("PASS archived logging source:",msg)

try:
    props=(ROOT/"liblog/properties.cpp").read_text()
    bp=(ROOT/"liblog/Android.bp").read_text()
    cat=(ROOT/"logcat/logcat.cpp").read_text()
    logd=(ROOT/"logd/main.cpp").read_text()
    logdbp=(ROOT/"logd/Android.bp").read_text()
    rust=(ROOT/"rust/Android.bp").read_text()
    mapping=json.loads((ROOT/"TEST_MAPPING").read_text())
    chk("int __android_log_is_debuggable()" in props and "if (ANDROID_DEBUGGABLE)" in props,
        "archived PE debugger property behavior")
    chk('"-DANDROID_DEBUGGABLE=0"' in bp and '"-DANDROID_DEBUGGABLE=1"' in bp,
        "archived Soong debug build-type controls")
    chk("case 'C':" in cat and 'SetLogFormat("color")' in cat and '"color"' in cat,
        "legacy logcat -C and --color alias")
    chk("GetBoolPropertyEngSvelteDefault" in logd and "GetBoolPropertyDebuggableSvelteDefault" in logd
        and '"logd.statistics"' in logd and '"ro.logd.kernel"' in logd,
        "old logd statistics/klog build-type gates")
    chk('name: "logd"' in logdbp and '"logd.rc"' in logdbp,
        "old logd binary and init source")
    chk('name: "liblogger"' in rust and '"liblog_rust"' in rust,
        "old Rust liblogger integration existed before AOSP17")
    tests={item["name"] for item in mapping.get("presubmit",[])}
    chk({"CtsLiblogTestCases","CtsLogdTestCases"}.issubset(tests),
        "old logging CTS mapping")
    print("PASS: historical source markers only; no changes to security, release logging or Android17 build.")
except (AssertionError,OSError,ValueError) as exc:
    print("FAIL:",exc,file=sys.stderr)
    sys.exit(1)
