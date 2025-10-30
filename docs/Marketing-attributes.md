# Marketing Attributes Tracking

This document describes all marketing and tracking attributes that are parsed from URLs and stored in OpenSearch for analytics.

## Overview

The system parses URL parameters from two sources:

1. **Client Request Query String** - Parameters in the actual page request URL
2. **Client Referrer URL** - Parameters in the HTTP referrer header

All parsed attributes are stored with prefixes:

- `clientRequest_*` - From the request query string
- `clientReferer_*` - From the referrer URL

---

## Standard UTM Parameters

UTM (Urchin Tracking Module) parameters are the industry standard for tracking marketing campaigns.

### Core UTM Parameters

| Parameter | Field Name | Description | Example |
|-----------|------------|-------------|---------|
| `utm_source` | `utm_source` | Identifies the source of traffic | `google`, `facebook`, `newsletter` |
| `utm_medium` | `utm_medium` | Identifies the marketing medium | `cpc`, `email`, `social`, `organic` |
| `utm_campaign` | `utm_campaign` | Identifies the specific campaign | `summer_sale_2024`, `product_launch` |
| `utm_content` | `utm_content` | Differentiates similar content or links | `header_link`, `footer_cta`, `banner_ad` |
| `utm_term` | `utm_term` | Identifies paid search keywords | `running+shoes`, `laptop+deals` |

### Extended UTM Parameters

| Parameter | Field Name | Description | Example |
|-----------|------------|-------------|---------|
| `utm_id` | `utm_id` | Campaign identifier | `abc.123` |
| `utm_campaign_id` | `utm_campaign_id` | Numeric campaign ID | `12345678` |
| `utm_ad_id` | `utm_ad_id` | Advertisement ID | `ad_98765` |
| `utm_source_platform` | `utm_source_platform` | Platform that directed traffic | `Google Ads`, `Facebook Ads` |
| `utm_creative_format` | `utm_creative_format` | Type of creative used | `display`, `video`, `carousel` |
| `utm_marketing_tactic` | `utm_marketing_tactic` | Marketing tactic used | `retargeting`, `prospecting` |
| `utm_creative_id` | `utm_creative_id` | Creative asset identifier | `creative_123` |

---

## Platform-Specific Auto-Tagging Parameters

### Google Ads

#### GCLID (Google Click Identifier)
| Parameter | Field Name | Description |
|-----------|------------|-------------|
| `gclid` | `gclid` | Unique click identifier for Google Ads auto-tagging |

**Example:** `gclid=Cj0KCQiA5...`

#### HSA Parameters (Google Ads Manual Tagging)
Used for tracking Google Ads campaigns with manual value tracking.

| Parameter | Field Name | Description | Example |
|-----------|------------|-------------|---------|
| `hsa_acc` | `hsa_acc` | Google Ads Account ID | `4047026695` |
| `hsa_cam` | `hsa_cam` | Campaign ID | `23070427670` |
| `hsa_grp` | `hsa_grp` | Ad Group ID | `187078508798` |
| `hsa_ad` | `hsa_ad` | Ad ID | `780265591864` |
| `hsa_src` | `hsa_src` | Traffic source | `g` (Google) |
| `hsa_tgt` | `hsa_tgt` | Keyword target | `kwd-652301726130` |
| `hsa_kw` | `hsa_kw` | Keyword (URL decoded & normalized) | `tax credit estimator` |
| `hsa_mt` | `hsa_mt` | Match type | `p` (phrase), `e` (exact), `b` (broad) |
| `hsa_net` | `hsa_net` | Network | `adwords`, `search`, `display` |
| `hsa_ver` | `hsa_ver` | Tracking version | `3` |

**Example URL:**
```
?hsa_acc=4047026695&hsa_cam=23070427670&hsa_grp=187078508798&hsa_ad=780265591864&hsa_src=g&hsa_tgt=kwd-652301726130&hsa_kw=tax%20credit%20estimator&hsa_mt=p&hsa_net=adwords&hsa_ver=3
```

#### GAD Parameters (Google Ads Enhanced)
Enhanced Google Ads tracking parameters.

| Parameter | Field Name | Description | Example |
|-----------|------------|-------------|---------|
| `gad_source` | `gad_source` | Google Ads traffic source indicator | `1`, `2` |
| `gad_campaignid` | `gad_campaignid` | Campaign ID for enhanced tracking | `23070427670` |

### Microsoft Ads (Bing)

