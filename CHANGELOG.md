# Change Log

## [1.1.2](https://github.com/pyouroboros/ouroboros/tree/1.1.2) (2019-02-02)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/1.1.1...1.1.2)

**Fixed bugs:**

- No default timezone [\#176](https://github.com/pyouroboros/ouroboros/issues/176)

**Closed issues:**

- cron documentation example update [\#182](https://github.com/pyouroboros/ouroboros/issues/182) [[documentation](https://github.com/pyouroboros/ouroboros/labels/documentation)]

**Other Pull Requests**
- v1.1.2 Merge [\#184](https://github.com/pyouroboros/ouroboros/pull/184) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- v1.1.2 to develop [\#183](https://github.com/pyouroboros/ouroboros/pull/183) ([DirtyCajunRice](https://github.com/DirtyCajunRice))

## [1.1.1](https://github.com/pyouroboros/ouroboros/tree/1.1.1) (2019-02-01)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/1.1.0...1.1.1)

**Implemented enhancements:**

- Support for adding an identifier \(hostname?\) to notifications [\#158](https://github.com/pyouroboros/ouroboros/issues/158)
- Influx config data + ocd cleanup [\#162](https://github.com/pyouroboros/ouroboros/pull/162) [[cleanup](https://github.com/pyouroboros/ouroboros/labels/cleanup)] ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- add cli arg for cron [\#157](https://github.com/pyouroboros/ouroboros/pull/157) ([DirtyCajunRice](https://github.com/DirtyCajunRice))

**Fixed bugs:**

- Ouroboros does not respect MONITOR= [\#166](https://github.com/pyouroboros/ouroboros/issues/166)
- Docker TLS over TCP connections [\#154](https://github.com/pyouroboros/ouroboros/issues/154) [[documentation](https://github.com/pyouroboros/ouroboros/labels/documentation)]
- Patch/group 4 [\#169](https://github.com/pyouroboros/ouroboros/pull/169) [[cleanup](https://github.com/pyouroboros/ouroboros/labels/cleanup)] ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- Recheck properly for only non lists [\#164](https://github.com/pyouroboros/ouroboros/pull/164) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- add some missing passthrough info for restart [\#163](https://github.com/pyouroboros/ouroboros/pull/163) ([DirtyCajunRice](https://github.com/DirtyCajunRice))

**Other Pull Requests**

- v1.1.1 Merge [\#173](https://github.com/pyouroboros/ouroboros/pull/173) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- v1.1.1 to develop [\#172](https://github.com/pyouroboros/ouroboros/pull/172) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- Patch/group 3 [\#167](https://github.com/pyouroboros/ouroboros/pull/167) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- Add hostname to the notifications [\#161](https://github.com/pyouroboros/ouroboros/pull/161) ([tlkamp](https://github.com/tlkamp))
- Patch/group 2 [\#155](https://github.com/pyouroboros/ouroboros/pull/155) ([DirtyCajunRice](https://github.com/DirtyCajunRice))

## [1.1.0](https://github.com/pyouroboros/ouroboros/tree/1.1.0) (2019-01-26)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/1.0.0...1.1.0)

**Implemented enhancements:**

- Notification via Telegram [\#146](https://github.com/pyouroboros/ouroboros/issues/146)
- Add flag to allow a labels\_only condition [\#142](https://github.com/pyouroboros/ouroboros/issues/142)
- DRY\_RUN flag [\#140](https://github.com/pyouroboros/ouroboros/issues/140)
- Notification on startup [\#138](https://github.com/pyouroboros/ouroboros/issues/138)
- Start/Stop containers in sequence [\#106](https://github.com/pyouroboros/ouroboros/issues/106)
- Refactor/notifications with apprise [\#151](https://github.com/pyouroboros/ouroboros/pull/151) [[breaking change](https://github.com/pyouroboros/ouroboros/labels/breaking%20change)] [[cleanup](https://github.com/pyouroboros/ouroboros/labels/cleanup)] [[documentation](https://github.com/pyouroboros/ouroboros/labels/documentation)] ([DirtyCajunRice](https://github.com/DirtyCajunRice))

**Fixed bugs:**

- Catch invalid docker socket config [\#148](https://github.com/pyouroboros/ouroboros/issues/148)
- Explicitly Define true/false [\#141](https://github.com/pyouroboros/ouroboros/issues/141) [[documentation](https://github.com/pyouroboros/ouroboros/labels/documentation)]

**Other Pull Requests**

- v1.1.0 Merge [\#153](https://github.com/pyouroboros/ouroboros/pull/153) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- v1.1.0 to develop [\#152](https://github.com/pyouroboros/ouroboros/pull/152) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- Patch/group 1 [\#150](https://github.com/pyouroboros/ouroboros/pull/150) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- Add volume for docker socket path [\#144](https://github.com/pyouroboros/ouroboros/pull/144) ([mauvehed](https://github.com/mauvehed))

## [1.0.0](https://github.com/pyouroboros/ouroboros/tree/1.0.0) (2019-01-23)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.6.0...1.0.0)

**Implemented enhancements:**

- Stop containers with alternate signal [\#107](https://github.com/pyouroboros/ouroboros/issues/107)
- Docker Socket secure connections [\#105](https://github.com/pyouroboros/ouroboros/issues/105)
- Selectively monitor containers with label [\#104](https://github.com/pyouroboros/ouroboros/issues/104)
- Allow stop-signal label [\#133](https://github.com/pyouroboros/ouroboros/pull/133) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- Docker TLS Verify option [\#132](https://github.com/pyouroboros/ouroboros/pull/132) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- add label priority feature for watch/ignore. Addresses \#104 [\#121](https://github.com/pyouroboros/ouroboros/pull/121) ([DirtyCajunRice](https://github.com/DirtyCajunRice))

**Fixed bugs:**

- Unexpected docker API causes program to quit ‘500 Server Error: Internal Server Error’ [\#130](https://github.com/pyouroboros/ouroboros/issues/130)
- Error tag handling under the registry with port [\#129](https://github.com/pyouroboros/ouroboros/issues/129)
- a fatal error when none tag image [\#122](https://github.com/pyouroboros/ouroboros/issues/122)
- Bug/ignore logic [\#135](https://github.com/pyouroboros/ouroboros/pull/135) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- Bug/registry logic [\#131](https://github.com/pyouroboros/ouroboros/pull/131) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- catch no tags in get\_running [\#124](https://github.com/pyouroboros/ouroboros/pull/124) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- fixed logic for latest vs develop, and added -f to specify file [\#119](https://github.com/pyouroboros/ouroboros/pull/119) ([DirtyCajunRice](https://github.com/DirtyCajunRice))

**Closed issues:**

- Missing docker-compose.yml from documentation [\#120](https://github.com/pyouroboros/ouroboros/issues/120) [[documentation](https://github.com/pyouroboros/ouroboros/labels/documentation)]
- Wiki usage docs reference old argument names [\#115](https://github.com/pyouroboros/ouroboros/issues/115) [[documentation](https://github.com/pyouroboros/ouroboros/labels/documentation)]

**Other Pull Requests**

- v1.0.0 Merge [\#137](https://github.com/pyouroboros/ouroboros/pull/137) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- v1.0.0 to develop [\#136](https://github.com/pyouroboros/ouroboros/pull/136) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- Clean old legacy files [\#134](https://github.com/pyouroboros/ouroboros/pull/134) [[cleanup](https://github.com/pyouroboros/ouroboros/labels/cleanup)] ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- Cleanup/qemu logic [\#128](https://github.com/pyouroboros/ouroboros/pull/128) [[cleanup](https://github.com/pyouroboros/ouroboros/labels/cleanup)] ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- fix readme wording for monitoring remote hosts [\#126](https://github.com/pyouroboros/ouroboros/pull/126) [[documentation](https://github.com/pyouroboros/ouroboros/labels/documentation)] ([circa10a](https://github.com/circa10a))

## [0.6.0](https://github.com/pyouroboros/ouroboros/tree/0.6.0) (2019-01-17)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.5.0...0.6.0)

**Implemented enhancements:**

- Support multi-architecture Docker images [\#78](https://github.com/pyouroboros/ouroboros/issues/78)
- Mail notification [\#59](https://github.com/pyouroboros/ouroboros/issues/59)
- Multi architecture docker [\#110](https://github.com/pyouroboros/ouroboros/pull/110) ([circa10a](https://github.com/circa10a))
- added logo to readme [\#109](https://github.com/pyouroboros/ouroboros/pull/109) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- Feature/ouroboros self\_update [\#103](https://github.com/pyouroboros/ouroboros/pull/103) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- add version cli arg [\#100](https://github.com/pyouroboros/ouroboros/pull/100) ([circa10a](https://github.com/circa10a))
- added email notifications. Addresses \#59 [\#97](https://github.com/pyouroboros/ouroboros/pull/97) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- Documentation [\#96](https://github.com/pyouroboros/ouroboros/pull/96) ([DirtyCajunRice](https://github.com/DirtyCajunRice))

**Fixed bugs:**

- Ignore not working as expected [\#98](https://github.com/pyouroboros/ouroboros/issues/98)
- specify for specificity! [\#114](https://github.com/pyouroboros/ouroboros/pull/114) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- manifesting failures [\#113](https://github.com/pyouroboros/ouroboros/pull/113) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- sigh. [\#112](https://github.com/pyouroboros/ouroboros/pull/112) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- Multiarch/fine tuning [\#111](https://github.com/pyouroboros/ouroboros/pull/111) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- catch index error and account for shared images, x [\#102](https://github.com/pyouroboros/ouroboros/pull/102) ([circa10a](https://github.com/circa10a))
- add monitor/ignore to list sanity check. Fixes \#98 [\#99](https://github.com/pyouroboros/ouroboros/pull/99) ([DirtyCajunRice](https://github.com/DirtyCajunRice))

**Other Pull Requests**

- v0.6.0 to develop [\#118](https://github.com/pyouroboros/ouroboros/pull/118) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- v0.6.0 Merge [\#117](https://github.com/pyouroboros/ouroboros/pull/117) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- add changelog formatting and fix all labels going back to 1 [\#116](https://github.com/pyouroboros/ouroboros/pull/116) [[documentation](https://github.com/pyouroboros/ouroboros/labels/documentation)] ([DirtyCajunRice](https://github.com/DirtyCajunRice))

## [0.5.0](https://github.com/pyouroboros/ouroboros/tree/0.5.0) (2019-01-13)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.4.3...0.5.0)

**Implemented enhancements:**

- Auto discover slack/discord notifications in WEBHOOK\_URLS [\#83](https://github.com/pyouroboros/ouroboros/issues/83)
- Add to schedule logic run now [\#75](https://github.com/pyouroboros/ouroboros/issues/75)
- add pushover functionality. Finishes other half of \#80 [\#93](https://github.com/pyouroboros/ouroboros/pull/93) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- add keep\_alive url for healthchecks. Addresses half of \#80 [\#89](https://github.com/pyouroboros/ouroboros/pull/89) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- changed webhook json to auto-deciding + fixed RUN\_ONCE no underscore [\#86](https://github.com/pyouroboros/ouroboros/pull/86) ([DirtyCajunRice](https://github.com/DirtyCajunRice))
- Refactor [\#79](https://github.com/pyouroboros/ouroboros/pull/79) ([DirtyCajunRice](https://github.com/DirtyCajunRice))

**Fixed bugs:**

- Fix log level case sensitivity [\#82](https://github.com/pyouroboros/ouroboros/issues/82)
- Invalid URL 'h': No schema supplied. Perhaps you meant http://h? [\#76](https://github.com/pyouroboros/ouroboros/issues/76)
- Installation via pip fails [\#73](https://github.com/pyouroboros/ouroboros/issues/73)
- Added try except [\#95](https://github.com/pyouroboros/ouroboros/pull/95) ([circa10a](https://github.com/circa10a))
- Fix dockerfile [\#92](https://github.com/pyouroboros/ouroboros/pull/92) ([circa10a](https://github.com/circa10a))
- use ouroboros script in dockerfile [\#91](https://github.com/pyouroboros/ouroboros/pull/91) ([circa10a](https://github.com/circa10a))
- fix deploy script to push git tags [\#90](https://github.com/pyouroboros/ouroboros/pull/90) ([circa10a](https://github.com/circa10a))
- change pypi travis username [\#88](https://github.com/pyouroboros/ouroboros/pull/88) ([circa10a](https://github.com/circa10a))
- install flake8 for travis, run on appropriate directories [\#87](https://github.com/pyouroboros/ouroboros/pull/87) ([circa10a](https://github.com/circa10a))
- Removed old test related items, removed the need for duplicate bin sc… [\#85](https://github.com/pyouroboros/ouroboros/pull/85) ([circa10a](https://github.com/circa10a))
- change loglevel to use upper\(\) [\#84](https://github.com/pyouroboros/ouroboros/pull/84) ([circa10a](https://github.com/circa10a))
- Prometheus bind fix, org rename [\#81](https://github.com/pyouroboros/ouroboros/pull/81) ([circa10a](https://github.com/circa10a))

## [0.4.3](https://github.com/pyouroboros/ouroboros/tree/0.4.3) (2019-01-09)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.4.2...0.4.3)

**Implemented enhancements:**

- grafana to metrics/prometheus endpoint [\#74](https://github.com/pyouroboros/ouroboros/issues/74)
- add aarch64 docker image [\#77](https://github.com/pyouroboros/ouroboros/pull/77) ([circa10a](https://github.com/circa10a))

## [0.4.2](https://github.com/pyouroboros/ouroboros/tree/0.4.2) (2019-01-08)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.4.1...0.4.2)

**Implemented enhancements:**

- Add autopep8 to the pre-merge checks [\#30](https://github.com/pyouroboros/ouroboros/issues/30)

## [0.4.1](https://github.com/pyouroboros/ouroboros/tree/0.4.1) (2018-12-30)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.4.0...0.4.1)

**Implemented enhancements:**

- Pre merge code quality checks [\#72](https://github.com/pyouroboros/ouroboros/pull/72) ([circa10a](https://github.com/circa10a))

## [0.4.0](https://github.com/pyouroboros/ouroboros/tree/0.4.0) (2018-12-30)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.3.7...0.4.0)

**Implemented enhancements:**

- Slack notification  [\#61](https://github.com/pyouroboros/ouroboros/issues/61)
- Webhook notifications [\#71](https://github.com/pyouroboros/ouroboros/pull/71) ([circa10a](https://github.com/circa10a))

## [0.3.7](https://github.com/pyouroboros/ouroboros/tree/0.3.7) (2018-12-26)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.3.6...0.3.7)

**Implemented enhancements:**

- Timezone Support [\#68](https://github.com/pyouroboros/ouroboros/issues/68)
- Add output to log at container start [\#66](https://github.com/pyouroboros/ouroboros/issues/66)
- Enable Timezone Configuration [\#69](https://github.com/pyouroboros/ouroboros/pull/69) ([circa10a](https://github.com/circa10a))

## [0.3.6](https://github.com/pyouroboros/ouroboros/tree/0.3.6) (2018-12-21)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.3.5...0.3.6)

**Implemented enhancements:**

- print ouroboros configuration on startup [\#67](https://github.com/pyouroboros/ouroboros/pull/67) ([circa10a](https://github.com/circa10a))

## [0.3.5](https://github.com/pyouroboros/ouroboros/tree/0.3.5) (2018-12-20)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.3.4...0.3.5)

**Implemented enhancements:**

- Raspberry Pi compatible docker image [\#62](https://github.com/pyouroboros/ouroboros/issues/62)
- Scheduling docs [\#65](https://github.com/pyouroboros/ouroboros/pull/65) ([circa10a](https://github.com/circa10a))

## [0.3.4](https://github.com/pyouroboros/ouroboros/tree/0.3.4) (2018-12-19)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.3.3...0.3.4)

**Implemented enhancements:**

- Rpi docker image [\#64](https://github.com/pyouroboros/ouroboros/pull/64) ([circa10a](https://github.com/circa10a))

## [0.3.3](https://github.com/pyouroboros/ouroboros/tree/0.3.3) (2018-11-29)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.3.2...0.3.3)

**Implemented enhancements:**

- add docs, bump version [\#58](https://github.com/pyouroboros/ouroboros/pull/58) ([circa10a](https://github.com/circa10a))

**Fixed bugs:**

- Problem accessing private registry [\#55](https://github.com/pyouroboros/ouroboros/issues/55)

**Closed issues:**

- Q: Add config file? [\#46](https://github.com/pyouroboros/ouroboros/issues/46) [[documentation](https://github.com/pyouroboros/ouroboros/labels/documentation)]

## [0.3.2](https://github.com/pyouroboros/ouroboros/tree/0.3.2) (2018-11-28)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.3.1...0.3.2)

**Fixed bugs:**

- unrecognized arguments [\#52](https://github.com/pyouroboros/ouroboros/issues/52)
- Fix config json [\#56](https://github.com/pyouroboros/ouroboros/pull/56) ([circa10a](https://github.com/circa10a))

## [0.3.1](https://github.com/pyouroboros/ouroboros/tree/0.3.1) (2018-11-16)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.3.0...0.3.1)

**Implemented enhancements:**

- Add Prometheus endpoint [\#23](https://github.com/pyouroboros/ouroboros/issues/23) [[hacktoberfest](https://github.com/pyouroboros/ouroboros/labels/hacktoberfest)]

**Fixed bugs:**

- fix bind address bug [\#53](https://github.com/pyouroboros/ouroboros/pull/53) ([circa10a](https://github.com/circa10a))

## [0.3.0](https://github.com/pyouroboros/ouroboros/tree/0.3.0) (2018-11-15)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.2.3...0.3.0)

**Implemented enhancements:**

- Q: continue to update to latest or same tag [\#43](https://github.com/pyouroboros/ouroboros/issues/43)
- Metrics [\#51](https://github.com/pyouroboros/ouroboros/pull/51) ([circa10a](https://github.com/circa10a))
- Disable pip cache in Dockerfile [\#50](https://github.com/pyouroboros/ouroboros/pull/50) ([Strayer](https://github.com/Strayer))

## [0.2.3](https://github.com/pyouroboros/ouroboros/tree/0.2.3) (2018-11-08)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.2.2...0.2.3)

**Implemented enhancements:**

- Keep tags [\#48](https://github.com/pyouroboros/ouroboros/pull/48) ([circa10a](https://github.com/circa10a))

## [0.2.2](https://github.com/pyouroboros/ouroboros/tree/0.2.2) (2018-11-03)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.2.1...0.2.2)

**Implemented enhancements:**

- Add ability to ignore select containers [\#35](https://github.com/pyouroboros/ouroboros/issues/35)
- Ignore containers [\#45](https://github.com/pyouroboros/ouroboros/pull/45) ([tlkamp](https://github.com/tlkamp))
- Update setup.py, travis param [\#42](https://github.com/pyouroboros/ouroboros/pull/42) ([circa10a](https://github.com/circa10a))

## [0.2.1](https://github.com/pyouroboros/ouroboros/tree/0.2.1) (2018-10-28)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.1.3...0.2.1)

**Implemented enhancements:**

- Option precedence [\#32](https://github.com/pyouroboros/ouroboros/issues/32)
- Add ouroboros to the user's path automagically [\#28](https://github.com/pyouroboros/ouroboros/issues/28)
- Deploy to Pypi [\#41](https://github.com/pyouroboros/ouroboros/pull/41) ([circa10a](https://github.com/circa10a))
- Add setup.py [\#40](https://github.com/pyouroboros/ouroboros/pull/40) ([tlkamp](https://github.com/tlkamp))
- change branch to master [\#39](https://github.com/pyouroboros/ouroboros/pull/39) ([circa10a](https://github.com/circa10a))
- Move api client out of cli.py [\#38](https://github.com/pyouroboros/ouroboros/pull/38) ([tlkamp](https://github.com/tlkamp))
- Handle the exceptions better in cli.py [\#36](https://github.com/pyouroboros/ouroboros/pull/36) ([tlkamp](https://github.com/tlkamp))

**Closed issues:**

- \[question\] network\_mode: "service:XXX" ? [\#33](https://github.com/pyouroboros/ouroboros/issues/33) [[documentation](https://github.com/pyouroboros/ouroboros/labels/documentation)]

**Other Pull Requests**

- Remove global hosts variable [\#37](https://github.com/pyouroboros/ouroboros/pull/37) [[cleanup](https://github.com/pyouroboros/ouroboros/labels/cleanup)] ([tlkamp](https://github.com/tlkamp))
- update docs [\#34](https://github.com/pyouroboros/ouroboros/pull/34) [[documentation](https://github.com/pyouroboros/ouroboros/labels/documentation)] ([circa10a](https://github.com/circa10a))

## [0.1.3](https://github.com/pyouroboros/ouroboros/tree/0.1.3) (2018-10-25)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.1.2...0.1.3)

**Implemented enhancements:**

- Make CLI expose fewer globals, formatting [\#31](https://github.com/pyouroboros/ouroboros/pull/31) ([tlkamp](https://github.com/tlkamp))

## [0.1.2](https://github.com/pyouroboros/ouroboros/tree/0.1.2) (2018-10-24)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.1.1...0.1.2)

**Implemented enhancements:**

- Rewrite script to use vendor packages if possible [\#25](https://github.com/pyouroboros/ouroboros/pull/25) ([dannysauer](https://github.com/dannysauer))
- Improve URL matching Regex [\#24](https://github.com/pyouroboros/ouroboros/pull/24) ([dannysauer](https://github.com/dannysauer))
- Add environment files to the project for those working with Conda [\#22](https://github.com/pyouroboros/ouroboros/pull/22) ([tlkamp](https://github.com/tlkamp))

**Other Pull Requests**

- regex changes, cli cleanup. [\#29](https://github.com/pyouroboros/ouroboros/pull/29) [[cleanup](https://github.com/pyouroboros/ouroboros/labels/cleanup)] ([circa10a](https://github.com/circa10a))
- Clean up cli.py [\#27](https://github.com/pyouroboros/ouroboros/pull/27) [[cleanup](https://github.com/pyouroboros/ouroboros/labels/cleanup)] ([tlkamp](https://github.com/tlkamp))

## [0.1.1](https://github.com/pyouroboros/ouroboros/tree/0.1.1) (2018-10-21)
[Full Changelog](https://github.com/pyouroboros/ouroboros/compare/0.1.0...0.1.1)

## [0.1.0](https://github.com/pyouroboros/ouroboros/tree/0.1.0) (2018-10-21)
**Implemented enhancements:**

- account for environment variables [\#19](https://github.com/pyouroboros/ouroboros/issues/19)
- Support private repos [\#10](https://github.com/pyouroboros/ouroboros/issues/10)
- Deploy to pypi [\#5](https://github.com/pyouroboros/ouroboros/issues/5)
- Create travis build [\#4](https://github.com/pyouroboros/ouroboros/issues/4)
- Rewrite new container class [\#3](https://github.com/pyouroboros/ouroboros/issues/3)
- Write Unit Tests [\#2](https://github.com/pyouroboros/ouroboros/issues/2)
- Add CLI Args [\#1](https://github.com/pyouroboros/ouroboros/issues/1)
- added support for private registries [\#12](https://github.com/pyouroboros/ouroboros/pull/12) ([circa10a](https://github.com/circa10a))
- Torpus cli args [\#11](https://github.com/pyouroboros/ouroboros/pull/11) ([Torpus](https://github.com/Torpus))
- single client [\#9](https://github.com/pyouroboros/ouroboros/pull/9) ([circa10a](https://github.com/circa10a))
- the less code the better [\#8](https://github.com/pyouroboros/ouroboros/pull/8) ([circa10a](https://github.com/circa10a))
- Initial stuff [\#6](https://github.com/pyouroboros/ouroboros/pull/6) ([circa10a](https://github.com/circa10a))

**Closed issues:**

- Create good docs [\#7](https://github.com/pyouroboros/ouroboros/issues/7) [[documentation](https://github.com/pyouroboros/ouroboros/labels/documentation)]

**Other Pull Requests**

- Docs [\#21](https://github.com/pyouroboros/ouroboros/pull/21) [[documentation](https://github.com/pyouroboros/ouroboros/labels/documentation)] ([circa10a](https://github.com/circa10a))
- Tests [\#20](https://github.com/pyouroboros/ouroboros/pull/20) [[cleanup](https://github.com/pyouroboros/ouroboros/labels/cleanup)] ([circa10a](https://github.com/circa10a))
- Add travis [\#18](https://github.com/pyouroboros/ouroboros/pull/18) [[cleanup](https://github.com/pyouroboros/ouroboros/labels/cleanup)] ([circa10a](https://github.com/circa10a))
- Tests [\#17](https://github.com/pyouroboros/ouroboros/pull/17) [[cleanup](https://github.com/pyouroboros/ouroboros/labels/cleanup)] ([circa10a](https://github.com/circa10a))
- Tests [\#16](https://github.com/pyouroboros/ouroboros/pull/16) [[cleanup](https://github.com/pyouroboros/ouroboros/labels/cleanup)] ([circa10a](https://github.com/circa10a))
- Tests [\#15](https://github.com/pyouroboros/ouroboros/pull/15) [[cleanup](https://github.com/pyouroboros/ouroboros/labels/cleanup)] ([circa10a](https://github.com/circa10a))
- Tests [\#14](https://github.com/pyouroboros/ouroboros/pull/14) [[cleanup](https://github.com/pyouroboros/ouroboros/labels/cleanup)] ([circa10a](https://github.com/circa10a))
- Tests [\#13](https://github.com/pyouroboros/ouroboros/pull/13) [[cleanup](https://github.com/pyouroboros/ouroboros/labels/cleanup)] ([circa10a](https://github.com/circa10a))
