# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
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
