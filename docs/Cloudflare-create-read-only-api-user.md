## 🔒 Read-Only Cloudflare GraphQL & Logs API Credential

This guide will walk you through the steps to create a versatile API Token with **read-only access** for Cloudflare's **GraphQL Analytics, Logs, and Account-level Analytics**. This token is ideal for tools or scripts that only need to **read** analytics and log data across your account and specific zones.


### Steps to Create the API Token

1.  **Log in to Cloudflare:**
    * Go to the Cloudflare dashboard and log in to your account.

2.  **Navigate to API Tokens:**
    * In the top-right corner, click on **"My Profile"** or your account name.
    * Select **"API Tokens"** from the sidebar or the dropdown menu.
    * Click the **"Create Token"** button.
    [View Screenshot](docs/assets/Cloudflare-Step-01.png)

3.  **Start with a Custom Token:**
    * Instead of using a template, select **"Create Custom Token"** at the bottom of the list. [View Screenshot](docs/assets/Cloudflare-Step-02.png)

4.  **Configure the Token Details:**

| Setting | Value/Selection | Notes |
| :--- | :--- | :--- |
| **Token Name** | `ReadOnly-Analytics-Logs` (or similar) | Choose a name that clearly identifies its purpose and scope. |
| **Permissions** | *(See Step 5 below)* | We will add the required permissions in the next step. |
| **Zone Resources** | *Include - Specific zone - **[Your Zone Name]*** | Select the specific domain/zone you want this token to access. **Required for Zone permissions.** |
| **Client IP Address Filtering** | *Optional* | Highly recommended for security. Enter the IP addresses that will be making API calls. |
| **TTL (Time to Live)** | *Optional* | Set an expiration date if you want the token to be temporary. |

5.  **Add Required Read-Only Permissions:**

    Under the **Permissions** section, add the following three entries, ensuring the permission level for each is set to **Read**:

| Component | Permission | Access Level |
| :--- | :--- | :--- |
| **Zone** | **Analytics** | **Read** |
| **Zone** | **Logs** | **Read** |
| **Account** | **Analytics** | **Read** |

[View Screenshot](docs/assets/Cloudflare-Step-03.png)

6.  **Continue and Review:**
    * Click **"Continue to Summary"**.
    * Review the permissions to confirm they are **Read** access only for the intended Zone and Account resources.

7.  **Create and Record the Token:**
    * Click **"Create Token"**.     [View Screenshot](docs/assets/Cloudflare-Step-04.png)
    * The generated token will be displayed **only once**. [View Screenshot](docs/assets/Cloudflare-Step-05.png)
    * **⚠️ IMPORTANT:** Copy the token and save it immediately in a secure location (like a password manager). You will **not** be able to see it again.

---

### Using the Token

The applications can use this generated token in the `Authorization` header of their requests to Cloudflare's various API endpoints, including the GraphQL Analytics API.

