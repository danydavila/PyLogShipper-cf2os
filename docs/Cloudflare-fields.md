## 🌩️ Cloudflare Log Fields & Premium Access

Cloudflare provides **different levels of log data access** depending on your account plan.
This project supports both **Basic** and **Premium (Bot Management / Enterprise)** field sets.

---

## ⚙️ Enabling Premium Fields

If your Cloudflare account includes **Bot Management** or **Enterprise** features, you can access additional log fields by enabling premium mode in your `.env` file:

```bash
INCLUDE_PREMIUM_FIELDS=true
```

By default, this value is `false`, meaning only the standard Free/Pro/Business fields will be retrieved.

> **Tip:**
> You can check your Cloudflare plan type under your Cloudflare Dashboard → *Account → Billing → Plan Type.*

---

## 📋 Field Reference

### 🧩 Free / Pro / Business Fields

These fields are always available:

| Field Name                    | Description                               |
| ----------------------------- | ----------------------------------------- |
| `clientCountryName`           | Country name of the client request        |
| `clientIP`                    | IP address of the client                  |
| `clientRequestHTTPHost`       | HTTP host requested                       |
| `clientRequestHTTPMethodName` | HTTP method (GET, POST, etc.)             |
| `clientRequestPath`           | Path portion of the request               |
| `datetime`                    | Timestamp of the request                  |
| `edgeResponseStatus`          | Response status code from Cloudflare edge |
| `originResponseStatus`        | Response status code from origin          |
| `sampleInterval`              | Sampling rate used for the logs           |
| `userAgent`                   | User agent string of the client           |

---

### 🛡️ Bot Management / Enterprise Fields

Available only when `INCLUDE_PREMIUM_FIELDS=true`:

| Field Name                    | Description                                    |
| ----------------------------- | ---------------------------------------------- |
| `originIP`                    | Origin server IP                               |
| `clientRequestQuery`          | Query string of the client request             |
| `clientRequestReferer`        | Full referer URL                               |
| `clientRefererHost`           | Host extracted from referer                    |
| `clientAsn`                   | ASN number of the client                       |
| `clientASNDescription`        | ASN organization description                   |
| `edgeResponseContentTypeName` | Content type of the response                   |
| `botManagementDecision`       | Cloudflare Bot Management decision             |
| `botScoreSrcName`             | Source of bot score                            |
| `securityAction`              | Security action taken (e.g., challenge, block) |
| `securitySource`              | Source of the security event                   |
| `wafAttackScore`              | Web Application Firewall attack score          |
| `wafAttackScoreClass`         | WAF score classification                       |
| `wafXssAttackScore`           | WAF cross-site scripting attack score          |
| `xRequestedWith`              | Header identifying AJAX/XHR requests           |

---

## 🧠 Summary

| Plan Type                   | `.env` Setting                 | Fields Available |
| --------------------------- | ------------------------------ | ---------------- |
| Free / Pro / Business       | `INCLUDE_PREMIUM_FIELDS=false` | Basic Fields     |
| Enterprise / Bot Management | `INCLUDE_PREMIUM_FIELDS=true`  | All Fields       |

---

## 🔗 Repository

Project: [**PyLogShipper-cf2os**](https://github.com/danydavila/PyLogShipper-cf2os)
This Python script automates pulling Cloudflare logs and shipping them to OpenSearch.
