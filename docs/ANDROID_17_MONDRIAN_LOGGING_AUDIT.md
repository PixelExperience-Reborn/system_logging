# P1 — Android17 system/logging: liblog, logcat, logd and security/boot audit

Date: 2026-11-04. **Historical source audit only; no ROM change, no log-access bypass and no physical mondrian test.**

## Provenance and build scope

- Archived PixelExperience-Reborn `system_logging` branch `seventeen`, revision `588953ea54b66450a90b9fd77be586d62ddf2f3c`, merges Android14 r21 on 2024-01-30. Not an Android17 production branch.
- Official AOSP17 r1 `platform/system/logging` exact Git tree `2d287c1e04ae4ebd59b12f1b1aabcfa1f0fb8db4`: https://android.googlesource.com/platform/system/logging/+/refs/tags/android-17.0.0_r1/ .
- Official Android17 contains `liblog`, `logcat`, `logd`, `logwrapper`, `rust`, with modern `logd/binder`, `logd/flags`, `liblog/rust` integration. The staged manifest retains the official `system/logging` repository. `liblog` symbols and `logd` behavior are shared by nearly every Android service.

## Relevant historical PE changes

| Commit | Archived behavior | Decision for Android17 |
| --- | --- | --- |
| `0ddc2b54ad31df39be7a95c33d40c1bdbc5d9020` (2020) | `liblog/properties.cpp` `__android_log_is_debuggable` uses `ANDROID_DEBUGGABLE` compile flag (return 1 in userdebug/eng), falls back to `ro.debuggable`; archived `liblog/Android.bp` sets `-DANDROID_DEBUGGABLE=0` and switches to 1 for debuggable product | **NO BLIND PORT**. AOSP17 build flags and debug control must be checked; do not make `user` releases report debuggable or leak sensitive logging. Follow upstream `liblog` and property access rules. |
| `417d952aadf386aeddefdf639bc9c92ea5b6fb8a` (2015) | `logcat -C` alias to `-v color`, with `--color` option and `SetLogFormat("color")` | **LOW PRIORITY** UI/diagnostics only; compare AOSP17 logcat option parsing first. Not a reason to replace logging subsystem. |
| `85d89819f56fc4b2bd2df04f4a8c9a61baed2d4a` (2023) | Historical upstream `DO NOT MERGE` log-statistics gating: `logd.statistics` enablement defaults to eng vs userdebug, while `ro.logd.kernel` can still depend on debuggable property | **SECURITY/PERF REVIEW**. This is historical AOSP development, not automatically PE-original. Do not disable logging/stats or suppress dropped-log diagnostics to improve benchmarks. Review Android17 `LogStatistics` and flag implementation. |

Other sampled history merges upstream Android14 logging changes such as dropped-log integration tests, audit log spacing, binary flush and `logcat` help. **Do not count upstream merged changes as custom PE features.**

## Platform and security requirements

- Keep official Android17 logging on `/dev/socket/logdw`/`logdr`, `liblog` and `logd` with the correct init, logging UID/group, kernel/audit logs, log buffers and SELinux. Treat unprivileged access restrictions and role permissions as security boundaries.
- Preserve log reproducibility for bring-up: verified `logcat -b all`, `dmesg` permissions and collecting logs from failed boot phases. Do not enable global verbose logging in release images or make security-restricted entries public.
- Review compatibility of `liblog` LLNDK/VNDK or vendor logging interface, static/shared variants, Rust logger, APEX visibility and `logd` flags against the actual Android17 Soong graph. Avoid mixed Android14/17 `liblog.map.txt` symbol ABI.
- Verify logd buffer sizes, filtering, pstore persistence, audit logging and crash/dropped-log reporting. Never fake successful init or mask service crashes. `logcat -C` is diagnostic convenience and must not alter actual priorities/read access.
- The new PE-Reborn Android17 **mondrian and sm8450-common trees must be independently authored**. Existing LF52406 LineageOS-based trees are hardware references only. If the device uses a vendor custom logging daemon, review its actual ELF dependencies and SELinux separately.
- Tests: `CtsLiblogTestCases`, `CtsLogdTestCases`, `logd_integration_test` where applicable, logcat host/unit tests, audit/SELinux and pstore pre/post reboot. Verify both user and userdebug build types; check that sensitive logs remain private.
- No Android17 Soong build or physical device tests have been run.

## Current result and gates

- [x] Archived old-source commit lineage and potential debug/logcat deltas identified.
- [x] Official AOSP17 r1 root Git tree and modern logging module directories identified.
- [x] Historical source regression and official pinned-tag source checks authored.
- [ ] Full Android17 `liblog`/`logd`/`logcat` Soong, Rust, APEX, CTS and linker ABI tests.
- [ ] Kernel/audit/pstore/SELinux and privacy behavior verified on a native PE-Reborn mondrian image.

**Decision:** keep official Android17 `system/logging` in staged manifest. No debug-property override, old logd behavior or legacy `logcat` fork activated.
