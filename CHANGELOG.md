# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [1.0.6](https://github.com/pawamoy/failprint/releases/tag/1.0.6) - 2025-08-15

<small>[Compare with 1.0.5](https://github.com/pawamoy/failprint/compare/1.0.5...1.0.6)</small>

### Build

- Use top-level entrypoint, not deprecated one in cli module ([486fe50](https://github.com/pawamoy/failprint/commit/486fe50b55863ccb76ab7faebce649b1bca1859c) by Timothée Mazzucotelli).

## [1.0.5](https://github.com/pawamoy/failprint/releases/tag/1.0.5) - 2025-07-22

<small>[Compare with 1.0.4](https://github.com/pawamoy/failprint/compare/1.0.4...1.0.5)</small>

### Bug Fixes

- Avoid name-shadowing in lazy module ([8abac02](https://github.com/pawamoy/failprint/commit/8abac021d60c533ebb7bb34e02b16bbc3013682b) by Timothée Mazzucotelli).

## [1.0.4](https://github.com/pawamoy/failprint/releases/tag/1.0.4) - 2025-07-15

<small>[Compare with 1.0.3](https://github.com/pawamoy/failprint/compare/1.0.3...1.0.4)</small>

### Code Refactoring

- Export and document every public object ([c7ad841](https://github.com/pawamoy/failprint/commit/c7ad841167233a19dac12864ced8ddc43e0e8ea2) by Timothée Mazzucotelli).
- Move modules into internal folder ([55066db](https://github.com/pawamoy/failprint/commit/55066dbfc69ab04b5f4258adf308239bfc77cf68) by Timothée Mazzucotelli).

## [1.0.3](https://github.com/pawamoy/failprint/releases/tag/1.0.3) - 2024-10-17

<small>[Compare with 1.0.2](https://github.com/pawamoy/failprint/compare/1.0.2...1.0.3)</small>

### Build

- Drop support for Python 3.8 ([a212375](https://github.com/pawamoy/failprint/commit/a212375c913bc2d883e50349b8471b2c99120f02) by Timothée Mazzucotelli).

## [1.0.2](https://github.com/pawamoy/failprint/releases/tag/1.0.2) - 2023-09-18

<small>[Compare with 1.0.1](https://github.com/pawamoy/failprint/compare/1.0.1...1.0.2)</small>

### Bug Fixes

- Escape contents in command and output, to prevent interpretation by ansimarkup ([0dbcb51](https://github.com/pawamoy/failprint/commit/0dbcb51d75263c3c7d47363016eabd822299a854) by Timothée Mazzucotelli).

## [1.0.1](https://github.com/pawamoy/failprint/releases/tag/1.0.1) - 2023-07-29

<small>[Compare with 1.0.0](https://github.com/pawamoy/failprint/compare/1.0.0...1.0.1)</small>

### Bug Fixes

- Don't hang on large output ([60b220f](https://github.com/pawamoy/failprint/commit/60b220f55084083ca676c88a06cf233bbf22ed30) by Timothée Mazzucotelli).

## [1.0.0](https://github.com/pawamoy/failprint/releases/tag/1.0.0) - 2023-07-27

<small>[Compare with 0.11.1](https://github.com/pawamoy/failprint/compare/0.11.1...1.0.0)</small>

## Breaking changes

- `failprint.runners.run_function_get_code(stderr)` parameter was removed.
- `failprint.capture.cast_capture` was removed. Use [Capture.cast][failprint.Capture.cast] instead.
- `failprint.capture.StdBuffer` was removed. Use [CaptureManager][failprint.CaptureManager] instead.
- `failprint.capture.stdbuffer` was removed. Use [Capture.here][failprint.Capture.here] instead.

### Features

- Capture standard output/error at the file descriptor level ([0fbb2d4](https://github.com/pawamoy/failprint/commit/0fbb2d4ba4d2166224e1725b73dfb20a6422bd01) by Timothée Mazzucotelli). [Issue #17](https://github.com/pawamoy/failprint/issues/17), [Issue markdown-exec#21](https://github.com/pawamoy/markdown-exec/issues/21)

### Code Refactoring

- Reduce PTY delays to speed up code and tests suite ([de543c8](https://github.com/pawamoy/failprint/commit/de543c84f40e7204166e165601c0f4e5c448824b) by Timothée Mazzucotelli).

## [0.11.1](https://github.com/pawamoy/failprint/releases/tag/0.11.1) - 2023-04-10

<small>[Compare with 0.11.0](https://github.com/pawamoy/failprint/compare/0.11.0...0.11.1)</small>

### Build

- Add missing typing-extensions dependency for Python less than 3.10 ([3d121fc](https://github.com/pawamoy/failprint/commit/3d121fcd056ecdc4d3c491bae678a04e6fd8b4a7) by Timothée Mazzucotelli).

## [0.11.0](https://github.com/pawamoy/failprint/releases/tag/0.11.0) - 2023-04-10

<small>[Compare with 0.10.0](https://github.com/pawamoy/failprint/compare/0.10.0...0.11.0)</small>

### Features

- Accept name in lazy decorator ([a0b9381](https://github.com/pawamoy/failprint/commit/a0b938118c0aa4df65dbeacd10990432b01f0720) by Timothée Mazzucotelli).

## [0.10.0](https://github.com/pawamoy/failprint/releases/tag/0.10.0) - 2023-02-18

<small>[Compare with 0.9.0](https://github.com/pawamoy/failprint/compare/0.9.0...0.10.0)</small>

### Features

- Provide a lazy decorator, allow running lazy callables ([fa066b5](https://github.com/pawamoy/failprint/commit/fa066b501353b1f7208f631dd7ac0f0b5cb4cba1) by Timothée Mazzucotelli).

## [0.9.0](https://github.com/pawamoy/failprint/releases/tag/0.9.0) - 2023-02-10

<small>[Compare with 0.8.0](https://github.com/pawamoy/failprint/compare/0.8.0...0.9.0)</small>

### Features

- Support callables that raise `SystemExit` ([867aa59](https://github.com/pawamoy/failprint/commit/867aa593b7abfe19331f6e9ba02e86f1d76fa383) by Timothée Mazzucotelli). [Issue #14](https://github.com/pawamoy/failprint/issues/14)
- Support tools that write to `sys.stdout.buffer` or `sys.stderr.buffer` ([1703b86](https://github.com/pawamoy/failprint/commit/1703b86375e764be06c2144a118c7f6230584c6f) by Timothée Mazzucotelli). [Issue #15](https://github.com/pawamoy/failprint/issues/15)
- Add command option to runner ([6642698](https://github.com/pawamoy/failprint/commit/66426985eecf7f0e87d17cf040b0e80aba87b55a) by Timothée Mazzucotelli). [Issue #9](https://github.com/pawamoy/failprint/issues/9)

### Bug Fixes

- Fetch callable names from back frames ([7f2a759](https://github.com/pawamoy/failprint/commit/7f2a75978690966a23f913802edbabd317e93f59) by Timothée Mazzucotelli). [Issue #16](https://github.com/pawamoy/failprint/issues/16)
- Support other `SystemExit` code values ([abcaf5e](https://github.com/pawamoy/failprint/commit/abcaf5ec9d28df6b3081736cae83b8bddc3f6bf0) by Timothée Mazzucotelli).
- Support `flush` method in buffers ([2fe8077](https://github.com/pawamoy/failprint/commit/2fe80770604695f9cc516f2c8f493698113e4da8) by Timothée Mazzucotelli).

### Code Refactoring

- Use future annotations ([ad23ec3](https://github.com/pawamoy/failprint/commit/ad23ec377a9f4cfd3647e7d11a038136b119ba33) by Timothée Mazzucotelli).

## [0.8.0](https://github.com/pawamoy/failprint/releases/tag/0.8.0) - 2021-07-31

<small>[Compare with 0.7.0](https://github.com/pawamoy/failprint/compare/0.7.0...0.8.0)</small>

### Features

- Support passing a string as standard input ([7c87a4c](https://github.com/pawamoy/failprint/commit/7c87a4cb82e2774df371b8e05013848ff28d9dec) by Timothée Mazzucotelli). [Issue #10](https://github.com/pawamoy/failprint/issues/10), [PR #11](https://github.com/pawamoy/failprint/pull/11)

### Bug Fixes

- Initialize colorama support for Windows ([deb0c78](https://github.com/pawamoy/failprint/commit/deb0c7832ccde671efbafa8d03773c26b4cf5ba6) by Timothée Mazzucotelli). [PR #12](https://github.com/pawamoy/failprint/pull/12)

## [0.7.0](https://github.com/pawamoy/failprint/releases/tag/0.7.0) - 2021-06-20

<small>[Compare with 0.6.2](https://github.com/pawamoy/failprint/compare/0.6.2...0.7.0)</small>

### Features

- Return output as well as exit code from the main runner ([34e8ac1](https://github.com/pawamoy/failprint/commit/34e8ac121581e3d262240f3dfbca81c42a5a30c3) by Timothée Mazzucotelli).

## [0.6.2](https://github.com/pawamoy/failprint/releases/tag/0.6.2) - 2021-01-20

<small>[Compare with 0.6.1](https://github.com/pawamoy/failprint/compare/0.6.1...0.6.2)</small>

### Code Refactoring

- Use parsed options as dict directly ([142e6f0](https://github.com/pawamoy/failprint/commit/142e6f08b71c5d89b0fe041af3bfe2d7309d43fd) by Timothée Mazzucotelli).
- Add option in `add_flags` not to set defaults ([dd9327e](https://github.com/pawamoy/failprint/commit/dd9327ee55425a4a3f08c470d41b5ef419c0bd8b) by Timothée Mazzucotelli).
- Consistently use `cmd` between options and API ([881d99d](https://github.com/pawamoy/failprint/commit/881d99d663ecd82d1178bf24a71de35a4e512a4d) by Timothée Mazzucotelli).
- Consistently use `fmt` between options and API ([bda06a2](https://github.com/pawamoy/failprint/commit/bda06a2819c27470ec902eacb85632812c4ce4e7) by Timothée Mazzucotelli).

## [0.6.1](https://github.com/pawamoy/failprint/releases/tag/0.6.1) - 2021-01-17

<small>[Compare with 0.6.0](https://github.com/pawamoy/failprint/compare/0.6.0...0.6.1)</small>

### Code 

- Separate method to add parser flags ([9f2a58f](https://github.com/pawamoy/failprint/commit/9f2a58fea80aea77aaf88144ec430cbcc94d8d75) by Timothée Mazzucotelli).

## [0.6.0](https://github.com/pawamoy/failprint/releases/tag/0.6.0) - 2020-10-11

<small>[Compare with 0.5.1](https://github.com/pawamoy/failprint/compare/0.5.1...0.6.0)</small>

### Features

- Refactor, add tests and fix bugs ([523e97b](https://github.com/pawamoy/failprint/commit/523e97bc2f2fe4db02a3db8373229244a5ff74e6) by Timothée Mazzucotelli).
    - Restructure modules: create `capture` and `process`
    - Rename argument `output_type` to `capture`
    - Rename `Output` enum to `Capture`
    - Rename `combine` enum value to `both`
    - Rename `nocombine` enum value to `none`
    - Accept `True` and `False` as `capture` values
    - Use more defaults in functions arguments
    - Fix decoding error on Windows


## [0.5.1](https://github.com/pawamoy/failprint/releases/tag/0.5.1) - 2020-10-04

<small>[Compare with 0.5.0](https://github.com/pawamoy/failprint/compare/0.5.0...0.5.1)</small>

### Bug Fixes

- Fix progress parser argument ([d5fe999](https://github.com/pawamoy/failprint/commit/d5fe999645388b42c06b33c75628aa9478d972db) by Timothée Mazzucotelli).

## [0.5.0](https://github.com/pawamoy/failprint/releases/tag/0.5.0) - 2020-10-04

<small>[Compare with 0.4.1](https://github.com/pawamoy/failprint/compare/0.4.1...0.5.0)</small>

### Bug Fixes

- Use which to find exec path on Windows ([5327b0c](https://github.com/pawamoy/failprint/commit/5327b0c8fc9ed45b352383142560728013f0d8ec) by Timothée Mazzucotelli).
- Fix quoting when running as shell command ([0f11995](https://github.com/pawamoy/failprint/commit/0f119954fe1c7f8d59c28aac1a0bd392c14675c7) by Timothée Mazzucotelli).
- Run with `shell=True` on Windows ([5e97141](https://github.com/pawamoy/failprint/commit/5e97141fa9c2f351ea513c7146230ff1179c75f2) by Timothée Mazzucotelli).

### Features

- Refactor and add features ([22a5e8d](https://github.com/pawamoy/failprint/commit/22a5e8d4acda90134cadf80b11878ad60e95eee5) by Timothée Mazzucotelli).
    - Add ability to run a function or callable
    - Add `nocapture` output type
    - Add silent option to API
    - Accept `None` as truthful function result
    - Add silent CLI flag
    - Add no progress CLI flag

## [0.4.1](https://github.com/pawamoy/failprint/releases/tag/0.4.1) - 2020-09-29

<small>[Compare with 0.4.0](https://github.com/pawamoy/failprint/compare/0.4.0...0.4.1)</small>

### Bug Fixes

- Don't crash on Windows ([aaa2673](https://github.com/pawamoy/failprint/commit/aaa2673177fae6fffa90dfea15ed27599058191a) by Timothée Mazzucotelli).

## [0.4.0](https://github.com/pawamoy/failprint/releases/tag/0.4.0) - 2020-09-25

<small>[Compare with 0.3.0](https://github.com/pawamoy/failprint/compare/0.3.0...0.4.0)</small>

### Features

- Add quiet option ([b676335](https://github.com/pawamoy/failprint/commit/b676335f4bfb960259c66dbe6d6b942f8cdcc916) by Timothée Mazzucotelli).
- Add option to allow failure ([79b3ae7](https://github.com/pawamoy/failprint/commit/79b3ae719888eddab1e8ff0040e15e32e4976002) by Timothée Mazzucotelli).

## [0.3.0](https://github.com/pawamoy/failprint/releases/tag/0.3.0) - 2020-05-01

<small>[Compare with 0.2.0](https://github.com/pawamoy/failprint/compare/0.2.0...0.3.0)</small>

### Features

- Implement progress display for pretty format ([7c244e2](https://github.com/pawamoy/failprint/commit/7c244e25d10a5db25caf9329ff1f4ec079d117d2) by Timothée Mazzucotelli).

## [0.2.0](https://github.com/pawamoy/failprint/releases/tag/0.2.0) - 2020-04-28

<small>[Compare with 0.1.1](https://github.com/pawamoy/failprint/compare/0.1.1...0.2.0)</small>

### Features

- Add `--no-pty` option ([5ba21e8](https://github.com/pawamoy/failprint/commit/5ba21e8662081a6db2d02b8c685896c925532a0c) by Timothée Mazzucotelli).

## [0.1.1](https://github.com/pawamoy/failprint/releases/tag/0.1.1) - 2020-04-23

<small>[Compare with 0.1.0](https://github.com/pawamoy/failprint/compare/0.1.0...0.1.1)</small>

### Bug Fixes

- Fix default output type ([f720cf7](https://github.com/pawamoy/failprint/commit/f720cf7b31ae7c7e25f16818769d55b5eed25b25) by Timothée Mazzucotelli).
- Fix environment variable name ([526f4df](https://github.com/pawamoy/failprint/commit/526f4df43c3bf68ad0d6b3338dd7a0b940ecccb3) by Timothée Mazzucotelli).

## [0.1.0](https://github.com/pawamoy/failprint/releases/tag/0.1.0) - 2020-04-23

<small>[Compare with first commit](https://github.com/pawamoy/failprint/compare/182af93b01611781bebd4c859d71a39fe73af1c5...0.1.0)</small>

### Features

- Support colors for combine format ([3756dbd](https://github.com/pawamoy/failprint/commit/3756dbde445625331b5e274fffc2c9e1ec1e49ca) by Timothée Mazzucotelli).
- Initial commit ([182af93](https://github.com/pawamoy/failprint/commit/182af93b01611781bebd4c859d71a39fe73af1c5) by Timothée Mazzucotelli).
