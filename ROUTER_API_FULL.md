# Deeper Router API Documentation (34.34.34.34)

Generated: 2026-04-08 14:05 UTC

## Scope and method
- Source: router web frontend bundle (`assets/*.js`) + live authenticated probes + second-pass review of dynamically composed paths.
- Auth tested with credentials: `admin/admin`.
- Safety: only read-only probes were executed automatically; write endpoints are documented but not invoked.

## Authentication
1. `POST /api/admin/login` with JSON `{ "username": "admin", "password": "<RSA_OAEP_BASE64>" }`.
2. On success router sets an HttpOnly session cookie (name is device-specific).
3. Send this cookie on all subsequent API calls (`withCredentials=true` in frontend).
4. Validate session with `POST /api/admin/validateToken`.

### Password encryption
- Frontend uses Node/Web crypto equivalent: `crypto.publicEncrypt(publicKey, Buffer.from(password)).toString("base64")`.
- The public key is embedded in the shipped frontend bundle and can be extracted from the authentication code path.

## High-level stats
- Endpoints discovered: **145**
- Methods: `GET`=71, `POST`=83, `DELETE`=2
- Read probes executed: **63** (`200`: 50, `400`: 5, `403`: 8)

## Important runtime findings
- `/api/admin/getDeviceId` is accessible without login cookie (returns device id).
- Wallet-related endpoints can return `403 {"walletLocked":true}` until wallet unlock.
- Some list endpoints require query params and return `400` when missing, e.g. `/api/smartRoute/getRoutingWhitelist/domain` -> `{"paramError":"Page param missing"}`.
- A second-pass bundle review uncovered extra endpoints hidden behind dynamic path composition, especially under `/api/security/*`.
- Raw string extraction also contains a false positive: `/api/wifi/getAPConfig request filed` is a frontend error log string, not a real API path.

## Category: `accessControl`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/accessControl/delete` | `POST` | `write` | `` | POST: macList |
| `/api/accessControl/list` | `GET` | `read` | `200` |  |
| `/api/accessControl/setOne` | `POST` | `write` | `` | POST: bwLimit, bypass, regionCode, remark, routeMode |
| `/api/accessControl/switch` | `GET, POST` | `write` | `200` | POST: value |

## Category: `admin`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/admin/changePassword` | `POST` | `write` | `` |  |
| `/api/admin/connect` | `POST` | `write` | `` |  |
| `/api/admin/consent` | `POST` | `write` | `` | POST: privacyPolicy, termsOfUse |
| `/api/admin/deeperLog` | `POST` | `write` | `` | POST: level, message |
| `/api/admin/downloadLog` | `GET` | `read` | `` |  |
| `/api/admin/getDeviceId` | `GET` | `read` | `200` |  |
| `/api/admin/getMyCountry` | `GET` | `read` | `200` |  |
| `/api/admin/language` | `GET, POST` | `write` | `` | POST: val |
| `/api/admin/logOut` | `POST` | `write` | `` |  |
| `/api/admin/login` | `POST` | `write` | `` | POST: password, username |
| `/api/admin/reboot` | `POST` | `critical-write` | `` |  |
| `/api/admin/remoteWeb` | `GET` | `read` | `200` |  |
| `/api/admin/remoteWeb/start` | `POST` | `write` | `` |  |
| `/api/admin/remoteWeb/stop` | `POST` | `write` | `` |  |
| `/api/admin/reset` | `POST` | `critical-write` | `` |  |
| `/api/admin/validateToken` | `POST` | `write` | `` |  |

## Category: `appRelocator`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/appRelocator/addApp` | `POST` | `write` | `` |  |
| `/api/appRelocator/apps` | `GET` | `read` | `200` |  |
| `/api/appRelocator/delApp` | `POST` | `write` | `` | POST: appName |

## Category: `autoReboot`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/autoReboot/config` | `GET, POST` | `critical-write` | `200` |  |

## Category: `betanet`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/betanet/getBalanceAndCredit` | `GET` | `read` | `403` |  |
| `/api/betanet/getBalanceHistory` | `GET` | `read` | `403` |  |
| `/api/betanet/getOnChainStatus` | `GET` | `read` | `403` |  |
| `/api/betanet/getTransactionList` | `GET` | `read` | `403` | GET: params |
| `/api/betanet/getTransactionSum` | `GET` | `read` | `403` | GET: params, position |
| `/api/betanet/redeemCredit` | `POST` | `write` | `` |  |
| `/api/betanet/setCreditLevel` | `POST` | `write` | `` |  |
| `/api/betanet/transfer` | `POST` | `critical-write` | `` |  |
| `/api/betanet/walletData` | `GET` | `read` | `403` |  |

## Category: `dynamic-data`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/dynamic-data` | `GET` | `read` | `200` |  |

## Category: `info`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/info` | `GET` | `read` | `200` |  |

## Category: `inform`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/inform` | `GET` | `read` | `200` |  |

## Category: `liquid`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/liquid` | `GET` | `read` | `200` |  |

## Category: `microPayment`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/microPayment/getDailyTraffic` | `GET` | `read` | `200` |  |