| Parameter | Field Name | Description |
|-----------|------------|-------------|
| `msclkid` | `msclkid` | Microsoft Click ID for auto-tagging |

**Example:** `msclkid=abc123def456`

### Facebook

| Parameter | Field Name | Description |
|-----------|------------|-------------|
| `fbclid` | `fbclid` | Facebook Click Identifier for tracking Facebook ad clicks |

**Example:** `fbclid=IwAR1234...`

### LinkedIn

| Parameter | Field Name | Description |
|-----------|------------|-------------|
| `li_fat_id` | `li_fat_id` | LinkedIn First-party Ad Tracking ID |

**Example:** `li_fat_id=abc-123-def-456`

---

## Search Keywords

The system automatically extracts search keywords from various query parameters used by different platforms.

### Supported Search Parameters

| Parameter | Priority | Description |
|-----------|----------|-------------|
| `q` | High | Most common search query parameter |
| `query` | High | Alternative search query parameter |
| `kw` | Medium | Keyword parameter |
| `ask` | Medium | Question/search parameter |
| `searchfor` | Medium | Search term parameter |
| `wd` | Low | Word/search parameter |
| `Q` | Low | Capitalized query parameter |

**Field Name:** `search_keyword`

**Notes:**
- Keywords are normalized (URL decoded, limited to 250 characters)
- Only the first matching parameter is used based on priority
- Applies to both request and referrer URLs

---

## Additional Custom Parameters

### Product Tracking

| Parameter | Field Name | Description | Example |
|-----------|------------|-------------|---------|
| `product` | `product` | Product identifier or category | `laptop-hp-15`, `category-electronics` |

---

## URL Structure Fields

Basic URL components are also extracted and stored:

| Field Name | Description | Example |
|------------|-------------|---------|
| `scheme` | URL protocol | `https`, `http` |
| `hostname` | Domain name | `example.com`, `www.example.com` |
| `path` | URL path | `/products/item-123` |
| `query` | Full query string | `utm_source=google&utm_medium=cpc` |

### Referrer-Specific Fields

| Field Name | Description |
|------------|-------------|
| `clientRefererScheme` | Referrer URL protocol |
| `clientRefererHost` | Referrer domain |
| `clientRefererPath` | Referrer path |
| `clientRefererQuery` | Referrer full query string |

---

## Data Processing Notes

### Normalization
- **Keywords and terms** are normalized to a maximum of 250 characters
- Commas in strings are replaced with colons
- URL encoding is automatically decoded (e.g., `%20` → space)

### Missing Values
- All marketing attributes default to empty string (`''`) if not present
- This ensures consistent data structure in OpenSearch

### Case Sensitivity
- Parameter names are case-sensitive
- Both `q` and `Q` are supported as separate parameters

---

## OpenSearch Field Mapping

### Client Request Fields
All parameters from the request URL are prefixed with `clientRequest_`:

```
clientRequest_utm_source
clientRequest_utm_medium
clientRequest_utm_campaign
clientRequest_hsa_acc
clientRequest_hsa_cam
clientRequest_gclid
clientRequest_search_keyword
... (and all other parameters)
```

### Client Referrer Fields
All parameters from the referrer URL are prefixed with `clientReferer_`:

```
clientReferer_utm_source
clientReferer_utm_medium
clientReferer_utm_campaign
clientReferer_hsa_acc
clientReferer_hsa_cam
clientReferer_gclid
clientReferer_search_keyword
... (and all other parameters)
```

---

## Usage Examples

### Example 1: Google Ads Campaign with UTM
```
https://example.com/landing?utm_source=google&utm_medium=cpc&utm_campaign=summer_sale&gclid=Cj0KCQiA5...
```

**Extracted Fields:**
- `clientRequest_utm_source`: `google`
- `clientRequest_utm_medium`: `cpc`
- `clientRequest_utm_campaign`: `summer_sale`
- `clientRequest_gclid`: `Cj0KCQiA5...`

### Example 2: Google Ads with HSA Parameters
```
https://example.com/product?hsa_acc=4047026695&hsa_cam=23070427670&hsa_kw=tax%20credit%20estimator&hsa_mt=p
```

**Extracted Fields:**
- `clientRequest_hsa_acc`: `4047026695`
- `clientRequest_hsa_cam`: `23070427670`
- `clientRequest_hsa_kw`: `tax credit estimator`
- `clientRequest_hsa_mt`: `p`

