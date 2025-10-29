## 📍 GeoLite2 Database Setup

This guide explains how to manually download and place the MaxMind **GeoLite2** databases for IP geolocation into the project directory at:

```
src/db/
```


## 🧾 Required Files

You will need the following two databases:

* `GeoLite2-City.mmdb`
* `GeoLite2-ASN.mmdb`


## 🪪 1. Create a Free MaxMind Account

1. Go to [https://www.maxmind.com](https://www.maxmind.com)
2. Click **Sign Up** and create a free account.
3. After logging in, go to **My Account → License Keys**.
4. Create a new **license key** and accept the GeoLite2 EULA.

> These files cannot be downloaded without logging in due to MaxMind’s licensing requirements.


## 💾 2. Download the Databases

1. Visit your [GeoLite2 Download Page](https://www.maxmind.com/en/accounts/current/geoip/downloads).

2. Under **GeoLite2 Databases**, download:

   * `GeoLite2-City.tar.gz`
   * `GeoLite2-ASN.tar.gz`

3. Extract each archive:

   ```bash
   tar -xzf GeoLite2-City.tar.gz
   tar -xzf GeoLite2-ASN.tar.gz
   ```

4. Inside each extracted folder, locate the `.mmdb` file:

   * `GeoLite2-City.mmdb`
   * `GeoLite2-ASN.mmdb`

---

## 📂 3. Move Files to Your Project

Copy both `.mmdb` files into your project folder:

```
src/db/
```

**Example (from terminal):**

```bash
mkdir -p src/db
cp GeoLite2-City_*/GeoLite2-City.mmdb src/db/
cp GeoLite2-ASN_*/GeoLite2-ASN.mmdb src/db/
```


## ✅ 4. Verify Placement

After copying, your project structure should look like:

```
project-root/
├── src/
│   ├── db/
│   │   ├── GeoLite2-ASN.mmdb
│   │   └── GeoLite2-City.mmdb
│   └── ...
└── README.md
```


## 🧠 5. Optional: Verify Databases

You can confirm the files are valid using the `mmdblookup` utility:

```bash
mmdblookup --file src/db/GeoLite2-City.mmdb --ip 8.8.8.8
mmdblookup --file src/db/GeoLite2-ASN.mmdb --ip 8.8.8.8
```


## ⚠️ License Reminder

These databases are provided by **MaxMind** under the [GeoLite2 EULA](https://www.maxmind.com/en/geolite2/eula).
Do **not** commit them publicly to version control or redistribute them.