## Category: `notifications`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/notifications` | `GET` | `read` | `` |  |

## Category: `rustdesk`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/rustdesk/config` | `GET` | `read` | `200` |  |
| `/api/rustdesk/forced` | `POST` | `write` | `` |  |
| `/api/rustdesk/hbbrLog` | `GET` | `read` | `200` |  |
| `/api/rustdesk/keys` | `DELETE` | `write` | `` |  |
| `/api/rustdesk/port` | `POST` | `write` | `` |  |
| `/api/rustdesk/switch` | `POST` | `write` | `` |  |
| `/api/rustdesk/version` | `GET` | `read` | `200` |  |
| `/api/rustdesk/vpnConfig` | `GET` | `read` | `200` |  |
| `/api/rustdesk/vpnSwitch` | `POST` | `write` | `` |  |

## Category: `security`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/security/addToBlacklist` | `POST` | `write` | `` | POST: domainName |
| `/api/security/addToWhitelist` | `POST` | `write` | `` | POST: domainName |
| `/api/security/blockedCounts` | `GET` | `read` | `200` |  |
| `/api/security/clearBlacklist` | `POST` | `write` | `` | POST: password |
| `/api/security/clearWhitelist` | `POST` | `write` | `` | POST: password |
| `/api/security/deleteFromBlacklist` | `POST` | `write` | `` |  |
| `/api/security/deleteFromWhitelist` | `POST` | `write` | `` |  |
| `/api/security/exportBlacklist` | `POST` | `read` | `` |  |
| `/api/security/exportWhitelist` | `POST` | `read` | `` |  |
| `/api/security/getFilterBlacklist` | `GET` | `read` | `` | GET: pageNo, pageSize |
| `/api/security/getFilterWhitelist` | `GET` | `read` | `` | GET: pageNo, pageSize |
| `/api/security/getUrlFilterData` | `GET` | `read` | `200` |  |
| `/api/security/importBlacklist` | `POST` | `write` | `` | POST: listFile |
| `/api/security/importWhitelist` | `POST` | `write` | `` | POST: listFile |
| `/api/security/setCategoryStates` | `POST` | `write` | `` |  |
| `/api/security/wanIpAccess` | `GET, POST` | `write` | `200` |  |

## Category: `sharing`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/sharing/blacklist` | `GET, POST, DELETE` | `write` | `400` | GET: pageNo, pageSize, params; POST: domain; DELETE: data |
| `/api/sharing/clearBlacklist` | `POST` | `write` | `` |  |
| `/api/sharing/getSharingConfig` | `GET` | `read` | `200` |  |
| `/api/sharing/getTrafficLimit` | `GET` | `read` | `200` |  |
| `/api/sharing/setBandwidthLimit` | `POST` | `write` | `` | POST: number |
| `/api/sharing/setBtSharing` | `POST` | `write` | `` | POST: btEnabled |
| `/api/sharing/setDnsBlacklistForSharing` | `POST` | `write` | `` | POST: dnsBlacklistForSharing |
| `/api/sharing/setSharingState` | `POST` | `write` | `` |  |
| `/api/sharing/setSmtpSharing` | `POST` | `write` | `` | POST: smtpEnabled |
| `/api/sharing/setTrafficLimit` | `POST` | `write` | `` | POST: number, unit |

## Category: `sharingSecurity`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/sharingSecurity/getList/1000` | `GET` | `read` | `200` |  |
| `/api/sharingSecurity/getList/{start}/{end}/{pageSize}/{offset}/{keyword}` | `GET` | `read` | `` |  |
| `/api/sharingSecurity/getMode` | `GET` | `read` | `200` |  |
| `/api/sharingSecurity/getTotal/{start}/{end}/{keyword}` | `GET` | `read` | `` |  |