### Example 3: Facebook Campaign
```
https://example.com/offer?utm_source=facebook&utm_medium=social&utm_campaign=spring_promo&fbclid=IwAR1234...
```

**Extracted Fields:**
- `clientRequest_utm_source`: `facebook`
- `clientRequest_utm_medium`: `social`
- `clientRequest_utm_campaign`: `spring_promo`
- `clientRequest_fbclid`: `IwAR1234...`

### Example 4: Search Query with Referrer
**Request URL:**
```
https://example.com/search?q=best+laptops+2024
```

**Referrer URL:**
```
https://google.com/search?q=laptop+deals
```

**Extracted Fields:**
- `clientRequest_search_keyword`: `best laptops 2024`
- `clientReferer_search_keyword`: `laptop deals`

---

## Analytics Use Cases

### Campaign Performance Analysis
Track campaign effectiveness by analyzing:

- Conversion rates by `utm_campaign`
- ROI by `utm_source` and `utm_medium`
- Ad performance by `hsa_ad` or `utm_ad_id`

### Attribution Modeling
- First-touch attribution using referrer parameters
- Last-touch attribution using request parameters
- Multi-touch attribution combining both sources

### Keyword Performance
- Identify high-performing keywords from `hsa_kw` and `utm_term`
- Analyze search terms from `search_keyword`
- Compare match types using `hsa_mt`

### Platform Comparison
- Compare Google Ads vs. Facebook vs. Microsoft Ads performance
- Analyze organic vs. paid traffic
- Identify best-performing platforms by source

### A/B Testing
- Compare creative variations using `utm_content` or `utm_creative_id`
- Test different messaging with `utm_creative_format`
- Analyze tactics with `utm_marketing_tactic`

---

## Implementation Details

### Source Files
- **URL Parsing:** `src/library/iohelper.py`
  - `parse_url()` - Core parsing function
  - `parse_client_request_query_string()` - Request URL parsing
  - `parse_client_referer_url_string()` - Referrer URL parsing

- **Data Processing:** `src/pull-traffics.py`
  - `sent_to_es()` - Processes and sends data to OpenSearch

### Dependencies
- `urllib.parse` - URL parsing and query string extraction
- `library.parseurl.ParseURL` - Custom URL parsing

---

## Best Practices

### For Marketers
1. **Use consistent naming conventions** across campaigns
2. **Always include utm_source and utm_medium** at minimum
3. **Use descriptive campaign names** that identify the initiative
4. **Leverage utm_content** for A/B testing different creatives
5. **Track keywords** with utm_term for paid search campaigns

### For Analysts
1. **Normalize campaign names** before analysis (case sensitivity matters)
2. **Handle missing values** appropriately in queries
3. **Join with other data sources** using campaign IDs
4. **Create dashboards** segmented by source, medium, and campaign
5. **Set up alerts** for unusual traffic patterns

### For Developers
1. **Validate URL parameters** before processing
2. **Test with URL-encoded values** to ensure proper decoding
3. **Monitor field lengths** to prevent truncation issues
4. **Document custom parameters** if extending the system
5. **Maintain backward compatibility** when adding new fields

---

## Troubleshooting

### Common Issues

**Issue:** Parameters not being captured
- **Solution:** Verify parameter names are spelled correctly and case-sensitive

**Issue:** Keywords showing as URL-encoded
- **Solution:** Check that `normalize_string()` is being applied

**Issue:** Empty values in OpenSearch
- **Solution:** Ensure URLs contain the expected parameters; empty strings are normal for missing parameters

**Issue:** Truncated keywords
- **Solution:** Keywords over 250 characters are intentionally truncated; adjust `normalize_string()` if needed


## Related Documentation

- [Cloudflare GraphQL API Documentation](https://developers.cloudflare.com/analytics/graphql-api/)
- [Google Analytics UTM Parameters](https://support.google.com/analytics/answer/1033863)
- [Google Ads ValueTrack Parameters](https://support.google.com/google-ads/answer/6305348)
- [Facebook Click ID (fbclid)](https://www.facebook.com/business/help/952192354843755)
- [Microsoft Advertising Auto-tagging](https://help.ads.microsoft.com/apex/index/3/en/56762)
- [PyLogShipper-cf2os](https://github.com/danydavila/PyLogShipper-cf2os)
---

## Support

For questions or issues related to marketing attribute tracking:

1. Review this documentation
2. Check the source code in `src/library/iohelper.py`
3. Verify OpenSearch field mappings
4. Submit issues to the project repository
