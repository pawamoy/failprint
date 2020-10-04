# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
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