## Category: `smartRoute`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/smartRoute/addToBlacklist/domain` | `POST` | `write` | `` |  |
| `/api/smartRoute/addToBlacklist/ip` | `POST` | `write` | `` |  |
| `/api/smartRoute/addToWhitelist/domain` | `POST` | `write` | `` |  |
| `/api/smartRoute/addToWhitelist/ip` | `POST` | `write` | `` |  |
| `/api/smartRoute/addTunnel` | `POST` | `write` | `` |  |
| `/api/smartRoute/deleteFromBlacklist/domain` | `POST` | `write` | `` |  |
| `/api/smartRoute/deleteFromBlacklist/ip` | `POST` | `write` | `` |  |
| `/api/smartRoute/deleteFromWhitelist/domain` | `POST` | `write` | `` |  |
| `/api/smartRoute/deleteFromWhitelist/ip` | `POST` | `write` | `` |  |
| `/api/smartRoute/deleteTunnels` | `POST` | `write` | `` |  |
| `/api/smartRoute/editWhiteEntry/domain` | `POST` | `write` | `` |  |
| `/api/smartRoute/editWhiteEntry/ip` | `POST` | `write` | `` |  |
| `/api/smartRoute/exportDirect/domain` | `POST` | `read` | `` |  |
| `/api/smartRoute/exportDirect/ip` | `POST` | `read` | `` |  |
| `/api/smartRoute/exportSmart/domain` | `POST` | `read` | `` |  |
| `/api/smartRoute/exportSmart/ip` | `POST` | `read` | `` |  |
| `/api/smartRoute/getDpnMode` | `GET` | `read` | `200` |  |
| `/api/smartRoute/getRoutingBlacklist/domain` | `GET` | `read` | `400` | GET: pageNo, pageSize, params |
| `/api/smartRoute/getRoutingBlacklist/ip` | `GET` | `read` | `400` | GET: pageNo, pageSize, params |
| `/api/smartRoute/getRoutingWhitelist/domain` | `GET` | `read` | `400` | GET: pageNo, pageSize, params |
| `/api/smartRoute/getRoutingWhitelist/ip` | `GET` | `read` | `400` | GET: pageNo, pageSize, params |
| `/api/smartRoute/importDirect/domain` | `POST` | `write` | `` |  |
| `/api/smartRoute/importDirect/ip` | `POST` | `write` | `` |  |
| `/api/smartRoute/importSmart/domain` | `POST` | `write` | `` |  |
| `/api/smartRoute/importSmart/ip` | `POST` | `write` | `` |  |
| `/api/smartRoute/listTunnelOptions` | `GET` | `read` | `200` |  |
| `/api/smartRoute/listTunnels` | `GET` | `read` | `200` |  |
| `/api/smartRoute/nodeLbMode` | `GET, POST` | `write` | `200` |  |
| `/api/smartRoute/refreshTunnel` | `POST` | `write` | `` |  |
| `/api/smartRoute/setDpnMode` | `POST` | `write` | `` |  |
| `/api/smartRoute/switchNode` | `POST` | `write` | `` |  |

## Category: `speedometer`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/speedometer` | `GET` | `read` | `200` |  |

## Category: `system-info`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/system-info/get-autoupdate` | `GET` | `read` | `200` |  |
| `/api/system-info/get-latestversion` | `GET` | `read` | `200` |  |
| `/api/system-info/hardware-info` | `GET` | `read` | `200` |  |
| `/api/system-info/network-address` | `GET` | `read` | `200` |  |
| `/api/system-info/session-info` | `GET` | `read` | `200` |  |
| `/api/system-info/set-autoupdate` | `GET` | `read` | `200` | GET: params |
| `/api/system-info/software-info` | `GET` | `read` | `200` |  |
| `/api/system-info/update-latestversion` | `GET` | `read` | `200` |  |
| `/api/system-info/usage` | `GET` | `read` | `200` |  |

## Category: `tproxy`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/tproxy/adsFilter` | `GET, POST` | `write` | `200` |  |
| `/api/tproxy/rootCaCert` | `GET` | `read` | `` |  |
| `/api/tproxy/rule` | `GET, POST` | `write` | `200` |  |
| `/api/tproxy/sslBypass` | `GET, POST` | `write` | `200` |  |

## Category: `traffic`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/traffic/routedInfo` | `GET` | `read` | `200` |  |
| `/api/traffic/savedTraffic` | `GET` | `read` | `200` |  |
| `/api/traffic/session-speed` | `GET` | `read` | `200` |  |
| `/api/traffic/total-traffic` | `GET` | `read` | `200` |  |

## Category: `wallet`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/wallet/bindWallet` | `POST` | `write` | `` |  |
| `/api/wallet/downloadKeystore` | `POST` | `write` | `` |  |
| `/api/wallet/generateWallet` | `POST` | `write` | `` | POST: password |
| `/api/wallet/publicKey` | `GET` | `read` | `403` |  |
| `/api/wallet/resetPassword` | `POST` | `critical-write` | `` |  |
| `/api/wallet/setPassword` | `POST` | `write` | `` | POST: password |
| `/api/wallet/unbindWallet` | `POST` | `critical-write` | `` |  |
| `/api/wallet/unlock` | `POST` | `write` | `` | POST: password |
| `/api/wallet/unstaking` | `GET, POST` | `write` | `403` | POST: choice, password |

## Category: `wifi`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/wifi/connect` | `POST` | `write` | `` |  |
| `/api/wifi/enable` | `GET` | `read` | `200` |  |
| `/api/wifi/forget` | `POST` | `write` | `` | POST: ssid |
| `/api/wifi/getAPConfig` | `GET` | `read` | `200` |  |
| `/api/wifi/hostapdLog` | `GET` | `read` | `200` |  |
| `/api/wifi/setDownstream` | `POST` | `write` | `` |  |
| `/api/wifi/upstreamList` | `GET` | `read` | `200` |  |
| `/api/wifi/workingInfo` | `GET` | `read` | `200` |  |

## Category: `worldmap-data`

| Path | Methods | Risk | Probe | Request body keys (if known) |
|---|---|---|---|---|
| `/api/worldmap-data` | `GET` | `read` | `200` |  |

## Files in this folder
- `router_api_catalog.json` - full machine-readable catalog.
- `router_api_openapi_like.json` - OpenAPI-like specification.
- `router_api_calls_catalog.json` - extracted frontend call inventory.
- `router_get_probe_results.json` - raw probe outputs for GET endpoints.
